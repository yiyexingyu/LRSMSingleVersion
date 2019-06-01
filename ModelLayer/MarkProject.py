# -*- coding: utf-8 -*-
# @Time    : 2019/6/1 14:57
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : MarkProject.py
# @Project : pyqt5_project
# @Software: PyCharm

from LRSMSingleVersion.ModelLayer.AbstractFile import AbstractFile
from LRSMSingleVersion.ModelLayer.AbstractFolder import AbstractFolder


class MarkProject(AbstractFolder, AbstractFile):
    """ 描述 """

    def __init__(self, name=None):
        super(MarkProject, self).__init__(name)
        AbstractFile.__init__(self)

    def get_project_data(self):
        """TODO 返回一JSON数据"""

