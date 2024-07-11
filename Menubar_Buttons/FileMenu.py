from PySide6.QtGui import QAction


def create_file_menu_actions(parent):
    actions = []

    # Tag actions
    save_tag_action = QAction("Save tag", parent)
    actions.append(save_tag_action)

    remove_tag_action = QAction("Remove tag", parent)
    actions.append(remove_tag_action)

    read_tag_action = QAction("Read tag", parent)
    actions.append(read_tag_action)

    export_action = QAction("Export...", parent)
    actions.append(export_action)

    # Separator
    actions.append(None)

    # Directory actions
    change_directory_action = QAction("Change directory...", parent)
    change_directory_action.triggered.connect(parent.open_directory_dialog)
    actions.append(change_directory_action)

    add_directory_action = QAction("Add directory...", parent)
    actions.append(add_directory_action)

    favourite_directory_action = QAction("Favourite directory...", parent)
    actions.append(favourite_directory_action)

    open_in_explorer_action = QAction("Open in Explorer", parent)
    actions.append(open_in_explorer_action)

    # Separator
    actions.append(None)

    # Configuration actions
    options_action = QAction("Options...", parent)
    options_action.triggered.connect(parent.open_options_dialog)
    actions.append(options_action)

    save_configuration_action = QAction("Save configuration...", parent)
    actions.append(save_configuration_action)

    open_configuration_folder_action = QAction("Open configuration folder", parent)
    actions.append(open_configuration_folder_action)

    # Separator
    actions.append(None)

    # Exit action
    exit_action = QAction("Exit", parent)
    exit_action.triggered.connect(parent.parent.close)  # Assuming parent has access to parent.main_window
    actions.append(exit_action)

    return actions
