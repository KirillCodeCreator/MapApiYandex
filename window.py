import os

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel

from constants import MAP_LAYERS, MAP_IMG_SIZE_V
from converter import lonlat_to_xy, xy_to_lonlat, lonlat_to_spn
from static_maps import show_map, MAP_TMP_FILENAME
from vec import Vec


class Window(QMainWindow):
    zoom: int
    lonlat: Vec
    map_type: str
    map_label: QLabel

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.init()

    def init(self):
        self.zoom = 9
        self.lonlat = Vec(37.530887, 55.703118)
        self.map_type = MAP_LAYERS[0]
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
        ym_spn = lonlat_to_spn(self.zoom, *self.lonlat.xy)

        return (cmp == -1 and (
                ym_spn.x < obj_size.x or
                ym_spn.y < obj_size.y
        )) or (cmp == 1 and (
                ym_spn.x > obj_size.x or
                ym_spn.y > obj_size.y
        ))
