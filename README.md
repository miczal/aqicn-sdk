aqicn Python SDK
================
[![PyPI version](https://badge.fury.io/py/aqicn.svg)](https://badge.fury.io/py/aqicn)

This library is implementation of [Aqicn JSON API](http://aqicn.org/json-api/doc/).

It also includes utility methods for scraping [aqicn](http://aqicn.org/) website (See: **Utility methods**).

Usage
-----

You first need to [create API token](http://aqicn.org/data-platform/token/).

```python
import aqicn

api = aqicn.AqicnApi(secret="YOUR_KEY")

ip_based_data = api.get_feed()
```

Installation
------------

With pip:
```bash

$ pip install aqicn
```
Manual:

```bash
$ pip install -e git+https://github.com/miczal/aqicn-sdk#egg=aqicn
```


Implemented API methods
-----------------------

| API                                    | SDK                  |
| -------------------------------------- | -------------------- |
| `city/station feed`                      | get_feed             |
| `geo-localized feed` (IP based)          | get_feed             |
| `stations on the map` (geo feed)         | get_location_feed    |
| `stations on the map` (map query)        | get_stations_in_area |
| `search by name`                         | search               |

Utility methods
---------------

Methods for scraping website. Useful to get e.g. available station names to JSON API.

| Method                                 | Description          |
| -------------------------------------- | -------------------- |
| `get_aqi_world_data()` | Scrapes current data directly from aqicn website and returns string with string in JSON format|
| `scrap_data_from_website(adapter)` | Returns adapted data in JSON format from aqicn website. If no adapter is provided, default will be used in `json.loads` as `object_hook` argument |
| `get_stations_data(key, fields_to_include, adapter)` | Returns dictionary of data for online stations with stations names as keys. Data to process is taken from `scrap_data_from_website` and includes only fields listed in `fields_to_include`. `key` argument is taken from JSON and serves as key to the resulting dictionary |
| `get_stations_id_data` | Returns only dictionary with data for identification of all stations. ID is the dictionary's key. |

TODO:
-----
 - request method and status codes in readme
 - coordinates
