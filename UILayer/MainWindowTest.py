import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from LRSMSingleVersion.Application.App import BASE_DIR
from LRSMSingleVersion.UILayer.Workbench.WorkbenchWidget import WorkbenchWidget, FileOpenFailException
from LRSMSingleVersion.UILayer.CustomWidget.GadgetButton import GadgetButton

__version__ = "1.0.0"


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # 窗体的中心 使用 QTabWidget # 中心部件
        self.center_tab_widget = QTabWidget(self)
        self.center_tab_widget.setMovable(True)
        self.center_tab_widget.setTabsClosable(True)
        self.center_tab_widget.tabCloseRequested.connect(self.close_file)

        self.center_tab_widget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.center_tab_widget)  # 设置此label为窗口的

        # 设置MenuBar
        self.menubar = self.menuBar()
        self._init_menubar()
        # 设置ToolBar
        self._init_toolbar()

        # 创建 main window的停靠窗口
        dock_widget_limit = Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea

        # 创建 gadget_dock_window 停靠窗口
        self.gadget_dock_widget, self.gadget_dock_content_widget = \
            self.create_dock_widget(" ", "gadget_dock_window", "gadget_dock_content_widget")
        self.gadget_dock_widget.setAllowedAreas(dock_widget_limit)
        self._create_gadget_dock_widget()
        self.gadget_dock_widget.setWidget(self.gadget_dock_content_widget)
        self.gadget_dock_widget.setMaximumSize(36, 1026)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.gadget_dock_widget)

        # 创建颜色设置的停靠窗口
        self.color_dock_widget, self.color_dock_content_widget = \
            self.create_dock_widget("颜色", "color_dock_widget", "color_dock_content_widget")
        self.color_dock_widget.setAllowedAreas(dock_widget_limit)
        self.color_dock_widget.setFixedSize(200, 140)
        self._create_color_dock_widget()
        self.color_dock_widget.setWidget(self.color_dock_content_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.color_dock_widget)

        # 创建图层停靠窗口
        self.layer_dock_widget, self.layer_dock_content_widget = \
            self.create_dock_widget("图层", "layer_dock_widget", "layer_dock_content_widget")
        self.layer_dock_widget.setAllowedAreas(dock_widget_limit)
        self._create_layer_dock_widget()
        self.layer_dock_widget.setWidget(self.layer_dock_content_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.layer_dock_widget)

        # 状态栏相关
        self.size_label = QLabel()
        self.size_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        status = self.statusBar()
        # 关闭状态栏的尺寸大小拖拽符
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.size_label)
        status.showMessage("Ready", 5000)  # 消息显示5秒

        self.screenRect = QApplication.desktop().screenGeometry()
        self.setWindowTitle("遥感地图地物类型标注")
        self.move(0, 0)

        self.resize(self.screenRect.width(), self.screenRect.height() - 90)
        self._restore_data()
        self.update_file_menu()
        # self.init_style()

    def init_style(self):
        # file(":/qss/psblack.qss");
        # file(":/qss/flatwhite.qss");
        file = QFile(os.path.join(os.getcwd(), "other/qss/lightblue.qss"))
        if file.open(QFile.ReadOnly):
            qss = file.readAll()
            palette_color = qss.mid(23, 7)
            print(palette_color)
            self.setPalette(QPalette(QColor(str(palette_color))))
            print(qss.data())
            self.setStyleSheet(str(qss))
            file.close()

    # 数据恢复
    def _restore_data(self):
        settings = QSettings()
        self.recent_files = settings.value("recent_files")

        window_state = settings.value("main_window/state")

        if not self.recent_files:
            self.recent_files = []
        # if window_state is not None:
        #     self.restoreState(window_state)
        QTimer.singleShot(0, self._load_initial_file)

    # 加载文件数据
    def _load_initial_file(self):
        pass

    # 重写 窗口关闭事件
    def closeEvent(self, event):

        if self.ok_to_continue():
            settings = QSettings()

            # 最近打开文件
            recently_files = QVariant(self.recent_files) if self.recent_files else QVariant()
            settings.setValue("recent_files", recently_files)

            # 主窗口的其他状态
            settings.setValue("main_window/state", QVariant(self.saveState()))
        else:
            event.ignore()

    # 用户关闭窗口前提问
    def ok_to_continue(self):
        tab_num = self.center_tab_widget.count()
        for _ in range(tab_num):
            if not self.close_file(index=0):
                return False
        return True

    def is_save_question(self, file_name):
        tip_text = "要在退出前保存对 图片\"" + file_name.split("/")[-1] + "\"的更改吗？"
        reply = QMessageBox.question(self, "遥感地图标注 - 未保存提示", tip_text,
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            return False
        elif reply == QMessageBox.Yes:
            self.save_file(file_name=file_name)
            return True
        else:
            return True

    # 创建菜单栏
    def _init_menubar(self):

        # 创建一级菜单
        self.file_menu = self.add_menu("文件(F)", self.menubar, "file_menu",
                                       slot=self.update_file_menu, signal="aboutToShow")
        self.edit_menu = self.add_menu("编辑(E)", self.menubar, "edit_menu")
        self.graph_menu = self.add_menu("图像(I)", self.menubar, "graph_menu")
        self.mark_menu = self.add_menu("标注(M)", self.menubar, "mark_menu")
        self.test_menu = self.add_menu("实验(T)", self.menubar, "test_menu")
        self.help_menu = self.add_menu("帮助(H)", self.menubar, "help_menu")

        # 创建文件菜单的二级菜单/动作
        # 由于要显示最近打开的文件 我们要动态的显示这个菜单
        open_file_action = self.create_action("打开(O)...", self.open_file, "Ctrl+O")
        close_action = self.create_action("关闭(C)", self.close_file, "Ctrl+W")
        close_all_action = self.create_action("全部关闭", self.close_all_file, "Alt+Ctrl+W")
        save_action = self.create_action("保存(S)", self.save_file, "Ctrl+S")
        save_as_action = self.create_action("保存(S)", self.save_file_as, "Shift+Ctrl+S")
        import_action = self.create_action("导入(M)...", self.import_file)
        export_action = self.create_action("导出(E)...", self.export_file)
        quit_action = self.create_action("退出(Q)", self.quit, "Ctrl+Q")

        close_action.setEnabled(False)
        close_all_action.setEnabled(False)
        # 先这些动作组织保存起来 等文件菜单aboutToShow时用
        self.file_menu_actions = [open_file_action, None, close_action, close_all_action,
                                  None, save_action, save_as_action, None, import_action,
                                  export_action, None, quit_action]

        # 创建编辑菜单的二级菜单/动作
        revert_action = self.create_action("还原(O)", self.edit_step, "Ctrl+Z")
        undo_action = self.create_action("后退一步(K)", self.edit_step, "Alt+Ctrl+Z")
        redo_action = self.create_action("前进一步(W)", self.edit_step, "Alt+Ctrl+Z")
        reference_action = self.create_action("首选项(N)...", self.edit_reference)
        # 将这些动作加入到 编辑菜单中
        self.add_actions(self.edit_menu, (revert_action, redo_action, undo_action, None, reference_action))

        # 创建图像菜单的二级菜单/动作
        self.mode_menu = self.graph_menu.addMenu("模式(M)")
        self.graph_menu.addSeparator()
        self.adjust_menu = self.graph_menu.addMenu("调整(J)")
        self.graph_menu.addSeparator()
        size_action = self.create_action("图像大小(I)...", self.graph_resize, "Ctrl+Alt+I")
        self.graph_menu.addAction(size_action)
        self.rotate_menu = self.graph_menu.addMenu("图像旋转(G)")

        # 创建图像菜单的二级菜单 模式 的二级动作
        bmp_action = self.create_action("位图(B)", self.graph_mode, signal="toggled", checkable=True)
        gray_action = self.create_action("灰度(G)", self.graph_mode, signal="toggled", checkable=True)
        rgb_action = self.create_action("位图(B)", self.graph_mode, signal="toggled", checkable=True)
        # 将这三个动作作为一个动作组
        self.join_group(QActionGroup(self), (bmp_action, gray_action, rgb_action))
        rgb_action.setChecked(True)  # 默认是rbg模式
        self.add_actions(self.mode_menu, (bmp_action, gray_action, rgb_action))

        # 创建 图像菜单 的二级菜单 调整 的二级动作
        bright_action = self.create_action("亮度/对比度(C)...", self.graph_adjust)
        self.adjust_menu.addAction(bright_action)

        # 创建 图像菜单 的二级菜单 图像旋转 的二级动作
        rotate_180_action = self.create_action("180度(1)", self.graph_rotate)
        rotate_clockwise90_action = self.create_action("90度(顺时针)(9)", self.graph_rotate)
        rotate_counterclockwise90_action = self.create_action("90度(逆时针)(9)", self.graph_rotate)
        rotate_any_action = self.create_action("任意角度(A)...", self.graph_rotate)
        self.add_actions(self.rotate_menu, (rotate_180_action, rotate_clockwise90_action,
                                            rotate_counterclockwise90_action, rotate_any_action))

        # 创建 标注 菜单的二级菜单/动作
        self.layer_menu = self.add_menu("图层(L)", self.mark_menu, "layer_menu")
        self.mark_menu.addSeparator()
        self.quick_select_menu = self.add_menu("快速选择工具", self.mark_menu, "quick_select_menu")
        self.mark_menu.addSeparator()
        self.outline_detect_menu = self.add_menu("轮廓检测(D)", self.mark_menu, "outline_detect_menu")

        # 创建 标注菜单 的二级菜单 图层 的二级动作
        new_layer_action = self.create_action("新建图层(N)", self.new_layer, "Shift+Ctrl+N")
        self.layer_menu.addAction(new_layer_action)

        # 创建 标注菜单 的二级菜单 快速选择工具 的二级动作
        rectangle_action = self.create_action("矩形选择框", self.switch_select_tool, signal="toggled", checkable=True)
        oval_action = self.create_action("椭圆选择框", self.switch_select_tool, signal="toggled", checkable=True)
        self.join_group(QActionGroup(self), (rectangle_action, oval_action))
        self.add_actions(self.quick_select_menu, (rectangle_action, oval_action))

        # 创建 标注菜单 的二级菜单 轮廓检测 的二级动作
        origin_outline_action = self.create_action("原始轮廓(O)", self.outline_detect, "Ctrl+A+O",
                                                   signal="toggled", checkable=True)
        convex_outline_action = self.create_action("凸性缺陷轮廓(C)", self.outline_detect, "Ctrl+A+C",
                                                   signal="toggled", checkable=True)
        polygon_outline_action = self.create_action("多边形轮廓(P)", self.outline_detect, "Ctrl+A+P",
                                                    signal="toggled", checkable=True)
        self.join_group(QActionGroup(self), (origin_outline_action, convex_outline_action, polygon_outline_action))
        self.add_actions(self.outline_detect_menu,
                         (origin_outline_action, convex_outline_action, polygon_outline_action))

        # 创建 实验 菜单的二级菜单/动作
        erosion_area_action = self.create_action("侵蚀面积(E)...", self.result_test)
        contrast_action = self.create_action("图像对比图(C)...", self.result_test)
        self.add_actions(self.test_menu, (erosion_area_action, contrast_action))

        # 创建 帮助 菜单的二级菜单/动作
        help_about_action = self.create_action("关于(A)...", self.help)
        help_help_action = self.create_action("帮助(H)...", self.help)
        self.add_actions(self.help_menu, (help_about_action, help_help_action))

    # 创建工具栏
    def _init_toolbar(self):
        # 添加 快速选择 的工具栏
        self.quick_select_toolbar = self.addToolBar("quick_select")
        quick_select_toolbar_stylesheet = """
        QCheckBox { margin: 0 10px; }
        QLabel { margin-left: 8px; }
        QLineEdit { margin-right: 7px; }
        """
        self.quick_select_toolbar.setStyleSheet(quick_select_toolbar_stylesheet)

        # 选区操作
        new_selection_action = self.create_action("", self.change_selection, tip="新建选区",
                                                  signal="toggled",  checkable=True,
                                                  image=os.path.join(BASE_DIR, "sources/icons/new_selection.ico"))
        add_to_selection_action = self.create_action("", self.change_selection, tip="添加到选区",
                                                     signal="toggled", checkable=True,
                                                     image=os.path.join(BASE_DIR, "sources/icons/new_selection.ico"))
        remove_from_selection_action = self.create_action("", self.change_selection, tip="从选区移除",
                                                          signal="toggled", checkable=True,
                                                          image=os.path.join(BASE_DIR, "sources/icons/new_selection.ico"))
        cross_with_selection_action = self.create_action("", self.change_selection, tip="与选区交叉",
                                                         signal="toggled", checkable=True,
                                                         image=os.path.join(BASE_DIR, "sources/icons/new_selection.ico"))

        # 加入组
        self.join_group(QActionGroup(self), (new_selection_action, add_to_selection_action,
                                             remove_from_selection_action, cross_with_selection_action))
        new_selection_action.setChecked(True)
        self.add_actions(self.quick_select_toolbar, (new_selection_action, add_to_selection_action,
                                                     remove_from_selection_action, cross_with_selection_action))
        self.quick_select_toolbar.addSeparator()

        # 消除锯齿 checkbox
        anti_aliasing_checkbox = QCheckBox("消除锯齿")
        anti_aliasing_checkbox.setChecked(True)  # 默认选择
        anti_aliasing_checkbox.stateChanged.connect(self.anti_aliasing)
        self.quick_select_toolbar.addWidget(anti_aliasing_checkbox)
        self.quick_select_toolbar.addSeparator()

        # 尺寸样式
        self.size_style = ("正常", "固定大小", "固定比例")
        size_style_label = QLabel("样式: ")
        size_style_combobox = QComboBox()
        size_style_combobox.addItems(self.size_style)
        size_style_combobox.currentIndexChanged.connect(self.set_size_style)
        size_style_label.setBuddy(size_style_combobox)
        self.quick_select_toolbar.addWidget(size_style_label)
        self.quick_select_toolbar.addWidget(size_style_combobox)

        # 设置宽高 根据样式的改变而禁用和启用
        input_width_label = QLabel("宽度: ")
        self.input_width = QLineEdit()
        self.input_width.setMaximumSize(QSize(60, 16777215))
        self.input_width.setMinimumSize(QSize(60, 16777215))
        self.input_width.returnPressed.connect(self.set_selection_size)
        input_width_label.setBuddy(self.input_width)
        self.quick_select_toolbar.addWidget(input_width_label)
        self.quick_select_toolbar.addWidget(self.input_width)

        # 宽高互换
        size_swap = self.create_action("", self.size_swap, tip="宽度和高度互换", signal="triggered",
                                       image=os.path.join(BASE_DIR, "sources/icons/size_swap.ico"))
        self.quick_select_toolbar.addAction(size_swap)

        input_height_label = QLabel("高度: ")
        self.input_height = QLineEdit()
        self.input_height.setMaximumSize(QSize(60, 16777215))
        self.input_height.setMinimumSize(QSize(60, 16777215))
        self.input_height.returnPressed.connect(self.set_selection_size)
        input_height_label.setBuddy(self.input_height)
        self.quick_select_toolbar.addWidget(input_height_label)
        self.quick_select_toolbar.addWidget(self.input_height)
        self.quick_select_toolbar.addSeparator()

        # 调整边缘
        adjust_edge_action = self.create_action(r"调整边缘...", self.adjust_edge)
        self.quick_select_toolbar.addAction(adjust_edge_action)

    # 创建停靠窗口
    def _create_gadget_dock_widget(self):

        def select_quick_select_tool(selected):
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

        def select_grip_tool(selected):
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

        self.verticalLayout = QVBoxLayout(self.gadget_dock_content_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

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
        self.gadget_dock_content_widget.setStyleSheet(gadget_dock_widget_stylesheet)

        quick_select_context_menu = (
            ("矩形选框工具", RECT_QUICK_SELECT_TOOL),
            ("椭圆选框工具", ELLIPSE_QUICK_SELECT_TOOL)
        )
        grip_context_menu = (
            ("抓手工具(H)", GRIP_TONGS),
            ("视图旋转工具(H)", GRIP_ROTATE)
        )

        move_tool_action = self.create_context_button(slot=self.change_selection, tip="移动工具(V)",
                                                      parent=self.gadget_dock_content_widget,
                                                      image=os.path.join(BASE_DIR, "sources/icons/move_select.ico"))
        self.quick_select_action = self.create_context_button(context_menu=quick_select_context_menu,
                                                              context_slot=select_quick_select_tool,
                                                              slot=self.change_gadget, tip="椭圆选择框(M)",
                                                              parent=self.gadget_dock_content_widget,
                                                              image=os.path.join(BASE_DIR,
                                                                                 "sources/icons/quick_select_oval.ico"))
        self.grip_action = self.create_context_button(context_menu=grip_context_menu,
                                                      context_slot=select_grip_tool,
                                                      slot=self.tongs, tip="抓手工具(H)",
                                                      parent=self.gadget_dock_content_widget,
                                                      image=os.path.join(BASE_DIR, "sources/icons/cursor_hand.ico"))
        zoom_action = self.create_context_button(slot=self.zoom, tip="缩放工具(Z)",
                                                 parent=self.gadget_dock_content_widget,
                                                 image=os.path.join(BASE_DIR, "sources/icons/zoom.ico"))

        self.join_group(QButtonGroup(self), (move_tool_action, self.quick_select_action, self.grip_action, zoom_action))

        zoom_action.setChecked(True)
        self.verticalLayout.addWidget(move_tool_action, alignment=Qt.AlignLeft)
        self.verticalLayout.addWidget(self.quick_select_action, alignment=Qt.AlignLeft)
        self.verticalLayout.addWidget(self.grip_action, alignment=Qt.AlignLeft)
        self.verticalLayout.addWidget(zoom_action, alignment=Qt.AlignLeft)
        spacer_item1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item1)

    def _create_color_dock_widget(self):

        def create_rgb_color_item(label_text):
            # 创建验证器 对输入进行预防验证
            validator = QRegExpValidator(QRegExp(r"25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9]"), self)

            color_slider = self.create_slider(slot=self.color_setting)
            color_label = QLabel(label_text, self.color_dock_content_widget)
            color_label.setBuddy(color_slider)
            color_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

            color_input = QLineEdit(self.color_dock_content_widget)
            color_input.setMaxLength(3)
            color_input.setValidator(validator)
            color_input.setFixedWidth(50)
            color_input.setText("0")
            return color_label, color_slider, color_input

        color_dock_widget_stylesheet = """
        QLineEdit { margin-right: 10px ;}
        """
        self.color_dock_content_widget.setStyleSheet(color_dock_widget_stylesheet)

        r_color_label, r_color_slider, r_color_input = create_rgb_color_item("R")
        g_color_label, g_color_slider, g_color_input = create_rgb_color_item("G")
        b_color_label, b_color_slider, b_color_input = create_rgb_color_item("B")

        self.color_dock_grid_layout = QGridLayout(self.color_dock_content_widget)
        self.color_dock_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.color_dock_grid_layout.setObjectName("color_dock_grid_layout")

        self.color_dock_grid_layout.addWidget(r_color_label, 0, 0)
        self.color_dock_grid_layout.addWidget(r_color_slider, 0, 1)
        self.color_dock_grid_layout.addWidget(r_color_input, 0, 2)

        self.color_dock_grid_layout.addWidget(g_color_label, 1, 0)
        self.color_dock_grid_layout.addWidget(g_color_slider, 1, 1)
        self.color_dock_grid_layout.addWidget(g_color_input, 1, 2)

        self.color_dock_grid_layout.addWidget(b_color_label, 2, 0)
        self.color_dock_grid_layout.addWidget(b_color_slider, 2, 1)
        self.color_dock_grid_layout.addWidget(b_color_input, 2, 2)

        spacer_item1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.color_dock_grid_layout.addItem(spacer_item1, 3, 0, 1, 1)

    def _create_layer_dock_widget(self):
        self.layer_dock_content_widget.setMinimumSize(150, 180)
        self.layer_dock_vertical_layout = QVBoxLayout(self.layer_dock_content_widget)

        self.layer_scroll_area = QScrollArea()
        self.layer_scroll_area.setObjectName("layer_scroll_area")
        self.layer_scroll_area.setWidgetResizable(True)
        self.layer_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.layer_scroll_area_content = QWidget()
        self.layer_scroll_area_content.setMinimumSize(150, 180)
        self.layer_scroll_area_content.setObjectName("layer_scroll_area_content")

        self.layer_scroll_area.setWidget(self.layer_scroll_area_content)
        self.layer_dock_vertical_layout.addWidget(self.layer_scroll_area)

    def create_dock_widget(self, widget_title, dock_widget_name, dock_widget_content_name):
        new_dock_widget = QDockWidget(widget_title, self)
        new_dock_widget.setObjectName(dock_widget_name)
        dock_widget_content = QWidget()
        dock_widget_content.setObjectName(dock_widget_content_name)
        return new_dock_widget, dock_widget_content

    # 创建动作
    def create_action(self, text, slot=None, shortcut=None, tip=None, icon=None,
                      checkable=False, signal="triggered", image=None):
        new_action = QAction(text, self)

        if icon:
            new_action.setIcon(QIcon(icon))
        if shortcut:
            new_action.setShortcut(shortcut)
        if tip:
            new_action.setToolTip(tip)
            new_action.setStatusTip(tip)
        if slot and callable(slot):
            if signal == "triggered":
                new_action.triggered.connect(slot)
            elif signal == "toggled":
                new_action.toggled.connect(slot)
        if checkable:
            new_action.setCheckable(True)
        if image:
            new_action.setIcon(QIcon(image))
        return new_action

    @staticmethod
    def create_context_button(context_menu=None, context_slot=None, slot=None, checkable=True,
                              image=None, tip=None, signal="toggled", parent=None):
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

    def create_slider(self, minimum=0, maximum=255, step=1,
                      tick_position=QSlider.TicksAbove, slot=None):

        new_slider = QSlider(Qt.Horizontal, self.color_dock_content_widget)
        new_slider.setRange(minimum, maximum)
        new_slider.setSingleStep(step)
        new_slider.setFixedWidth(110)
        new_slider.setTickPosition(tick_position)
        new_slider.setStyleSheet("QSlider::groove:horizontal {\n"
"        height: 6px;\n"
"        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 rgb(255, 255, 255), stop: 1.0 rgb(0, 0, 0));\n"
"}\n"
"QSlider::handle:horizontal {\n"
"        width: 8px;\n"
"        background: rgb(0, 160, 230);\n"
"        margin: -6px 0px -6px 0px;\n"
"        border-radius: 9px;\n"
"}")
        if slot and callable(slot):
            new_slider.valueChanged.connect(slot)
        return new_slider

    @staticmethod
    def add_menu(text, target, object_name=None, tip=None, slot=None, signal=None):
        new_menu = target.addMenu(text)
        if object_name:
            new_menu.setObjectName(object_name)
        if tip:
            new_menu.setToolTip(tip)
        if slot and signal:
            if signal == "aboutToShow":
                # 这里还要判断 slot是否可调用
                new_menu.aboutToShow.connect(slot)
        return new_menu

    @staticmethod
    def add_actions(target, actions):
        for action in actions:
            if action:
                target.addAction(action)
            else:
                target.addSeparator()

    @staticmethod
    def set_widgets(target, widgets):
        for widget in widgets:
            target.setWidget(widget)

    @staticmethod
    def join_group(target, actions):
        for action in actions:
            if action and isinstance(action, QAction):
                target.addAction(action)
            elif action and isinstance(action, QAbstractButton):
                target.addButton(action)

    def update_file_menu(self):
        self.file_menu.clear()
        self.file_menu.addAction(self.file_menu_actions[0])
        recent_files_menu = self.file_menu.addMenu("打开最近的文件(T)...")

        if self.recent_files:
            for i, file_name in enumerate(self.recent_files):
                dir_file_name = file_name.split("/")[-1]
                action = self.create_action(str(i + 1) + " " + dir_file_name, slot=self._open_file_from_recent)
                action.setData(QVariant(file_name))
                recent_files_menu.addAction(action)
            recent_files_menu.addSeparator()
        remove_action = self.create_action("清空最近打开的文件列表", slot=self.remove_recent_files)
        recent_files_menu.addAction(remove_action)

        self.add_actions(self.file_menu, self.file_menu_actions[1:])

    def open_file(self, file_name=None):
        if file_name is None or isinstance(file_name, bool):
            dir_ = os.path.dirname(self.recent_files[0]) if self.recent_files else os.path.dirname(".")
            # 打开一个 文件选择对口框
            file_name = QFileDialog.getOpenFileName(self, "选择遥感图片", dir_, "Image files (*.png *.jpg *.ico)")[0]

        if file_name:
            file_names = []
            for index in range(self.center_tab_widget.count()):
                file_names.append(self.center_tab_widget.widget(index).get_file_name())

            if file_name not in file_names:
                message = self.create_new_tab(file_name)
            else:
                message = "文件 %s 已经打开" % file_name
                self.center_tab_widget.setCurrentIndex(file_names.index(file_name))
            self.statusBar().showMessage(message, 5000)

    def _open_file_from_recent(self):
        sender = self.sender()
        if isinstance(sender, QAction):
            file_name = sender.data()
            self.open_file(file_name)

    def create_new_tab(self, file_name):
        try:
            new_tab = WorkbenchWidget(file_name=file_name)
            tab_text = file_name.split("/")[-1]
            self.center_tab_widget.addTab(new_tab, tab_text)
            self.center_tab_widget.setCurrentWidget(new_tab)
            self.center_tab_widget.setTabToolTip(self.center_tab_widget.currentIndex(), file_name)
            self.update_close_button_enabled()
            self.add_recent_file(file_name)
            return "打开文件\"" + file_name + "\"成功"
        except FileOpenFailException as e:
            return e.message
        finally:
            return " "

    def add_recent_file(self, file_name):
        if file_name:
            if file_name in self.recent_files:
                self.recent_files.remove(file_name)
            self.recent_files.insert(0, file_name)
            while len(self.recent_files) > 10:
                self.recent_files.pop()

    def remove_recent_files(self):
        if self.recent_files:
            self.recent_files.clear()

    def close_file(self, index=None):
        if index is not None and isinstance(index, int):
            tab_widget = self.center_tab_widget.widget(index)
            if tab_widget.is_dirty():
                if not self.is_save_question(tab_widget.get_file_name()):
                    return False
            self.center_tab_widget.removeTab(index)
            del tab_widget

        if index and isinstance(index, bool) and self.center_tab_widget.count() != 0:
            current_index = self.center_tab_widget.currentIndex()
            current_widget = self.center_tab_widget.currentWidget()
            if current_widget.is_dirty():
                if self.is_save_question(current_index):
                    self.center_tab_widget.removeTab(current_index)
                    del current_widget
        self.update_close_button_enabled()
        return True

    def update_close_button_enabled(self):
        is_tab_empty = self.center_tab_widget.count() != 0
        self.file_menu_actions[2].setEnabled(is_tab_empty)
        self.file_menu_actions[3].setEnabled(is_tab_empty)

    def close_all_file(self):
        self.ok_to_continue()

    def save_file(self, index=None, file_name=None):
        pass

    def save_file_as(self):
        pass

    def import_file(self):
        pass

    def export_file(self):
        pass

    def quit(self):
        self.close()

    def edit_step(self):
        pass

    def edit_reference(self):
        pass

    def graph_mode(self):
        pass

    def graph_adjust(self):
        pass

    def graph_resize(self):
        pass

    def graph_rotate(self):
        pass

    def new_layer(self):
        pass

    def switch_select_tool(self):
        pass

    def outline_detect(self):
        pass

    def result_test(self):
        pass

    def help(self):
        pass

    def change_selection(self):
        pass

    def anti_aliasing(self, state):
        pass

    def set_size_style(self):
        pass

    def set_selection_size(self):
        pass

    def adjust_edge(self):
        pass

    def size_swap(self):
        pass

    def change_gadget(self):
        pass

    def color_setting(self):
        pass

    def zoom(self):
        pass

    def tongs(self):
        pass


RECT_QUICK_SELECT_TOOL = 1
ELLIPSE_QUICK_SELECT_TOOL = 2

GRIP_TONGS = 3
GRIP_ROTATE = 4


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("LRSM Ltd.")
    app.setOrganizationDomain("lrsm.eu")
    app.setApplicationName("LRSMSingleVersion")
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()







