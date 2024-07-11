from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMainWindow, QLabel, QProgressBar, QApplication
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
        self._is_running = True

    def run(self):
        if not self.directory_path:
            self.finished_loading.emit()
            return

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
            if not self._is_running:
                break

            file_path = os.path.join(self.directory_path, image_file)
            image = Image.open(file_path)
            width, height = image.size

            metadata = {
                "filename": image_file,
                "path": file_path,
                "tags": None,
                "title": None,
                "subject": None,
                "author": None,
                "date_taken": None,
                "dimensions": f"{width} x {height}"
            }

            current_progress += progress_step
            self.progress_updated.emit(int(current_progress), idx + 1, num_files)
            self.image_info_ready.emit(metadata)

        self.finished_loading.emit()

    def stop(self):
        self._is_running = False


class ProgressBarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading Images")
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
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

    def update_progress(self, value, current, total):
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"Loading {current} of {total} images")


class ItemList(QWidget):
    def __init__(self, directory_path):
        super().__init__()
        self.directory_path = directory_path
        self.setMinimumWidth(350)
        self.main_layout = QVBoxLayout()
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(
            ["Filename", "Path", "Tags", "Title", "Subject", "Author", "Date taken", "Dimensions"])
        self.main_layout.addWidget(self.table_widget)
        self.setLayout(self.main_layout)
        self.image_loader_thread = None
        self.progress_window = ProgressBarWindow()
        self.start_loading()

    def start_loading(self):
        if not self.directory_path:
            return
        if self.image_loader_thread:
            self.image_loader_thread.stop()
            self.image_loader_thread.wait()
        self.image_loader_thread = ImageLoaderThread(self.directory_path)
        self.image_loader_thread.progress_updated.connect(self.update_progress)
        self.image_loader_thread.finished_loading.connect(self.loading_finished)
        self.image_loader_thread.image_info_ready.connect(self.add_image_info_to_table)
        self.progress_window.show()
        self.image_loader_thread.start()

    def update_progress(self, value, current, total):
        self.progress_window.update_progress(value, current, total)

    def add_image_info_to_table(self, metadata):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        self.table_widget.setItem(row_position, 0, QTableWidgetItem(metadata["filename"]))
        self.table_widget.setItem(row_position, 1, QTableWidgetItem(metadata["path"]))
        self.table_widget.setItem(row_position, 2, QTableWidgetItem(metadata["tags"] if metadata["tags"] else ""))
        self.table_widget.setItem(row_position, 3, QTableWidgetItem(metadata["title"] if metadata["title"] else ""))
        self.table_widget.setItem(row_position, 4, QTableWidgetItem(metadata["subject"] if metadata["subject"] else ""))
        self.table_widget.setItem(row_position, 5, QTableWidgetItem(metadata["author"] if metadata["author"] else ""))
        self.table_widget.setItem(row_position, 6, QTableWidgetItem(metadata["date_taken"] if metadata["date_taken"] else ""))
        self.table_widget.setItem(row_position, 7, QTableWidgetItem(metadata["dimensions"]))
        self.table_widget.resizeColumnsToContents()

    def loading_finished(self):
        self.progress_window.close()

    def set_directory_path(self, directory_path):
        self.directory_path = directory_path

    def reload_images(self):
        self.table_widget.setRowCount(0)  # Clear the table
        self.start_loading()

    def clear(self):
        self.table_widget.setRowCount(0)  # Clear the table


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    directory_path = 'C:/Users/Joshua/OneDrive/Pictures/Saved Pictures'
    item_list_widget = ItemList(directory_path)
    item_list_widget.show()
    sys.exit(app.exec())
