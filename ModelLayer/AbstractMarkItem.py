# -*- coding: utf-8 -*-
# @Time    : 2019/5/31 15:53
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : AbstractMarkItem.py
# @Project : pyqt5_project
# @Software: PyCharm


class AbstractMarkItem(object):
    """ 描述 """

    def __init__(self, name):
        self._name = name
        self._has_band = False

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def has_band(self, hans_band=None):
        if hans_band is None:
            return self._has_band
        else:
            self._has_band = hans_band
            return hans_band

    def set_selection(self, selection):
        pass
