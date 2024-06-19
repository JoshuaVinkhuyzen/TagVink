from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QSizePolicy, QFormLayout

import TagWindow, ItemList


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("TagVink")
        self.setMinimumSize(400, 300)

        self.main_layout = QHBoxLayout(self)

        tag_window = TagWindow.TagWindow()
        self.main_layout.addWidget(tag_window)

        directory_path = ('D:/Programing/PycharmProjects/Kitepower_Tether_Inspection/Tether_Inspection_Software/'
                          'Saved_Images/Parallel_1/1_Side')

        item_list = ItemList.ItemList(directory_path)
        self.main_layout.addWidget(item_list)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)



