from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel


class TagWidget(QWidget):
    def __init__(self):
        super(TagWidget, self).__init__()

        layout = QVBoxLayout()
        titel = QLabel("[ERROR] specify label")
        titel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        box = QComboBox()
        box.setEditable(True)
        box.addItems(["< blank >", "< keep >"])

        layout.addWidget(titel)
        layout.addWidget(box)



    def createWidget(self, titel):

        layout = QVBoxLayout()
        titel = QLabel(titel)
        titel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        box = QComboBox()
        box.setEditable(True)
        box.addItems(["< blank >", "< keep >"])

        layout.addWidget(titel)
        layout.addWidget(box)
