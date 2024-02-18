import sys

import requests

from constants import SEARCH_MAPS_APIKEY, SEARCH_API_SERVER
from vec import Vec


def search_org(lo_la, text):
    params = {
        'apikey': SEARCH_MAPS_APIKEY,
        'lang': 'ru_RU',
        'type': 'biz',
        'll': lo_la.to_ym(),
        'text': text
    }

    response = requests.get(SEARCH_API_SERVER, params=params)

    if not response:
        print('Произошла ошибка при выполнении поиска. Программа будет закрыта')
        print(f'{response.status_code}: {response.reason}')
        print(response.text)
        sys.exit()

    json_response = response.json()

    try:
        return json_response['features'][0]
    except IndexError:
        return


def get_org_lon_lat(org):
    return Vec(*org['geometry']['coordinates'])


def get_org_name(org):
    return org['properties']['CompanyMetaData']['name']


def get_org_address(org):
    return org['properties']['CompanyMetaData'].get(
        'address', 'нет адреса'
    )