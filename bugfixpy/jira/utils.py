"""Utility functions for jira class"""


def append_project_type_if_not_present(
    valid_issue_number: str, project_type: str
) -> str:
    """Append project type if not already present"""

    if project_type not in valid_issue_number:
        return f"{project_type}-{valid_issue_number}"

    return valid_issue_number
