import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import gdal

from  LRSMSingleVersion.UILayer.Workbench.BorderItem import BorderItem


class GraphicsView(QGraphicsView):

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        # 设置拖拽描述 橡皮筋？
        self.setDragMode(QGraphicsView.RubberBandDrag)
        # 渲染提示 hint提示  Antialiasing：消除混叠现象，消除走样，图形保真;
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setStyleSheet("""
        border: 0;
        """)

        # 缩放因子
        self.scale_factor = 20
        # 上一次鼠标触发的位置
        self.is_mouse_pressed = False
        self.last_cursor_pos = QPoint()
        # 图像元数据模型
        self.img_meta_model = QStandardItemModel()
        # 文件列表数据模型
        self.file_list_model = QStandardItemModel()
        # 图像数据集
        self.img_dataset = None
        # 缩放显示RGB彩色图
        self.show_color = True
        self.border = None

    def read_image(self, img_path):
        # gdal 注册
        gdal.AllRegister()
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
        self.img_dataset = gdal.Open(img_path, gdal.GA_ReadOnly)

        if not self.img_dataset:
            return

        self.show_file_list(img_path)
        self.show_image_info(img_path)

        # 根据波段 显示图片
        if self.img_dataset.RasterCount() != 3:
            self.show_color = False
            band = (self.img_dataset.GetRasterBand(1)) * 3,
            self.show_image(band)
        else:
            self.img_dataset = True
            band_list = (self.img_dataset.GetRasterBand(1),
                         self.img_dataset.GetRasterBand(2),
                         self.img_dataset.GetRasterBand(3))
            self.show_image(band_list)

    def show_file_list(self, img_path):
        pass

    def show_image_info(self, img_path):
        pass

    def show_image(self, band_list):
        pass

    def wheelEvent(self, event):
        factor = event.angleDelta().y() / 120.0
        factor = 2. if factor > 0 else 0.5
        self.scale(factor, factor)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            global_point = event.pos()
            BorderItem(self.mapToScene(global_point), self.scene())

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = True
            self.last_cursor_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # if self.is_mouse_pressed and event.button() == Qt.RightButton:
        if event.buttons() and Qt.LeftButton:
            if self.border is None:
                self.border = BorderItem(self.mapToScene(self.last_cursor_pos),
                                         self.scene(), rect=QRectF(0., 0., 0., 0.))
            mouse_point = event.pos()
            width = mouse_point.x() - self.last_cursor_pos.x()
            height = mouse_point.y() - self.last_cursor_pos.y()
            x, y = self.last_cursor_pos.x(), self.last_cursor_pos.y()
            if width < 0:
                x = mouse_point.x()
            if height < 0:
                y = mouse_point.y()
            self.border.setPos(self.mapToScene(QPoint(x, y)))
            self.border.set_rect(abs(width), abs(height))

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.is_mouse_pressed and event.button() == Qt.LeftButton:
            self.is_mouse_pressed = False
            self.border = None

    # def mouseMoveEvent(self, event):
    #     pass