from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QMainWindow, QSplitter, QWidget, QApplication, QFileDialog, QVBoxLayout, QPushButton, QMenuBar
from PySide6.QtGui import QAction
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

    def create_menu(self):
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Settings")

        reset_action = QAction("Reset State", self)
        reset_action.triggered.connect(self.reset_state)
        settings_menu.addAction(reset_action)

        select_directory_action = QAction("Select Directory", self)
        select_directory_action.triggered.connect(self.open_directory_dialog)
        settings_menu.addAction(select_directory_action)

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


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
