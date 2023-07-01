import requests
from collections import UserDict
from functools import partial
from itertools import repeat

from .utils import string_to_dict, slugify, try_request, parallelize
from .config import make_headers


class Collection(UserDict):
    id: str
    _url: str
    _items_url: str
    _headers: dict[str, str]
    _max_items_per_request: int = 100
    delay: int
    max_retries: int

    def __init__(self, collection_id: str, max_retries: int = 50, throttle_delay: int = 10):
        self.id = collection_id
        self._url = f'https://api.webflow.com/collections/{collection_id}'
        self._items_url = f'https://api.webflow.com/collections/{collection_id}/items?live="true"'
        self._headers = make_headers()
        self.delay = throttle_delay
        self.max_retries = max_retries
        self.data = self.get_data()
    

    def get_data(self) -> dict:
        return self._request(requests.get)
    

    def _request(self, request_fn: callable, url: str = None, data: dict = None) -> dict:
        if url is None:
            url = self._items_url
        
        return try_request(request_fn, url, self._headers, data, self.max_retries, self.delay)
    

    def post_item(self, fields: dict[str,any], draft: bool = False):
        payload = {'fields': {'_archived': False, '_draft': draft}}
        payload['fields'].update(fields)

        data = self._request(requests.post, self._items_url, payload)
        
        return data
    

    def post_items(self, fields_list: list[dict[str,any]], draft: bool = False):
        post_item = partial(self.post_item, draft = draft)
        data = parallelize(post_item, fields_list)
        
        return data


    def publish_items(self, item_ids: list[str]) -> dict:
        max_items = self._max_items_per_request  # API rule
        url = self._url + '/items/publish'
        data = {}

        # split IDs into lists of max 100 items
        item_ids = [item_ids[i:i+max_items] for i in range(0, len(item_ids), max_items)]
        payloads = [{"itemIds": ids} for ids in item_ids]

        # send parallel requests
        parallel_arguments = zip(repeat(url), payloads)
        returns  = parallelize(lambda args: requests.put(*args), parallel_arguments)

        # merge responses
        for key in ['publishedItemIds', 'errors']:
            data[key] = [item for resp in returns for item in resp[key]]
        
        return data
    

    def delete_items(self, item_ids: list[str]) -> dict[str,list[any]]:
        max_items = self._max_items_per_request  # API rule
        data = {}

        # split IDs into lists of max 100 items
        item_ids = [item_ids[i:i+max_items] for i in range(0, len(item_ids), max_items)]
        payloads = [{"itemIds": ids} for ids in item_ids]

        # send parallel requests
        parallel_arguments = zip(repeat(self._items_url), payloads)
        returns  = parallelize(lambda args: requests.delete(*args), parallel_arguments)

        # merge responses
        for key in ['deletedItemIds', 'errors']:
            data[key] = [item for resp in returns for item in resp[key]]

        return data
    

    def get_all_items(self) -> list[dict]:
        # update total number of items
        self.data = self.get_data()
        max_items = self._max_items_per_request  # API rule
        total = self.data['total']

        # prepare one URL request for each offset in 0..total..limit
        item_lists = parallelize(self.get_items, range(0, total, max_items))
        all_items = [item for item_list in item_lists for item in item_list['items']]
        
        return all_items
    

    def get_items(self, offset: int = 0, limit: int = 100) -> list[dict]:
        url = self._items_url + f"&offset={offset}&limit={limit}"
        data = self._request(requests.get, url)
        
        return data

