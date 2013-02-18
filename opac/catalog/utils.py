class Navigation(object):

    def __init__(self, journal):

        self._issues = dict((issue['data']['order'], issue['data']['id']) for issue in journal.issues)

    def next_issue(self, current_order):
        """
        This method retrieves the next issue id according to the
        order sequence. If there is a gap in the issues sequence,
        for legacy compliance, the script will attempt a 100 different
        order numbers before delivery "None".
        """
        for i in range(1, 100):
            match = current_order + i
            next = self._issues.get(match)
            if next:
                return next

        raise ValueError('no next issues found')

    def previous_issue(self, current_order):
        """
        This method retrieves the previous issue id according to the
        order sequence. If there is a gap in the issues sequence,
        for legacy compliance, the script will attempt a 100 different
        order numbers before delivery "None".
        """
        for i in range(1, 100):
            match = current_order - i

            if match == 0:
                break

            previous = self._issues.get(match)
            if previous:
                return previous

        raise ValueError('no next issues found')
