from PySide6.QtWidgets import QLabel


class AspectRatioLabel(QLabel):
    def __init__(self, pixmap):
        super().__init__()
        self.setPixmap(pixmap)
        self.setScaledContents(True)
        self.setMinimumSize(456, 256)

    def resizeEvent(self, event):
        pixmap = self.pixmap()
        if pixmap:
            size = event.size()
            aspect_ratio = pixmap.width() / pixmap.height()
            if size.width() / size.height() > aspect_ratio:
                self.resize(size.height() * aspect_ratio, size.height())
            else:
                self.resize(size.width(), size.width() / aspect_ratio)
