import requests
from collections import UserDict

from .utils import string_to_dict, slugify, try_request
from .config import make_headers


def list_sites():
    data = try_request(requests.get, 'https://api.webflow.com/sites', make_headers())
    return data


class Site(UserDict):
    id: str
    _url: str
    _headers: dict[str, str]
    delay: int
    max_retries: int

    def __init__(self, site_id: str, max_retries: int = 50, throttle_delay: int = 10):
        self.id = site_id
        self._url = f'https://api.webflow.com/sites/{site_id}'
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
    

    def publish(self, domains: list[str] = None) -> dict:
        if not domains:
            domains = [domain['name'] for domain in self.get_domains()]

        return self._request(requests.post, self._url + '/publish', {"domains": domains})
    

    def get_domains(self) -> dict:
        return self._request(requests.get, self._url + '/domains')


    def get_collections(self) -> list[dict]:
        return self._request(requests.get, self._url + '/collections')