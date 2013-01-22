# coding: utf-8
import abc
import re

from utils.sync.datacollector import SciELOManagerAPI


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

    def __init__(self, data, manager_api_lib=SciELOManagerAPI):
        """
        ``data`` can be the raw data, in case the pipe is the
        first segment of the pipeline, or a generator in case
        it receives data from another pipe.
        """
        self._manager_api = manager_api_lib('http://manager.scielo.org/api/v1/')

        # initial data
        if isinstance(data, dict):
            data = [data]

        self._iterable_data = data

    def __iter__(self):
        """
        Iters through all items of ``self._iterable_data``, yielding its
        data already transformed.

        The iterable interface is the heart of the pipeline machinery.
        """
        for data in self._iterable_data:
            yield self.transform(data)

    def _parse_resource_uri(self, resource_uri):
        """
        Parses a tipical resource path and returns a key-value pair
        with the ``endpoint`` and ``resource_id``.
        """
        cleaned = [seg for seg in resource_uri.split('/') if seg]
        endpoint, resource_id = cleaned[-2:]

        return {'endpoint': endpoint, 'resource_id': resource_id}

    def _fetch_resource(self, resource_path):
        """
        Fetch data from a specific resource.

        ``endpoint`` is a string representing the entity type.
        ``resource_id`` is a string.
        """
        _qry_params = self._parse_resource_uri(resource_path)
        return self._manager_api.fetch_data(_qry_params['endpoint'],
            _qry_params['resource_id'])

    @abc.abstractmethod
    def transform(self, data):
        """
        Performs the desired transformation to the data.
        """


def pissue_precondition(data):
    """
    Asserts that:

    * The item ``issues`` exists.
    * All resources are valid in terms of syntax.
    """
    pattern = re.compile('/api/v1/issues/\d+/$')

    if 'issues' not in data:
        raise UnmetPrecondition('missing issues item')

    if not all([re.match(pattern, uri) for uri in data['issues']]):
        raise UnmetPrecondition('invalid uri')


class PIssue(Pipe):

    @precondition(pissue_precondition)
    def transform(self, data):
        new_issues = []
        for issue in data['issues']:
            _tmp_issue = self._fetch_resource(issue)

            if 'journal' in _tmp_issue:
                del(_tmp_issue['journal'])

            # rearranging the overall structure
            _new_issue = {'id': _tmp_issue['id'], 'data': _tmp_issue}

            new_issues.append(_new_issue)

        # rebinding the issues attr
        data['issues'] = new_issues

        return data


def pmission_precondition(data):
    """
    Asserts that:

    * The item ``missions`` exists.
    """
    if 'missions' not in data:
        raise UnmetPrecondition('missing missions item')


class PMission(Pipe):

    @precondition(pmission_precondition)
    def transform(self, data):

        new_missions = {}
        for mission in data['missions']:
            new_missions[mission[0]] = mission[1]

        # rebinding the issues attr
        data['missions'] = new_missions

        return data
