import os

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel

from constants import MAP_LAYERS
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.zoom += 1
            if not self.check_zoom():
                self.zoom -= 1
        elif event.key() == Qt.Key_PageDown:
            self.zoom -= 1
            if not self.check_zoom():
                self.zoom += 1
        else:
            return
        self.update_map()

    def check_zoom(self):
        return 0 <= self.zoom <= 21
