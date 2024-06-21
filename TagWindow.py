from PySide6.QtWidgets import QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QFormLayout, QLabel, QListWidget, QLineEdit
from PySide6.QtGui import QPixmap


class AspectRatioLabel(QLabel):
    def __init__(self, pixmap):
        super().__init__()
        self.setPixmap(pixmap)
        self.setScaledContents(True)
        self.setMinimumSize(250, 250)

    def resizeEvent(self, event):
        pixmap = self.pixmap()
        if pixmap:
            size = event.size()
            aspect_ratio = pixmap.width() / pixmap.height()
            if size.width() / size.height() > aspect_ratio:
                self.resize(size.height() * aspect_ratio, size.height())
            else:
                self.resize(size.width(), size.width() / aspect_ratio)


def sort_list_widget(list_widget):
    items = [list_widget.item(i).text() for i in range(list_widget.count())]
    items.sort()
    list_widget.clear()
    for item in items:
        list_widget.addItem(item)


def create_tag_widget(label_text):
    widget = QWidget()
    layout = QVBoxLayout()

    title_label = QLabel(label_text)
    box = QComboBox()
    box.setEditable(True)
    box.addItems(["< blank >", "< keep >"])

    layout.addWidget(title_label)
    layout.addWidget(box)

    widget.setLayout(layout)
    return widget


class TagWindow(QWidget):
    def __init__(self):
        super(TagWindow, self).__init__()

        self.setWindowTitle("TagWindow")
        self.setMinimumWidth(350)
        self.setMaximumWidth(700)

        self.main_layout = QVBoxLayout()

        self.filename_widget = create_tag_widget("Title:")
        self.main_layout.addWidget(self.filename_widget)

        '''Date buttons'''
        self.date_layout = QHBoxLayout()

        # Day
        self.day_widget = create_tag_widget("Day:")
        self.date_layout.addWidget(self.day_widget)

        # Month
        self.month_widget = create_tag_widget("Month:")
        self.date_layout.addWidget(self.month_widget)

        # Year
        self.year_widget = create_tag_widget("Year:")
        self.date_layout.addWidget(self.year_widget)

        self.main_layout.addLayout(self.date_layout)

        '''Comments'''
        self.filename_widget = create_tag_widget("Comments:")
        self.main_layout.addWidget(self.filename_widget)

        '''Authors'''
        self.filename_widget = create_tag_widget("Authors:")
        self.main_layout.addWidget(self.filename_widget)

        '''Tag Layout'''
        self.tag_layout = QVBoxLayout()

        # Applied Tags QLineEdit
        self.applied_tags_input = QLineEdit()
        self.applied_tags_input.setPlaceholderText("Enter tags here")
        self.tag_layout.addWidget(self.applied_tags_input)

        # Available Tags
        self.available_tags_widget = QListWidget()
        self.available_tags_widget.itemDoubleClicked.connect(self.transfer_tag_to_applied)
        self.tag_layout.addWidget(self.available_tags_widget)

        self.main_layout.addLayout(self.tag_layout)

        image_widget = AspectRatioLabel(
            QPixmap('D:/Programing/PycharmProjects/Kitepower_Tether_Inspection/Images/Good/frame0.jpg'))
        self.main_layout.addWidget(image_widget)

        self.setLayout(self.main_layout)

        # Populate the available tags list
        self.populate_available_tags()

    def populate_available_tags(self):
        sample_tags = ["Tag1", "Tag2", "Tag3", "Tag5", "Tag4"]
        for tag in sample_tags:
            self.available_tags_widget.addItem(tag)
        # Sort the available tags
        sort_list_widget(self.available_tags_widget)

    def transfer_tag_to_applied(self, item):
        # Check if the item is already in the applied tags input
        current_tags = self.applied_tags_input.text().split(',')
        if item.text() not in current_tags:
            if self.applied_tags_input.text():
                self.applied_tags_input.setText(self.applied_tags_input.text() + ', ' + item.text())
            else:
                self.applied_tags_input.setText(item.text())
        else:
            # Item already exists in the applied tags input
            return


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = TagWindow()
    window.show()
    sys.exit(app.exec())
