from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont

class DebugPanel(QTextEdit):
    def __init__(self, parent=None):
        super(DebugPanel, self).__init__(parent)
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 10))
        self.setStyleSheet("background-color: #f0f0f0; color: black;")

    def append_message(self, message):
        self.append(message)

