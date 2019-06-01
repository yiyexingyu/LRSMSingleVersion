# -*- coding: utf-8 -*-
# @Time    : 2019/6/1 14:41
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : Folder.py
# @Project : pyqt5_project
# @Software: PyCharm

from LRSMSingleVersion.ModelLayer.AbstractFile import AbstractFile
from LRSMSingleVersion.ModelLayer.AbstractFolder import AbstractFolder


class Folder(AbstractFolder, AbstractFile):
    """ 描述 """

    def __init__(self, name=None):
        super(Folder, self).__init__(name)
        AbstractFile.__init__(self)

