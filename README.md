# fast-webflow
a WebFlow CMS API Client in Python

[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)
<!--[![PyPI version](https://badge.fury.io/py/webflow-api.svg)](https://badge.fury.io/py/webflow-api)
[![Python version](https://img.shields.io/pypi/pyversions/webflow-api.svg)](https://pypi.org/project/webflow-api)-->

Python WebFlow CMS API Client is a Python library that provides a convenient interface to interact with the WebFlow CMS API. It simplifies the process of integrating your Python applications with the WebFlow content management system, allowing you to create, read, update, and delete items within your WebFlow collections.

**DISCLAIMER**: This is an unofficial abstraction over WebFlow's API and I am not associated with the WebFlow team.

## Features
- Authenticate with the WebFlow API using your API key
- Fetch collection data and items from WebFlow
- Create, update, and delete items within WebFlow collections
- Search for items within collections using filter parameters
- Handle pagination for large datasets
- Retrieve collection schema and field information
- Upload files to WebFlow

## Installation
You can install the Python WebFlow CMS API Client library using pip:

```bash
pip install webflow-api
```

## Getting Started

1. Obtain an API key from WebFlow by following their [API Authentication Guide](https://developers.webflow.com/authentication).
2. Import the `WebFlow` class from the `webflow` module:

```python
from webflow import WebFlow
```

3. Initialize the `WebFlow` client with your API key:

```python
api_key = 'YOUR_API_KEY'
client = WebFlow(api_key)
```

4. Start interacting with the WebFlow API using the provided methods. For example, to fetch all items from a collection:

```python
collection_id = 'COLLECTION_ID'
items = client.get_collection_items(collection_id)
for item in items:
    print(item)
```

For more detailed usage examples and API documentation, please refer to the [API Reference](API_REFERENCE.md).

## Contributing
Contributions to the Python WebFlow CMS API Client library are welcome! If you encounter any bugs, have suggestions, or would like to contribute new features, please feel free to open an issue or submit a pull request on GitHub.

## License
This project is licensed under the GNU GPLv3 License. See the [LICENSE](LICENSE) file for more information.
