from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QFormLayout, QLabel, QListWidget
from PySide6.QtGui import QPixmap

import TagWidget, AspectRatioLabel

class TagWindow(QWidget):
    def __init__(self):
        super(TagWindow, self).__init__()

        self.setWindowTitle("TagWindow")

        self.main_layout = QVBoxLayout()

        self.filename_widget = TagWidget.TagWidget("Title:")
        self.main_layout.addWidget(self.filename_widget)

        '''Date buttons'''
        self.date_layout = QHBoxLayout()

        # Day
        self.day_widget = TagWidget.TagWidget("Day:")
        self.date_layout.addWidget(self.day_widget)

        # Month
        self.month_widget = TagWidget.TagWidget("Month:")
        self.date_layout.addWidget(self.month_widget)

        # Year
        self.year_widget = TagWidget.TagWidget("Year:")
        self.date_layout.addWidget(self.year_widget)

        self.main_layout.addLayout(self.date_layout)

        '''Tag Layout'''
        self.tag_layout = QHBoxLayout()

        # Tags
        self.applied_tags_widget = QListWidget()
        self.applied_tags_widget.itemDoubleClicked.connect(self.remove_tag_from_applied)
        self.tag_layout.addWidget(self.applied_tags_widget)

        # Available Tags
        self.available_tags_widget = QListWidget()
        self.available_tags_widget.itemDoubleClicked.connect(self.transfer_tag_to_applied)
        self.tag_layout.addWidget(self.available_tags_widget)

        self.main_layout.addLayout(self.tag_layout)

        image_widget = AspectRatioLabel.AspectRatioLabel(
            QPixmap('D:/Programing/PycharmProjects/Kitepower_Tether_Inspection/Images/Good/frame0.jpg'))
        self.main_layout.addWidget(image_widget)

        self.setLayout(self.main_layout)

        # Populate the available tags list
        self.populate_available_tags()

    def populate_available_tags(self):
        sample_tags = ["Tag1", "Tag2", "Tag3", "Tag4", "Tag5"]
        for tag in sample_tags:
            self.available_tags_widget.addItem(tag)
        # Sort the applied tags
        self.sort_list_widget(self.applied_tags_widget)

    def sort_list_widget(self, list_widget):
        items = [list_widget.item(i).text() for i in range(list_widget.count())]
        items.sort()
        list_widget.clear()
        for item in items:
            list_widget.addItem(item)

    def transfer_tag_to_applied(self, item):
        # Check if the item is already in the applied_tags_widget
        for i in range(self.applied_tags_widget.count()):
            if self.applied_tags_widget.item(i).text() == item.text():
                return  # Item already exists, do not add again

        # If not found, add the item to the applied_tags_widget
        self.applied_tags_widget.addItem(item.text())
        # Sort the applied tags
        self.sort_list_widget(self.applied_tags_widget)

    def remove_tag_from_applied(self, item):
        self.applied_tags_widget.takeItem(self.applied_tags_widget.row(item))
        # Sort the applied tags
        self.sort_list_widget(self.applied_tags_widget)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = TagWindow()
    window.show()
    sys.exit(app.exec())
