# coding: utf-8
import abc


class UnmetPrecondition(Exception):
    pass


def precondition(precond):
    """
    Runs the callable responsible for making some assertions
    about the data structure expected for the transformation.

    If the precondition is not achieved, a UnmetPrecondition
    exception must be raised, and then the transformation pipe
    is bypassed.
    """
    def decorator(f):
        def decorated(instance, data):
            try:
                precond(data)
            except UnmetPrecondition:
                # bypass the pipe
                return data
            else:
                return f(instance, data)
        return decorated
    return decorator


class Pipe(object):
    """
    A segment of the transformation pipeline.

    ``transform`` method must return the transformation result.
    Sometimes a transformation process may need to fetch content
    from different endpoints, and it can be achieved through
    the ``fetch_resource`` method.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, data):
        """
        ``data`` can be the raw data, in case the pipe is the
        first segment of the pipeline, or a generator in case
        it receives data from another pipe.
        """
        if not hasattr(data, 'next'):
            data = [data]

        self._iterable_data = data

    def __iter__(self):
        for data in self._iterable_data:
            yield self.transform(data)

    def _fetch_resource(self, endpoint, resource_id):
        """
        Fetch data of the specific resource.

        ``endpoint`` is a string representing the entity type.
        ``resource_id`` is a string.
        """
        return {
            'cover': None,
            'created': '2010-04-01T01:01:01',
            'ctrl_vocabulary': 'nd',
            'editorial_standard': 'vancouv',
            'id': 1,
            'is_marked_up': False,
            'is_press_release': False,
            'is_trashed': False,
            'journal': '/api/v1/journals/1/',
            'label': '45 (4)',
            'number': '4',
            'order': 4,
            'publication_end_month': 12,
            'publication_start_month': 10,
            'publication_year': 2009,
            'resource_uri': '/api/v1/issues/1/',
            'sections': [
                '/api/v1/sections/514/',
            ],
            'suppl_number': None,
            'suppl_volume': None,
            'total_documents': 17,
            'updated': '2012-11-08T10:35:37.193612',
            'volume': '45'
        }

    @abc.abstractmethod
    def transform(self, data):
        """
        Performs the desired transformation to the data.
        """


class PIssue(Pipe):
    """
    Transforms Issues
    """
    def _parse_resource_uri(self, resource_uri):
        cleaned = [seg for seg in resource_uri.split('/') if seg]
        endpoint, resource_id = cleaned[-2:]

        return {'endpoint': endpoint, 'resource_id': resource_id}

    def transform(self, data):

        new_issues = []
        for issue in data['issues']:
            _qry_params = self._parse_resource_uri(issue)
            _tmp_issue = self._fetch_resource(_qry_params['endpoint'],
                _qry_params['resource_id'])

            del(_tmp_issue['journal'])

            # rearranging the overall structure
            _new_issue = {'id': _tmp_issue['id'], 'data': _tmp_issue}

            new_issues.append(_new_issue)

        # rebinding the issues attr
        data['issues'] = new_issues

        return data
