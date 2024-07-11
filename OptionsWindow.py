from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QDialog, QVBoxLayout, QRadioButton, QDialogButtonBox, QLabel, QButtonGroup


class OptionsWindow(QDialog):
    def __init__(self, parent=None):
        super(OptionsWindow, self).__init__(parent)
        self.setWindowTitle("Options")

        self.settings = QSettings("YourCompany", "YourAppName")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select Theme:"))

        self.theme_group = QButtonGroup()

        self.default_radio = QRadioButton("Default")
        self.light_radio = QRadioButton("Light")
        self.dark_radio = QRadioButton("Dark")
        self.blue_radio = QRadioButton("Blue")
        self.green_radio = QRadioButton("Green")

        self.theme_group.addButton(self.default_radio)
        self.theme_group.addButton(self.light_radio)
        self.theme_group.addButton(self.dark_radio)
        self.theme_group.addButton(self.blue_radio)
        self.theme_group.addButton(self.green_radio)

        layout.addWidget(self.default_radio)
        layout.addWidget(self.light_radio)
        layout.addWidget(self.dark_radio)
        layout.addWidget(self.blue_radio)
        layout.addWidget(self.green_radio)

        self.load_settings()

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def load_settings(self):
        theme = self.settings.value("theme", "default")
        if theme == "light":
            self.light_radio.setChecked(True)
        elif theme == "dark":
            self.dark_radio.setChecked(True)
        elif theme == "blue":
            self.blue_radio.setChecked(True)
        elif theme == "green":
            self.green_radio.setChecked(True)
        else:
            self.default_radio.setChecked(True)

    def accept(self):
        if self.light_radio.isChecked():
            self.settings.setValue("theme", "light")
        elif self.dark_radio.isChecked():
            self.settings.setValue("theme", "dark")
        elif self.blue_radio.isChecked():
            self.settings.setValue("theme", "blue")
        elif self.green_radio.isChecked():
            self.settings.setValue("theme", "green")
        else:
            self.settings.setValue("theme", "default")

        super().accept()
