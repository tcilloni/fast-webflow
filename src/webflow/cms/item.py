import requests
from collections import UserDict

from ..utils import try_request
from ..config import make_headers
from ..entity import Entity


class Item(Entity):
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

    def __init__(self, collection_id: str, id: str, *args, **kwargs):
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
        super(Item, self).__init__(id, *args, **kwargs)
        self._url = f'https://api.webflow.com/collections/{collection_id}/items/{id}'
        self.data = self.get_data()
    

    def get_data(self) -> dict[str, any]:
        '''
        Fetch the item's information.
        See the `official documentation <https://developers.webflow.com/reference/get-item>`__ 
        for more info. Upon being called, this method will also update the object's internal dictionary.

        Returns:
            dict[str, any]: information about this item (name, slug, etc.).
        '''
        self.data = self._get()['items'][0]
        return self.data


    def update(self, fields: dict[str,any], draft: bool = False) -> dict[str, str]:
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

        data = self._put(payload = payload)
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

        data = self._patch(payload = payload)
        self.get_data() # self-update
        
        return data


    def delete(self) -> dict[str, int]:
        '''
        Delete this Item.
        The deletion will take place both in the CMS and locally (you cannot use this object afterwards).

        Returns:
            dict: dictionary that should be `{'deleted': 1}` if deletion was successful.
        '''
        data = self._delete()

        # destroy itself
        self._request = lambda: (_ for _ in ()).throw(Exception('Item does not exist anymore'))
        self.data = None

        return data

