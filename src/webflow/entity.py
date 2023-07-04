import requests
import time
from collections import UserDict

from .utils import string_to_dict
from .config import make_headers


class Entity(UserDict):
    """
    An Entity is a general-purpose object that connects with WebFlow's API.

    Upon initialization, the object behaves like a dictionary, where its keys are the fields
    returned by the API's `get` method on the entity. 
    
    Attributes:
        id (str): ID field (`_id` throught the API Docs) of the entity.
        delay (float): number of seconds to wait after a request hits the rate limit.
        max_retries (int): number of times failed requests are retried (including after hitting rate limits).
        data (dict): dictionary representation of the entity's data.
    """

    def __init__(self, id: str, max_retries: int = 50, throttle_delay: int = 10):
        '''
        Create a new Entity object.

        Args:
            id (str): ID field (`_id` throught the API Docs) of the entity.
            max_retries (int, optional): number of times failed requests are retried (including 
                after hitting rate limits). Defaults to 50.
            throttle_delay (float, optional): number of seconds to wait after a request hits the 
                rate limit. Defaults to 10.
        '''
        self.id = id
        self.delay = throttle_delay
        self.max_retries = max_retries
        self._headers = make_headers()
    

    def _request(self, request_fn: callable, url: str = None, data: dict = None) -> any:
        '''
        Default request method for the item object.
        The returned value, if the call is successful, is either a dictionary or a list of dictionaries,
        always parsed from the JSON in the API's response.

        Args:
            request_fn (callable): function to call (one of requests.get/put/post/delete).
            url (str, optional): specify to use a different URL than the default one. Defaults to `_url`.
            data (dict, optional): optional JSON data to ship with the request. Defaults to None.

        Returns:
            any: whatever the response is, if valid, and always a dictionary or list of dictinaries.
        '''
        current_try = 0
        url = url or self._url

        if not url:
            raise NotImplementedError('Class must set the `_url` field upon instantiation, or have a URL passed.')

        # loop until either: 
        while True:
            response = request_fn(url, json = data, headers = self._headers)

            # TRY AGAIN; hit API limit
            if response.status_code == 429:
                if current_try < self.max_retries: 
                    time.sleep(self.delay)
                    current_try += 1
                else:
                    raise 
            
            # SUCCESS; return the result
            elif response.status_code == 200:
                return string_to_dict(response.text)

            # ERROR; return it
            else:
                response.raise_for_status()

    
    def _get(self, url: str = None) -> any:
        '''
        Wrapper for the GET method.

        Args:
            url (str, optional): fully formed url to connect to. Defaults to `_url`.

        Returns:
            any: if there are no errors, returns a dict or list of dicts parsed from the JSON response.
        '''
        return self._request(requests.get, url)


    def _put(self, url: str = None, payload: dict = None) -> any:
        '''
        Wrapper for the PUT method.

        Args:
            url (str, optional): fully formed url to connect to. Defaults to `_url`.
            payload (dict, optional): optional data to send along the request as JSON. Defaults to None.

        Returns:
            any: if there are no errors, returns a dict or list of dicts parsed from the JSON response.
        '''
        return self._request(requests.put, url, payload)


    def _post(self, url: str = None, payload: dict = None) -> any:
        '''
        Wrapper for the POST method.

        Args:
            url (str, optional): fully formed url to connect to. Defaults to `_url`.
            payload (dict, optional): optional data to send along the request as JSON. Defaults to None.

        Returns:
            any: if there are no errors, returns a dict or list of dicts parsed from the JSON response.
        '''
        return self._request(requests.post, url, payload)


    def _patch(self, url: str = None, payload: dict = None) -> any:
        '''
        Wrapper for the PATCH method.

        Args:
            url (str, optional): fully formed url to connect to. Defaults to `_url`.
            payload (dict, optional): optional data to send along the request as JSON. Defaults to None.

        Returns:
            any: if there are no errors, returns a dict or list of dicts parsed from the JSON response.
        '''
        return self._request(requests.patch, url, payload)


    def _delete(self, url: str = None, payload: dict = None) -> any:
        '''
        Wrapper for the DELETE method.

        Args:
            url (str, optional): fully formed url to connect to. Defaults to `_url`.
            payload (dict, optional): optional data to send along the request as JSON. Defaults to None.

        Returns:
            any: if there are no errors, returns a dict or list of dicts parsed from the JSON response.
        '''
        return self._request(requests.delete, url, payload)

