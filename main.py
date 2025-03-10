import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFontDatabase, QFont
from PyQt5.QtCore import Qt
from gui.code_editor import CodeEditor
from gui.debug_panel import DebugPanel
from gui.crafting_table import CraftingTableWidget
from gui.template_panel import TemplatePanel
from controller.interpreter_controller import InterpreterController

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Minecraft Crafting Interpreter")
        self.setGeometry(100, 100, 1200, 800)
        self.init_ui()

    def init_ui(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        cobblestone_path = os.path.join(base_dir, "resources/images/cobblestone_background.png").replace("\\", "/")
        cobblestone_pixmap = QPixmap(cobblestone_path)
        if not cobblestone_pixmap.isNull():
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(cobblestone_pixmap))
            self.setPalette(palette)
            self.setAutoFillBackground(True)
        else:
            print(f"Background image not found: {cobblestone_path}")

        dark_brown = "#4E342E"   
        light_brown = "#DEB887"  
        birch_color = "#F0EAD6" 

        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(10)

        left_panel = QWidget()
        left_panel.setStyleSheet(f"background-color: {dark_brown};")
        left_panel.setMaximumWidth(800)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(10)
        
        left_content = QWidget()
        left_content.setStyleSheet(f"background-color: {light_brown};")
        left_content_layout = QVBoxLayout(left_content)
        left_content_layout.setContentsMargins(10, 10, 10, 10)
        left_content_layout.setSpacing(10)
        
        self.code_editor = CodeEditor()
        self.code_editor.setStyleSheet(f"background-color: {birch_color};")
        self.debug_panel = DebugPanel()
        self.debug_panel.setStyleSheet(f"background-color: {birch_color};")
        self.run_button = QPushButton("Run Code")
        self.run_button.setStyleSheet("background-color: white;")
        self.run_button.clicked.connect(self.run_code)
        
        left_content_layout.addWidget(self.code_editor)
        left_content_layout.addWidget(self.debug_panel)
        left_content_layout.addWidget(self.run_button)
        
        left_layout.addWidget(left_content)

        right_panel = QWidget()
        right_panel.setStyleSheet(f"background-color: {dark_brown};")
        right_panel.setMaximumWidth(600)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(10)
        
        right_content = QWidget()
        right_content.setStyleSheet(f"background-color: {light_brown};")
        right_content_layout = QVBoxLayout(right_content)
        right_content_layout.setContentsMargins(10, 10, 10, 10)
        right_content_layout.setSpacing(10)
        right_content_layout.addStretch()
        self.crafting_table = CraftingTableWidget()
        right_content_layout.addWidget(self.crafting_table, alignment=Qt.AlignCenter)
        right_content_layout.addStretch()
        self.template_panel = TemplatePanel("templates", self.code_editor)
        self.template_panel.setStyleSheet(f"background-color: {birch_color};")
        right_content_layout.addWidget(self.template_panel, 0)
        right_layout.addWidget(right_content)
        
        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(right_panel, 1)
        
        self.interpreter_controller = InterpreterController(
            self.code_editor, self.crafting_table, self.debug_panel
        )

    def run_code(self):
        self.interpreter_controller.interpret_code()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_dir, "resources/fonts/Minecraftia.ttf").replace("\\", "/")
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                minecraft_font = QFont(families[0], 10)
                app.setFont(minecraft_font)
            else:
                print("No font families found after loading Minecraftia.ttf")
        else:
            print("Failed to load Minecraftia.ttf")
    else:
        print(f"Font file not found: {font_path}")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())