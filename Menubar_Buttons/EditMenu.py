from PySide6.QtGui import QAction


def create_edit_menu_actions(parent):
    edit_menu_actions = []

    undo_action = QAction("Undo", parent)
    edit_menu_actions.append(undo_action)

    redo_action = QAction("Redo", parent)
    edit_menu_actions.append(redo_action)

    return edit_menu_actions
