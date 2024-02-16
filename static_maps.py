import sys

import requests
from PyQt5.QtGui import QPixmap

from constants import MAP_API_SERVER, MAP_TMP_FILENAME, \
    MAP_IMG_SIZE


def show_map(map_label, z, lola, map_type):
    params = {
        'z': z,
        'll': lola.to_ym(),
        'l': map_type,
        'size': MAP_IMG_SIZE
    }

    response = requests.get(MAP_API_SERVER, params=params)

    if not response:
        print('Произошла ошибка при получении карты.')
        print(f'{response.status_code}: {response.reason}')
        print(response.text)
        sys.exit(1)

    with open(MAP_TMP_FILENAME, 'wb') as o_file:
        o_file.write(response.content)

    map_label.setPixmap(QPixmap(MAP_TMP_FILENAME))
