import os
from PyQt5.QtWidgets import *
from LRSMSingleVersion.UILayer.CommonHelper.CommonHelper import *


class Menubar:
    
    def __init__(self, main_window: QMainWindow):
        
        self.menubar = main_window.menuBar()
        self._init_menubar(main_window)
        
    def _init_menubar(self, main_window: QMainWindow):
        # 创建一级菜单
        self.file_menu = main_window.add_menu("文件(F)", self.menubar, "file_menu",
                                              slot=self.update_file_menu, signal="aboutToShow")
        self.edit_menu = main_window.add_menu("编辑(E)", self.menubar, "edit_menu")
        self.graph_menu = main_window.add_menu("图像(I)", self.menubar, "graph_menu")
        self.mark_menu = main_window.add_menu("标注(M)", self.menubar, "mark_menu")
        self.test_menu = main_window.add_menu("实验(T)", self.menubar, "test_menu")
        self.help_menu = main_window.add_menu("帮助(H)", self.menubar, "help_menu")

        # 创建文件菜单的二级菜单/动作
        # 由于要显示最近打开的文件 我们要动态的显示这个菜单
        open_file_action = create_action("打开(O)...", self.open_file, "Ctrl+O")
        close_action = create_action("关闭(C)", self.close_file, "Ctrl+W")
        close_all_action = create_action("全部关闭", self.close_all_file, "Alt+Ctrl+W")
        save_action = create_action("保存(S)", self.save_file, "Ctrl+S")
        save_as_action = create_action("保存(S)", self.save_file_as, "Shift+Ctrl+S")
        import_action = create_action("导入(M)...", self.import_file)
        export_action = create_action("导出(E)...", self.export_file)
        quit_action = create_action("退出(Q)", self.quit, "Ctrl+Q")

        close_action.setEnabled(False)
        close_all_action.setEnabled(False)
        # 先这些动作组织保存起来 等文件菜单aboutToShow时用
        self.file_menu_actions = [open_file_action, None, close_action, close_all_action,
                                  None, save_action, save_as_action, None, import_action,
                                  export_action, None, quit_action]

        # 创建编辑菜单的二级菜单/动作
        revert_action = create_action("还原(O)", self.edit_step, "Ctrl+Z")
        undo_action = create_action("后退一步(K)", self.edit_step, "Alt+Ctrl+Z")
        redo_action = create_action("前进一步(W)", self.edit_step, "Alt+Ctrl+Z")
        reference_action = create_action("首选项(N)...", self.edit_reference)
        # 将这些动作加入到 编辑菜单中
        add_actions(self.edit_menu, (revert_action, redo_action, undo_action, None, reference_action))

        # 创建图像菜单的二级菜单/动作
        self.mode_menu = self.graph_menu.addMenu("模式(M)")
        self.graph_menu.addSeparator()
        self.adjust_menu = self.graph_menu.addMenu("调整(J)")
        self.graph_menu.addSeparator()
        size_action = create_action("图像大小(I)...", self.graph_resize, "Ctrl+Alt+I")
        self.graph_menu.addAction(size_action)
        self.rotate_menu = self.graph_menu.addMenu("图像旋转(G)")

        # 创建图像菜单的二级菜单 模式 的二级动作
        bmp_action = create_action("位图(B)", self.graph_mode, signal="toggled", checkable=True)
        gray_action = create_action("灰度(G)", self.graph_mode, signal="toggled", checkable=True)
        rgb_action = create_action("位图(B)", self.graph_mode, signal="toggled", checkable=True)
        # 将这三个动作作为一个动作组
        join_group(QActionGroup(self), (bmp_action, gray_action, rgb_action))
        rgb_action.setChecked(True)  # 默认是rbg模式
        add_actions(self.mode_menu, (bmp_action, gray_action, rgb_action))

        # 创建 图像菜单 的二级菜单 调整 的二级动作
        bright_action = create_action("亮度/对比度(C)...", self.graph_adjust)
        self.adjust_menu.addAction(bright_action)

        # 创建 图像菜单 的二级菜单 图像旋转 的二级动作
        rotate_180_action = create_action("180度(1)", self.graph_rotate)
        rotate_clockwise90_action = create_action("90度(顺时针)(9)", self.graph_rotate)
        rotate_counterclockwise90_action = create_action("90度(逆时针)(9)", self.graph_rotate)
        rotate_any_action = create_action("任意角度(A)...", self.graph_rotate)
        add_actions(self.rotate_menu, (rotate_180_action, rotate_clockwise90_action,
                                            rotate_counterclockwise90_action, rotate_any_action))

        # 创建 标注 菜单的二级菜单/动作
        self.layer_menu = main_window.add_menu("图层(L)", self.mark_menu, "layer_menu")
        self.mark_menu.addSeparator()
        self.quick_select_menu = main_window.add_menu("快速选择工具", self.mark_menu, "quick_select_menu")
        self.mark_menu.addSeparator()
        self.outline_detect_menu = main_window.add_menu("轮廓检测(D)", self.mark_menu, "outline_detect_menu")

        # 创建 标注菜单 的二级菜单 图层 的二级动作
        new_layer_action = create_action("新建图层(N)", self.new_layer, "Shift+Ctrl+N")
        self.layer_menu.addAction(new_layer_action)

        # 创建 标注菜单 的二级菜单 快速选择工具 的二级动作
        rectangle_action = create_action("矩形选择框", self.switch_select_tool, signal="toggled", checkable=True)
        oval_action = create_action("椭圆选择框", self.switch_select_tool, signal="toggled", checkable=True)
        join_group(QActionGroup(main_window), (rectangle_action, oval_action))
        add_actions(self.quick_select_menu, (rectangle_action, oval_action))

        # 创建 标注菜单 的二级菜单 轮廓检测 的二级动作
        origin_outline_action = create_action("原始轮廓(O)", self.outline_detect, "Ctrl+A+O",
                                              signal="toggled", checkable=True)
        convex_outline_action = create_action("凸性缺陷轮廓(C)", self.outline_detect, "Ctrl+A+C",
                                              signal="toggled", checkable=True)
        polygon_outline_action = create_action("多边形轮廓(P)", self.outline_detect, "Ctrl+A+P",
                                               signal="toggled", checkable=True)
        join_group(QActionGroup(main_window), (origin_outline_action, convex_outline_action, polygon_outline_action))
        add_actions(self.outline_detect_menu,
                         (origin_outline_action, convex_outline_action, polygon_outline_action))

        # 创建 实验 菜单的二级菜单/动作
        erosion_area_action = create_action("侵蚀面积(E)...", self.result_test)
        contrast_action = create_action("图像对比图(C)...", self.result_test)
        add_actions(self.test_menu, (erosion_area_action, contrast_action))

        # 创建 帮助 菜单的二级菜单/动作
        help_about_action = create_action("关于(A)...", self.help)
        help_help_action = create_action("帮助(H)...", self.help)
        add_actions(self.help_menu, (help_about_action, help_help_action))
