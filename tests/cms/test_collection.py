import pytest
from collections import UserDict

from webflow.cms import list_sites, Site, Collection


def test_initialization():
    sites = list_sites()
    site_id = sites[0]['_id']
    site = Site(site_id)

    collections = site.get_collections()
    collection_id = collections[0]['_id']

    pytest.collection_id = collection_id


def test_collection_creation():
    collection_id = pytest.collection_id
    collection = Collection(collection_id)
    assert isinstance(collection, Collection) and isinstance(collection, UserDict), \
        f'Collection creation failed, type "{type(collection)}" is wrong.'


def test_post_items():
    pass


def test_get_items():
    pass


def test_delete_items():
    pass

