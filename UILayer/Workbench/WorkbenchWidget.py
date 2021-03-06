import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRectF, QRect
import cv2
from LRSMSingleVersion.UILayer.Workbench.GraphicsView import GraphicsView
from LRSMSingleVersion.CONST.CONST import *

"""
    每个WorkbenchWidget对应一张用户要处理的图片
"""


class WorkbenchWidget(QWidget):
    """

    """
    def __init__(self, file_name=None, gadget=None, parent=None):
        super(WorkbenchWidget, self).__init__(parent)

        self.image_label = QLabel("image_label")
        self.image_label.setAlignment(Qt.AlignCenter)

        # 文件名 包含文件的路径
        self.file_name = file_name
        # 文件是否存在未保存数据标志
        self.dirty = False
        # 当前工作区的图片数据
        self.image = None
        self.current_gadget = None

        # 图片的垂直镜像
        self.mirrored_vertically = False
        # 水平镜像
        self.mirrored_horizontally = False
        # 创建视图
        self.workbench_view = GraphicsView(self)
        self.workbench_view.setObjectName("workbench_view")

        # 创建场景
        self.workbench_scene = QGraphicsScene(self)
        self.workbench_scene.setObjectName("workbench_scene")

        # 把场景添加到视图中
        self.workbench_view.setScene(self.workbench_scene)

        # 布局
        self.tab_vertical_layout = QVBoxLayout(self)
        self.tab_vertical_layout.addWidget(self.workbench_view)

        self._load_image()

        # 当前选择小工具
        self.change_gadget(gadget)

    def get_file_name(self):
        return self.file_name

    def is_dirty(self):
        return self.dirty

    def _load_image(self):
        image = QImage(self.file_name)
        # cv2_img = cv2.imread(self.file_name, cv2.IMREAD_COLOR)
        # print(self.file_name)
        # print(cv2_img)
        # print(cv2_img.shape)
        # # cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        # image = QImage(cv2_img, cv2_img.shape[1], cv2_img.shape[0], QImage.Format_RGB8888)

        self.workbench_scene.setSceneRect(0, 0, image.width(), image.height())
        if image.isNull():
            del self
            raise FileOpenFailException(self.file_name)
        else:
            self.image = image
            self.image = QPixmap.fromImage(self.image)
            pixmap_item = QGraphicsPixmapItem(self.image)
            pixmap_item.setPos(0, 0)
            self.workbench_scene.addItem(pixmap_item)

    def rotate(self, angle):
        for item in self.workbench_scene.selectedItems():
            item.rotate(angle)

    def delete(self):
        items = self.workbench_scene.selectedItems()
        if len(items) and QMessageBox.question(self, "您确认要删除这些项吗？", "?????",
                                               QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            while items:
                item = items.pop()
                self.workbench_scene.removeItem(item)
                del item
            self.dirty = True

    def change_gadget(self, gadget):
        self.current_gadget = gadget
        if self.current_gadget == MOVE_TOOL:
            self.setCursor(Qt.SizeAllCursor)
        elif self.current_gadget == RECT_QUICK_SELECT_TOOL or \
                self.current_gadget == ELLIPSE_QUICK_SELECT_TOOL:
            self.setCursor(Qt.CrossCursor)
        elif self.current_gadget == GRIP_TONGS:
            self.setCursor(Qt.OpenHandCursor)
        elif self.current_gadget == GRIP_ROTATE:
            self.setCursor(Qt.SizeFDiagCursor)
        elif self.current_gadget == ZOOM_TOOL:
            self.setCursor(Qt.SizeHorCursor)
        self.workbench_view.set_shape(self.current_gadget)


class FileOpenFailException(Exception):

    def __init__(self, file_name):
        self.message = "打开文件\"" + file_name + "\"失败"

    def __str__(self):
        return repr(self.message)
