from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QFormLayout, QLabel
from PySide6.QtGui import QPixmap

import TagWidget, AspectRatioLabel

'''Thoughts:
    - Day/Month/Year seperate or combine into one date box?
'''


class TagWindow(QWidget):
    def __init__(self):
        super(TagWindow, self).__init__()

        self.setWindowTitle("TagWindow")

        self.tag_layout = QVBoxLayout()

        self.filename_widget = TagWidget.TagWidget("Filename")
        self.tag_layout.addWidget(self.filename_widget)

        '''Date buttons'''
        self.date_layout = QHBoxLayout()

        # Day
        self.day_widget = TagWidget.TagWidget("Day")
        self.date_layout.addWidget(self.day_widget)

        # Month
        self.month_widget = TagWidget.TagWidget("Month")
        self.date_layout.addWidget(self.month_widget)

        # Year
        self.year_widget = TagWidget.TagWidget("Year")
        self.date_layout.addWidget(self.year_widget)

        self.tag_layout.addLayout(self.date_layout)

        image_widget = AspectRatioLabel.AspectRatioLabel(
            QPixmap('C:\\Users\\Joshua\\Desktop\\Fotos van CD\\2007-05-06 Chris en Ria 35 Jaar\\_MG_3457.jpg'))
        self.tag_layout.addWidget(image_widget)

        self.setLayout(self.tag_layout)


