# -*- coding: utf-8 -*-
# @Time    : 2019/5/31 17:24
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : AbstractFile.py
# @Project : pyqt5_project
# @Software: PyCharm

from LRSMSingleVersion.ModelLayer.MarkItem import MarkItem


class AbstractFile(object):
    """ 描述 """

    def __init__(self):
        self._mark_items = []

    def add_mark_item(self, mark_item: MarkItem):
        self._mark_items.append(mark_item)

    def add_mark_items(self, mark_items):
        self._mark_items.extend(mark_items)

    def remove_item_by_item(self, mark_item: MarkItem):
        self._mark_items.remove(mark_item)

    def remove_item_by_index(self, index):
        self._mark_items.pop(index)

    def remove_item_by_name(self, name):
        for item in self._mark_items:
            if item.get_name() == name:
                self._mark_items.remove(item)
                return item
        return None

    def remove_all(self):
        temp = list(self._mark_items)
        self._mark_items.clear()
        return temp

    def get_file_data(self):
        """TODO 返回一个JSON数据"""
