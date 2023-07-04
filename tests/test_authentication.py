import pytest
import webflow
from webflow.cms import Collection


with open('env/api_key', 'r') as f:
    api_key = f.read()

def test_authenticate():
    webflow.authenticate(api_key)

