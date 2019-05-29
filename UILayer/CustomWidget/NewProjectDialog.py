import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QGridLayout, \
    QWidget, QApplication, \
    QLineEdit, QFileDialog, QMessageBox, \
    QLabel, QPushButton, QDialogButtonBox


class NewProjectDialog(QDialog):

    def __init__(self, pro_last_dir="./", img_last_dir="./", parent=None):
        super(NewProjectDialog, self).__init__(parent)
        self.setWindowTitle("新建项目")
        self.setMinimumWidth(970)

        self.pro_last_dir = pro_last_dir
        self.img_last_dir = img_last_dir

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setObjectName("newProjectDialogGridLayout")

        project_name_label = QLabel("项目名称(N)：")
        self.project_name_edit = QLineEdit()
        project_name_label.setBuddy(self.project_name_edit)
        self.grid_layout.addWidget(project_name_label, 0, 0)
        self.grid_layout.addWidget(self.project_name_edit, 0, 1)

        project_location_label = QLabel("项目位置(L)：")
        self.project_location_edit = QLineEdit()
        self.select_pro_location_btn = QPushButton("浏览(B)...")
        project_location_label.setBuddy(self.project_location_edit)
        self.grid_layout.addWidget(project_location_label, 1, 0)
        self.grid_layout.addWidget(self.project_location_edit, 1, 1)
        self.grid_layout.addWidget(self.select_pro_location_btn, 1, 2)

        image_location_label = QLabel("原始图片(I)：")
        self.image_location_edit = QLineEdit()
        self.select_img_location_btn = QPushButton("浏览(S)...")
        image_location_label.setBuddy(self.image_location_edit)
        self.grid_layout.addWidget(image_location_label, 2, 0)
        self.grid_layout.addWidget(self.image_location_edit, 2, 1)
        self.grid_layout.addWidget(self.select_img_location_btn, 2, 2)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        self.buttonBox.setObjectName("buttonBox")
        self.grid_layout.addWidget(self.buttonBox, 3, 1, 1, 2)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.project_name_edit.textChanged.connect(self._set_ok_btn_enabled)
        self.project_location_edit.textChanged.connect(self._set_ok_btn_enabled)
        self.image_location_edit.textChanged.connect(self._set_ok_btn_enabled)

        self.select_pro_location_btn.clicked.connect(self._get_project_location)
        self.select_img_location_btn.clicked.connect(self._get_image_location)

    def _get_project_location(self):
        project_directory = QFileDialog.getExistingDirectory(
            self, "项目位置",
            self.pro_last_dir)
        self.project_location_edit.setText(project_directory)

    def _get_image_location(self):
        file_format = "Image files (*.png *.jpg *.ico *tif)"
        image_file = QFileDialog.getOpenFileName(
            self, "选择原始图片",
            self.img_last_dir,
            file_format
        )[0]
        self.image_location_edit.setText(image_file)

    def _set_ok_btn_enabled(self):
        project_directory = self.project_location_edit.text()
        image_file = self.image_location_edit.text()
        project_name = self.project_name_edit.text()

        if all([project_directory, image_file, project_name]):
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def new_project_info(self):
        return self.project_name_edit.text(), \
               self.project_location_edit.text(),\
               self.image_location_edit.text()

    def accept(self):

        class ProjectNameError(Exception):
            pass

        class ProjectDirError(Exception):
            pass

        class ImageFileError(Exception):
            pass

        project_directory = self.project_location_edit.text()
        image_file = self.image_location_edit.text()
        project_name = self.project_name_edit.text()

        try:
            if not os.path.exists(project_directory[:3]):
                raise ProjectDirError
        except ProjectDirError:
            QMessageBox.critical(self, "新建项目", "项目位置无效，请输入正确的项目位置！")
            return
        QDialog.accept(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree_widget = NewProjectDialog()
    tree_widget.show()
    sys.exit(app.exec_())