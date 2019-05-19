from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TextItem(QGraphicsTextItem):

    def __init__(self, text, position, scene, font=QFont("Times", 10), transform=QTransform()):
        super(TextItem, self).__init__(text)

        # 设置标志
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

        self.setFont(font)
        self.setPos(position)
        self.setTransform(transform)

        scene.clearSelection()
        scene.addItem(self)

    def parentWidget(self):
        # 返回场景的第一个视图
        return self.scene().views()[0]

    def itemChange(self, change, variant):
        # 非选择状态的变化 要设置dirty标志
        if change != QGraphicsItem.ItemSelectedChange:
            print("text item is changed!")

        return QGraphicsTextItem.itemChange(self, change, variant)

    def mouseDoubleClickEvent(self, event):
        dialog = TextItemDlg(self, self.parentWidget())
        dialog.exec_()


class TextItemDlg(QDialog):

    def __init__(self, item=None, position=None, scene=None, parent=None):
        super(QDialog, self).__init__(parent)

        self.item = item
        self.position = position
        self.scene = scene

        self.editor = QTextEdit()
        self.editor.setAcceptRichText(False)
        self.editor.setTabChangesFocus(True)
        editorLabel = QLabel("&Text:")
        editorLabel.setBuddy(self.editor)
        self.fontComboBox = QFontComboBox()
        self.fontComboBox.setCurrentFont(QFont("Times",10))
        fontLabel = QLabel("&Font:")
        fontLabel.setBuddy(self.fontComboBox)
        self.fontSpinBox = QSpinBox()
        self.fontSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.fontSpinBox.setRange(6, 280)
        self.fontSpinBox.setValue(10)
        fontSizeLabel = QLabel("&Size:")
        fontSizeLabel.setBuddy(self.fontSpinBox)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Cancel)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        if self.item is not None:
            self.editor.setPlainText(self.item.toPlainText())
            self.fontComboBox.setCurrentFont(self.item.font())
            self.fontSpinBox.setValue(self.item.font().pointSize())

        layout = QGridLayout()
        layout.addWidget(editorLabel, 0, 0)
        layout.addWidget(self.editor, 1, 0, 1, 6)
        layout.addWidget(fontLabel, 2, 0)
        layout.addWidget(self.fontComboBox, 2, 1, 1, 2)
        layout.addWidget(fontSizeLabel, 2, 3)
        layout.addWidget(self.fontSpinBox, 2, 4, 1, 2)
        layout.addWidget(self.buttonBox, 3, 0, 1, 6)
        self.setLayout(layout)

        self.fontComboBox.currentFontChanged.connect(self.updateUi)
        self.fontSpinBox.valueChanged.connect(self.updateUi)
        self.editor.textChanged.connect(self.updateUi)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.setWindowTitle("Page Designer - {0} Text Item".format(
                "Add" if self.item is None else "Edit"))
        self.updateUi()

    def updateUi(self):
        font = self.fontComboBox.currentFont()
        font.setPointSize(self.fontSpinBox.value())
        self.editor.document().setDefaultFont(font)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(
                bool(self.editor.toPlainText()))

    def accept(self):
        if self.item is None:
            self.item = TextItem("", self.position, self.scene)
        font = self.fontComboBox.currentFont()
        font.setPointSize(self.fontSpinBox.value())
        self.item.setFont(font)
        self.item.setPlainText(self.editor.toPlainText())
        self.item.update()
        QDialog.accept(self)











