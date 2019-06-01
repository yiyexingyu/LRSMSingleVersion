# -*- coding: utf-8 -*-
# @Time    : 2019/5/30 21:57
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : Selection.py
# @Project : LRSMSingleVersion
# @Software: PyCharm

from PyQt5.QtCore import QRect
from LRSMSingleVersion.CONST.CONST import *
from LRSMSingleVersion.ModelLayer.AbstractMarkItem import AbstractMarkItem


class Selection(object):
    """ 描述 """

    def __init__(self, rect: QRect = QRect(), shape=RECTANGLE, name=None):
        self._rect = rect
        self._shape = shape
        self._name = name
        self._has_bind_to = []

    def get_rect(self):
        return self._rect

    def set_rect(self, rect: QRect):
        self._rect = rect

    def set_size(self, width, height):
        self._rect.setWidth(width)
        self._rect.setHeight(height)

    def get_shape(self):
        return self._shape

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def bind_to(self, mark_item: AbstractMarkItem):
        pass

    def unbind_to(self, mark_item: AbstractMarkItem):
        pass