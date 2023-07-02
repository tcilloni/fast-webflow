import requests
from collections import UserDict

from .utils import string_to_dict, slugify, try_request, parallelize
from .config import make_headers


class Item(UserDict):
    """
    An Item object connects with WebFlow's CMS API.

    Upon initialization, the object behaves like a dictionary, where its keys are the fields
    returned by the API's `get` method on the collection. The object allows getting, deleting, and 
    updating the relative item.
    
    You must supply the collection ID as well as the item ID in order to uniquely find the item.

    Attributes:
        id (str): ID field (often `_id`) of the item in the CMS.
        delay (float): number of seconds to wait after a request hits the rate limit.
        max_retries (int): number of times failed requests are retried (including after hitting rate limits).
        data (dict): dictionary representation of the item's data.
    """

    def __init__(self, collection_id: str, item_id: str, max_retries: int = 50, throttle_delay: int = 10):
        '''
        Create a new Item object.
        You must supply the collection ID as well as the item ID in order to uniquely find the item.

        Args:
            collection_id (str): ID field (often `_id`) of the collection in the CMS.
            item_id (str): ID field (often `_id`) of the item in the CMS.
            throttle_delay (float, optional): number of seconds to wait after a request hits the 
                rate limit. Defaults to 10.
            max_retries (int, optional): number of times failed requests are retried (including 
                after hitting rate limits). Defaults to 50.
        '''
        self.id = item_id
        self.delay = throttle_delay
        self.max_retries = max_retries
        self.data = self.get_data()

        self._url = f'https://api.webflow.com/collections/{collection_id}/items/{item_id}?live=true'
        self._headers = make_headers()
    

    def get_data(self) -> dict[str, any]:
        '''
        Fetch the item's information.
        See the `official documentation <https://developers.webflow.com/reference/get-item>`__ 
        for more info. Upon being called, this method will also update the object's internal dictionary.

        Returns:
            dict[str, any]: information about this item (name, slug, etc.).
        '''
        self.data = self._request(requests.get)
        return self.data
    

    def _request(self, request_fn: callable, url: str = None, data: dict = None) -> dict[str, any]:
        '''
        Default request method for the item object.

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
    

    def update_data(self, fields: dict[str,any], draft: bool = False) -> dict[str, str]:
        '''
        Update the item's data completely.
        This method will also update this object's data.

        Args:
            fields (dict[str,any]): new object data.
            draft (bool, optional): draft changes (True) or stage for publish (False). Defaults to False.

        Returns:
            dict[str, str]: basic information about the updated item.
        '''
        payload = {'fields': {'_archived': False, '_draft': draft}}
        payload['fields'].update(fields)

        data = self._request(requests.put, self._url, payload)
        self.get_data() # self-update
        
        return data
    

    def patch(self, fields: dict[str,any], draft: bool = False) -> dict[str, str]:
        '''
        Update the item's data partially.
        This method will also update this object's data.

        Args:
            fields (dict[str,any]): new object data (only that which changes).
            draft (bool, optional): draft changes (True) or stage for publish (False). Defaults to False.

        Returns:
            dict[str, str]: basic information about the updated item.
        '''
        payload = {'fields': {'_archived': False, '_draft': draft}}
        payload['fields'].update(fields)

        data = self._request(requests.patch, self._url, payload)
        self.get_data() # self-update
        
        return data


    def delete(self) -> dict[str, int]:
        '''
        Delete this Item.
        The deletion will take place both in the CMS and locally (you cannot use this object afterwards).

        Returns:
            dict: dictionary that should be `{'deleted': 1}` if deletion was successful.
        '''
        data = self._request(requests.delete, self._url)

        # destroy itself
        self._request = lambda: (_ for _ in ()).throw(Exception('Item does not exist anymore'))
        self.data = None

        return data

