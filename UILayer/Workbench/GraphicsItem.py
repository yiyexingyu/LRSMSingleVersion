import functools

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GraphicsItem(QGraphicsItem):

    def __init__(self, style=Qt.DashLine, transform=QTransform(), parent=None):
        super(GraphicsItem, self).__init__(parent)

        self.line_style = style
        self.setTransform(transform)

    def set_line_style(self, style):
        self.line_style = style
        self.update()

    def parentWidget(self):
        # 返回场景的第一个视图
        return self.scene().views()[0]

    def itemChange(self, change, variant):
        # 非选择状态的变化 要设置dirty标志
        if change != QGraphicsItem.ItemSelectedChange:
            print("item is changed!")

    def contextMenuEvent(self, event):
        wrapped = []
        menu = QMenu(self.parentWidget())
        for text, line_style in (("实线", Qt.SolidLine),
                                 ("线型虚线", Qt.DashLine),
                                 ("点型虚线", Qt.DotLine),
                                 ("DashDotLine", Qt.DashDotLine),
                                 ("DashDotDotLine", Qt.DashDotDotLine)):
            wrapper = functools.partial(self.set_line_style, line_style)
            wrapped.append(wrapper)
            menu.addAction(text, wrapper)
        menu.exec_(event.screenPos())

    # 继承QGraphicsItem类必须实现 boundingRect() paint()两个方法
    # 返回本item的 包围和矩形 QRectF 用于item的点击等判断
    def boundingRect(self):
        # TODO
        pass

    def paint(self, painter, option, widget=None) -> None:
        # TODO
        pass


class EllipseItem(QGraphicsEllipseItem):

    def __init__(self, position, scene, style=Qt.DashLine,
                 rect=None, transform=QTransform(), parent=None):
        super(EllipseItem, self).__init__(parent)

        self.setFlags(QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIsFocusable)

        if rect is None:
            rect = QRect(0, 0, 0, 0)
        self.setPos(position)
        self.setRect(rect)

        scene.clearSelection()
        scene.addItem(self)
        self.setSelected(True)
        self.setFocus()

    def set_rect(self, width, height):
        self.setRect(0, 0, width, height)
