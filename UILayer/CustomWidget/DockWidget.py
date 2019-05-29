from PyQt5.QtWidgets import QDockWidget, QWidget


class DockWidget(QDockWidget):

    def __init__(self, widget_title, parent=None):
        super(DockWidget, self).__init__(widget_title, parent)
        self.content_widget = QWidget()
        self.setWidget(self.content_widget)

    def _init_content_widget(self):
        pass
