import pytest
from webflow.cms import list_sites, Site


def test_fetch_sites():
    sites = list_sites()
    assert type(sites) == list, f'List sites did not return a valid list of sites, but a "{type(sites)}".'
    assert len(sites) > 0, f'Need at least one site to test with.'

    # pass reference to next test
    pytest.sites = sites


def test_create_site():
    site_id = pytest.sites[0]['_id']
    site = Site(site_id)
    assert site.id == site['_id'] == site_id, 'Site ID mismatch.'

    pytest.site = site


def test_get_site_data():
    site = pytest.site
    data = site.get_data()
    assert data == site.data, 'Fetched site data does not match site dictionary.'

    expected_keys = ['_id', 'createdOn', 'name', 'shortName', 'lastPublished', 'previewUrl', 'timezone']

    for key in expected_keys:
        assert key in data, f'Site data is missing key "{key}"'


def test_publish_site():
    site = pytest.site 
    response = site.publish([f'{site["name"]}.webflow.io'])
    expected = {'queued': True}
    assert response == expected, 'Failed to publish site.'


def test_get_domains():
    site = pytest.site
    domains = site.get_domains()
    assert type(domains) == list, 'Returned domains are not a list.'


def test_get_collections():
    site = pytest.site
    collections = site.get_collections()
    assert type(collections) == list, 'Returned collections are not a list.'

    expected_keys = ['_id', 'lastUpdated', 'createdOn', 'name', 'slug',]

    for collection in collections:
        for key in expected_keys:
            assert key in collection, f'A returned Collection is missing key "{key}"'

