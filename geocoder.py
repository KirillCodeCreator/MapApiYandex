import sys

import requests

from constants import GEOCODER_API_SERVER, GEOCODER_APIKEY
from vec import Vec


def get_toponym(address):
    params = {
        "apikey": GEOCODER_APIKEY,
        "geocode": address,
        "format": "json"
    }

    response = requests.get(GEOCODER_API_SERVER, params=params)

    if not response:
        print("Ошибка получения топонима:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit()

    json_response = response.json()
    return json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]


def get_toponym_lonlat(toponym):
    toponym_pos = toponym["Point"]["pos"]
    lo, la = map(float, toponym_pos.split(" "))
    return Vec(lo, la)


def get_toponym_spn(toponym):
    corners = toponym["boundedBy"]["Envelope"]
    lc = [*map(float, corners["lowerCorner"].split())]
    uc = [*map(float, corners["upperCorner"].split())]
    return Vec(uc[0] - lc[0], uc[1] - lc[1])

def get_address(toponym):
    address = toponym['metaDataProperty']['GeocoderMetaData'][
        'Address']['formatted']
    return address

def get_post_index(toponym):
    try:
        post_index = toponym['metaDataProperty']['GeocoderMetaData'][
            'Address']['postal_code']
    except KeyError:
        return '\nнет индекса'
    return post_index
