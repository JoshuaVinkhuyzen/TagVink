from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QProgressBar


class ProgressBarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading Images")
        self.setGeometry(400, 300, 300, 100)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
