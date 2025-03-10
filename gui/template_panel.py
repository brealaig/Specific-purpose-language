import os
from PyQt5.QtWidgets import QListWidget

class TemplatePanel(QListWidget):
    def __init__(self, templates_dir, code_editor, parent=None):
        super(TemplatePanel, self).__init__(parent)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = os.path.join(base_dir, "..", templates_dir)
        self.code_editor = code_editor
        self.load_templates()
        self.itemClicked.connect(self.load_template)

    def load_templates(self):
        self.clear()
        try:
            for filename in os.listdir(self.templates_dir):
                if filename.endswith('.txt'):
                    self.addItem(filename)
        except Exception as e:
            print("Error loading templates:", e)

    def load_template(self, item):
        filepath = os.path.join(self.templates_dir, item.text())
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()
            self.code_editor.setPlainText(code)
        except Exception as e:
            print("Error loading template:", e)
