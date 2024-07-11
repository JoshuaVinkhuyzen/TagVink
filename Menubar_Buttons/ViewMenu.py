from PySide6.QtGui import QAction


def create_view_menu_actions(parent):
    view_menu_actions = []

    zoom_in_action = QAction("Zoom In", parent)
    view_menu_actions.append(zoom_in_action)

    zoom_out_action = QAction("Zoom Out", parent)
    view_menu_actions.append(zoom_out_action)

    return view_menu_actions
