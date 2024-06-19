from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QFormLayout, QLabel, QListWidget, QLineEdit


class ItemList(QWidget):
    def __init__(self):
        super(ItemList, self).__init__()

        self.setWindowTitle("Item List")
        self.setMinimumSize(400, 300)

        self.main_layout = QVBoxLayout()

        self.setLayout(self.main_layout)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ItemList()
    window.show()
    sys.exit(app.exec())
