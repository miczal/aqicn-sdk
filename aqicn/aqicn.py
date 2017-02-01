from collections import namedtuple

import requests
import logging
import urllib.parse

Coordinate = namedtuple('Coordinate', ['lat', 'lng'])

class AqicnApiError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class AqicnApi:
    """
    Wrapper for aqicn API. Implementation based on documentation from http://aqicn.org/json-api/doc/
    Implemented API methods always return response in JSON format or throw AqicnApiError when data is invalid

    Available methods:
        - get_feed
        - get_location_feed
        - get_stations_in_area
        - search
    """

    _protocol = "https"
    _domain = "api.waqi.info"
    _header = {'user-agent': 'aqicn-sdk/0.1'}
    _expected_response_status = 200

    def __init__(self, secret, proxy=None):
        """
        Args:
            secret (str): API token
            proxy (dict [str, str]): proxies in form { 'https': 'x.x.x.x', 'http': 'y.y.y.y' }
        """
        self.secret = secret
        self.proxy = proxy if proxy else None
        self.base_url = urllib.parse.urlunparse((self._protocol, self._domain, "", "", "", ""))

    def request(self, endpoint, params = {}):
        """
        Sends a GET request to the configured API.

        Args:
            endpoint (str):
            params (dict): request parameters

        Returns:
             Response in requests.Response format."""
        params.update({"token": self.secret})
        return requests.get(url=self.base_url + "/" + endpoint,
                            params=params,
                            headers=self._header,
                            proxies=self.proxy)

    def json_request(self, endpoint, params={}):
        """
        Wrapper for GET request to the configured API.
        Response ALWAYS has status_code == 200 according to the documentation.

        If "data" != "ok" then AqicnApiError is thrown.

        Args:
            endpoint (str)
            params (dict): request parameters

        Returns:
             Response in JSON format (dict)

        Every request can throw AqicnApiError with "overQuota" and "invalidKey" messages.
        """
        r = self.request(endpoint=endpoint, params=params)

        if r.status_code != self._expected_response_status:
            logging.getLogger(__name__).warning("Default status code changed - see API documentation for more possible changes")
        json_resp = r.json()
        if json_resp["status"] != "ok": raise AqicnApiError(json_resp["data"])
        return json_resp

    # All API methods according to:
    # http://aqicn.org/json-api/doc/

    def get_feed(self, *city_name_or_station_id):
        """
        IP based feed if no arguments, city or station (id) based if 1 argument present.

        Args:
            city_name_or_station_id (str): city name in English or station id

        Throws:
            ValueError if more than 1 argument given
            AqicnApiError("Unknown station") if wrong id / city name given.
        """
        if len(city_name_or_station_id) > 1: raise ValueError("Only 0 or 1 arguments possible")
        return self.json_request("feed/" + ("".join(city_name_or_station_id) + "/" if city_name_or_station_id else "here/"))

    def get_location_feed(self, coord):
        """
        Geo-localized feed for the nearest station.

        Args:
            coord (Coordinate): lat lng coordinates tuple (either numeric or sting)
        """
        return self.json_request("feed/geo:{0};{1}/".format(coord.lat, coord.lng))

    def get_stations_in_area(self, lower_left, upper_right):
        """
        Feed for stations in rectangular are made from points [lower_left, upper_right].

        Args:
            lower_left (Coordinate): lat lng coordinates tuple (either numeric or sting)
            upper_right (Coordinate): lat lng coordinates tuple (either numeric or sting)
        """
        return self.json_request("map/bounds/",
                                 params={"latlng": "{0},{1},{2},{3}".format(str(lower_left.lat),  str(lower_left.lng),
                                                                            str(upper_right.lat), str(upper_right.lng))})

    def search(self, keyword):
        """
        Search for stations based on keyword.

        Args:
            keyword (str): search phrase
        """
        return self.json_request("search/", params={"keyword": keyword})
