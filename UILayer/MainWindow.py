import os
import platform
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from LRSMSingleVersion.Aplication.App import BASE_DIR

__version__ = "1.0.0"


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.image = QImage()
        # 是否存在未保存的修改
        self.dirty = False
        # 没有图片还是有尚未保存的新创建的图片
        self.file_name = None
        # 图片的垂直镜像
        self.mirrored_vertically = False
        # 水平镜像
        self.mirrored_horizontally = False

        self.image_label = QLabel()
        # 设置最小尺寸 以便在没有图片的时候也占一定的空间
        self.image_label.setMinimumSize(200, 200)
        # 设置 水平和垂直居中
        self.image_label.setAlignment(Qt.AlignCenter)
        # 设置其上下文菜单策略
        self.image_label.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.image_label)   # 设置此label为窗口的中心部件

        # 设置MenuBar
        self.menubar = self.menuBar()
        self.init_menubar()

        # 设置ToolBar
        self.init_toolbar()

        self.size_label = QLabel()
        self.size_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        status = self.statusBar()
        # 关闭状态栏的尺寸大小拖拽符
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.size_label)
        status.showMessage("Ready", 5000)  # 消息显示5秒

        # 工具栏
        # file_toolbar = self.addToolBar("File")
        # file_toolbar.setObjectName("FileToolBar")
        # self.add_actions(file_toolbar, [file_new_action])

        self.setWindowTitle("遥感地图地物类型标注")
        self.resize(640, 480)

    # 创建菜单栏
    def init_menubar(self):

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

    def init_toolbar(self):
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
        adjust_edge_action = self.create_action("调整边缘...", self.adjust_edge)
        self.quick_select_toolbar.addAction(adjust_edge_action)

    # 创建动作
    def create_action(self, text, slot=None, shortcut=None, tip=None,
                      icon=None, checkable=False, signal="triggered", image=None):
        new_action = QAction(text, self)
        if icon:
            # new_action.setIcon(QIcon(":/%s.png" % icon))
            new_action.setIcon(QIcon(icon))
        if shortcut:
            new_action.setShortcut(shortcut)
        if tip:
            new_action.setToolTip(tip)
            new_action.setStatusTip(tip)
        if slot:
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
    def join_group(target, actions):
        for action in actions:
            if action:
                target.addAction(action)

    def update_file(self):
        self.add_actions(self.file_menu, self.file_menu_actions)

    def open_file(self):
        pass

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


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()








