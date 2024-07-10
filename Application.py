from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QMainWindow, QSplitter, QApplication, QFileDialog
from PySide6.QtGui import QAction, QPalette, QColor
import platform
import sys

from options import OptionsWindow
import TagWindow, ItemList


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("TagVink")
        self.setMinimumSize(400, 300)

        self.settings = QSettings("YourCompany", "YourAppName")

        self.create_menu()

        self.main_layout = QSplitter(Qt.Horizontal)
        self.main_layout.setChildrenCollapsible(False)

        self.tag_window = TagWindow.TagWindow()
        self.main_layout.addWidget(self.tag_window)

        self.directory_path = self.settings.value("directory_path", "")
        self.item_list = ItemList.ItemList(self.directory_path)
        self.main_layout.addWidget(self.item_list)

        self.setCentralWidget(self.main_layout)

        self.load_window_state()
        self.apply_theme()

    def create_menu(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")

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
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menubar.addMenu("Edit")

        # Example actions for Edit menu
        undo_action = QAction("Undo", self)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        edit_menu.addAction(redo_action)

        # View Menu
        view_menu = menubar.addMenu("View")

        # Example actions for View menu
        zoom_in_action = QAction("Zoom In", self)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        view_menu.addAction(zoom_out_action)

        # Help Menu
        help_menu = menubar.addMenu("Help")

        # Example actions for Help menu
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

    def closeEvent(self, event):
        self.save_window_state()
        event.accept()

    def save_window_state(self):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        self.settings.setValue("splitterState", self.main_layout.saveState())
        self.settings.setValue("directory_path", self.directory_path)

    def load_window_state(self):
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        window_state = self.settings.value("windowState")
        if window_state:
            self.restoreState(window_state)
        splitter_state = self.settings.value("splitterState")
        if splitter_state:
            self.main_layout.restoreState(splitter_state)

    def reset_state(self):
        self.settings.clear()
        self.load_window_state()
        self.directory_path = ""
        self.item_list.clear()

    def open_directory_dialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec():
            self.directory_path = dialog.selectedFiles()[0]
            self.item_list.set_directory_path(self.directory_path)
            self.item_list.reload_images()  # Assuming you have this method to reload the images

    def open_options_dialog(self):
        options_dialog = OptionsWindow(self)
        if options_dialog.exec():
            self.apply_theme()

    def apply_theme(self):
        theme = self.settings.value("theme", "default")
        if theme == "dark":
            set_dark_theme(app)
        elif theme == "light":
            set_light_theme(app)
        else:
            if platform.system() == "Windows":
                if is_windows_dark_mode():
                    set_dark_theme(app)
                else:
                    set_light_theme(app)
            elif platform.system() == "Darwin":  # macOS
                if app.palette().color(QPalette.Window).value() < 128:
                    set_dark_theme(app)
                else:
                    set_light_theme(app)

def set_dark_theme(app):
    app.setStyle("Fusion")
    palette = QPalette()

    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(palette)


def set_light_theme(app):
    app.setStyle("Fusion")
    palette = QPalette()

    palette.setColor(QPalette.Window, Qt.white)
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, Qt.white)
    palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(245, 245, 245))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.white)

    app.setPalette(palette)


def is_windows_dark_mode():
    try:
        import winreg
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize')
        value, regtype = winreg.QueryValueEx(key, 'AppsUseLightTheme')
        return value == 0
    except Exception as e:
        return False


def main():
    global app  # Declare app as global
    app = QApplication(sys.argv)

    # Apply system theme
    if platform.system() == "Windows":
        if is_windows_dark_mode():
            set_dark_theme(app)
        else:
            set_light_theme(app)
    elif platform.system() == "Darwin":  # macOS
        if app.palette().color(QPalette.Window).value() < 128:
            set_dark_theme(app)
        else:
            set_light_theme(app)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
