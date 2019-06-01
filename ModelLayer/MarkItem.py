# -*- coding: utf-8 -*-
# @Time    : 2019/5/31 16:06
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : MarkItem.py
# @Project : pyqt5_project
# @Software: PyCharm

from LRSMSingleVersion.ModelLayer.AbstractMarkItem import AbstractMarkItem


class MarkItem(AbstractMarkItem):
    """ 描述 """

    def __init__(self, name=None):
        super(MarkItem, self).__init__(name)

        self._outline_array = []
        self._mark_type = None
        self._girth = -1
        self._area = -1
        self._markers = []
        self._mark_time = None

    def set_outline(self, outline_array: list):
        self._outline_array = list(outline_array)

    def get_outline(self):
        return tuple(self._outline_array)

    def set_mark_type(self, mark_type):
        self._mark_type = mark_type

    def get_mark_type(self):
        return self._mark_type

    def set_girth(self, girth):
        self._girth = girth

    def get_girth(self):
        return self._girth

    def count_girth(self, count_algorithm):
        if callable(count_algorithm):
            self._girth = count_algorithm(self._outline_array)

    def set_area(self, area):
        self._area = area

    def get_area(self):
        return self._area

    def count_area(self, count_algorithm):
        if callable(count_algorithm):
            self._area = count_algorithm(self._outline_array)

    def set_mark_time(self, mark_time):
        self._mark_time = mark_time

    def get_mark_time(self):
        return self._mark_time

    def add_marker(self, marker):
        self._markers.append(marker)

    def add_markers(self, markers: list):
        self._markers.extend(markers)

    def remove_marker_by_name(self, marker):
        self._markers.remove(marker)

    def remove_marker_by_index(self, index):
        self._markers.pop(index)

    def get_mark_item_data(self):
        """TODO 返回一个JSON数据"""
