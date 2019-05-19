from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class RectangleItem(QGraphicsRectItem):

    def __init__(self, parent=None):
        super(RectangleItem, self).__init__(parent)
