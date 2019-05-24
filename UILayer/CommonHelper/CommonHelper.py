from PyQt5.QtWidgets import QAction, QAbstractButton
from PyQt5.QtGui import QTransform

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


def add_actions(target, actions):
    for action in actions:
        if action:
            target.addAction(action)
        else:
            target.addSeparator()


def set_widgets(target, widgets):
    for widget in widgets:
        target.setWidget(widget)


def join_group(target, actions):
    for index, action in enumerate(actions):
        if action and isinstance(action, QAction):
            target.addAction(action)
        elif action and isinstance(action, QAbstractButton):
            target.addButton(action, index)


def print_transform(text, transform=QTransform()):
    print(text)
    print(transform.m11(), " ", end="")
    print(transform.m12(), " ", end="")
    print(transform.m13(), " ", end="")
    print(" ")
    print(transform.m21(), " ", end="")
    print(transform.m22(), " ", end="")
    print(transform.m23(), " ", end="")
    print(" ")
    print(transform.m31(), " ", end="")
    print(transform.m32(), " ", end="")
    print(transform.m33(), " ", end="")
    print(" ")
