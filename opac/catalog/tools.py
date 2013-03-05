import collections
from catalog import mongomodels


class Navigation(object):

    def __init__(self,
                 journal,
                 issue=None,
                 issue_lib=mongomodels.Issue):

        issues = dict(((iss['data']['publication_year'], iss['data']['order']),
                             iss['data']['id']) for iss in journal.issues)

        self._issues = collections.OrderedDict(sorted(issues.items()))

        self._current_key = max(self._issues)
        self._current_value = self._issues[self._current_key]
        self._issue_lib = issue_lib

        if issue:
            self._issue = issue

        self._journal = journal

    def _load_issue(self):
        self._issue = self._issue_lib.get_issue(
                                        self._journal.acronym,
                                        self._current_value
                                        )

    @property
    def ahead(self):

        ahead = self._journal.current_ahead_documents

        if ahead > 0:
            return '/ahead/{0}/'.format(self._journal.acronym)
        else:
            return None

    @property
    def current_issue(self):
        """
        This method retrives a link to the current issue from a
        given journal.
        """

        return '/issue/{0}/{1}/'.format(
                                        self._journal.acronym,
                                        self._current_value
                                        )

    @property
    def next_issue(self):
        """
        This method retrieves the next issue url according to the
        order sequence. If there is a gap in the issues sequence,
        for legacy compliance, the script will attempt a 100 different
        order numbers before delivery "None".
        """
        if not hasattr(self, '_issue'):
            self._load_issue()

        index = self._issues.keys().index((self._issue.publication_year,
                                          self._issue.order))

        try:
            next_index = self._issues.keys()[index + 1]
        except IndexError:
            return None

        next = self._issues.get(next_index)

        if next:
            return '/issue/{0}/{1}/'.format(
                                    self._journal.acronym,
                                    next)


    @property
    def previous_issue(self):
        """
        This method retrieves the previous issue url according to the
        order sequence. If there is a gap in the issues sequence,
        for legacy compliance, the script will attempt a 100 different
        order numbers before delivery "None".
        """
        if not hasattr(self, '_issue'):
            self._load_issue()

        index = self._issues.keys().index((self._issue.publication_year,
                                          self._issue.order))

        if index != 0:
            previous_index = self._issues.keys()[index - 1]
        else:
            return None

        previous = self._issues.get(previous_index)

        if previous:
            return '/issue/{0}/{1}/'.format(
                                    self._journal.acronym,
                                    previous)
