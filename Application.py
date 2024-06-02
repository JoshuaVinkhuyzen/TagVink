from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QSizePolicy, QFormLayout

import TagWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("TagVink")
        self.setMinimumSize(400, 300)

        self.main_layout = QVBoxLayout(self)

        tag_window = TagWindow.TagWindow()
        self.main_layout.addWidget(tag_window)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)



