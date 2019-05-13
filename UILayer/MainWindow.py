import os
import platform
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from LRSMSingleVersion.Application.App import BASE_DIR

__version__ = "1.0.0"


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # self.image = QImage()
        # 是否存在未保存的修改
        self.dirty = False
        # 没有图片还是有尚未保存的新创建的图片
        self.file_name = None
        # 图片的垂直镜像
        self.mirrored_vertically = False
        # 水平镜像
        self.mirrored_horizontally = False

        # 窗体的中心 使用 QTabWidget
        self.center_tab_widget = QTabWidget(self)
        # 设置 水平和垂直居中
        # self.image_label.setAlignment(Qt.AlignCenter)
        # 设置其上下文菜单策略
        # self.image_label.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.center_tab_widget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.center_tab_widget)   # 设置此label为窗口的
        # 中心部件

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

        self.size_label = QLabel()
        self.size_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        status = self.statusBar()
        # 关闭状态栏的尺寸大小拖拽符
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.size_label)
        status.showMessage("Ready", 5000)  # 消息显示5秒

        self.tab_id = 0
        self.screenRect = QApplication.desktop().screenGeometry()
        self.setWindowTitle("遥感地图地物类型标注")
        self.move(0, 0)
        self.resize(self.screenRect.width(), self.screenRect.height())

    # 创建菜单栏
    def _init_menubar(self):

        # 创建一级菜单
        self.file_menu = self.add_menu("文件(F)", self.menubar, "file_menu", slot=self.update_file, signal="aboutToShow")
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
        # 先这些动作组织保存起来 等文件菜单aboutToShow时用
        self.file_menu_actions = (open_file_action, None, close_action, close_all_action,
                                  None, save_action, save_as_action, None, import_action,
                                  export_action, None, quit_action)

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
        bmp_action = self.create_action("位图(B)", self.graph_mode, signal="toggled")
        gray_action = self.create_action("灰度(G)", self.graph_mode, signal="toggled")
        rgb_action = self.create_action("位图(B)", self.graph_mode, signal="toggled")
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
        rectangle_action = self.create_action("矩形选择框", self.switch_select_tool, signal="toggled")
        oval_action = self.create_action("椭圆选择框", self.switch_select_tool, signal="toggled")
        self.join_group(QActionGroup(self), (rectangle_action, oval_action))
        self.add_actions(self.quick_select_menu, (rectangle_action, oval_action))

        # 创建 标注菜单 的二级菜单 轮廓检测 的二级动作
        origin_outline_action = self.create_action("原始轮廓(O)", self.outline_detect, "Ctrl+A+O", signal="toggled")
        convex_outline_action = self.create_action("凸性缺陷轮廓(C)", self.outline_detect, "Ctrl+A+C", signal="toggled")
        polygon_outline_action = self.create_action("多边形轮廓(P)", self.outline_detect, "Ctrl+A+P", signal="toggled")
        self.join_group(QActionGroup(self), (origin_outline_action, convex_outline_action, polygon_outline_action))
        self.add_actions(self.outline_detect_menu, (origin_outline_action, convex_outline_action, polygon_outline_action))

        # 创建 实验 菜单的二级菜单/动作
        erosion_area_action = self.create_action("侵蚀面积(E)...", self.result_test)
        contrast_action = self.create_action("图像对比图(C)...", self.result_test)
        self.add_actions(self.test_menu, (erosion_area_action, contrast_action))

        # 创建 帮助 菜单的二级菜单/动作
        help_about_action = self.create_action("关于(A)...", self.help)
        help_help_action = self.create_action("帮助(H)...", self.help)
        self.add_actions(self.help_menu, (help_about_action, help_help_action))

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
        new_selection_action = self.create_action("", self.change_selection, tip="新建选区", signal="toggled",
                                                  image=os.path.join(BASE_DIR, "sources/icons/new_selection.ico"))
        add_to_selection_action = self.create_action("", self.change_selection, tip="添加到选区", signal="toggled",
                                                     image=os.path.join(BASE_DIR, "sources/icons/new_selection.ico"))
        remove_from_selection_action = self.create_action("", self.change_selection, tip="从选区移除", signal="toggled",
                                                    image=os.path.join(BASE_DIR, "sources/icons/new_selection.ico"))
        cross_with_selection_action = self.create_action("", self.change_selection, tip="与选区交叉", signal="toggled",
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
        anti_aliasing_checkbox.setChecked(True)   # 默认选择
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

    def _create_gadget_dock_widget(self):
        self.verticalLayout = QVBoxLayout(self.gadget_dock_content_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        gadget_dock_widget_stylesheet = """
        QPushButton { 
            border: 0;
            padding: 0 8px;
        }
        """
        self.gadget_dock_content_widget.setStyleSheet(gadget_dock_widget_stylesheet)

        move_tool_action = self.create_action("", self.change_gadget, tip="移动工具(V)", signal="toggled",
                                              type_="Button", parent=self.gadget_dock_content_widget,
                                              image=os.path.join(BASE_DIR, "sources/icons/move_select.ico"))
        self.quick_select_action = self.create_action("", self.change_gadget, tip="快速选择工具(M)", signal="toggled",
                                                      type_="Button", parent=self.gadget_dock_content_widget,
                                                      image=os.path.join(BASE_DIR, "sources/icons/quick_select_oval.ico"))
        self.grip_action = self.create_action("", self.change_gadget, tip="抓手工具(H)", signal="toggled",
                                              type_="Button", parent=self.gadget_dock_content_widget,
                                              image=os.path.join(BASE_DIR, "sources/icons/cursor_hand.ico"))
        zoom_action = self.create_action("", self.change_gadget, tip="缩放工具(Z)", signal="toggled",
                                         type_="Button",   # parent=self.gadget_dock_content_widget,
                                         image=os.path.join(BASE_DIR, "sources/icons/zoom.ico"))

        self.join_group(QButtonGroup(self), (move_tool_action, self.quick_select_action, self.grip_action, zoom_action))

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
    def create_action(self, text, slot=None, shortcut=None, tip=None, type_="QAction",
                      icon=None, checkable=False, signal="triggered", image=None, parent=None):
        if type_ == "QAction":
            new_action = QAction(text, self)
        else:
            new_action = QPushButton(text, parent)

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

    def create_slider(self, minimum=0, maximum=255, step=1, tick_position=QSlider.TicksAbove, slot=None):
        new_slider = QSlider(Qt.Horizontal, self.color_dock_content_widget)
        new_slider.setRange(minimum, maximum)
        new_slider.setSingleStep(step)
        new_slider.setFixedWidth(110)
        new_slider.setTickPosition(tick_position)
        if slot and callable(slot):
            new_slider.valueChanged.connect(slot)
        return new_slider

    @staticmethod
    def add_menu(text, target, object_name=None, tip=None, slot=None, signal=None):
        # new_menu = QMenu(text, target)
        # if isinstance(target, QMenuBar):
        #     new_menu = target.addMenu(text)
        # else:
        #     new_menu = QMenu(text, target)
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

    def update_file(self):
        self.add_actions(self.file_menu, self.file_menu_actions)

    def open_file(self):
        if True:
            dir_ = os.path.dirname(self.file_name) if self.file_name else "."

            # file_format = ["*.%s" % format_.lower() for format_ in QImageReader.supportedImageFormats()]
            file_format = "*.png *.jpg *.ico"
            # 打开一个 文件选择对口框
            file_name = QFileDialog.getOpenFileName(self, "选择遥感图片", dir_,
                                                    "Image files (%s)" % " ".join(file_format))[0]
            if file_name:
                self._load_file(file_name)

    def _load_file(self, file_name):
        print(file_name)
        if file_name:
            image = QImage(file_name)
            if image.isNull():
                message = "打开文件 %s 失败" % file_name
            else:
                self.image = QImage()
                self.image = image
                self.file_name = file_name
                self.create_new_tab()
                self.dirty = False
                message = "打开文件 %s 成功" % file_name
        # self.updateStatus(message)

    def create_new_tab(self):
        new_tab = QWidget()
        tab_vertical_layout = QVBoxLayout(new_tab)

        image_label = QLabel("image_label")
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setPixmap(QPixmap.fromImage(self.image))
        tab_vertical_layout.addWidget(image_label)

        tab_text = self.file_name.split("/")[-1]
        self.center_tab_widget.addTab(new_tab, tab_text)

    def clear_open_history(self):
        pass

    def close_file(self):
        pass

    def close_all_file(self):
        pass

    def save_file(self):
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


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()








