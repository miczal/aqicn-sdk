from aqicn import AqicnApi

import pytest

@pytest.fixture
def demo_client():
    return AqicnApi(secret="demo")

def assert_ok_status(json_resp):
    assert "ok" == json_resp["status"]

def assert_error_status(json_resp):
    assert json_resp["status"] == "error"

def test_ok_feed_from_shanghai(demo_client):
    assert_ok_status(demo_client.get_feed_city(city="shanghai"))

def test_ok_feed_from_here(demo_client):
    assert_ok_status(demo_client.get_feed_here())

def test_ok_feed_from_geo(demo_client):
    assert_ok_status(demo_client.get_feed_geo(lat=10.3, lng=20.7))

def test_status_codes_for_responses():
    # Lower level request method to check the status code - it always should be 200 regardless of the status field
    default_api_status_code = 200
    assert default_api_status_code == demo_client().request(endpoint="/feed/here/").status_code
    assert default_api_status_code == AqicnApi(secret="NOT_OK_TOKEN").request(endpoint="/feed/here/").status_code

