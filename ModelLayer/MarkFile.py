# -*- coding: utf-8 -*-
# @Time    : 2019/5/31 17:12
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : MarkFile.py
# @Project : pyqt5_project
# @Software: PyCharm

from LRSMSingleVersion.ModelLayer.AbstractMarkItem import AbstractMarkItem
from LRSMSingleVersion.ModelLayer.AbstractFile import AbstractFile


class MarkFile(AbstractMarkItem, AbstractFile):
    """ 描述 """

    def __init__(self, name=None):
        super(MarkFile, self).__init__(name)
        AbstractFile.__init__(self)


