# coding: utf-8
import abc
import re

from django.conf import settings

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

    def __init__(self, data,
                       manager_api_lib=SciELOManagerAPI,
                       settings=settings):
        """
        ``data`` must be an iterable
        """
        api_username = getattr(settings, 'SCIELOMANAGER_API_USERNAME', None)
        api_key = getattr(settings, 'SCIELOMANAGER_API_KEY', None)
        api_uri = getattr(settings, 'SCIELOMANAGER_API_URI', None)

        if not api_username or not api_key or not api_uri:
            raise ValueError('missing config to manager api')

        self._manager_api = manager_api_lib(api_uri,
                                            username=api_username,
                                            api_key=api_key)
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
        raise UnmetPrecondition('missing item "issues"')

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
        raise UnmetPrecondition('missing item "missions"')


class PMission(Pipe):

    @precondition(pmission_precondition)
    def transform(self, data):

        new_missions = {}
        for mission in data['missions']:
            new_missions[mission[0]] = mission[1]

        # rebinding the issues attr
        data['missions'] = new_missions

        return data


def psection_precondition(data):
    """
    Asserts that:

    * ``sections`` exists
    * ``rosource_uri``'s are valid
    """
    pattern = re.compile('/api/v1/sections/\d+/$')

    if 'sections' not in data:
        raise UnmetPrecondition('missing item "sections"')

    if not all([re.match(pattern, uri) for uri in data['sections']]):
        raise UnmetPrecondition('invalid uri')


class PSection(Pipe):

    @precondition(psection_precondition)
    def transform(self, data):

        new_sections = []
        for section in data['sections']:
            _api_res = self._fetch_resource(section)
            _tmp_section = {
                'id': _api_res['id'],
                'resource_uri': section,
                'titles': [{title[0]: title[1]} for title in _api_res['titles']]
            }
            new_sections.append(_tmp_section)

        if 'issues' in data:
            for issue in data['issues']:
                for i, section in enumerate(issue['data']['sections']):
                    _tmp_inner_section = {
                        'id': int(self._parse_resource_uri(section)['resource_id']),
                    }
                    # Changing the inner section datastructure cirurgically
                    issue['data']['sections'][i] = _tmp_inner_section

        # rebinding the sections attr
        data['sections'] = new_sections

        return data


class PCleanup(Pipe):

    def transform(self, data):
        if 'is_trashed' in data:
            del(data['is_trashed'])

        return data


class Pipeline(object):
    """
    Represents a chain of pipes (duh).

    ``*args`` are the pipes that will be executed in order
    to transform the input data.
    """
    def __init__(self, *args):
        self._pipes = args

    def run(self, data, rewrap=False):
        """
        Wires the pipeline and returns a lazy object of
        the transformed data.

        ``data`` must be an iterable, where a full document
        must be returned for each loop

        ``rewrap`` is a bool that indicates the need to rewrap
        data in case iterating over it produces undesired data,
        for instance ``dict`` instances.
        """
        if rewrap:
            data = [data]

        for pipe in self._pipes:
            data = pipe(data)
        else:
            for out_data in data:
                yield out_data
