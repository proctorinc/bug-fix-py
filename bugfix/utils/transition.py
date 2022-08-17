from bugfix.api import (
    get_current_fix_version,
    transition_issue_to_planned,
    transition_issue_to_in_progress,
    transition_issue_to_closed,
    transition_issue_to_feedback_open,
    get_linked_challenges,
    transition_issue_to_feedback_review,
    edit_issue_details,
)

from .input import (
    get_chlc
)

from bugfix.formatting import (
    Colors
)

def transition_jira_issues(chlrq, fix_message, is_cherrypick_required):
    """
    Use Jira API to transition tickets through Jira workflow
    """
    # API call to get current version name and id
    fixVersionName, fixVersionID = get_current_fix_version()

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
    plannedResult = transition_issue_to_planned(chlrq, fixVersionID)
    if plannedResult.status_code == 204:
        print(f'\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
    else:
        print(f'\t{Colors.FAIL}[FAILED - {plannedResult.status_code}: {plannedResult.reason}]{Colors.ENDC}')

    # Transition to in progress
    print(f'\tTo In Progress', end='')
    
    # If api returns 204, transition was successful
    inProgressResult = transition_issue_to_in_progress(chlrq)
    if inProgressResult.status_code == 204:
        print(f'\t\t\t\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
    else:
        print(f'\t\t\t\t{Colors.FAIL}[FAILED - {inProgressResult.status_code}: {inProgressResult.reason}]{Colors.ENDC}')

    #################################################################################
    # Linking CHLC to CHLRQ no longer required. Step is now done on ticket creation #
    #################################################################################
    # # Link CHLC to CHLRQ
    # print(f'\tLinking {Colors.HEADER}{chlc}{Colors.ENDC} [relates to]', end='')
    
    # # If api returns 204, transition was successful
    # linkResult = link_creation_chlc(chlrq, chlc[-4:])
    # if linkResult == 201:
    #     print(f'\t\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
    # else:
    #     print(f'\t\t{Colors.FAIL}[FAILED - {linkResult}]{Colors.ENDC}')

    # Transition CHLRQ to closed w/ fix message
    print(f'\tTo Closed [with description of fix]', end='')
    
    # If api returns 204, transition was successful
    closedResult = transition_issue_to_closed(chlrq, fix_message)
    if closedResult.status_code == 204:
        print(f'\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
    else:
        print(f'\t{Colors.FAIL}[FAILED - {closedResult.status_code}: {closedResult.reason}]{Colors.ENDC}')

    # If full app and fix was on the secure branch, transition all CHLC's
    if is_cherrypick_required:
        # Get application CHLC
        print('\n[Enter Application CHLC]')
        application_chlc = get_chlc()

        # Notify user of parent CHLC number
        print(f'Application CHLC: {Colors.WARNING}{application_chlc}{Colors.ENDC}')

        # Get all CHLC's linked to the creation ticket
        challenges = get_linked_challenges(application_chlc)

        # Print number of challenges to bulk transition
        print(f'Challenges to bulk transition: {len(challenges)}')
    
    else:
        # Get challenge chlc
        print('\n[Enter Challenge CHLC]')
        challenge_chlc = get_chlc()

        # Set challenges to the initial chlc
        challenges = ['CHLC-' + challenge_chlc[-4:]]

    print(f'\nTransitioning [{Colors.OKCYAN}{len(challenges)}{Colors.ENDC}] {Colors.HEADER}CHLC\'s{Colors.ENDC}')

    # Transition all challenges
    for challenge in challenges:
        # print('Up now:', challenge)

        print(f'Transitioning {Colors.HEADER}{challenge}{Colors.ENDC}:')

        # Transition challenge to Feedback Open
        print('\tTo Feedback Open', end='')
        
        # If api returns 204, transition was successful
        feedbackOpenResult = transition_issue_to_feedback_open(challenge)
        if feedbackOpenResult.status_code == 204:
            print(f'\t\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
        else:
            print(f'\t\t{Colors.FAIL}[FAILED - {feedbackOpenResult.status_code}: {feedbackOpenResult.reason}]{Colors.ENDC}')

        # Transition challenge to Feedback Review w/ fix message and set assignee to Thomas
        print('\tTo Feedback Review', end='')

        # If api returns 204, transition was successful
        feedbackReviewResult = transition_issue_to_feedback_review(challenge)
        if feedbackReviewResult.status_code == 204:
            print(f'\t\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
        else:
            print(f'\t\t{Colors.FAIL}[FAILED - {feedbackReviewResult.status_code}: {feedbackReviewResult.reason}]{Colors.ENDC}')

        # Sets assignee and adds CHLRQ as comment
        print('\tAdding assignee and comment', end='')

        # If api returns 204, transition was successful
        editResult = edit_issue_details(challenge, chlrq)
        if editResult.status_code == 204:
            print(f'\t{Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
        else:
            print(f'\t{Colors.FAIL}[FAILED - {editResult.status_code}]{Colors.ENDC}')
            print(f'{Colors.FAIL}{editResult.text}')
