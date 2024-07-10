from PySide6.QtWidgets import QDialog, QVBoxLayout, QRadioButton, QPushButton, QApplication
from PySide6.QtCore import QSettings


class OptionsWindow(QDialog):
    def __init__(self, parent=None):
        super(OptionsWindow, self).__init__(parent)
        self.setWindowTitle("Options")

        self.settings = QSettings("YourCompany", "YourAppName")

        layout = QVBoxLayout()

        self.default_theme_rb = QRadioButton("Default")
        self.light_theme_rb = QRadioButton("Light")
        self.dark_theme_rb = QRadioButton("Dark")

        # Load current theme setting
        current_theme = self.settings.value("theme", "default")
        if current_theme == "light":
            self.light_theme_rb.setChecked(True)
        elif current_theme == "dark":
            self.dark_theme_rb.setChecked(True)
        else:
            self.default_theme_rb.setChecked(True)

        layout.addWidget(self.default_theme_rb)
        layout.addWidget(self.light_theme_rb)
        layout.addWidget(self.dark_theme_rb)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_settings(self):
        if self.light_theme_rb.isChecked():
            self.settings.setValue("theme", "light")
        elif self.dark_theme_rb.isChecked():
            self.settings.setValue("theme", "dark")
        else:
            self.settings.setValue("theme", "default")

        self.accept()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    options_window = OptionsWindow()
    options_window.exec()
    sys.exit(app.exec())
