from PyQt5.QtCore import Qt, QRegExp, pyqtSignal
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLabel, QGridLayout, \
    QLineEdit, QSpacerItem, QSizePolicy, QSlider

from LRSMSingleVersion.UILayer.CustomWidget.DockWidget import DockWidget


class ColorDockWidget(DockWidget):

    def __init__(self, title_text="颜色", parent=None):
        super(ColorDockWidget, self).__init__(title_text, parent)

        self.setObjectName("color_dock_widget")
        self.content_widget.setObjectName("color_dock_content_widget")
        self.setWidget(self.content_widget)
        self._init_content_widget()

    def _init_content_widget(self):
        def create_rgb_color_item(label_text):
            # 创建验证器 对输入进行预防验证
            validator = QRegExpValidator(QRegExp(r"25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9]"), self)

            color_slider = self.create_slider(slot=self.color_setting)
            color_label = QLabel(label_text, self.content_widget)
            color_label.setBuddy(color_slider)
            color_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

            color_input = QLineEdit(self.content_widget)
            color_input.setMaxLength(3)
            color_input.setValidator(validator)
            color_input.setFixedWidth(50)
            color_input.setText("0")
            return color_label, color_slider, color_input

        color_dock_widget_stylesheet = """
        QLineEdit { margin-right: 10px ;}
        """
        self.content_widget.setStyleSheet(color_dock_widget_stylesheet)

        r_color_label, r_color_slider, r_color_input = create_rgb_color_item("R")
        g_color_label, g_color_slider, g_color_input = create_rgb_color_item("G")
        b_color_label, b_color_slider, b_color_input = create_rgb_color_item("B")

        self.color_dock_grid_layout = QGridLayout(self.content_widget)
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

    def create_slider(self, minimum=0, maximum=255, step=1,
                      tick_position=QSlider.TicksAbove, slot=None):
        new_slider = QSlider(Qt.Horizontal, self.content_widget)
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

    def color_setting(self):
        pass
