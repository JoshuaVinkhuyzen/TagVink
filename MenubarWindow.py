from PySide6.QtWidgets import QMenuBar, QFileDialog
from PySide6.QtGui import QAction
from OptionsWindow import OptionsWindow


class MenuBarWindow(QMenuBar):
    def __init__(self, parent=None):
        super(MenuBarWindow, self).__init__(parent)
        self.parent = parent  # Store a reference to the parent (MainWindow)

        # File Menu
        file_menu = self.addMenu("File")

        # Tag actions
        save_tag_action = QAction("Save tag", self)
        file_menu.addAction(save_tag_action)

        remove_tag_action = QAction("Remove tag", self)
        file_menu.addAction(remove_tag_action)

        read_tag_action = QAction("Read tag", self)
        file_menu.addAction(read_tag_action)

        export_action = QAction("Export...", self)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        # Directory actions
        change_directory_action = QAction("Change directory...", self)
        change_directory_action.triggered.connect(self.open_directory_dialog)
        file_menu.addAction(change_directory_action)

        add_directory_action = QAction("Add directory...", self)
        file_menu.addAction(add_directory_action)

        favourite_directory_action = QAction("Favourite directory...", self)
        file_menu.addAction(favourite_directory_action)

        open_in_explorer_action = QAction("Open in Explorer", self)
        file_menu.addAction(open_in_explorer_action)

        file_menu.addSeparator()

        # Configuration actions
        options_action = QAction("Options...", self)
        options_action.triggered.connect(self.open_options_dialog)
        file_menu.addAction(options_action)

        save_configuration_action = QAction("Save configuration...", self)
        file_menu.addAction(save_configuration_action)

        open_configuration_folder_action = QAction("Open configuration folder", self)
        file_menu.addAction(open_configuration_folder_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = self.addMenu("Edit")

        # Example actions for Edit menu
        undo_action = QAction("Undo", self)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        edit_menu.addAction(redo_action)

        # View Menu
        view_menu = self.addMenu("View")

        # Example actions for View menu
        zoom_in_action = QAction("Zoom In", self)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        view_menu.addAction(zoom_out_action)

        # Help Menu
        help_menu = self.addMenu("Help")

        # Example actions for Help menu
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

    def open_directory_dialog(self):
        dialog = QFileDialog(self.parent)
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec():
            self.parent.directory_path = dialog.selectedFiles()[0]
            self.parent.item_list.set_directory_path(self.parent.directory_path)
            self.parent.item_list.reload_images()  # Assuming you have this method to reload the images

    def open_options_dialog(self):
        options_dialog = OptionsWindow(self.parent)
        if options_dialog.exec():
            self.parent.apply_theme()
