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

        return '/issue/{0}/{1}'.format(self._journal.get('acronym'),
                                       self._issue.id)

    def next_issue(self):
        """
        This method retrieves the next issue url according to the
        order sequence. If there is a gap in the issues sequence,
        for legacy compliance, the script will attempt a 100 different
        order numbers before delivery "None".
        """
        for i in range(1, 100):
            match = self._issue['order'] + i
            next = self._issues.get(match)
            if next:
                return '/issue/{0}/{1}'.format(
                                        self._journal._data.get('acronym'),
                                        next
                                        )

        return None

    def previous_issue(self):
        """
        This method retrieves the previous issue url according to the
        order sequence. If there is a gap in the issues sequence,
        for legacy compliance, the script will attempt a 100 different
        order numbers before delivery "None".
        """
        for i in range(1, 100):
            match = self._issue['order'] - i

            if match == 0:
                break

            previous = self._issues.get(match)
            if previous:
                return '/issue/{0}/{1}'.format(
                                        self._journal._data.get('acronym'),
                                        previous)

        return None
