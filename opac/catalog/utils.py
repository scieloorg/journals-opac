class Navigation(object):

    def __init__(self, journal, issue):

        self._issues = dict((issue['data']['order'],
                             issue['data']['id']) for issue in journal.issues)

        self._issue = issue
        self._journal = journal

    @property
    def current_issue(self):
        """
        This method retrives a link to the current issue from a
        given journal.
        """
        current_issue = self._journal.current_issue
        return '/issue/{0}/{1}/'.format(
                                    self._journal._data.get('acronym'),
                                    current_issue
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
