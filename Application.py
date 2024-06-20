from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QMainWindow, QSplitter, QWidget, QApplication, QFileDialog, QVBoxLayout, QPushButton
from PySide6.QtGui import QAction

import TagWindow
import ItemList


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("TagVink")
        self.setMinimumSize(400, 300)

        self.splitter = QSplitter(Qt.Horizontal)  # Create a horizontal splitter
        self.setCentralWidget(self.splitter)

        self.tag_window = TagWindow.TagWindow()
        self.splitter.addWidget(self.tag_window)

        self.item_list = None

        # Menu for selecting a directory
        select_directory_action = QAction("Select Directory", self)
        select_directory_action.triggered.connect(self.select_directory)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(select_directory_action)

        # Load settings (including splitter state, window geometry, and last directory)
        self.load_settings()

        # Load the previously selected directory if it exists
        self.load_saved_directory()

    def closeEvent(self, event):
        # Save settings (including splitter state, window geometry, and last directory)
        self.save_settings()
        super().closeEvent(event)

    def save_settings(self):
        settings = QSettings("MyCompany", "TagVink")
        settings.setValue("splitterSizes", self.splitter.sizes())
        settings.setValue("windowGeometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        if self.item_list:
            settings.setValue("lastDirectory", self.item_list.directory_path)

    def load_settings(self):
        settings = QSettings("MyCompany", "TagVink")
        sizes = settings.value("splitterSizes")
        if sizes:
            self.splitter.setSizes([int(size) for size in sizes])
        geometry = settings.value("windowGeometry")
        if geometry:
            self.restoreGeometry(geometry)
        state = settings.value("windowState")
        if state:
            self.restoreState(state)

    def load_saved_directory(self):
        settings = QSettings("MyCompany", "TagVink")
        directory_path = settings.value("lastDirectory")
        if directory_path:
            self.load_directory(directory_path)

    def select_directory(self):
        directory_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory_path:
            self.load_directory(directory_path)

    def load_directory(self, directory_path):
        if self.item_list:
            self.splitter.widget(1).deleteLater()
        self.item_list = ItemList.ItemList(directory_path)
        self.splitter.addWidget(self.item_list)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
