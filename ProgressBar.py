from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QProgressBar, QLabel, QWidget


class ProgressBarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading Images")
        self.setGeometry(400, 300, 300, 100)

        self.setFixedSize(300, 60)

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
