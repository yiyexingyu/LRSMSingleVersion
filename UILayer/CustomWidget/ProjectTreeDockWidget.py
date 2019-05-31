import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QContextMenuEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, \
    QTreeWidget, QTreeWidgetItem, QDockWidget, QMenu, QInputDialog

from LRSMSingleVersion.Application.App import BASE_DIR
from LRSMSingleVersion.UILayer.CommonHelper.CommonHelper import *


class ProjectDockWidget(QDockWidget):
    MAKE_FILE = "mark_file"
    MAKE_ITEM = "mark_item"

    def __init__(self, parent=None):
        super(ProjectDockWidget, self).__init__("标注项目", parent)

        self.setObjectName("projectTreeDockWidget")

        self.project_tree = QTreeWidget(self)
        self.project_tree.setColumnCount(1)
        self.project_tree.setHeaderHidden(True)
        self.project_tree.setObjectName("projectTree")
        self.project_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_tree.customContextMenuRequested.connect(self.project_tree_item_context_menu)
        self.project_tree_root_context_menu = self._create_project_root_context_menu()
        self.setWidget(self.project_tree)

    def _create_project_root_context_menu(self):
        menu = QMenu(self.project_tree)
        rename_action = create_action(menu, "重命名", slot=self.rename)
        new_mark_file = create_action(menu, "新建标注文件", slot=self.create_mark_file)
        new_mark_item = create_action(menu, "新建标注项", slot=self.create_mark_item)
        property_setting = create_action(menu, "属性", slot=self.property_setting)

        add_actions(menu, (new_mark_file, new_mark_item, None, rename_action, None, property_setting))
        return menu

    def create_project(self, project_info):
        root = QTreeWidgetItem(self.project_tree)
        root.setText(0, project_info["project_name"])
        root.setIcon(0, QIcon(os.path.join(BASE_DIR, "sources/images/file.png")))

        # 原始图片
        original_img_child = QTreeWidgetItem()
        original_img_child.setText(0, project_info["org_img_name"])
        original_img_child.setIcon(0, QIcon(os.path.join(BASE_DIR, "sources/images/img_icon.png")))
        root.addChild(original_img_child)

    def project_tree_item_context_menu(self, point):
        point = self.project_tree.mapToGlobal(point)
        current_item = self.project_tree.currentItem()
        if current_item:
            if not current_item.parent():
                self.project_tree_root_context_menu.exec_(point)

    def rename(self):
        current_item = self.project_tree.currentItem()
        new_name, ok = QInputDialog.getText(self, "重命名", "请输入新的名字：", text=current_item.text(0))
        if ok:
            current_item.setText(0, new_name)

    def create_mark_file(self):
        mark_file_name, ok = QInputDialog.getText(self, "新建标注文件", "请输入标注文件名：")
        if ok:
            new_mark_file = QTreeWidgetItem()
            new_mark_file.setText(0, mark_file_name)
            new_mark_file.setWhatsThis(0, self.MAKE_FILE)
            new_mark_file.setIcon(0, QIcon(os.path.join(BASE_DIR, "sources/images/file.png")))
            self.project_tree.currentItem().addChild(new_mark_file)

    def create_mark_item(self):
        mark_item_name, ok = QInputDialog.getText(self, "新建标注项", "请输入标注项的名称：")
        if ok:
            new_mark_item = QTreeWidgetItem()
            new_mark_item.setText(0, mark_item_name)
            new_mark_item.setWhatsThis(0, self.MAKE_ITEM)
            new_mark_item.setIcon(0, QIcon(os.path.join(BASE_DIR, "sources/images/mark_item.jpg")))
            self.project_tree.currentItem().addChild(new_mark_item)

    # 标注项目属性的设置
    def property_setting(self):
        pass


class ProjectTreeWidget(QTreeWidget):

    def __init__(self, parent=None):
        super(ProjectTreeWidget, self).__init__(parent)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        if self.topLevelItemCount():
            current_item = self.currentItem()
            print(current_item.text(0))
