from api import (
    getCurrentFixVersion,
    apiTransitionToPlanned,
    apiTransitionToInProgress,
    apiLinkCreationTicket,
    apiTransitionToClosed,
    apiGetCreationCHLC,
    apiTransitionToFeedbackOpen,
    apiGetLinkedChallenges,
    apiTransitionToFeedbackReview,
    apiEditAssigneeAndComment,
)

from .input import (
    getCHLC
)

from text import (
    Colors
)

def transitionJiraTickets(chlrq, chlc, fix_message, is_cherrypick_required):
    """
    Use Jira API to transition tickets through Jira workflow
    """
    # API call to get current version name and id
    fixVersionName, fixVersionID = getCurrentFixVersion()

    # Check that version id was successfully got
    if not fixVersionID:
        # Print error
        print('Unable to determine fix version. Cannot auto-transition tickets. Exiting.')
        exit(1)

    # Transitioning CHLRQ
    print(f'\nTransitioning {Colors.OKCYAN}CHLRQ-{chlrq}{Colors.ENDC}')

    # Transition to in planned, include fix version
    print(f'\tTo Planned [Fix Version: {fixVersionName}]', end='')
    
    # If api returns 204, transition was successful
    plannedResult = apiTransitionToPlanned(chlrq, fixVersionID)
    if plannedResult == 204:
        print(f'\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
    else:
        print(f'\t{Colors.FAIL}[FAILED - {plannedResult}]{Colors.ENDC}')

    # Transition to in progress
    print(f'\tTo In Progress', end='')
    
    # If api returns 204, transition was successful
    inProgressResult = apiTransitionToInProgress(chlrq)
    if inProgressResult == 204:
        print(f'\t\t\t\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
    else:
        print(f'\t\t\t\t{Colors.FAIL}[FAILED - {inProgressResult}]{Colors.ENDC}')

    # Link CHLC to CHLRQ
    print(f'\tLinking {Colors.HEADER}{chlc}{Colors.ENDC} [relates to]', end='')
    
    # If api returns 204, transition was successful
    linkResult = apiLinkCreationTicket(chlrq, chlc[-4:])
    if linkResult == 201:
        print(f'\t\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
    else:
        print(f'\t\t{Colors.FAIL}[FAILED - {linkResult}]{Colors.ENDC}')

    # Transition CHLRQ to closed w/ fix message
    print(f'\tTo Closed [with description of fix]', end='')
    
    # If api returns 204, transition was successful
    closedResult = apiTransitionToClosed(chlrq, fix_message)
    if closedResult == 204:
        print(f'\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
    else:
        print(f'\t{Colors.FAIL}[FAILED - {closedResult}]{Colors.ENDC}')

    # If full app and fix was on the secure branch, transition all CHLC's
    if is_cherrypick_required:
        # Get creation CHLC
        # parent_chlc = apiGetCreationCHLC(chlc)
        print('\n[Enter Creation CHLC below]')
        parent_chlc = getCHLC()

        # Notify user of parent CHLC number
        print(f'Parent CHLC: {Colors.WARNING}{parent_chlc}{Colors.ENDC}')

        # Get all CHLC's linked to the creation ticket
        challenges = apiGetLinkedChallenges(parent_chlc)

        # Print number of challenges to bulk transition
        print(f'Challenges to bulk transition: {len(challenges)}')
    
    else:
        # Set challenges to the initial chlc
        challenges = ['CHLC-' + chlc[-4]]

    print(f'\nTransitioning [{Colors.OKCYAN}{len(challenges)}{Colors.ENDC}] {Colors.HEADER}CHLC\'s{Colors.ENDC}')

    # Transition all challenges
    for challenge in challenges:
        print('Up now:', challenge)

        print(f'Transitioning {Colors.HEADER}{challenge}{Colors.ENDC}:')

        # Transition challenge to Feedback Open
        print('\tTo Feedback Open', end='')
        
        # If api returns 204, transition was successful
        feedbackOpenResult = apiTransitionToFeedbackOpen(challenge)
        if feedbackOpenResult.status_code == 204:
            print(f'\t\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
        else:
            print(f'\t\t{Colors.FAIL}[FAILED - {feedbackOpenResult.status_code}]{Colors.ENDC}')
            print(f'{Colors.FAIL}{feedbackOpenResult.text}')

        # Transition challenge to Feedback Review w/ fix message and set assignee to Thomas
        print('\tTo Feedback Review', end='')

        # If api returns 204, transition was successful
        feedbackReviewResult = apiTransitionToFeedbackReview(challenge)
        if feedbackReviewResult.status_code == 204:
            print(f'\t\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
        else:
            print(f'\t\t{Colors.FAIL}[FAILED - {feedbackReviewResult.status_code}]{Colors.ENDC}')
            print(f'{Colors.FAIL}{feedbackReviewResult.text}')

        # Sets assignee and adds CHLRQ as comment
        print('\tAdding assignee and comment', end='')

        # If api returns 204, transition was successful
        editResult = apiEditAssigneeAndComment(challenge, chlrq)
        if editResult.status_code == 204:
            print(f'\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
        else:
            print(f'\t{Colors.FAIL}[FAILED - {editResult.status_code}]{Colors.ENDC}')
            print(f'{Colors.FAIL}{editResult.text}')
