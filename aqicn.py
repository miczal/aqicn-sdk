import requests
import logging
import urllib.parse

class AqicnApiError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class AqicnApi:

    _protocol = "https"
    _domain = "api.waqi.info"
    _header = {'user-agent': 'aqicn-api/0.1'}
    _expected_response_status = 200

    def __init__(self, secret):
        self.secret = secret
        self.base_url = urllib.parse.urlunparse((AqicnApi._protocol, AqicnApi._domain, "", "", "", ""))

    def request(self, endpoint, params = {}):
        """Sends a GET request to the configured API.

            :param endpoint: API endpoint
            :param params: (optional) Dictionary to be sent in the query string for the :class:`Request`.
            :return: :class:`Response <Response>` object
            :rtype: requests.Response
        """
        params.update({"token": self.secret})
        return requests.get(url=self.base_url + "/" + endpoint,
                            params=params,
                            headers=self._header)

    def json_request(self, endpoint, params={}):
        """Wrapper for GET request to the configured API.
        Response ALWAYS has status_code == 200 according to the documentation.

            :param endpoint: API endpoint
            :param params: (optional) Dictionary to be sent in the query string for the :class:`Request`.
            :return: json response
            :rtype: dict()
        """
        r = self.request(endpoint=endpoint, params=params)
        if r.status_code == AqicnApi._expected_response_status:
            logging.getLogger(__name__).warning("Default status code changed - see API documentation for more possible changes")
        json_resp = r.json()
        if json_resp["status"] != "ok": raise AqicnApiError(r["data"])
        return json_resp

    def get_feed_city(self, city):
        # /feed/:city/?token=:token
        return self.json_request("feed/" + city + "/")

    def get_feed_here(self):
        # /feed/here/?token=:token
        return self.json_request("feed/here/")

    def get_feed_geo(self, lat, lng):
        # /feed/geo:10.3;20.7/?token=demo
        return self.json_request("feed/" + "geo:" + ";".join([str(coord) for coord in (lat,lng)])+ "/")
