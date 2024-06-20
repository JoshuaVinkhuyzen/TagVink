from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMainWindow, QLabel, QProgressBar, \
    QApplication
from PySide6.QtCore import Qt, QThread, Signal
from PIL import Image
import os


class ImageLoaderThread(QThread):
    progress_updated = Signal(int, int, int)  # Current progress, current count, total count
    finished_loading = Signal()
    image_info_ready = Signal(dict)  # Emit a dictionary with all the metadata

    def __init__(self, directory_path):
        super().__init__()
        self.directory_path = directory_path

    def run(self):
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        image_files = [file for file in os.listdir(self.directory_path)
                       if os.path.isfile(os.path.join(self.directory_path, file))
                       and os.path.splitext(file)[1].lower() in image_extensions]

        num_files = len(image_files)
        if num_files == 0:
            self.finished_loading.emit()
            return

        progress_step = 100 / num_files
        current_progress = 0

        for idx, image_file in enumerate(image_files):
            file_path = os.path.join(self.directory_path, image_file)
            image = Image.open(file_path)
            width, height = image.size

            # Mock metadata for demonstration
            metadata = {
                "filename": image_file,
                "path": file_path,
                "tags": "Tag1, Tag2",
                "title": "Sample Title",
                "subject": "Sample Subject",
                "author": "Sample Author",
                "date_taken": "2024-06-19",
                "dimensions": f"{width} x {height}"
            }

            # Emit signal to update progress
            current_progress += progress_step
            self.progress_updated.emit(int(current_progress), idx + 1, num_files)

            # Emit signal with image information
            self.image_info_ready.emit(metadata)

        self.finished_loading.emit()


class ProgressBarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading Images")

        # Set a fixed size for the window
        self.setFixedSize(300, 100)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        self.progress_label = QLabel("Loading 0 of 0 images")

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_progress(self, value, current, total):
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"Loading {current} of {total} images")


class ItemList(QWidget):
    def __init__(self, directory_path):
        super().__init__()

        self.directory_path = directory_path

        self.setWindowTitle("TagWindow")
        self.setMinimumWidth(350)

        self.main_layout = QVBoxLayout()

        # Table Widget to display image filenames and metadata
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(
            8)  # Columns: Filename, Path, Tags, Title, Subject, Author, Date taken, Dimensions
        self.table_widget.setHorizontalHeaderLabels(
            ["Filename", "Path", "Tags", "Title", "Subject", "Author", "Date taken", "Dimensions"])
        self.main_layout.addWidget(self.table_widget)

        self.setLayout(self.main_layout)

        # Connect signals and start image loading thread
        self.image_loader_thread = ImageLoaderThread(self.directory_path)
        self.image_loader_thread.progress_updated.connect(self.update_progress)
        self.image_loader_thread.finished_loading.connect(self.loading_finished)
        self.image_loader_thread.image_info_ready.connect(self.add_image_info_to_table)

        # Show progress bar window
        self.progress_window = ProgressBarWindow()
        self.progress_window.show()

        self.image_loader_thread.start()

    def update_progress(self, value, current, total):
        self.progress_window.update_progress(value, current, total)

    def add_image_info_to_table(self, metadata):
        # Insert a new row
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        # Populate the row with metadata
        self.table_widget.setItem(row_position, 0, QTableWidgetItem(metadata["filename"]))
        self.table_widget.setItem(row_position, 1, QTableWidgetItem(metadata["path"]))
        self.table_widget.setItem(row_position, 2, QTableWidgetItem(metadata["tags"]))
        self.table_widget.setItem(row_position, 3, QTableWidgetItem(metadata["title"]))
        self.table_widget.setItem(row_position, 4, QTableWidgetItem(metadata["subject"]))
        self.table_widget.setItem(row_position, 5, QTableWidgetItem(metadata["author"]))
        self.table_widget.setItem(row_position, 6, QTableWidgetItem(metadata["date_taken"]))
        self.table_widget.setItem(row_position, 7, QTableWidgetItem(metadata["dimensions"]))

        # Resize columns to fit content
        self.table_widget.resizeColumnsToContents()

    def loading_finished(self):
        # Close progress bar window once loading is complete
        self.progress_window.close()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # Example directory path
    directory_path = 'C:/Users/Joshua/OneDrive/Pictures/Saved Pictures'

    item_list_widget = ItemList(directory_path)
    item_list_widget.show()

    sys.exit(app.exec())
