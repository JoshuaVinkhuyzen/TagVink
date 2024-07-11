from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QMainWindow, QSplitter
from themes import apply_system_theme, set_dark_theme, set_light_theme, set_blue_theme, set_green_theme
import TagWindow, ItemsWindow
from MenubarWindow import MenuBarWindow

class MainWindow(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app  # Store the app reference
        self.setWindowTitle("TagVink")
        self.setMinimumSize(400, 300)

        self.settings = QSettings("YourCompany", "YourAppName")

        self.menu_bar = MenuBarWindow(self)
        self.setMenuBar(self.menu_bar)

        self.main_layout = QSplitter(Qt.Horizontal)
        self.main_layout.setChildrenCollapsible(False)

        self.tag_window = TagWindow.TagWindow()
        self.main_layout.addWidget(self.tag_window)

        self.directory_path = self.settings.value("directory_path", "")
        self.item_list = ItemsWindow.ItemList(self.directory_path)
        self.main_layout.addWidget(self.item_list)

        self.setCentralWidget(self.main_layout)

        self.load_window_state()
        self.apply_theme()

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

    def apply_theme(self):
        theme = self.settings.value("theme", "default")
        if theme == "dark":
            set_dark_theme(self.app)
        elif theme == "light":
            set_light_theme(self.app)
        elif theme == "blue":
            set_blue_theme(self.app)
        elif theme == "green":
            set_green_theme(self.app)
        else:
            apply_system_theme(self.app)
