

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Fivezi_ui import Ui_MainWindow
from const_Icon import *
import sys


class PanUnit(QObject):

    def __init__(self, pb):
        self.qizi = None
        self.pb = pb
        # self.pb.clicked.connect(self.change)

    def change(self):
        print('dddddd')
        if self.qizi == None:
            self.qizi = HONG
            self.set_h()
        else:
            self.qizi = LV
            self.set_l()

    def set_h(self):
        self.pb.setIcon(QIcon(self.convert_svg_to_pixmap(HONG)))

    def set_l(self):
        self.pb.setIcon(QIcon(self.convert_svg_to_pixmap(LV)))

    def convert_svg_to_pixmap(self, svg_str: str):
        pixmap = QPixmap()
        pixmap.loadFromData(svg_str.encode())
        return pixmap


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__init_parameters()
        self.__init_ui()
        self.__init_connections()
        self.show()

    def __init_parameters(self):
        self.panu = PanUnit(self.pushButton)
        self.pushButton.clicked.connect(self.change)

    def __init_ui(self):
        self.pushButton.setIcon(QIcon(self.convert_svg_to_pixmap(PAN)))
        psize = self.pushButton.geometry()
        self.pushButton.setIconSize(QSize(150, 150))

    def __init_connections(self):
        ...
        # self.pushButton.clicked.connect(self.set_qizi)

    def convert_svg_to_pixmap(self, svg_str: str):
        pixmap = QPixmap()
        pixmap.loadFromData(svg_str.encode())
        return pixmap

    def change(self):
        if self.panu.qizi == None or self.panu.qizi == LV:
            self.panu.qizi = HONG
            self.set_h()
        else:
            self.panu.qizi = LV
            self.set_l()

    def set_h(self):
        self.pushButton.setIcon(QIcon(self.convert_svg_to_pixmap(HONG)))

    def set_l(self):
        self.pushButton.setIcon(QIcon(self.convert_svg_to_pixmap(LV)))


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
