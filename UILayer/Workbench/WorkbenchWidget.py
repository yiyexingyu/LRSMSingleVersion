from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

"""
    每个WorkbenchWidget对应一张用户要处理的图片
"""


class WorkbenchWidget(QWidget):
    """

    """
    def __init__(self, file_name=None, image=None, parent=None):
        super(WorkbenchWidget, self).__init__(parent)

        self.image_label = QLabel("image_label")
        self.image_label.setAlignment(Qt.AlignCenter)

        # 文件名 包含文件的路径
        self.file_name = file_name
        # 文件是否存在未保存数据标志
        self.dirty = True
        # 当前工作区的图片数据
        self.image = None
        self.set_image(image)

        # 图片的垂直镜像
        self.mirrored_vertically = False
        # 水平镜像
        self.mirrored_horizontally = False

        # 布局
        self.tab_vertical_layout = QVBoxLayout(self)
        self.tab_vertical_layout.addWidget(self.image_label)

    def get_file_name(self):
        return self.file_name

    def is_dirty(self):
        return self.dirty

    def set_image(self, image):
        if isinstance(image, QImage):
            self.image = image
            self.image_label.setPixmap(QPixmap.fromImage(self.image))
