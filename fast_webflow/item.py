import requests
from collections import UserDict

from .utils import string_to_dict, slugify, try_request, parallelize
from .config import make_headers


class Item(UserDict):
    id: str
    _url: str
    _headers: dict[str, str]
    delay: int
    max_retries: int

    def __init__(self, collection_id: str, item_id: str, max_retries: int = 50, throttle_delay: int = 10):
        self.id = item_id
        self._url = f'https://api.webflow.com/collections/{collection_id}/items/{item_id}?live=true'
        self._headers = make_headers()
        self.delay = throttle_delay
        self.max_retries = max_retries
        self.data = self.get_data()
    

    def get_data(self) -> dict:
        return self._request(requests.get)
    

    def _request(self, request_fn: callable, url: str = None, data: dict = None) -> dict:
        if url is None:
            url = self._url
        
        return try_request(request_fn, url, self._headers, data, self.max_retries, self.delay)
    

    def update(self, fields: dict[str,any], draft: bool = False) -> dict:
        payload = {'fields': {'_archived': False, '_draft': draft}}
        payload['fields'].update(fields)

        data = self._request(requests.put, self._url, payload)
        
        return data
    

    def path(self, fields: dict[str,any], draft: bool = False) -> dict:
        payload = {'fields': {'_archived': False, '_draft': draft}}
        payload['fields'].update(fields)

        data = self._request(requests.patch, self._url, payload)
        
        return data


    def delete(self) -> dict:
        data = self._request(requests.delete, self._url)
        return data

