# coding: utf-8
import slumber


class SciELOManagerAPI(object):
    """
    Responsible for collecting data from SciELO Manager's RESTful
    interface, and making them available as Python datastructures.
    """

    def __init__(self,
                 resource_url,
                 slumber_lib=slumber,
                 username=None,
                 api_key=None):
        self._resource_url = resource_url
        self._slumber_lib = slumber_lib
        self._api = self._slumber_lib.API(resource_url)
        self._username = username
        self._api_key = api_key

    def fetch_data(self, endpoint,
                         resource_id=None,
                         **kwargs):
        """
        Fetches the specified resource from the SciELO Manager API.
        """

        if all([self._username, self._api_key]):
            kwargs['username'] = self._username
            kwargs['api_key'] = self._api_key

        resource = getattr(self._api, endpoint)

        if resource_id:
            resource = resource(resource_id)

        return resource.get(**kwargs)
