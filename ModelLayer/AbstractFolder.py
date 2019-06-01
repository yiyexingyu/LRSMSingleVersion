# -*- coding: utf-8 -*-
# @Time    : 2019/6/1 13:24
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : AbstractFolder.py
# @Project : pyqt5_project
# @Software: PyCharm

from LRSMSingleVersion.CommonHelper.CommonHelper \
    import remove_object_by_indexes, remove_object_by_objects


class AbstractFolder(object):
    """ 描述 """

    def __init__(self, name):
        self._name = name
        self._mark_files = []
        self._folders = []

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def add_mark_file(self, mark_file):
        self._mark_files.append(mark_file)

    def add_mark_files(self, make_files):
        self._mark_files.extend(make_files)

    def remove_mark_file_by_mark_file(self, mark_file):
        if mark_file in self._mark_files:
            self._mark_files.remove(mark_file)

    def remove_mark_files_by_mark_files(self, mark_files):
        remove_object_by_objects(self._mark_files, mark_files)
        # for mark_file in mark_files:
        #     if mark_file in self._mark_files:
        #         self._mark_files.remove(mark_file)

    def remove_mark_file_by_index(self, index):
        if 0 <= index < len(self._mark_files):
            self._mark_files.pop(index)

    def remove_mark_files_by_indexes(self, indexes):
        remove_object_by_indexes(self._mark_files, indexes)
        # indexes = reversed(sorted(indexes))
        # for index in indexes:
        #     if 0 <= index < len(self._mark_files):
        #         self._mark_files.pop(index)

    def add_folder(self, folder):
        self._folders.append(folder)

    def add_folders(self, folders):
        self._folders.extend(folders)

    def remove_folder_by_folder(self, folder):
        if folder in self._folders:
            self._folders.remove(folder)

    def remove_folder_by_index(self, index):
        if 0 <= index < len(self._folders):
            self._folders.pop(index)

    def remove_folders_by_folders(self, folders):
        remove_object_by_objects(self._folders, folders)
        # for folder in folders:
        #     if folder in self._folders:
        #         self._folders.remove(folder)

    def remove_folders_by_indexes(self, indexes):
        remove_object_by_indexes(self._folders, indexes)

    def get_folder_data(self):
        """TODO"""
