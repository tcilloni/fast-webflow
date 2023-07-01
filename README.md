# Welcome to fast-webflow
a WebFlow CMS API Client in Python

[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](./LICENSE)
<!--[![PyPI version](https://badge.fury.io/py/webflow-api.svg)](https://badge.fury.io/py/webflow-api)
[![Python version](https://img.shields.io/pypi/pyversions/webflow-api.svg)](https://pypi.org/project/webflow-api)-->

This Python library provides an **intuitive** and **fast** interface over WebFlow's API. It simplifies the process of integrating your Python applications with the WebFlow content management system (CMS), allowing you to create, read, update, and delete items within your WebFlow collections.

> Check out an example website built with the help of `fast-webflow`: [**liguriasegreta.com**](https://www.liguriasegreta.com)

### DISCLAIMER
This is an **unofficial** abstraction over WebFlow's API and I am not associated with the WebFlow team.


## Roadmap
- [ ] Add *e-commerce* functionality
- [ ] Add *membership* functionality
- [ ] Add tests
- [ ] Finish documentation
- [x] Publish to PyPi


## Features
- **Authenticate** with the WebFlow API using your API key
- **Fetch**, **Create**, **Update**, and **Delete** Items and files from WebFlow Collections
- Handle **pagination** for large Collections
- Hidden parallelization for **faster operations** (with implicit error handling)

## Installation
You can install the package using pip:
```bash
pip install fast-webflow
```

## Getting Started

1. Obtain an API key from WebFlow by following their [API Access Token](https://developers.webflow.com/docs/access-token).
2. Import the `cms` module from the `fast-webflow` package automatically to interact with the WebFlow CMS API; then authenticate:

```python
import cms
api_key = 'YOUR_API_KEY'
cms.authenticate(api_key)
```

3. Start interacting with the WebFlow API using the provided methods. For example, to fetch all items from a collection:

```python
from cms import Collection

collection_id = 'COLLECTION_ID'
collection = Collection(collection_id)
items = collection.get_all_items()

for item in items:
    print(item["slug"])
```

## Contributing
Contributions to the fast-WebFlow Python Client library are welcome! If you encounter any bugs, have suggestions, or would like to contribute new features, please feel free to open an issue or submit a pull request on GitHub. You can also contact me directly!
- [Open a new issue](https://github.com/tcilloni/fast-webflow/issues/new)
- [Pull Requests](https://github.com/tcilloni/fast-webflow/pulls)
- [Email me](mailto:tcilloni@outlook.com)

## License
This project is licensed under the GNU GPLv3 License. See the [LICENSE](./LICENSE) file for more information.
