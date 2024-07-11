from PySide6.QtGui import QAction


def create_help_menu_actions(parent):
    help_menu_actions = []

    about_action = QAction("About", parent)
    help_menu_actions.append(about_action)

    return help_menu_actions
