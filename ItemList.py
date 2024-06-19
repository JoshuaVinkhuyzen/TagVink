from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QProgressBar, QMainWindow
from PySide6.QtCore import Qt, QThread, Signal
from PIL import Image
import os

import ProgressBar


class ImageLoaderThread(QThread):
    progress_updated = Signal(int, int, int)  # Current progress, current count, total count
    finished_loading = Signal()
    image_info_ready = Signal(str, int, int)  # Custom signal with filename, width, height

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

            # Emit signal to update progress
            current_progress += progress_step
            self.progress_updated.emit(int(current_progress), idx + 1, num_files)

            # Emit signal with image information
            self.image_info_ready.emit(image_file, width, height)

        self.finished_loading.emit()


class ItemList(QWidget):
    def __init__(self, directory_path):
        super().__init__()

        self.setWindowTitle("Item List")
        self.setMinimumSize(400, 300)

        self.directory_path = directory_path

        self.main_layout = QVBoxLayout()

        # Table Widget to display image filenames and metadata
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)  # Two columns: File Name, Dimensions
        self.table_widget.setHorizontalHeaderLabels(["File Name", "Dimensions"])
        self.main_layout.addWidget(self.table_widget)

        self.setLayout(self.main_layout)

        # Connect signals and start image loading thread
        self.image_loader_thread = ImageLoaderThread(self.directory_path)
        self.image_loader_thread.progress_updated.connect(self.update_progress)
        self.image_loader_thread.finished_loading.connect(self.loading_finished)
        self.image_loader_thread.image_info_ready.connect(self.add_image_info_to_table)

        # Show progress bar window
        self.progress_window = ProgressBar.ProgressBarWindow()
        self.progress_window.show()

        self.image_loader_thread.start()

    def update_progress(self, value, current, total):
        self.progress_window.update_progress(value, current, total)

    def add_image_info_to_table(self, image_file, width, height):
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

        # Resize columns to fit content
        self.table_widget.resizeColumnsToContents()

    def loading_finished(self):
        # Close progress bar window once loading is complete
        self.progress_window.close()


# Example usage
if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Example directory path
    directory_path = 'C:/Users/Joshua/OneDrive/Pictures/Saved Pictures'

    item_list_widget = ItemList(directory_path)
    item_list_widget.show()

    sys.exit(app.exec())
