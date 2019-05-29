import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, \
    QTreeWidget, QTreeWidgetItem, QDockWidget

from LRSMSingleVersion.Application.App import BASE_DIR


class ProjectDockWidget(QDockWidget):

    def __init__(self, parent=None):
        super(ProjectDockWidget, self).__init__("标注项目", parent)

        self.setObjectName("projectTreeDockWidget")

        self.project_tree = QTreeWidget(self)
        self.project_tree.setColumnCount(1)
        self.project_tree.setHeaderHidden(True)
        self.project_tree.setObjectName("projectTree")
        self.setWidget(self.project_tree)

    def create_project(self, project_info):
        root = QTreeWidgetItem(self.project_tree)
        root.setText(0, project_info["project_name"])
        root.setIcon(0, QIcon(os.path.join(BASE_DIR, "sources/images/file.png")))

        # 原始图片
        original_img_child = QTreeWidgetItem()
        original_img_child.setText(0, project_info["org_img_name"])
        original_img_child.setIcon(0, QIcon(os.path.join(BASE_DIR, "sources/images/img_icon.png")))
        root.addChild(original_img_child)

