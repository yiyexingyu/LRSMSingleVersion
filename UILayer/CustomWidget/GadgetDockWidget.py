import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDockWidget, QWidget,\
    QButtonGroup, QVBoxLayout, QSpacerItem, QSizePolicy
from LRSMSingleVersion.Application.App import BASE_DIR
from LRSMSingleVersion.CONST.CONST import *
from LRSMSingleVersion.UILayer.CustomWidget.GadgetButton import GadgetButton
from LRSMSingleVersion.UILayer.CustomWidget.DockWidget import DockWidget


class GadgetDockWidget(DockWidget):

    gadget_changed = pyqtSignal(int)

    def __init__(self, widget_title=None, parent=None):
        if widget_title is None:
            widget_title = " "
        super(GadgetDockWidget, self).__init__(widget_title, parent)

        self.setObjectName("gadget_dock_window")
        self.content_widget.setObjectName("gadget_dock_content_widget")

        self.current_quick_select_tool = ELLIPSE_QUICK_SELECT_TOOL
        self.current_grip_tool = GRIP_TONGS
        self.current_gadget = None

        self._init_content_widget()
        self.setWidget(self.content_widget)

    def _init_content_widget(self):
        gadget_dock_widget_stylesheet = """
        QPushButton { 
            border: 0;
            padding: 8px;
        }
        QPushButton:hover{
            background-color: rgb(151, 151, 151)
        }
        QPushButton:checked{
            background-color: rgb(151, 151, 151)
        }
        """
        self.content_widget.setStyleSheet(gadget_dock_widget_stylesheet)

        quick_select_context_menu = (
            ("椭圆选框工具", ELLIPSE_QUICK_SELECT_TOOL),
            ("矩形选框工具", RECT_QUICK_SELECT_TOOL)
        )
        grip_context_menu = (
            ("抓手工具(H)", GRIP_TONGS),
            ("视图旋转工具(H)", GRIP_ROTATE)
        )

        move_tool_action = self.create_context_button(
            tip="移动工具(V)", parent=self.content_widget,
            image=os.path.join(BASE_DIR, "sources/icons/move_select.ico"))
        self.quick_select_action = self.create_context_button(
            context_menu=quick_select_context_menu,
            context_slot=self.select_quick_select_tool,
            tip="椭圆选择框(M)", parent=self.content_widget,
            image=os.path.join(BASE_DIR, "sources/icons/quick_select_oval.ico"))
        self.grip_action = self.create_context_button(
            context_menu=grip_context_menu,
            context_slot=self.select_grip_tool,
            tip="抓手工具(H)", parent=self.content_widget,
            image=os.path.join(BASE_DIR, "sources/icons/cursor_hand.ico"))
        zoom_action = self.create_context_button(
            tip="缩放工具(Z)", parent=self.content_widget,
            image=os.path.join(BASE_DIR, "sources/icons/zoom.ico"))

        self.gadget_button_group = QButtonGroup(self)
        self.join_group(
            self.gadget_button_group,
            ((move_tool_action, MOVE_TOOL),
             (self.quick_select_action, QUICK_SELECT_TOOL),
             (self.grip_action, GRIP_TOOL),
             (zoom_action, ZOOM_TOOL)))
        self.gadget_button_group.buttonClicked.connect(self.select_gadget)

        self.verticalLayout = QVBoxLayout(self.content_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.verticalLayout.addWidget(move_tool_action, alignment=Qt.AlignLeft)
        self.verticalLayout.addWidget(self.quick_select_action, alignment=Qt.AlignLeft)
        self.verticalLayout.addWidget(self.grip_action, alignment=Qt.AlignLeft)
        self.verticalLayout.addWidget(zoom_action, alignment=Qt.AlignLeft)
        spacer_item1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item1)

    def get_current_gadget(self):
        if self.current_gadget == QUICK_SELECT_TOOL:
            return self.current_quick_select_tool
        if self.current_gadget == GRIP_TOOL:
            return self.current_grip_tool
        else:
            return self.current_gadget

    @staticmethod
    def create_context_button(context_menu=None, context_slot=None, slot=None, tip=None,
                              checkable=True, image=None, signal="toggled", parent=None):
        new_action = GadgetButton(context_menu, context_slot, parent)
        if checkable:
            new_action.setCheckable(True)
        if tip:
            new_action.setToolTip(tip)
            new_action.setStatusTip(tip)
        if slot and callable(slot):
            if signal == "clicked":
                new_action.clicked.connect(slot)
            elif signal == "toggled":
                new_action.toggled.connect(slot)
        if image:
            new_action.setIcon(QIcon(image))
        return new_action

    @staticmethod
    def join_group(target, actions):
        for action in actions:
            target.addButton(action[0], action[1])

    def select_quick_select_tool(self, selected):
        if selected == RECT_QUICK_SELECT_TOOL:
            self.quick_select_action.setToolTip("矩形选择框(M)")
            self.quick_select_action.setStatusTip("矩形选择框(M)")
            self.quick_select_action.setIcon(
                QIcon(os.path.join(BASE_DIR, "sources/icons/quick_select_rectangle.ico")))
        elif selected == ELLIPSE_QUICK_SELECT_TOOL:
            self.quick_select_action.setToolTip("椭圆选择框(M)")
            self.quick_select_action.setStatusTip("椭圆选择框(M)")
            self.quick_select_action.setIcon(
                QIcon(os.path.join(BASE_DIR, "sources/icons/quick_select_oval.ico")))
        elif selected == NONE_RES:
            selected = self.current_quick_select_tool

        self.current_quick_select_tool = self.current_gadget = selected
        self.change_gadget(self.current_quick_select_tool)

    def select_grip_tool(self, selected):
        if selected == GRIP_TONGS:
            self.grip_action.setToolTip("抓手工具(H)")
            self.grip_action.setStatusTip("抓手工具(H)")
            self.grip_action.setIcon(
                QIcon(os.path.join(BASE_DIR, "sources/icons/cursor_hand.ico")))
        elif selected == GRIP_ROTATE:
            self.grip_action.setToolTip("视图旋转工具(R)")
            self.grip_action.setStatusTip("视图旋转工具(R)")
            self.grip_action.setIcon(
                QIcon(os.path.join(BASE_DIR, "sources/icons/rotate.ico")))
        elif selected == NONE_RES:
            selected = self.current_grip_tool
        self.current_grip_tool = self.current_gadget = selected
        self.change_gadget(self.current_grip_tool)

    def select_gadget(self):
        btn_id = self.gadget_button_group.checkedId()
        self.current_gadget = btn_id
        if btn_id == MOVE_TOOL:
            self.change_gadget(MOVE_TOOL)
        elif btn_id == QUICK_SELECT_TOOL:
            self.change_gadget(self.current_quick_select_tool)
        elif btn_id == GRIP_TOOL:
            self.change_gadget(self.current_grip_tool)
        elif btn_id == ZOOM_TOOL:
            self.change_gadget(ZOOM_TOOL)

    def change_gadget(self, gadget):
        self.gadget_changed.emit(gadget)

