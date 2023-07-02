import requests
from collections import UserDict

from .utils import string_to_dict, slugify, try_request
from .config import make_headers


def list_sites():
    data = try_request(requests.get, 'https://api.webflow.com/sites', make_headers())
    return data


class Site(UserDict):
    """
    A Site object connects with WebFlow's General API.

    Upon initialization, the object behaves like a dictionary, where its keys are the fields
    returned by the API's `get` method on the site. The object allows all operations that the API
    allows for sites.
    
    Attributes:
        id (str): ID field (often `_id`) of the site in the CMS.
        delay (float): number of seconds to wait after a request hits the rate limit.
        max_retries (int): number of times failed requests are retried (including after hitting rate limits).
        data (dict): dictionary representation of the site's data.
    """

    def __init__(self, site_id: str, max_retries: int = 50, throttle_delay: int = 10):
        '''
        Create a new Site object.

        Args:
            site_id (str): ID field (often `_id`) of the site in the CMS.
            throttle_delay (float, optional): number of seconds to wait after a request hits the 
                rate limit. Defaults to 10.
            max_retries (int, optional): number of times failed requests are retried (including 
                after hitting rate limits). Defaults to 50.
        '''
        self.id = site_id
        self.delay = throttle_delay
        self.max_retries = max_retries
        self.data = self.get_data()

        self._url = f'https://api.webflow.com/sites/{site_id}'
        self._headers = make_headers()
    

    def get_data(self) -> dict[str, any]:
        '''
        Fetch the site's information.
        See the `official documentation <https://developers.webflow.com/reference/get-site>`__ 
        for more info. Upon being called, this method will also update the object's internal dictionary.

        Returns:
            dict[str, any]: information about this site (name, domains, etc.).
        '''
        return self._request(requests.get)


    def _request(self, request_fn: callable, url: str = None, data: dict = None) -> dict[str, any]:
        '''
        Default request method for the site object.

        Args:
            request_fn (callable): function to call (one of requests.get/put/post/delete).
            url (str, optional): specify to use a different URL than the default one. Defaults to `_url`.
            data (dict, optional): optional JSON data to ship with the request. Defaults to None.

        Returns:
            dict[str, any]: whatever the response is, if valid, and always a dictionary.
        '''
        if url is None:
            url = self._url
        
        return try_request(request_fn, url, self._headers, data, self.max_retries, self.delay)
    

    def publish(self, domains: list[str] = None) -> dict[str, bool]:
        '''
        Publish the website to any domain(s).
        By default, the website is published to all associated domains.

        Args:
            domains (list[str], optional): domain URLs to publish to. Defaults to All.

        Returns:
            dict[str, bool]: `{'queued': True}` if successful, `{'queued': False}` otherwise
        '''
        # `queued`
        if not domains:
            domains = [domain['name'] for domain in self.get_domains()]

        return self._request(requests.post, self._url + '/publish', {"domains": domains})
    

    def get_domains(self) -> list[dict[str, str]]:
        '''
        Get a list of domains the site can be published to.

        Returns:
            list[dict[str, str]]: list of `{'id': id, 'name': name}` dictionaries.
        '''
        return self._request(requests.get, self._url + '/domains')


    def get_collections(self) -> list[dict[str, any]]:
        '''
        List the collections in the site's CMS.

        Returns:
            list[dict[str, any]]: list of collections with some basic data.
        '''
        return self._request(requests.get, self._url + '/collections')