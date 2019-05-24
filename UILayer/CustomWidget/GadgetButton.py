import functools
from PyQt5.QtWidgets import QPushButton, QMenu, QActionGroup
from PyQt5.QtGui import QContextMenuEvent, QCursor
from LRSMSingleVersion.CONST.CONST import NONE_RES


class GadgetButton(QPushButton):

    def __init__(self, menu_tuple=None, slot=None, is_group=True, parent=None):
        super(GadgetButton, self).__init__(parent)

        self.context_menu = None
        if menu_tuple and slot:
            self.slot = slot
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
                actions[0].setChecked(True)
            else:
                del actions

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        self.setChecked(True)
        if self.context_menu:
            if self.context_menu.exec_(QCursor.pos()) is not None:
                event.accept()
                return
            else:
                self.slot(NONE_RES)
        event.ignore()
        # QPushButton.contextMenuEvent(self, event)
