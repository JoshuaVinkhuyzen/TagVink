from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QProgressBar
from PySide6.QtGui import QPixmap
import os
from PIL import Image


class ItemList(QWidget):
    def __init__(self, directory_path):
        super(ItemList, self).__init__()

        self.directory_path = directory_path

        self.main_layout = QVBoxLayout()

        # Table Widget to display image filenames and metadata
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)  # Two columns: File Name, Dimensions
        self.table_widget.setHorizontalHeaderLabels(["File Name", "Dimensions"])
        self.main_layout.addWidget(self.table_widget)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.main_layout.addWidget(self.progress_bar)

        self.setLayout(self.main_layout)

        # Populate the table widget with image files and metadata
        self.populate_table()

    def populate_table(self):
        # Clear existing items in case of re-population
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)  # Reset row count

        # Scan directory for image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        image_files = [file for file in os.listdir(self.directory_path)
                       if os.path.isfile(os.path.join(self.directory_path, file))
                       and os.path.splitext(file)[1].lower() in image_extensions]

        num_files = len(image_files)
        if num_files == 0:
            return

        # Update progress bar incrementally
        progress_step = 100 / num_files
        current_progress = 0

        # Add each image file with metadata to the table widget
        for idx, image_file in enumerate(image_files):
            # Get full file path
            file_path = os.path.join(self.directory_path, image_file)

            # Get image dimensions using PIL
            image = Image.open(file_path)
            width, height = image.size

            # Insert a new row
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)

            # Add file name to the first column
            filename_item = QTableWidgetItem(image_file)
            self.table_widget.setItem(row_position, 0, filename_item)

            # Add dimensions to the second column
            dimensions_text = f"{width} x {height}"
            dimensions_item = QTableWidgetItem(dimensions_text)
            self.table_widget.setItem(row_position, 1, dimensions_item)

            # Update progress bar
            current_progress += progress_step
            self.progress_bar.setValue(current_progress)

        # Resize columns to fit content
        self.table_widget.resizeColumnsToContents()


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Example directory path
    directory_path = ('D:/Programing/PycharmProjects/Kitepower_Tether_Inspection/Tether_Inspection_Software/'
                      'Saved_Images/Parallel_1/1_Side')

    item_list_widget = ItemList(directory_path)
    item_list_widget.show()

    sys.exit(app.exec())
