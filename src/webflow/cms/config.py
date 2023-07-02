import requests
from .utils import string_to_dict

_auth_token = None


def make_headers() -> dict[str, str]:
    '''
    Generate headers with the API TOKEN to include in all requests.

    Returns:
        dict[str, str]: complete headers dict.
    '''
    assert _auth_token, 'You must first set the `auth_token` variable.'

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {_auth_token}"
    }

    return headers


def authenticate(auth_token: str) -> None:
    '''
    Authenticate to the WebFlow API using a valid API TOKEN.
    Visit the `Site API TOKEN <https://developers.webflow.com/docs/access-token>`__ page for more info.
    Upon successful login, the method prints to the standard output a welcome message with the name
    of the associated user.

    Args:
        auth_token (str): your API TOKEN.

    Raises:
        Exception: if the token is not valid.
    '''
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