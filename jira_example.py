# JIRA playing
#
from jira.client import JIRA

class JiraException(Exception):
    pass

class JiraAPi:
    """
    Simple class to update the status of a jira issue
    """
    def __init__(self, username, password, server):
        options = {'server': server}
        self.jira = JIRA(options, basic_auth=(username, password))

    def get_issue(self, issue_key):
        """
        Returns issue object

        Useful fields:
        Who raised: issue.fields.reporter.displayName
        Priority: issue.fields.priority.name
        Status: issue.fields.status.name
        Title: issue.fields.summary
        Last Updated: issue.fields.updated
        """
        return self.jira.issue(issue_key)

    def check_release_status(self, issue_key):
        """
        Returns true if status is Approved
        """
        issue = self.get_issue(issue_key)
        if issue.fields.status.name == 'Approved':
            return True
        return False