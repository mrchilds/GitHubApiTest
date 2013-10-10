# Playing with GitHub api for integration into hubot
#
# Important: Maximum 3000 api requests per hour on authorized requests.
#
# Consider storing results locally if exceeding limit
#
# Public repo so no auth required
from github3 import GitHub

class GitHubApi:
    """
    GitHub API interaction using github3
    """
    def __init__(self, repo_owner, repo_name, token):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.gh = GitHub(token=token)

    def get_issues(self, label=None):
        """Returns all issues (matching label)"""
        return self.gh.iter_repo_issues(self.repo_owner, self.repo_name, labels=label)

    def get_issue(self, issue_id):
        """Returns issue"""
        return self.gh.issue(self.repo_owner, self.repo_name, issue_id)

    def get_matching_pull_requests(self, label=None):
        """
        Returns all matching issues

        Pull requests are treated as issues
        """
        pull_request_list = []
        for issue in self.get_issues(label):
            # Get Pull Request
            pull_request_list.append(self.pull_request_information(issue.number))
        return pull_request_list

    def get_pull_request_status(self, label=None):
        """Returns"""
        pull_requests = self.get_matching_pull_requests(label)
        pull_requests_information = "Pull Requests - %s\n\n" % label
        for pr in pull_requests:
            pull_requests_information += "Title: %s\nBranch: %s\nLink: %s\nMergeable: %s\n\n"\
                % (pr.title, pr.head.ref, pr.html_url, pr.mergeable)
        return pull_requests_information

    def pull_request_information(self, pull_request_id):
        """Returns specified pull request"""
        pull_request = self.gh.pull_request(self.repo_owner, self.repo_name, pull_request_id)
        return pull_request

    def assign_new_label_to_issue(self, branch, label, who):
        """Update issue label"""
        # Find issue
        issue = self.filter_on_branch(self.get_matching_pull_requests(), branch)
        # Remove all existing labels
        issue.remove_all_labels()
        # Add label 'release'
        issue.add_labels(label)
        # Add comment for tracking
        issue.create_comment("%s assigned label '%s' via hipchat" % (who, label))

    def filter_on_branch(self, pull_requests, branch):
        for pull_request in pull_requests:
            if pull_request.head.ref == branch:
                # Get issue
                return self.get_issue(pull_request.number)