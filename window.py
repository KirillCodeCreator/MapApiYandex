import os

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QComboBox, QLineEdit, QMessageBox, QVBoxLayout

from constants import MAP_LAYERS, MAP_IMG_SIZE_V
from converter import lonlat_to_xy, xy_to_lonlat, lonlat_to_spn
from geocoder import get_toponym, get_toponym_lonlat, get_toponym_spn
from static_maps import show_map, MAP_TMP_FILENAME, show_map_with_dot
from vec import Vec


class Window(QMainWindow):
    zoom: int
    lonlat: Vec
    map_type: str
    map_label: QLabel
    layer_input: QComboBox
    address_input: QLineEdit
    options_layout: QVBoxLayout

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.init()

    def init(self):
        self.options_layout.setAlignment(Qt.AlignTop)
        self.layer_input.currentIndexChanged.connect(self.layer_changed)
        self.map_type = MAP_LAYERS[self.layer_input.currentIndex()]

        self.find_button.clicked.connect(self.find_obj)

        self.zoom = 9
        self.lonlat = Vec(37.530887, 55.703118)
        self.update_map()

    def layer_changed(self, index):
        self.map_type = MAP_LAYERS[index]
        self.update_map()

    def update_map(self):
        show_map(self.map_label, self.zoom, self.lonlat, self.map_type)

    def closeEvent(self, event):
        os.remove(MAP_TMP_FILENAME)

    def move_map(self, v):
        old_lola = self.lonlat

        v *= MAP_IMG_SIZE_V
        x, y = lonlat_to_xy(self.zoom, *self.lonlat.xy)
        x, y = x + v.x, y + v.y

        self.lonlat = Vec(*xy_to_lonlat(self.zoom, x, y))
        if not self.check_borders():
            self.lonlat = old_lola

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.zoom += 1
            if not self.check_borders():
                self.zoom -= 1
        elif event.key() == Qt.Key_PageDown:
            self.zoom -= 1
            if not self.check_borders():
                self.zoom += 1
        elif event.key() == Qt.Key_Left:
            self.move_map(Vec(-1, 0))
        elif event.key() == Qt.Key_Right:
            self.move_map(Vec(1, 0))
        elif event.key() == Qt.Key_Up:
            self.move_map(Vec(0, -1))
        elif event.key() == Qt.Key_Down:
            self.move_map(Vec(0, 1))
        else:
            return

        self.update_map()

    def check_borders(self):
        return not (
                abs(abs(self.lonlat.x) - 180) < 0.5 or
                abs(abs(self.lonlat.y) - 85) < 0.5 or
                not (0 <= self.zoom <= 21)
        )

    def layer_changed(self, index):
        self.map_type = MAP_LAYERS[index]
        self.update_map()

    def compare_spn(self, obj_size, cmp):
        map_spn = lonlat_to_spn(self.zoom, *self.lonlat.xy)

        return ((cmp == -1 and (map_spn.x < obj_size.x or map_spn.y < obj_size.y))
                or (cmp == 1 and (map_spn.x > obj_size.x or map_spn.y > obj_size.y)))

    def delete_search_results(self):
        self.update_map()

    def search_toponym(self, search_text):
        try:
            return get_toponym(search_text)
        except IndexError:
            QMessageBox.critical(
                self, 'Ошибка', 'Объект по данному запросу не найден')
            return None

    def find_obj(self):
        self.delete_search_results()
        toponym = self.search_toponym(self.address_input.text())
        if toponym is None:
            return

        coords = get_toponym_lonlat(toponym)
        obj_size = get_toponym_spn(toponym)
        self.lonlat = dot = coords

        while self.compare_spn(obj_size, 1):
            self.zoom += 1
        while self.compare_spn(obj_size, -1):
            self.zoom -= 1

        show_map_with_dot(self.map_label, self.zoom, self.lonlat, self.map_type, dot)
