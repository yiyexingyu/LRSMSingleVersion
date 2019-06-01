from PyQt5.QtWidgets import QAction, QAbstractButton, QMenu
from PyQt5.QtGui import QTransform, QIcon


def add_menu(text, target, object_name=None, tip=None, slot=None, signal=None) -> QMenu:
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


def create_action(parent=None, text="", shortcut=None, slot=None, tip=None,
                  icon=None, checkable=False, signal="triggered", image=None):
    new_action = QAction(text, parent)
    if icon:
        new_action.setIcon(QIcon(icon))
    if shortcut:
        new_action.setShortcut(shortcut)
    if tip:
        new_action.setToolTip(tip)
        new_action.setStatusTip(tip)
    if slot and callable(slot):
        if signal == "triggered":
            new_action.triggered.connect(slot)
        elif signal == "toggled":
            new_action.toggled.connect(slot)
    if checkable:
        new_action.setCheckable(True)
    if image:
        new_action.setIcon(QIcon(image))
    return new_action


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


def remove_object_by_objects(src_list, objects):
    if isinstance(src_list, list):
        for obj in objects:
            if obj in src_list:
                src_list.remove(obj)
    return src_list


def remove_object_by_indexes(src_list, indexes):
    if isinstance(src_list, list):
        if isinstance(indexes, list):
            indexes = reversed(sorted(indexes))
            for index in indexes:
                if 0 <= index < len(src_list):
                    src_list.pop(index)
        elif isinstance(indexes, int):
            if 0 <= indexes < len(src_list):
                src_list.pop(indexes)
    return src_list


def counter(start_at=1):
    count_num = start_at
    while True:
        val = (yield count_num)
        if val is not None:
            count_num = val
        else:
            count_num += 1

