from src import constants, api

from .input import (
    get_chlc
)

def transition_jira_issues(chlrq, fix_message, is_cherrypick_required):
    """
    Use Jira API to transition tickets through Jira workflow
    """
    # API call to get current version name and id
    fixVersionName, fixVersionID = api.get_current_fix_version()

    # Check that version id was successfully got
    if not fixVersionID:
        # Print error
        print('Unable to determine fix version. Cannot auto-transition tickets. Exiting.')
        exit(1)

    # Transitioning CHLRQ
    print(f'\nTransitioning {constants.OKCYAN}CHLRQ-{chlrq}{constants.ENDC}')

    # Transition to in planned, include fix version
    print(f'\tTo Planned [Fix Version: {fixVersionName}]', end='')
    
    # If api returns 204, transition was successful
    plannedResult = api.transition_issue_to_planned(chlrq, fixVersionID)
    if plannedResult.status_code == 204:
        print(f'\t{constants.OKGREEN}[COMPLETE]{constants.ENDC}')
    else:
        print(f'\t{constants.FAIL}[FAILED - {plannedResult.status_code}: {plannedResult.reason}]{constants.ENDC}')

    # Transition to in progress
    print(f'\tTo In Progress', end='')
    
    # If api returns 204, transition was successful
    inProgressResult = api.transition_issue_to_in_progress(chlrq)
    if inProgressResult.status_code == 204:
        print(f'\t\t\t\t{constants.OKGREEN}[COMPLETE]{constants.ENDC}')
    else:
        print(f'\t\t\t\t{constants.FAIL}[FAILED - {inProgressResult.status_code}: {inProgressResult.reason}]{constants.ENDC}')

    #################################################################################
    # Linking CHLC to CHLRQ no longer required. Step is now done on ticket creation #
    #################################################################################
    # # Link CHLC to CHLRQ
    # print(f'\tLinking {constants.HEADER}{chlc}{constants.ENDC} [relates to]', end='')
    
    # # If api returns 204, transition was successful
    # linkResult = link_creation_chlc(chlrq, chlc[-4:])
    # if linkResult == 201:
    #     print(f'\t\t{constants.OKGREEN}[COMPLETE]{constants.ENDC}')
    # else:
    #     print(f'\t\t{constants.FAIL}[FAILED - {linkResult}]{constants.ENDC}')

    # Transition CHLRQ to closed w/ fix message
    print(f'\tTo Closed [with description of fix]', end='')
    
    # If api returns 204, transition was successful
    closedResult = api.transition_issue_to_closed(chlrq, fix_message)
    if closedResult.status_code == 204:
        print(f'\t{constants.OKGREEN}[COMPLETE]{constants.ENDC}')
    else:
        print(f'\t{constants.FAIL}[FAILED - {closedResult.status_code}: {closedResult.reason}]{constants.ENDC}')

    # If full app and fix was on the secure branch, transition all CHLC's
    if is_cherrypick_required:
        # Get application CHLC
        print('\n[Enter Application CHLC]')
        application_chlc = get_chlc()

        # Notify user of parent CHLC number
        print(f'Application CHLC: {constants.WARNING}{application_chlc}{constants.ENDC}')

        # Get all CHLC's linked to the creation ticket
        challenges = api.get_linked_challenges(application_chlc)

        # Print number of challenges to bulk transition
        print(f'Challenges to bulk transition: {len(challenges)}')
    
    else:
        # Get challenge chlc
        print('\n[Enter Challenge CHLC]')
        challenge_chlc = get_chlc()

        # Set challenges to the initial chlc
        challenges = ['CHLC-' + challenge_chlc[-4:]]

    print(f'\nTransitioning [{constants.OKCYAN}{len(challenges)}{constants.ENDC}] {constants.HEADER}CHLC\'s{constants.ENDC}')

    # Transition all challenges
    for challenge in challenges:
        # print('Up now:', challenge)

        print(f'Transitioning {constants.HEADER}{challenge}{constants.ENDC}:')

        # Transition challenge to Feedback Open
        print('\tTo Feedback Open', end='')
        
        # If api returns 204, transition was successful
        feedbackOpenResult = api.transition_issue_to_feedback_open(challenge)
        if feedbackOpenResult.status_code == 204:
            print(f'\t\t{constants.OKGREEN}[COMPLETE]{constants.ENDC}')
        else:
            print(f'\t\t{constants.FAIL}[FAILED - {feedbackOpenResult.status_code}: {feedbackOpenResult.reason}]{constants.ENDC}')

        # Transition challenge to Feedback Review w/ fix message and set assignee to Thomas
        print('\tTo Feedback Review', end='')

        # If api returns 204, transition was successful
        feedbackReviewResult = api.transition_issue_to_feedback_review(challenge)
        if feedbackReviewResult.status_code == 204:
            print(f'\t\t{constants.OKGREEN}[COMPLETE]{constants.ENDC}')
        else:
            print(f'\t\t{constants.FAIL}[FAILED - {feedbackReviewResult.status_code}: {feedbackReviewResult.reason}]{constants.ENDC}')

        # Sets assignee and adds CHLRQ as comment
        print('\tAdding assignee and comment', end='')

        # If api returns 204, transition was successful
        editResult = api.edit_issue_details(challenge, chlrq)
        if editResult.status_code == 204:
            print(f'\t{constants.OKGREEN}[COMPLETE]{constants.ENDC}')
        else:
            print(f'\t{constants.FAIL}[FAILED - {editResult.status_code}]{constants.ENDC}')
            print(f'{constants.FAIL}{editResult.text}')
