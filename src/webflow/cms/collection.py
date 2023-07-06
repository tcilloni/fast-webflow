import requests
from collections import UserDict
from functools import partial
from itertools import repeat

from ..utils import try_request, parallelize, parallelize_multiargs
from ..config import make_headers
from ..entity import Entity


class Collection(Entity):
    """
    A Collection object connects with WebFlow's CMS API.

    Upon initialization, the object behaves like a dictionary, where its keys are the fields
    returned by the API's `get` method on the collection. The object allows getting, removing, and
    publishing lists of items concurrently.
    
    Attributes:
        id (str): ID field (often `_id`) of the collection in the CMS.
        delay (float): number of seconds to wait after a request hits the rate limit.
        max_retries (int): number of times failed requests are retried (including after hitting rate limits).
        data (dict): dictionary representation of the collection's data.
    """

    def __init__(self, id: str, *args, **kwargs):
        """
        Create a new Collection object.

        Args:
            collection_id (str): ID field (often `_id`) of the collection in the CMS.
            throttle_delay (float, optional): number of seconds to wait after a request hits the 
                rate limit. Defaults to 10.
            max_retries (int, optional): number of times failed requests are retried (including 
                after hitting rate limits). Defaults to 50.
        """
        super(Collection, self).__init__(id, *args, **kwargs)
        self._url = f'https://api.webflow.com/collections/{id}'
        self._items_url = f'https://api.webflow.com/collections/{id}/items'
        self._max_items_per_request = 100
        self.data = self.get_data()
    

    def get_data(self) -> dict[str, any]:
        '''
        Fetch the collection's information.
        See the `official documentation <https://developers.webflow.com/reference/get-collection>`__ 
        for more info. Upon being called, this method will also update the object's internal dictionary.

        Returns:
            dict[str, any]: information about this collection (name, slug, etc.).
        '''
        return self._get()


    def post_item(self, fields: dict[str,any], draft: bool = False) -> dict[str, any]:
        '''
        Add an item to the collection.

        Args:
            fields (dict[str,any]): item data (only fields' key:value pairs, not _archived and _draft)
            draft (bool, optional): draft the item or publish it directly. Defaults to False.

        Returns:
            dict[str, any]: if successful, information about the added item (including its slug).
        '''
        payload = {'fields': {'_archived': False, '_draft': draft}}
        payload['fields'].update(fields)
        
        return self._post(self._items_url, payload)
    

    def post_items(self, fields_list: list[dict[str,any]], draft: bool = False) -> list[dict[str, any]]:
        '''
        Add multiple items to the collection.
        This method is a wrapper for multiple `post_item` method calls in parallel. Refer to that
        for more information.

        Args:
            fields_list (list[dict[str,any]]): list of item data.
            draft (bool, optional): draft the item or publish it directly. Defaults to False.

        Returns:
            list[dict[str, any]]: one data dictionary per added item.
        '''
        post_item = partial(self.post_item, draft = draft)
        data = parallelize(post_item, fields_list)
        
        return data


    def publish_items(self, item_ids: list[str]) -> dict[str, list[str]]:
        '''
        Publish a list of items that are already in the collection.
        This method is optimized to split the list of items into several lists of length up to 100
        and send the requests concurrently. For instance, 350 items will be published in 4 requests.

        Args:
            item_ids (list[str]): list of item IDs to publish.

        Returns:
            dict[str, list[str]]: list of successful (key `publishedItemIds`) and failed (key `errors`) IDs.
        '''
        max_items = self._max_items_per_request  # API rule
        url = self._url + '/items/publish'
        data = {}

        # split IDs into lists of max 100 items
        item_ids = [item_ids[i:i+max_items] for i in range(0, len(item_ids), max_items)]
        payloads = [{"itemIds": ids} for ids in item_ids]

        # send parallel requests
        urls_and_data = zip(repeat(url), payloads)
        returns  = parallelize_multiargs(self._put, urls_and_data)

        # merge responses
        for key in ['publishedItemIds', 'errors']:
            data[key] = [item for resp in returns for item in resp[key]]
        
        return data
    

    def delete_items(self, item_ids: list[str]) -> dict[str, list[any]]:
        '''
        Delete a list of items from the collection.
        This method is optimized to split the list of items into several lists of length up to 100
        and send the requests concurrently. For instance, 350 items will be published in 4 requests.

        Args:
            item_ids (list[str]): list of item IDs to delete.

        Returns:
            dict[str, list[str]]: list of successful (key `deletedItemIds`) and failed (key `errors`) IDs.
        '''
        max_items = self._max_items_per_request  # API rule
        data = {}

        # split IDs into lists of max 100 items
        item_ids = [item_ids[i:i+max_items] for i in range(0, len(item_ids), max_items)]
        payloads = [{"itemIds": ids} for ids in item_ids]

        # send parallel requests
        urls_and_data = zip(repeat(self._items_url), payloads)
        returns = parallelize_multiargs(self._delete, urls_and_data)

        # merge responses
        for key in ['deletedItemIds', 'errors']:
            data[key] = [item for resp in returns for item in resp[key]]

        return data
    

    def get_items(self, offset: int = 0, limit: int = 100) -> dict[str, any]:
        '''
        Fetch a list of items in this collection.
        Use the offset and limit parameters to control pagination. If you want to get all items in
        the collection, see the method `get_all_items`.

        Args:
            offset (int, optional): number of items to skip. Defaults to 0.
            limit (int, optional): max number of items to return (capped at 100). Defaults to 100.

        Returns:
            dict[str, any]: group of items (index with the key `items` to get the actual data).
        '''
        url = self._items_url + f"?offset={offset}&limit={limit}"

        return self._get(url)
    

    def get_all_items(self) -> list[dict]:
        '''
        Fetch all items in this collection.
        This is a convenient wrapper around the `get_items` method to automatically control pagination
        and fetch all items in parallel. Note that the method first sends a get request to get the 
        updated number of records in the collection; then uses that number to calculate the number 
        of pages and send the requests.

        Returns:
            list[dict]: list of each item's data.
        '''
        # update total number of items
        max_items = self._max_items_per_request  # API rule
        initial_data = self._get(self._items_url)
        total = initial_data['total']

        # prepare one URL request for each offset in 0..total..limit
        item_lists = parallelize(self.get_items, range(0, total, max_items))
        all_items = [item for item_list in item_lists for item in item_list['items']]
        
        return all_items

