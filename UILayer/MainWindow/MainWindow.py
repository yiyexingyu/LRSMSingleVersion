import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from LRSMSingleVersion.CommonHelper.CommonHelper import *
from LRSMSingleVersion.UILayer.Workbench.WorkbenchWidget import WorkbenchWidget, FileOpenFailException
from LRSMSingleVersion.UILayer.CustomWidget.NewProjectDialog import NewProjectDialog
from LRSMSingleVersion.UILayer.MainWindow.MainWindowUi import MainWindowUI


class WindowStateData(object):

    def __init__(self):
        self.recent_files = []
        self.recent_projects = []


class MainWindow(QMainWindow, MainWindowUI):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        super(MainWindow, self)._init_ui(self)

        self.window_state_data = WindowStateData()

        self._connect_notify()
        self._load_initial_file()
        self._restore_data()
        self._init_style()

    def _init_style(self):
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
        self.window_state_data.recent_files = settings.value("recent_files", [])
        self.window_state_data.recent_projects = settings.value("recent_project", [])
        window_state = settings.value("main_window/state")

        if not self.window_state_data.recent_files:
            self.window_state_data.recent_files = []
        if not self.window_state_data.recent_projects:
            self.window_state_data.recent_projects = []
        # if window_state is not None:
        #     self.restoreState(window_state)
        QTimer.singleShot(0, self._load_initial_file)

    # 加载文件数据
    def _load_initial_file(self):
        pass

    def _connect_notify(self):
        """
        统一进行窗口组件事件信号的和槽函数连接
        :return:
        """
        self.center_tab_widget.tabCloseRequested.connect(self.close_file)
        self.file_menu.aboutToShow.connect(self.update_file_menu)
        self.new_project_action.triggered.connect(self.create_new_project)
        self.open_original_image_action.triggered.connect(self.open_file)
        self.close_all_action.triggered.connect(self.close_all_file)
        self.quit_action.triggered.connect(self.close)

        self.cmp_history_action.triggered.connect(self.cmp_history)

    # 重写 窗口关闭事件
    def closeEvent(self, event):
        if self.ok_to_continue():
            settings = QSettings()
            # 最近打开文件
            recently_files = QVariant(self.window_state_data.recent_files) \
                if self.window_state_data.recent_files else QVariant()
            recently_projects = QVariant(self.window_state_data.recent_projects) \
                if self.window_state_data.recent_projects else QVariant()
            settings.setValue("recent_files", recently_files)
            settings.setValue("project_files", recently_projects)
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
        tip_text = "要在退出前保存对 图片\"" + os.path.basename(file_name) + "\"的更改吗？"
        reply = QMessageBox.question(
            self, "遥感地图标注 - 未保存提示", tip_text,
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            return False
        elif reply == QMessageBox.Yes:
            # 保存文件 待写
            """TODO"""
            # self.save_file(file_name=file_name)
            return True
        else:
            return True

    # ########################################  槽函数代码段  ###########################################

    def update_file_menu(self):
        self.file_menu.clear()
        self.file_menu.addAction(self.file_menu_actions[0])
        self.file_menu.addAction(self.file_menu_actions[1])
        self.file_menu.addAction(self.file_menu_actions[2])

        self.file_menu.addSeparator()
        recent_files_menu = self.file_menu.addMenu("打开最近的文件(T)...")
        if self.window_state_data.recent_files:
            for i, file_name in enumerate(self.window_state_data.recent_files):
                dir_file_name = os.path.basename(file_name)
                action = create_action(
                    parent=recent_files_menu,
                    text=str(i + 1) + " " + dir_file_name,
                    slot=self._open_file_from_recent)
                action.setData(QVariant(file_name))
                recent_files_menu.addAction(action)
            recent_files_menu.addSeparator()
        remove_action = create_action(
            parent=recent_files_menu,
            text="清空最近打开的文件列表",
            slot=self.remove_recent_files)
        recent_files_menu.addAction(remove_action)

        recent_project_menu = self.file_menu.addMenu("打开最近的项目(P)...")
        if self.window_state_data.recent_projects:
            for i, file_name in enumerate(self.window_state_data.recent_projects):
                dir_file_name = file_name
                action = create_action(
                    parent=recent_project_menu,
                    text=str(i + 1) + " " + dir_file_name,
                    slot=self._open_project_from_recent())
                action.setData(QVariant(file_name))
                recent_project_menu.addAction(action)
            recent_project_menu.addSeparator()
        remove_action = create_action(
            parent=recent_files_menu,
            text="清空最近打开的项目列表",
            slot=self.remove_recent_project)
        recent_project_menu.addAction(remove_action)
        self.file_menu.addSeparator()

        add_actions(self.file_menu, self.file_menu_actions[3:])

    def remove_recent_files(self):
        self.window_state_data.recent_files.clear()

    def add_recent_file(self, file_name):
        if file_name:
            if file_name in self.window_state_data.recent_files:
                self.window_state_data.recent_files.remove(file_name)
            self.window_state_data.recent_files.insert(0, file_name)
            while len(self.window_state_data.recent_files) > 9:
                print(self.window_state_data.recent_files.pop())

    def remove_recent_project(self):
        self.window_state_data.recent_projects.clear()

    def add_recent_file_project(self, project_name):
        if project_name:
            if project_name in self.window_state_data.recent_projects:
                self.window_state_data.recent_files.remove(project_name)
            self.window_state_data.recent_files.insert(0, project_name)
            while len(self.window_state_data.recent_projects) > 9:
                print(self.window_state_data.recent_projects.pop())

    def open_file(self, file_name=None):
        if file_name is None or isinstance(file_name, bool):
            dir_ = os.path.dirname(self.window_state_data.recent_files[0]) \
                if self.window_state_data.recent_files else os.path.dirname(".")
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

    def create_new_project(self):
        image_last_dir = os.path.dirname(self.window_state_data.recent_files[0]) \
            if self.window_state_data.recent_files else os.path.dirname(".")
        new_project_dialog = NewProjectDialog(img_last_dir=image_last_dir, parent=self)
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

    def _open_file_from_recent(self):
        sender = self.sender()
        if isinstance(sender, QAction):
            file_name = sender.data()
            self.open_file(file_name)

    def _open_project_from_recent(self):
        sender = self.sender()
        if isinstance(sender, QAction):
            file_name = sender.data()
            self.open_file(file_name)

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

    def close_all_file(self):
        self.ok_to_continue()

    def cmp_history(self):
        dir_ = os.path.dirname(self.window_state_data.recent_files[0]) \
            if self.window_state_data.recent_files else os.path.dirname(".")
        # 打开一个 文件选择对口框
        file_format = "Image files (*.png *.jpg *.ico *tif)"

        file_names = QFileDialog.getOpenFileNames(self, "选择遥感图片", dir_, file_format)[0]

    def count_area(self, outline_array: tuple, ratio: int) -> float:
        """
        :param outline_array: 轮廓的像素的矩阵
        :param ratio: 图像的分辨率 以米为单位
        :return: float类型的面积
        """
        pass

    # ####################################################################################################

    def update_close_button_enabled(self):
        is_tab_empty = self.center_tab_widget.count() != 0
        self.file_menu_actions[4].setEnabled(is_tab_empty)
        self.file_menu_actions[5].setEnabled(is_tab_empty)
        self.file_menu_actions[6].setEnabled(is_tab_empty)

    def create_new_tab(self, file_name):
        try:
            new_tab = WorkbenchWidget(
                file_name=file_name, gadget=self.gadget_dock_widget.get_current_gadget())
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


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("LRSM Ltd.")
    app.setOrganizationDomain("lrsm.eu")
    app.setApplicationName("LRSMSingleVersion")
    form = MainWindow()
    form.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
