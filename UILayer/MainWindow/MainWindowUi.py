import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from LRSMSingleVersion.Application.App import BASE_DIR
from LRSMSingleVersion.UILayer.CommonHelper.CommonHelper import *
from LRSMSingleVersion.UILayer.CustomWidget.GadgetDockWidget import GadgetDockWidget
from LRSMSingleVersion.UILayer.CustomWidget.ProjectTreeDockWidget import ProjectDockWidget

__version__ = "1.0.0"


class MainWindowUI(object):

    def _init_ui(self, main_window: QMainWindow):

        # 窗体的中心 使用 QTabWidget # 中心部件
        self.center_tab_widget = QTabWidget(main_window)
        self.center_tab_widget.setMovable(True)
        self.center_tab_widget.setTabsClosable(True)
        # self.center_tab_widget.tabCloseRequested.connect(self.close_file)

        self.center_tab_widget.setContextMenuPolicy(Qt.ActionsContextMenu)
        main_window.setCentralWidget(self.center_tab_widget)  # 设置此label为窗口的

        # 设置MenuBar
        self.menubar = main_window.menuBar()
        self._init_menubar(main_window)
        # # 设置ToolBar
        self._init_toolbar(main_window)

        # 创建 main window的停靠窗口
        dock_widget_limit = Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea
        self.gadget_dock_widget = GadgetDockWidget(parent=self)
        self.gadget_dock_widget.setMaximumSize(36, 1026)
        main_window.addDockWidget(Qt.LeftDockWidgetArea, self.gadget_dock_widget)

        # 创建项目目录树 停靠窗口
        self.project_dock_widget = ProjectDockWidget(parent=self)
        self.project_dock_widget.setAllowedAreas(dock_widget_limit)
        main_window.addDockWidget(Qt.RightDockWidgetArea, self.project_dock_widget)

        # 状态栏相关
        self.size_label = QLabel()
        self.size_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        status = main_window.statusBar()
        # 关闭状态栏的尺寸大小拖拽符
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.size_label)
        status.showMessage("Ready", 5000)  # 消息显示5秒

        # self.screenRect = QApplication.desktop().screenGeometry()
        main_window.setWindowTitle("遥感地图地物类型标注")
        self._set_style_property()

    def _init_menubar(self, main_window: QMainWindow):

        # 创建一级菜单
        self.file_menu = add_menu("文件(F)", self.menubar, "file_menu")
        self.edit_menu = add_menu("编辑(E)", self.menubar, "edit_menu")
        self.project_menu = add_menu("项目(P)", self.menubar, "project_menu")
        self.graph_menu = add_menu("图像(I)", self.menubar, "graph_menu")
        self.mark_menu = add_menu("标注(M)", self.menubar, "mark_menu")
        self.count_menu = add_menu("计算(C)", self.menubar, "count_menu")
        self.cmp_menu = add_menu("对比(D)", self.menubar, "cmp_menu")
        self.help_menu = add_menu("帮助(H)", self.menubar, "help_menu")

        # 创建文件菜单的二级菜单/动作
        # 由于要显示最近打开的文件 我们要动态的显示这个菜单
        self.new_project_action = create_action(main_window, "新建项目(N)...", "Ctrl+N")
        self.open_project_action = create_action(main_window, "打开项目(O)...", "Ctrl+O")
        self.open_original_image_action = create_action(main_window, "打开原始图片...", "Shift+Ctrl+O")

        self.save_project_action = create_action(main_window, "保存项目(S)", "Ctrl+S")
        self.save_project_as_action = create_action(main_window, "另存为...", "Shift+Ctrl+S")
        self.save_all_action = create_action(main_window, "保存全部", "Shift+Ctrl+A")

        self.close_project_action = create_action(main_window, "关闭项目", "Ctrl+P")
        self.close_action = create_action(main_window, "关闭(C)", "Ctrl+W")
        self.close_all_action = create_action(main_window, "全部关闭", "Alt+Ctrl+W")

        self.import_action = create_action(main_window, "导入(M)...")
        self.export_action = create_action(main_window, "导出(E)...")
        self.project_info_action = create_action(main_window, "项目简介(F)...")
        self.quit_action = create_action(main_window, "退出(Q)",  "Ctrl+Q")

        self.close_action.setEnabled(False)
        self.close_all_action.setEnabled(False)
        self.close_project_action.setEnabled(False)
        # 先这些动作组织保存起来 等文件菜单aboutToShow时用
        self.file_menu_actions = [
            self.new_project_action, self.open_project_action, self.open_original_image_action, None,
            self.close_project_action, self.close_action, self.close_all_action, None,
            self.save_project_action, self.save_project_as_action, self.save_all_action, None,
            self.import_action, self.export_action, None, self.project_info_action, None, self.quit_action
        ]

        # 创建编辑菜单的二级菜单/动作
        self.revert_action = create_action(main_window, "还原(O)", "Ctrl+Z")
        self.undo_action = create_action(main_window, "后退一步(K)", "Alt+Ctrl+Z")
        self.redo_action = create_action(main_window, "前进一步(W)",  "Alt+Ctrl+Z")
        self.reference_action = create_action(main_window, "首选项(N)...")
        # 创建 编辑菜单 的二级菜单 查找并替换 的二级菜单
        self.find_replace_menu = self.edit_menu.addMenu("查找和替换(F)")
        self.quick_find_action = create_action(main_window, "快速查找(F)", shortcut="Ctrl+F")
        self.quick_replace_action = create_action(main_window, "快速替换(R)", shortcut="Ctrl+H")
        self.quick_find_in_file_action = create_action(main_window, "在文件中查找(I)", shortcut="Shift+Ctrl+F")
        self.quick_replace_in_file_action = create_action(main_window, "在文件中替换(S)", shortcut="Shift+Ctrl+H")
        add_actions(self.find_replace_menu, (self.quick_find_action, self.quick_replace_action,
                                             self.quick_find_in_file_action, self.quick_replace_in_file_action))
        # 将这些动作加入到 编辑菜单中
        add_actions(self.edit_menu, (None, self.revert_action, self.redo_action,
                                     self.undo_action, None, self.reference_action))

        # 创建 项目 菜单的二级菜单
        self.new_mark_action = create_action(main_window, "添加标注文件(N)", shortcut="Shift+Ctrl+N")
        self.new_mark_from_action = create_action(main_window, "添加现有标注文件", shortcut="Alt+Ctrl+N")
        add_actions(self.project_menu, (self.new_mark_action, self.new_mark_from_action))

        # 创建图像菜单的二级菜单/动作
        self.mode_menu = self.graph_menu.addMenu("模式(M)")
        self.graph_menu.addSeparator()
        self.adjust_menu = self.graph_menu.addMenu("调整(J)")
        self.graph_menu.addSeparator()
        self.size_action = create_action(main_window, "图像大小(I)...", "Ctrl+Alt+I")
        self.graph_menu.addAction(self.size_action)
        self.rotate_menu = self.graph_menu.addMenu("图像旋转(G)")

        # 创建图像菜单的二级菜单 模式 的二级动作
        self.bmp_action = create_action(main_window, "位图(B)", checkable=True)
        self.gray_action = create_action(main_window, "灰度(G)", checkable=True)
        self.rgb_action = create_action(main_window, "位图(B)", checkable=True)
        # 将这三个动作作为一个动作组
        join_group(QActionGroup(main_window), (self.bmp_action, self.gray_action, self.rgb_action))
        self.rgb_action.setChecked(True)  # 默认是rbg模式
        add_actions(self.mode_menu, (self.bmp_action, self.gray_action, self.rgb_action))

        # 创建 图像菜单 的二级菜单 调整 的二级动作
        self.bright_action = create_action(main_window, "亮度/对比度(C)...")
        self.adjust_menu.addAction(self.bright_action)

        # 创建 图像菜单 的二级菜单 图像旋转 的二级动作
        self.rotate_180_action = create_action(main_window, "180度(1)")
        self.rotate_clockwise90_action = create_action(main_window, "90度(顺时针)(9)")
        self.rotate_counterclockwise90_action = create_action(main_window, "90度(逆时针)(9)")
        self.rotate_any_action = create_action(main_window, "任意角度(A)...")
        add_actions(self.rotate_menu, (self.rotate_180_action, self.rotate_clockwise90_action,
                                       self.rotate_counterclockwise90_action, self.rotate_any_action))

        # 创建 标注 菜单的二级菜单/动作
        self.quick_select_menu = add_menu("选择工具", self.mark_menu, "quick_select_menu")
        self.mark_menu.addSeparator()
        self.outline_detect_menu = add_menu("轮廓检测(D)", self.mark_menu, "outline_detect_menu")

        # 创建 标注菜单 的二级菜单 快速选择工具 的二级动作
        self.rectangle_action = create_action(main_window, "矩形选择框", checkable=True)
        self.oval_action = create_action(main_window, "椭圆选择框", checkable=True)
        join_group(QActionGroup(main_window), (self.rectangle_action, self.oval_action))
        add_actions(self.quick_select_menu, (self.rectangle_action, self.oval_action))

        # 创建 标注菜单 的二级菜单 轮廓检测 的二级动作
        self.origin_outline_action = create_action(main_window, "原始轮廓(O)", "Ctrl+A+O", checkable=True)
        self.convex_outline_action = create_action(main_window, "凸性缺陷轮廓(C)", "Ctrl+A+C", checkable=True)
        self.polygon_outline_action = create_action(main_window, "多边形轮廓(P)", "Ctrl+A+P",  checkable=True)
        outline_actions = (self.origin_outline_action, self.convex_outline_action, self.polygon_outline_action)
        join_group(QActionGroup(main_window), outline_actions)
        add_actions(self.outline_detect_menu, outline_actions)

        # 创建 计算 菜单的二级菜单/动作
        self.erosion_area_action = create_action(main_window, "总面积(E)...")
        self.girth_area_action = create_action(main_window, "总周长(C)...")
        add_actions(self.count_menu, (self.erosion_area_action, self.girth_area_action))
        self.connected_graph_menu = add_menu("连通图", self.count_menu, "connected_graph_menu")
        self.connected_graph_menu.setEnabled(False)

        # 创建 计算 菜单的二级菜单/动作
        self.cmp_history_action = create_action(main_window, "历史图片对比...")
        self.cmp_menu.addAction(self.cmp_history_action)

        # 创建 帮助 菜单的二级菜单/动作
        self.help_about_action = create_action(main_window, "关于(A)...")
        self.help_help_action = create_action(main_window, "帮助(H)...")
        add_actions(self.help_menu, (self.help_about_action, self.help_help_action))

    # 创建工具栏
    def _init_toolbar(self, main_window: QMainWindow):
        # 添加 快速选择 的工具栏
        self.quick_select_toolbar = main_window.addToolBar("quick_select")
        quick_select_toolbar_stylesheet = """
        QCheckBox { margin: 0 10px; }
        QLabel { margin-left: 8px; }
        QLineEdit { margin-right: 7px; }
        """
        self.quick_select_toolbar.setStyleSheet(quick_select_toolbar_stylesheet)

        # 选区操作
        self.new_selection_action = create_action(
            main_window, "", tip="新建选区",  checkable=True,
            image=os.path.join(BASE_DIR, "sources/icons/new_selection.ico"))
        self.add_to_selection_action = create_action(
            main_window, "", tip="添加到选区", checkable=True,
            image=os.path.join(BASE_DIR, "sources/icons/new_selection.ico"))
        self.remove_from_selection_action = create_action(
            main_window, "", tip="从选区移除", checkable=True,
            image=os.path.join(BASE_DIR, "sources/icons/new_selection.ico"))
        self.cross_with_selection_action = create_action(
            main_window, "", tip="与选区交叉",  checkable=True,
            image=os.path.join(BASE_DIR, "sources/icons/new_selection.ico"))
        selection_actions = (self.new_selection_action,
                             self.add_to_selection_action,
                             self.remove_from_selection_action,
                             self.cross_with_selection_action)
        # 加入组
        join_group(QActionGroup(main_window), selection_actions)
        self.new_selection_action.setChecked(True)
        add_actions(self.quick_select_toolbar, selection_actions)
        self.quick_select_toolbar.addSeparator()

        # 消除锯齿 checkbox
        self.anti_aliasing_checkbox = QCheckBox("消除锯齿")
        self.anti_aliasing_checkbox.setChecked(True)  # 默认选择
        self.quick_select_toolbar.addWidget(self.anti_aliasing_checkbox)
        self.quick_select_toolbar.addSeparator()

        # 尺寸样式
        self.size_style = ("正常", "固定大小", "固定比例")
        size_style_label = QLabel("样式: ")
        self.size_style_combobox = QComboBox()
        self.size_style_combobox.addItems(self.size_style)
        size_style_label.setBuddy(self.size_style_combobox)
        self.quick_select_toolbar.addWidget(size_style_label)
        self.quick_select_toolbar.addWidget(self.size_style_combobox)

        # 设置宽高 根据样式的改变而禁用和启用
        input_width_label = QLabel("宽度: ")
        self.input_width = QLineEdit()
        self.input_width.setMaximumSize(QSize(60, 16777215))
        self.input_width.setMinimumSize(QSize(60, 16777215))
        # self.input_width.returnPressed.connect(self.set_selection_size)
        input_width_label.setBuddy(self.input_width)
        self.quick_select_toolbar.addWidget(input_width_label)
        self.quick_select_toolbar.addWidget(self.input_width)

        # 宽高互换
        self.size_swap = create_action(
            main_window, "", tip="宽度和高度互换",
            image=os.path.join(BASE_DIR, "sources/icons/size_swap.ico"))
        self.quick_select_toolbar.addAction(self.size_swap)

        input_height_label = QLabel("高度: ")
        self.input_height = QLineEdit()
        self.input_height.setMaximumSize(QSize(60, 16777215))
        self.input_height.setMinimumSize(QSize(60, 16777215))
        # self.input_height.returnPressed.connect(self.set_selection_size)
        input_height_label.setBuddy(self.input_height)
        self.quick_select_toolbar.addWidget(input_height_label)
        self.quick_select_toolbar.addWidget(self.input_height)
        self.quick_select_toolbar.addSeparator()

        # 调整边缘
        self.adjust_edge_action = create_action(main_window, r"调整边缘...")
        self.quick_select_toolbar.addAction(self.adjust_edge_action)

    def _set_style_property(self):
        pass









