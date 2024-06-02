from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QFormLayout


class TagWidget(QWidget):
    def __init__(self, label_text, parent=None):
        super(TagWidget, self).__init__()

        self.layout = QFormLayout()

        self.titel = QLabel(label_text)

        self.box = QComboBox()
        self.box.setEditable(True)
        self.box.addItems(["< blank >", "< keep >"])

        # Add widgets to form layout with alignment
        self.layout.addRow(self.titel, self.box)

        # Align label and combo box to top left
        self.layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.layout.addWidget(self.titel)
        self.layout.addWidget(self.box)

        self.setLayout(self.layout)
