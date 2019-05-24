from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from LRSMSingleVersion.UILayer.CustomWidget.DockWidget import DockWidget


class LayerDockWidget(DockWidget):

    def __init__(self, title_text="图层", parent=None):
        super(LayerDockWidget, self).__init__(title_text, parent)

        self.setObjectName("layer_dock_widget")
        self.content_widget.setObjectName("layer_dock_content_widget")
        self.content_widget.setMinimumSize(150, 180)
        self.setWidget(self.content_widget)
        self._init_content_widget()

    def _init_content_widget(self):
        self.layer_dock_vertical_layout = QVBoxLayout(self.content_widget)

        self.layer_scroll_area = QScrollArea()
        self.layer_scroll_area.setObjectName("layer_scroll_area")
        self.layer_scroll_area.setWidgetResizable(True)
        self.layer_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.layer_scroll_area_content = QWidget()
        self.layer_scroll_area_content.setMinimumSize(150, 180)
        self.layer_scroll_area_content.setObjectName("layer_scroll_area_content")

        self.layer_scroll_area.setWidget(self.layer_scroll_area_content)
        self.layer_dock_vertical_layout.addWidget(self.layer_scroll_area)
