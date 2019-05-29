import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from LRSMSingleVersion.Application.App import BASE_DIR

from LRSMSingleVersion.UILayer.CustomWidget.GadgetDockWidget import GadgetDockWidget
from LRSMSingleVersion.UILayer.CustomWidget.ColorDockWidget import ColorDockWidget
from LRSMSingleVersion.UILayer.CustomWidget.LayerDockWidget import LayerDockWidget
from LRSMSingleVersion.UILayer.Workbench.WorkbenchWidget import WorkbenchWidget, FileOpenFailException
from LRSMSingleVersion.UILayer.CustomWidget.ProjectTreeDockWidget import ProjectDockWidget
from LRSMSingleVersion.UILayer.CustomWidget.NewProjectDialog import NewProjectDialog

__version__ = "1.0.0"


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.current_gadget = None
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
        self.gadget_dock_widget = GadgetDockWidget(parent=self)
        self.gadget_dock_widget.setMaximumSize(36, 1026)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.gadget_dock_widget)

        # # 创建颜色设置的停靠窗口
        # self.color_dock_widget = ColorDockWidget(parent=self)
        # self.color_dock_widget.setAllowedAreas(dock_widget_limit)
        # self.color_dock_widget.setFixedSize(200, 140)
        # self.addDockWidget(Qt.RightDockWidgetArea, self.color_dock_widget)
        #
        # # 创建图层停靠窗口
        # self.layer_dock_widget = LayerDockWidget(parent=self)
        # self.layer_dock_widget.setAllowedAreas(dock_widget_limit)
        # self.addDockWidget(Qt.RightDockWidgetArea, self.layer_dock_widget)

        # 创建项目目录树 停靠窗口
        project_info = {
            "project_name": "testProject",
            "org_img_name": "北京市"
        }
        self.project_dock_widget = ProjectDockWidget(parent=self)
        # self.project_dock_widget.create_project(project_info)
        self.project_dock_widget.setAllowedAreas(dock_widget_limit)
        self.addDockWidget(Qt.RightDockWidgetArea, self.project_dock_widget)

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
        # self.update_file_menu()
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
        self.project_menu = self.add_menu("项目(P)", self.menubar, "project_menu")
        self.graph_menu = self.add_menu("图像(I)", self.menubar, "graph_menu")
        self.mark_menu = self.add_menu("标注(M)", self.menubar, "mark_menu")
        self.test_menu = self.add_menu("实验(T)", self.menubar, "test_menu")
        self.help_menu = self.add_menu("帮助(H)", self.menubar, "help_menu")

        # 创建文件菜单的二级菜单/动作
        # 由于要显示最近打开的文件 我们要动态的显示这个菜单
        new_project_action = self.create_action("新建项目(N)...", self.create_new_project, "Ctrl+N")
        open_project_action = self.create_action("打开项目(O)...", self.open_project, "Ctrl+O")
        open_original_image_action = self.create_action("打开原始图片...", self.open_file, "Shift+Ctrl+O")

        save_project_action = self.create_action("保存项目(S)", self.save_file, "Ctrl+S")
        save_project_as_action = self.create_action("另存为...", self.save_file_as, "Shift+Ctrl+S")
        save_all_action = self.create_action("保存全部", self.save_all, "Shift+Ctrl+A")

        close_project_action = self.create_action("关闭项目", self.close_project, "Ctrl+P")
        close_action = self.create_action("关闭(C)", self.close_file, "Ctrl+W")
        close_all_action = self.create_action("全部关闭", self.close_all_file, "Alt+Ctrl+W")

        import_action = self.create_action("导入(M)...", self.import_file)
        export_action = self.create_action("导出(E)...", self.export_file)
        project_info_action = self.create_action("项目简介(F)...", self.project_info)
        quit_action = self.create_action("退出(Q)", self.quit, "Ctrl+Q")

        close_action.setEnabled(False)
        close_all_action.setEnabled(False)
        close_project_action.setEnabled(False)
        # 先这些动作组织保存起来 等文件菜单aboutToShow时用
        self.file_menu_actions = [new_project_action, open_project_action, open_original_image_action,
                                  None, close_project_action, close_action, close_all_action,
                                  None, save_project_action, save_project_as_action, save_all_action,
                                  None, import_action, export_action, None, project_info_action,None, quit_action]

        # 创建编辑菜单的二级菜单/动作
        revert_action = self.create_action("还原(O)", self.edit_step, "Ctrl+Z")
        undo_action = self.create_action("后退一步(K)", self.edit_step, "Alt+Ctrl+Z")
        redo_action = self.create_action("前进一步(W)", self.edit_step, "Alt+Ctrl+Z")
        reference_action = self.create_action("首选项(N)...", self.edit_reference)
        # 创建 编辑菜单 的二级菜单 查找并替换 的二级菜单
        self.find_replace_menu = self.edit_menu.addMenu("查找和替换(F)")
        quick_find_action = self.create_action("快速查找(F)", shortcut="Ctrl+F")
        quick_replace_action = self.create_action("快速替换(R)", shortcut="Ctrl+H")
        quick_find_in_file_action = self.create_action("在文件中查找(I)", shortcut="Shift+Ctrl+F")
        quick_replace_in_file_action = self.create_action("在文件中替换(S)", shortcut="Shift+Ctrl+H")
        self.add_actions(self.find_replace_menu, (quick_find_action, quick_replace_action,
                                                  quick_find_in_file_action, quick_replace_in_file_action))
        # 将这些动作加入到 编辑菜单中
        self.add_actions(self.edit_menu, (None, revert_action, redo_action, undo_action, None, reference_action))

        # 创建 项目 菜单的二级菜单
        new_mark_action = self.create_action("添加标注文件(N)", shortcut="Shift+Ctrl+N")
        new_mark_from_action = self.create_action("添加现有标注文件", shortcut="Alt+Ctrl+N")
        self.add_actions(self.project_menu, (new_mark_action, new_mark_from_action))

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
        self.quick_select_menu = self.add_menu("快速选择工具", self.mark_menu, "quick_select_menu")
        self.mark_menu.addSeparator()
        self.outline_detect_menu = self.add_menu("轮廓检测(D)", self.mark_menu, "outline_detect_menu")

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
                target.addButton(action, actions.index(action))

    def update_file_menu(self):
        self.file_menu.clear()
        self.file_menu.addAction(self.file_menu_actions[0])
        self.file_menu.addAction(self.file_menu_actions[1])
        self.file_menu.addAction(self.file_menu_actions[2])
        recent_files_menu = self.file_menu.addMenu("打开最近的文件(T)...")

        if self.recent_files:
            for i, file_name in enumerate(self.recent_files):
                dir_file_name = file_name.split("/")[-1]
                action = self.create_action(str(i + 1) + " " + dir_file_name,
                                            slot=self._open_file_from_recent)
                action.setData(QVariant(file_name))
                recent_files_menu.addAction(action)
            recent_files_menu.addSeparator()
        remove_action = self.create_action("清空最近打开的文件列表", slot=self.remove_recent_files)
        recent_files_menu.addAction(remove_action)

        self.add_actions(self.file_menu, self.file_menu_actions[3:])

    def open_file(self, file_name=None):
        if file_name is None or isinstance(file_name, bool):
            dir_ = os.path.dirname(self.recent_files[0]) if self.recent_files else os.path.dirname(".")
            # 打开一个 文件选择对口框
            file_format = "Image files (*.png *.jpg *.ico *tif)"
            file_name = QFileDialog.getOpenFileName(self, "选择遥感图片", dir_, file_format)[0]

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
            new_tab = WorkbenchWidget(file_name=file_name,
                                      gadget=self.gadget_dock_widget.get_current_gadget())
            tab_text = os.path.basename(file_name)
            self.center_tab_widget.addTab(new_tab, tab_text)
            self.center_tab_widget.setCurrentWidget(new_tab)
            self.center_tab_widget.setTabToolTip(self.center_tab_widget.currentIndex(), file_name)
            self.gadget_dock_widget.gadget_changed.connect(new_tab.change_gadget)
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
            while len(self.recent_files) > 9:
                print(self.recent_files.pop())

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
        self.file_menu_actions[4].setEnabled(is_tab_empty)
        self.file_menu_actions[5].setEnabled(is_tab_empty)
        self.file_menu_actions[6].setEnabled(is_tab_empty)

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

    def create_new_project(self):
        new_project_dialog = NewProjectDialog(parent=self)
        if new_project_dialog.exec_():
            self.setCursor(Qt.BusyCursor)
            project_name, project_dir, image_file = new_project_dialog.new_project_info()

            image_name = os.path.basename(image_file)
            image_dir = os.path.dirname(image_file)
            project_info = {
                "project_name": project_name,
                "org_img_name": image_name
            }

            self.create_new_tab(image_file)
            self.project_dock_widget.create_project(project_info)

            self.setCursor(Qt.ArrowCursor)

    def open_project(self):
        pass

    def close_project(self):
        pass

    def project_info(self):
        pass

    def save_all(self):
        pass


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







