from requests.auth import HTTPBasicAuth
import requests
import json
import datetime
from datetime import date

from constants import (
    THOMAS_ACCT_ID,
    AUTH,
    HEADERS,
    TRANSITION_PLANNED,
    TRANSITION_IN_PROGRESS,
)

from text import (
    Colors
)

def apiIsValidCredentials(api_email=None, api_key=None):
    """
    GET
    Checks if credentials are able to retrieve data from API
    """
    isValid = True

    if api_email and api_key:
        auth = HTTPBasicAuth(api_email, api_key)
    else:
        auth = AUTH

    try:
        url = 'https://securecodewarrior.atlassian.net/rest/api/latest/issue/CHLC-1520/'
        response = requests.get(url, headers=HEADERS, auth=auth)
        json_response = json.loads(response.text)

        if 'errorMessages' in json_response:
            print('Invalid API credentials: Invalid email or permissions on account')
            print('confirm your credentials are correct')
            print('run bug-fix.py --setup to change credentials')
            isValid = False
    
    except json.decoder.JSONDecodeError:
        print('Invalid API credentials: Invalid API key')
        print('run bug-fix.py --setup to change credentials')
        isValid = False

    return isValid


def getAllLinkedCHLC(issuelinks):
    """
    Parses json issuelinks and returns list of all linked CHLC's
    """
    chlcs = []
    for link in issuelinks:
        if 'outwardIssue' in link:
            issue = link['outwardIssue']['key']
        elif 'inwardIssue' in link:
            issue = link['inwardIssue']['key']

        if issue and 'CHLC-' in issue:
            chlcs.append(issue)
    
    return chlcs

def getCurrentFixVersion():
    """
    GET
    Gets current fix version based off of the current date
    """
    today = date.today()
    datetime_object = datetime.datetime.strptime(str(today.month), "%m")
    month = datetime_object.strftime("%b")
    version_name = None
    version_id = None

    url = f'https://securecodewarrior.atlassian.net/rest/api/latest/project/CHLRQ/versions'
    response = requests.get(url, headers=HEADERS, auth=AUTH)
    json_response = json.loads(response.text)

    for version in json_response:
        if str(today.year) in version['name'] and month in version['name']:
            version_name = version['name']
            version_id = version['id']

    return version_name, version_id

def apiTransitionToPlanned(chlrq, fixVersionID):
    """
    POST
    Transition CHLRQ to Planned w/ fix version
    """
    url = f'https://securecodewarrior.atlassian.net/rest/api/latest/issue/CHLRQ-{chlrq}/transitions'
    data = {"transition": {"id": TRANSITION_PLANNED}, "update": {"fixVersions": [{"add": {"id": fixVersionID}}]}}
    response = requests.post(url, headers=HEADERS, auth=AUTH, json=data)

    return response.status_code

def apiTransitionToInProgress(chlrq):
    """
    POST
    Transition CHLRQ to In Progress
    """
    url = f'https://securecodewarrior.atlassian.net/rest/api/latest/issue/CHLRQ-{chlrq}/transitions'
    data = {"transition":{"id":TRANSITION_IN_PROGRESS}}
    response = requests.post(url, headers=HEADERS, auth=AUTH, json=data)

    return response.status_code

# TODO: THIS DOESN'T WORK FOR ALL CHALLENGES!
def apiGetCreationCHLC(chlc):
    """
    GET
    Get parent CHLC's creation CHLC 
    """
    url = f'https://securecodewarrior.atlassian.net/rest/api/latest/issue/CHLC-{chlc}/'
    response = requests.get(url, headers=HEADERS, auth=AUTH)
    json_response = json.loads(response.text)

    if response.text:
        json_response = json.loads(response.text)

        if 'errorMessages' in json_response:
            print(f'{Colors.FAIL}Error getting creation CHLC{Colors.ENDC}')
    
    return json_response['fields']['parent']['key']

def apiGetLinkedChallenges(chlc):
    """
    GET
    Gets creation CHLC's children CHLCs
    """
    url = f'https://securecodewarrior.atlassian.net/rest/api/latest/issue/CHLC-{chlc}'
    response = requests.get(url, headers=HEADERS, auth=AUTH)
    json_response = json.loads(response.text)

    return getAllLinkedCHLC(json_response['fields']['issuelinks'])

def apiLinkCreationTicket(chlrq, chlc):
    """
    POST
    Links creation CHLC to CHLRQ
    """
    url = f'https://securecodewarrior.atlassian.net/rest/api/latest/issueLink'
    body = {'type':{'name':'Relates'},'outwardIssue':{'key':f'CHLRQ-{chlrq}'},'inwardIssue':{'key':f'CHLC-{chlc}'}}
    response = requests.post(url, json=body, headers=HEADERS, auth=AUTH)
    
    return response.status_code

def apiTransitionToClosed(chlrq, comment):
    """
    POST
    Links transitions CHLRQ to closed
    """
    url = f'https://securecodewarrior.atlassian.net/rest/api/latest/issue/CHLRQ-{chlrq}/transitions'
    data = {'transition':{'id':'191'},'update':{'comment':[{'add':{'body':comment}}]}}
    response = requests.post(url, headers=HEADERS, auth=AUTH, json=data)

    return response.status_code

def apiTransitionToFeedbackOpen(chlc):
    print('Transitioning:', chlc)
    """
    POST
    Transition CHLC to feedback open
    """
    url = f'https://securecodewarrior.atlassian.net/rest/api/latest/issue/{chlc}/transitions'
    data = {'transition':{'id':'511'}}
    response = requests.post(url, headers=HEADERS, auth=AUTH, json=data)

    return response

def apiTransitionToFeedbackReview(chlc):
    print('Transitioning:', chlc)
    """
    POST
    Transition CHLC to feedback review and add comment and change assignee to Thomas
    """
    url = f'https://securecodewarrior.atlassian.net/rest/api/latest/issue/{chlc}/transitions'
    data = {'transition':{'id':'521'}}
    response = requests.post(url, headers=HEADERS, auth=AUTH, json=data)

    return response

def apiEditAssigneeAndComment(chlc, chlrq):
    print('Transitioning:', chlc)
    print('Transitioning:', chlrq)
    """
    PUT
    Jira edit query. Changes CHLC's assignee to Thomas and adds comment
    """
    url = f'https://securecodewarrior.atlassian.net/rest/api/latest/issue/{chlc}'
    data = {'fields':{'assignee':{'accountId':THOMAS_ACCT_ID}}, 'update':{'comment':[{'add':{'body':f'CHLRQ-{chlrq}'}}]}}
    response = requests.put(url, headers=HEADERS, auth=AUTH, json=data)

    return response


def apiConfirmCHLC(chlc):
    """
    GET
    Confirm that chlc number is valid
    """
    url = f'https://securecodewarrior.atlassian.net/rest/api/latest/issue/CHLC-{chlc}/'
    response = requests.get(url, headers=HEADERS, auth=AUTH)
    json_response = json.loads(response.text)

    return 'key' in json_response and 'CHLC' in json_response['key']

def apiConfirmCHLRQ(chlrq):
    """
    GET
    Confirm that chlrq number is valid
    """
    url = f'https://securecodewarrior.atlassian.net/rest/api/latest/issue/CHLRQ-{chlrq}/'
    response = requests.get(url, headers=HEADERS, auth=AUTH)
    json_response = json.loads(response.text)
    
    return 'key' in json_response and 'CHLRQ' in json_response['key']