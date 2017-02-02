aqicn Python SDK
================
[![PyPI version](https://badge.fury.io/py/aqicn.svg)](https://badge.fury.io/py/aqicn)

This library is implementation of [Aqicn JSON API](http://aqicn.org/json-api/doc/).

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


Implemented methods
-------------------

| API                                    | SDK                  |
| -------------------------------------- | -------------------- |
| city/station feed                      | get_feed             |
| geo-localized feed (IP based)          | get_feed             |
| stations on the map (geo feed)         | get_location_feed    |
| stations on the map (map query)        | get_stations_in_area |
| search by name                         | search               |

Utility methods
---------------

- stations_by_name
- update stations

TODO:
-----
 - request method and status codes in readme
 - coordinates
 - utils
 - cities -> stations
