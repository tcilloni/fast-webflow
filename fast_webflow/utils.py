import json
import unicodedata
from concurrent.futures import ThreadPoolExecutor


def string_to_dict(string: str) -> dict:
    return json.loads(string)


def slugify(txt: str) -> str:
    # remove accents
    nfkd = unicodedata.normalize('NFKD', txt)
    txt = u''.join([c for c in nfkd if not unicodedata.combining(c)])

    # normalize
    txt = ''.join([c for c in txt if c.isalnum() or c == ' '])
    txt = txt.replace(' ', '-').lower()

    return txt


def parallelize(function: callable, data: list[any], verbose: bool = True, threads: int = 50, await_completion: bool = True) -> list[any]:
    executor = ThreadPoolExecutor(max_workers = threads)
    futures = executor.map(function, data)
    results = list(futures) if await_completion else futures
    return results


def save_dict(d: dict, fname: str) -> None:
    with open(fname, 'w') as f:
        f.write(json.dumps(d, indent = 4))
