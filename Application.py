from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QSplitter, QVBoxLayout, QWidget

import TagWindow
import ItemList

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("TagVink")
        self.setMinimumSize(400, 300)

        splitter = QSplitter(Qt.Horizontal)  # Use a horizontal splitter

        tag_window = TagWindow.TagWindow()
        splitter.addWidget(tag_window)

        directory_path = 'C:/Users/joshu/OneDrive/Pictures/Saved Pictures'

        item_list = ItemList.ItemList(directory_path)
        splitter.addWidget(item_list)

        splitter.setStretchFactor(0, 1)  # Set stretch factor for tag_window
        splitter.setStretchFactor(1, 1)  # Set stretch factor for item_list

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
