import requests
from collections import UserDict

from ..entity import Entity
from ..utils import try_request


def list_sites():
    return Entity(None)._get('https://api.webflow.com/sites')


class Site(Entity):
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

    def __init__(self, id: str, *args, **kwargs):
        '''
        Create a new Site object.

        Args:
            site_id (str): ID field (often `_id`) of the site in the CMS.
            throttle_delay (float, optional): number of seconds to wait after a request hits the 
                rate limit. Defaults to 10.
            max_retries (int, optional): number of times failed requests are retried (including 
                after hitting rate limits). Defaults to 50.
        '''
        super(Site, self).__init__(id, *args, **kwargs)
        self._url = f'https://api.webflow.com/sites/{id}'
        self.data = self.get_data()
    

    def get_data(self) -> dict[str, any]:
        '''
        Fetch the site's information.
        See the `official documentation <https://developers.webflow.com/reference/get-site>`__ 
        for more info. Upon being called, this method will also update the object's internal dictionary.

        Returns:
            dict[str, any]: information about this site (name, domains, etc.).
        '''
        return self._get()


    def publish(self, domains: list[str] = None) -> dict[str, bool]:
        '''
        Publish the website to any domain(s).
        By default, the website is published to all associated domains.

        Args:
            domains (list[str], optional): domain URLs to publish to. Defaults to All.

        Returns:
            dict[str, bool]: `{'queued': True}` if successful, `{'queued': False}` otherwise
        '''
        domains = domains or [domain['name'] for domain in self.get_domains()]
        return self._post(self._url + '/publish', {"domains": domains})
    

    def get_domains(self) -> list[dict[str, str]]:
        '''
        Get a list of domains the site can be published to.

        Returns:
            list[dict[str, str]]: list of `{'id': id, 'name': name}` dictionaries.
        '''
        return self._get(self._url + '/domains')


    def get_collections(self) -> list[dict[str, any]]:
        '''
        List the collections in the site's CMS.

        Returns:
            list[dict[str, any]]: list of collections with some basic data.
        '''
        return self._get(self._url + '/collections')