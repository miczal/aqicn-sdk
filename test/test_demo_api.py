from aqicn.aqicn import AqicnApi, Coordinate

import pytest

@pytest.fixture
def demo_client():
    return AqicnApi(secret="demo")

def assert_ok_status(json_resp):
    assert "ok" == json_resp["status"]

### Tests ###
#
# Demo API tests taken from:
# http://aqicn.org/json-api/doc/
#

def test_feed_from_shanghai(demo_client):
    assert_ok_status(demo_client.get_feed("shanghai"))

def test_feed_from_here(demo_client):
    # Demo token does NOT return data based on IP
    assert_ok_status(demo_client.get_feed())

def test_location_feed(demo_client):
    assert_ok_status(demo_client.get_location_feed(Coordinate(lat=10.3, lng=20.7)))

def test_stations_in_area(demo_client):
    # Decimal places are important for demo key that's why data is in str format
    assert_ok_status(demo_client.get_stations_in_area(Coordinate("39.379436", "116.091230"),
                                                      Coordinate("40.235643", "116.784382")))

def test_search(demo_client):
    assert_ok_status(demo_client.search("bangalore"))

def test_status_codes_for_responses():
    # Lower level request method to check the status code - it always should be 200 regardless of the status field
    default_api_status_code = 200

    ok_resp = demo_client().request(endpoint="/feed/here/")
    nok_resp = AqicnApi(secret="NOT_OK_TOKEN").request(endpoint="/feed/here/")

    assert default_api_status_code == ok_resp.status_code

    assert default_api_status_code == nok_resp.status_code
    assert "error" == nok_resp.json()["status"]

