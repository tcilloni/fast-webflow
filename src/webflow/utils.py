import json
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor


def string_to_dict(string: str) -> dict:
    '''
    Convert a string to a dictionary.

    Args:
        string (str): valid string representation of a dictionary (like a JSON object).

    Returns:
        dict: the equivalent dictionary.
    '''
    return json.loads(string)


def slugify(txt: str) -> str:
    '''
    Generate a valid slug for a given string.
    I am not sure if this is the best, or only way, to generate a slug. And it is most likely not
    needed for most applications. But, just in case, I leave it here.

    Args:
        txt (str): string to convert

    Returns:
        str: equivalent slug string
    '''
    # remove accents
    nfkd = unicodedata.normalize('NFKD', txt)
    txt = u''.join([c for c in nfkd if not unicodedata.combining(c)])

    # normalize
    txt = ''.join([c for c in txt if c.isalnum() or c == ' '])
    txt = txt.replace(' ', '-').lower()

    return txt


def parallelize(function: callable, data: list[any], threads: int = 50, await_completion: bool = True) -> list[any]:
    '''
    Parallelize the execution of a method over a list of arguments.

    Args:
        function (callable): function to parallelize
        data (list[any]): list of arguments
        threads (int, optional): number of threads to use. Defaults to 50.
        await_completion (bool, optional): if `True` waits for and returns a list of results; 
            If `False` it immeditely returns a list of futures that need to be waited for. Defaults to True.

    Returns:
        list[any]: list of futures or results.
    '''
    executor = ThreadPoolExecutor(max_workers = threads)
    futures = executor.map(function, data)
    results = list(futures) if await_completion else futures
    return results


def parallelize_multiargs(function: callable, data: list[any], threads: int = 50, await_completion: bool = True) -> list[any]:
    return parallelize(lambda args: function(*args), data, threads, await_completion)


def try_request(request_fn: callable, url: str, headers: dict[str, str], data: dict = None, 
        max_retries: int = 50, delay: float = 10) -> dict:
    '''
    Execute a request to the WebFlow API with implicit Rate Limit handling.

    Args:
        request_fn (callable): prepared requests function to execute.
        url (str): url for the request.
        headers (dict[str, str]): headers with the API TOKEN.
        data (dict, optional): optional data to supply as a JSON object. Defaults to None.
        max_retries (int, optional): number of times a limit hit error is retried. Defaults to 50.
        delay (float, optional): seconds to wait before retrying after hitting a rate limit. Defaults to 10.

    Returns:
        dict: parsed dictionary of the response's JSON.
    '''
    retry = 0

    while True:
        response = request_fn(url, json = data, headers = headers)

        # hit API limit
        if response.status_code == 429 and retry < max_retries: 
            time.sleep(delay)
            retry += 1
        
        # success, can return
        elif response.status_code == 200:
            return string_to_dict(response.text)

        # some other error; return it
        else:
            response.raise_for_status()