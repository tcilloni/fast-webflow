import requests
import time
from functools import partial

from .utils import string_to_dict, slugify
from .config import make_headers


class Collection:
    colletion_id: str
    url: str
    headers: dict[str, str]
    delay: int
    max_retries: int

    def __init__(self, auth_token: str, collection_id: str, max_retries: int = 50, throttle_delay: int = 10):
        self.collection_id = collection_id
        self.url = f'https://api.webflow.com/collections/{collection_id}/items?live="true"'
        self.headers = make_headers(auth_token)
        self.delay = throttle_delay
        self.max_retries = max_retries
    

    def try_request(self, request_fn: callable, url: str, data: dict = None) -> tuple[bool,dict]:
        retry = 0

        while True:
            response = request_fn(url, json = data, headers = self.headers)

            # hit API limit
            if response.status_code == 429 and retry < self.max_retries: 
                time.sleep(self.delay)
                retry += 1
            
            # success, can return
            elif response.status_code == 200:
                return True, string_to_dict(response.text)

            # some other error; return it
            else:
                return False, string_to_dict(response.text)
    

    def post_item(self, fields: dict[str,any], draft: bool = False):
        payload = {'fields': {'_archived': False, '_draft': draft}}
        payload['fields'].update(fields)

        success, data = self.try_request(requests.post, self.url, payload)
        
        return success, data


    def publish_items(self, item_ids: list[str]) -> tuple[bool, dict]:
        url = f"https://api.webflow.com/collections/{self.collection_id}/items/publish"
        success, data = self.try_request(requests.put, url, {"itemIds": item_ids})

        return success, data
    

    def delete_items(self, item_ids: list[str]) -> tuple[bool, dict[str,list[any]]]:
        max_items = 100  # API rule
        success = True
        data_dicts = []
        merged_data = {}

        # expect similar responses
        for i in range(0, len(item_ids), max_items):
            payload = {"itemIds": item_ids[i : i + max_items]}
            _success, _data = self.try_request(requests.delete, self.url, payload)
            
            success = success and _success
            data_dicts.append(_data)
        
        # merge the responses
        if len(data_dicts) > 0:
            for key in data_dicts[0].keys():
                merged_data[key] = []

                for d in data_dicts:
                    merged_data[key].extend(d.get(key, []))

        return success, merged_data
    

    def get_items(self) -> tuple[bool, list[dict]]:
        offset = 0
        total = 1  # temp number to trigger one loop iteration
        all_items = []

        while offset < total:
            url = self.url + f"&offset={offset}"
            success, data = self.try_request(requests.get, url)
            
            total      = data['total']
            offset    += data['count']
            all_items += data['items']
        
        return True, all_items