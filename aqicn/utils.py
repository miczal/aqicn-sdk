import requests
from aqicn import AqicnApi


def get_aqi_world_data():
    import re
    stations_data_regex = re.compile(r"mapInitWithData\((\[.*?\])\)")
    return re.search(stations_data_regex, requests.get("http://aqicn.org/map/world/", headers=AqicnApi._header).text).group(1)

def scrap_data_from_website(adapter=None):
    def default_world_data_adapter(dct):
        to_replace = {'x': 'id',
                      'g': 'geo'}
        for k, v in list(dct.items()):
            if k in to_replace.keys():
                del dct[k]
                dct[to_replace[k]] = v

        for k, v in list(dct.items()):
            if k not in ["aqi", "utime", "geo", "city", "id"]: del dct[k]
            if k == "aqi" and v == "-" or v == "placeholder" or v == 999: dct[k] = 0
        return dct

    import json
    return json.loads(get_aqi_world_data(), object_hook=adapter if adapter else default_world_data_adapter)

def get_stations_data(key="city", fields_to_include=["aqi", "id", "geo", "utime"], adapter=None):
    data = scrap_data_from_website(adapter)
    stations = {}
    for entry in data:
        fields = {}
        for field in fields_to_include: fields[field] = entry[field]
        stations[entry[key]] = fields
    return stations

def get_stations_id_data():
    def id_adapter(dct):
        to_keep = ['city']
        to_replace = {'x': 'id',
                      'g': 'geo'}
        for k, v in list(dct.items()):
            if k not in to_keep and k not in to_replace: del dct[k]
            if k in to_replace.keys():
                dct[to_replace[k]] = v
                del dct[k]
        return dct

    data = scrap_data_from_website(id_adapter)
    res = {}
    for entry in data:
        res[entry["id"]] = {"city": entry["city"], "geo": entry["geo"]}
    return res
