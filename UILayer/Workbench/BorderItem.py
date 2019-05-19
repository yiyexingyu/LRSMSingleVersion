import functools

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class BorderItem(QGraphicsItem):
    """
    边框
    """

    def __init__(self, position, scene, style=Qt.DashDotLine, rect=None, transform=QTransform()):
        super(BorderItem, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable)
        print(scene)
        if rect is None:
            rect = QRectF(0., 0., 200., 150.)
        self.rect = rect
        self.line_style = style

        self.setPos(position)
        self.setTransform(transform)

        scene.clearSelection()
        scene.addItem(self)
        self.setSelected(True)
        self.setFocus()

    def parentWidget(self):
        # 返回场景的第一个视图
        return self.scene().views()[0]

    def itemChange(self, change, variant):
        # 非选择状态的变化 要设置dirty标志
        if change != QGraphicsItem.ItemSelectedChange:
            print("item is changed!")

        return QGraphicsItem.itemChange(self, change, variant)

    def set_line_style(self, style):
        self.line_style = style
        self.update()

    def set_rect(self, width, height):
        self.rect.setWidth(width)
        self.rect.setHeight(height)
        self.update()

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

    def keyPressEvent(self, event):
        factor = 2.
        change = False
        if event.modifiers() & Qt.ShiftModifier:
            if event.key() == Qt.Key_Left:  # 按下左箭头
                self.rect.setRight(self.rect.right() - factor)
                change = True
            elif event.key() == Qt.Key_Right:   # 按下右箭头
                self.rect.setRight(self.rect.right() + factor)
                change = True
            elif event.key() == Qt.Key_Up:   # 按下右箭头
                self.rect.setBottom(self.rect.bottom() - factor)
                change = True
            elif event.key() == Qt.Key_Down:   # 按下右箭头
                self.rect.setBottom(self.rect.bottom() + factor)
                change = True

        if change:
            self.update()
        else:
            # 交给父类处理
            QGraphicsItem.keyPressEvent(self, event)

    # 继承QGraphicsItem类必须实现 boundingRect() paint()两个方法
    # 返回本item的 包围和矩形 QRectF 用于item的点击等判断
    def boundingRect(self):
        return self.rect.adjusted(-2, -2, -2, -2)

    def rectangle(self):
        return QRect(self.pos().x(), self.pos().y(), self.rect.width(), self.rect.height())

    # def paint(self, QPainter, QStyleOptionGraphicsItem, widget=None):
    def paint(self, painter, option, widget=None):
        pen = QPen(self.line_style)
        pen.setColor(Qt.black)
        pen.setWidth(1)

        if option.state & QStyle.State_Selected:
            pen.setColor(Qt.blue)

        painter.setPen(pen)
        painter.drawRect(self.rect)








