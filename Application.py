from PySide6.QtWidgets import QMainWindow, QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel

'''Thoughts:
    - Day/Month/Year seperate or combine into one date box?
'''

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TagVink")

        self.setMinimumSize(400, 300)

        tag_layout = QVBoxLayout()

        filename_box = QComboBox()
        filename_box.setEditable(True)

        tag_layout.addWidget(filename_box)

        tag_box = QComboBox()
        tag_box.setEditable(True)

        tag_layout.addWidget(tag_box)

        # Date buttons
        date_layout = QHBoxLayout()

        # Day
        day_layout = QVBoxLayout()
        day_titel = QLabel("Day")

        day_box = QComboBox()
        day_box.setEditable(True)

        day_layout.addWidget(day_titel)
        day_layout.addWidget(day_box)

        # Month
        month_layout = QVBoxLayout()
        month_titel = QLabel("Month")

        month_box = QComboBox()
        month_box.setEditable(True)

        month_layout.addWidget(month_titel)
        month_layout.addWidget(month_box)

        # Year
        year_layout = QVBoxLayout()
        year_titel = QLabel("Year")

        year_box = QComboBox()
        year_box.setEditable(True)
        year_box.addItems(["< blank >", "< keep >"])

        year_layout.addWidget(year_titel)
        year_layout.addWidget(year_box)

        date_layout.addLayout(day_layout)
        date_layout.addLayout(month_layout)
        date_layout.addLayout(year_layout)

        tag_layout.addLayout(date_layout)

        file_name_box = QComboBox()
        file_name_box.setEditable(True)

        tag_widget = QWidget()
        tag_widget.setLayout(tag_layout)

        self.setCentralWidget(tag_widget)
