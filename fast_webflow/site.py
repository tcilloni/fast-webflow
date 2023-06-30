import requests
import time
from functools import partial

from .utils import string_to_dict, slugify, try_request
from .config import make_headers


def list_sites():
    data = try_request(requests.get, 'https://api.webflow.com/sites', make_headers())
    return data


class Site:
    site_id: str
    url: str
    headers: dict[str, str]
    delay: int
    max_retries: int

    def __init__(self, site_id: str, max_retries: int = 50, throttle_delay: int = 10):
        self.site_id = site_id
        self.url = f'https://api.webflow.com/sites/{site_id}'
        self.headers = make_headers()
        self.delay = throttle_delay
        self.max_retries = max_retries


    def _request(self, request_fn: callable, url: str = None, data: dict = None) -> dict:
        if url is None:
            url = self.url
        
        return try_request(request_fn, url, self.headers, data, self.max_retries, self.delay)
    
    def get_info(self) -> dict:
        return self._request(requests.get)
    
    def publish(self, domains: list[str] = None) -> dict:
        if not domains:
            domains = [domain['name'] for domain in self.get_domains()]

        return self._request(requests.post, self.url + '/publish', {"domains": domains})
    
    def get_domains(self) -> dict:
        return self._request(requests.get, self.url + '/domains')