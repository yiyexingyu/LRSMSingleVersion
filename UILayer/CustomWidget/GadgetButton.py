import functools
from PyQt5.QtWidgets import QPushButton, QMenu, QActionGroup
from PyQt5.QtGui import QContextMenuEvent, QCursor
from PyQt5.QtCore import Qt, QPoint


class GadgetButton(QPushButton):

    def __init__(self, menu_tuple=None, slot=None, is_group=True, parent=None):
        super(GadgetButton, self).__init__(parent)

        self.context_menu = None
        if menu_tuple and slot:
            self.context_menu = QMenu()
            actions = []
            for text, arg in menu_tuple:
                wrapper = functools.partial(slot, arg)
                actions.append(self.context_menu.addAction(text, wrapper))

            if is_group:
                group = QActionGroup(self)
                for action in actions:
                    action.setCheckable(True)
                    group.addAction(action)
            else:
                del actions

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        self.setChecked(True)
        if self.context_menu:
            self.context_menu.exec_(QCursor.pos())
        else:
            QPushButton.contextMenuEvent(self, event)
