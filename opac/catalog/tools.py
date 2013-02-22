from catalog import mongomodels


class Navigation(object):

    def __init__(self,
                 journal,
                 issue=None,
                 issue_lib=mongomodels.Issue):

        self._issues = dict((iss['data']['order'],
                             iss['data']['id']) for iss in journal.issues)

        current = max(self._issues, key=lambda x: x)
        self._current = self._issues[current]
        self._issue_lib = issue_lib

        if issue:
            self._issue = issue

        self._journal = journal

    def _load_issue(self):
        self._issue = self._issue_lib.get_issue(
                                        self._journal.acronym,
                                        self._current
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
                                        self._current
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

        for i in range(1, 100):
            match = self._issue.order + i

            next = self._issues.get(match)
            if next:
                return '/issue/{0}/{1}/'.format(
                                        self._journal.acronym,
                                        next
                                        )

        return None

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

        for i in range(1, 100):
            match = self._issue.order - i

            if match == 0:
                break

            previous = self._issues.get(match)
            if previous:
                return '/issue/{0}/{1}/'.format(
                                        self._journal.acronym,
                                        previous)

        return None
