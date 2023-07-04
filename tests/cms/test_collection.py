import pytest
from collections import UserDict
from webflow.cms import authenticate, list_sites, Site, Collection


# first of all, authenticate
with open('env/api_key', 'r') as f:
    api_key = f.read()
    authenticate(api_key)

# First connect to a Site (assuming previous tests were successful)
sites = list_sites()
site_id = sites[0]['_id']
site = Site(site_id)
pytest.site = site


def test_collection_creation():
    site = pytest.site

    collections = site.get_collections()
    assert isinstance(collections, list), \
        f'Returned list of collections is not a list, but a "{type(collections)}".'

    collection_id = collections[0]['_id']
    collection = Collection(collection_id)
    assert isinstance(collection, Collection) and isinstance(collection, UserDict), \
        f'Collection creation failed, type "{type(collection)}" is wrong.'

    pytest.collection = collection


def test_post_items():
    pass


def test_get_items():
    pass


def test_delete_items():
    pass

