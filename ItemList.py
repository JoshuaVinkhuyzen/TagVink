from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMainWindow, QLabel, QProgressBar, \
    QApplication, QPushButton, QMessageBox
from PySide6.QtCore import Qt, QThread, Signal
import os
import exiftool


class ImageLoaderThread(QThread):
    progress_updated = Signal(int, int, int)  # Signal for progress updates
    image_info_ready = Signal(dict)  # Signal for emitting image metadata
    finished_loading = Signal()  # Signal for indicating loading finished

    def __init__(self, directory_path):
        super().__init__()
        self.directory_path = directory_path
        self.et = exiftool.ExifTool(executable='./tools/exiftool.exe')  # Update to use the bundled ExifTool
        self.cancelled = False

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

        try:
            with self.et:
                for idx, image_file in enumerate(image_files):
                    if self.cancelled:
                        break

                    file_path = os.path.join(self.directory_path, image_file)
                    metadata = self.et.execute_json('-G', '-j', file_path)

                    # Extract metadata from JSON response
                    filename = os.path.basename(file_path)
                    path = file_path
                    tags = metadata[0].get('Keywords', '')
                    title = metadata[0].get('Title', '')
                    subject = metadata[0].get('Subject', '')
                    author = metadata[0].get('Creator', '')
                    date_taken = metadata[0].get('DateTimeOriginal', '')
                    width = metadata[0].get('ImageWidth', 0)
                    height = metadata[0].get('ImageHeight', 0)
                    dimensions = f"{width} x {height}"

                    # Emit signal to update progress
                    current_progress += progress_step
                    self.progress_updated.emit(int(current_progress), idx + 1, num_files)

                    # Create metadata dictionary
                    image_metadata = {
                        "filename": filename,
                        "path": path,
                        "tags": tags,
                        "title": title,
                        "subject": subject,
                        "author": author,
                        "date_taken": date_taken,
                        "dimensions": dimensions
                    }

                    # Emit signal with image information
                    self.image_info_ready.emit(image_metadata)

        except Exception as e:
            print(f"Error loading images: {e}")

        finally:
            self.finished_loading.emit()

    def cancel_loading(self):
        self.cancelled = True

    def update_metadata(self, file_path, metadata):
        try:
            # Construct command to update metadata using ExifTool
            command = []
            for key, value in metadata.items():
                command.extend(['-' + key, value])
            command.append(file_path)

            # Execute the command to update metadata
            self.et.execute(*command)

        except Exception as e:
            print(f"Error updating metadata for {file_path}: {e}")


class ProgressBarWindow(QMainWindow):
    def __init__(self, image_loader_thread):
        super().__init__()
        self.setWindowTitle("Loading Images")
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        # Ensure the window stays on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.progress_label = QLabel("Loading 0 of 0 images")

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_loading)

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.cancel_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image_loader_thread = image_loader_thread
        self.image_loader_thread.progress_updated.connect(self.update_progress)
        self.image_loader_thread.finished_loading.connect(self.loading_finished)

    def update_progress(self, value, current, total):
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"Loading {current} of {total} images")

    def cancel_loading(self):
        self.image_loader_thread.cancel_loading()
        self.close()

    def loading_finished(self):
        self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Cancel Loading', 'Are you sure you want to cancel loading?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.image_loader_thread.cancel_loading()
            event.accept()
        else:
            event.ignore()


class ItemList(QWidget):
    def __init__(self, directory_path):
        super().__init__()

        self.directory_path = directory_path

        self.main_layout = QVBoxLayout()

        # Table Widget to display image filenames and metadata
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(
            8)  # Columns: Filename, Path, Tags, Title, Subject, Author, Date taken, Dimensions
        self.table_widget.setHorizontalHeaderLabels(
            ["Filename", "Path", "Tags", "Title", "Subject", "Author", "Date taken", "Dimensions"])
        self.main_layout.addWidget(self.table_widget)

        # Update Metadata Button
        self.update_metadata_button = QPushButton("Update Metadata")
        self.update_metadata_button.clicked.connect(self.update_metadata)
        self.main_layout.addWidget(self.update_metadata_button)

        self.setLayout(self.main_layout)

        # Connect signals and start image loading thread
        self.image_loader_thread = ImageLoaderThread(self.directory_path)
        self.image_loader_thread.progress_updated.connect(self.update_progress)
        self.image_loader_thread.finished_loading.connect(self.loading_finished)
        self.image_loader_thread.image_info_ready.connect(self.add_image_info_to_table)

        # Show progress bar window
        self.progress_window = ProgressBarWindow(self.image_loader_thread)
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

    def update_metadata(self):
        for row in range(self.table_widget.rowCount()):
            file_path = self.table_widget.item(row, 1).text()
            metadata = {
                "Keywords": self.table_widget.item(row, 2).text(),
                "Title": self.table_widget.item(row, 3).text(),
                "Subject": self.table_widget.item(row, 4).text(),
                "Creator": self.table_widget.item(row, 5).text(),
                "DateTimeOriginal": self.table_widget.item(row, 6).text()
            }
            self.image_loader_thread.update_metadata(file_path, metadata)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # Example directory path
    directory_path = 'C:/Users/Joshua/OneDrive/Pictures/Saved Pictures'

    item_list_widget = ItemList(directory_path)
    item_list_widget.show()

    sys.exit(app.exec())
