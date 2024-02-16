from vec import Vec

# Константы для работы с API Яндекс.Карт
MAP_API_SERVER = 'https://static-maps.yandex.ru/1.x/'
GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"
SEARCH_API_SERVER = 'https://search-maps.yandex.ru/v1/'

MAP_TMP_FILENAME = 'map.png'
MAP_IMG_SIZE = '600,450'
MAP_IMG_SIZE_V = Vec(600, 450)

MAP_LAYERS = ('map', 'sat', 'sat,skl')

GEOCODER_APIKEY = "40d1649f-0493-4b70-98ba-98533de7710b"