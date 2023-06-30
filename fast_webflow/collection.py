import requests

from .utils import string_to_dict, slugify, try_request
from .config import make_headers


class Collection:
    colletion_id: str
    url: str
    headers: dict[str, str]
    delay: int
    max_retries: int

    def __init__(self, collection_id: str, max_retries: int = 50, throttle_delay: int = 10):
        self.collection_id = collection_id
        self.url = f'https://api.webflow.com/collections/{collection_id}/items?live="true"'
        self.headers = make_headers()
        self.delay = throttle_delay
        self.max_retries = max_retries
    

    def request(self, request_fn: callable, url: str = None, data: dict = None) -> dict:
        if url is None:
            url = self.url
        
        return try_request(request_fn, url, self.headers, data, self.max_retries, self.delay)
    

    def post_item(self, fields: dict[str,any], draft: bool = False):
        payload = {'fields': {'_archived': False, '_draft': draft}}
        payload['fields'].update(fields)

        data = self.request(requests.post, self.url, payload)
        
        return data


    def publish_items(self, item_ids: list[str]) -> dict:
        url = f"https://api.webflow.com/collections/{self.collection_id}/items/publish"
        data = self.request(requests.put, url, {"itemIds": item_ids})

        return data
    

    def delete_items(self, item_ids: list[str]) -> dict[str,list[any]]:
        max_items = 100  # API rule
        data_dicts = []
        merged_data = {}

        # expect similar responses
        for i in range(0, len(item_ids), max_items):
            payload = {"itemIds": item_ids[i : i + max_items]}
            data = self.request(requests.delete, self.url, payload)
            
            data_dicts.append(data)
        
        # merge the responses
        if len(data_dicts) > 0:
            for key in data_dicts[0].keys():
                merged_data[key] = []

                for d in data_dicts:
                    merged_data[key].extend(d.get(key, []))

        return merged_data
    

    def get_items(self) -> list[dict]:
        offset = 0
        total = 1  # temp number to trigger one loop iteration
        all_items = []

        while offset < total:
            url = self.url + f"&offset={offset}"
            data = self.request(requests.get, url)
            
            total      = data['total']
            offset    += data['count']
            all_items += data['items']
        
        return all_items