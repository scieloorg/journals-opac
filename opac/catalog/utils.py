from catalog import mongomodels


class Navigation(object):

    def __init__(self, journal, issue=None):

        self._issues = dict((iss['data']['order'],
                             iss['data']['id']) for iss in journal.issues)

        current = max(self._issues, key=lambda x: x)
        self._current = self._issues[current]

        if issue:
            self._issue = issue
        else:
            self._issue = mongomodels.Issue.get_issue(
                                        journal._data.get('acronym'),
                                        self._current
                                        )

        self._journal = journal

    @property
    def current_issue(self):
        """
        This method retrives a link to the current issue from a
        given journal.
        """

        return '/issue/{0}/{1}/'.format(
                                        self._journal._data.get('acronym'),
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
        for i in range(1, 100):
            match = self._issue._data.get('order') + i

            next = self._issues.get(match)
            if next:
                return '/issue/{0}/{1}/'.format(
                                        self._journal._data.get('acronym'),
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

        for i in range(1, 100):
            match = self._issue._data.get('order') - i

            if match == 0:
                break

            previous = self._issues.get(match)
            if previous:
                return '/issue/{0}/{1}/'.format(
                                        self._journal._data.get('acronym'),
                                        previous)

        return None
