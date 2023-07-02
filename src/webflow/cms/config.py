import requests
from .utils import string_to_dict

_auth_token = None


def make_headers() -> dict[str, str]:
    assert _auth_token, 'You must first set the `auth_token` variable.'

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {_auth_token}"
    }

    return headers


def authenticate(auth_token: str) -> None:
    global _auth_token

    # set the new token
    _auth_token = auth_token
    response = requests.get("https://api.webflow.com/user", headers = make_headers())

    # check if it is valid
    if response.status_code == 200:
        user = string_to_dict(response.text)['user']
        print(f'User "{user["firstName"]} {user["lastName"]}" authenticated successfully.')
    else:
        raise Exception(response.text)