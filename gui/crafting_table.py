import os
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem
from PyQt5.QtGui import QPen, QBrush, QColor, QPixmap
from PyQt5.QtCore import QRectF, Qt

class CraftingTableWidget(QGraphicsView):
    def __init__(self, rows=3, cols=3, cell_size=80, margin=20, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.margin = margin
        self.grid_width = self.cols * self.cell_size  
        self.grid_height = self.rows * self.cell_size   
        self.bg_width = (self.grid_width + 4 * self.margin)+100 
        self.bg_height = (self.grid_height + 4 * self.margin)+100 

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, self.bg_width, self.bg_height)
        self.setFixedSize(self.bg_width+50, self.bg_height+50)
        self._load_background()
        self._draw_grid()
        self.items = {}

    def _load_background(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(base_dir, "..", "resources", "images", "crafting_table_bg.png")
        bg_path = bg_path.replace("\\", "/")
        pixmap = QPixmap(bg_path)
        if pixmap.isNull():
            print(f"Error: Could not load background image from {bg_path}")
            return
        scaled_pixmap = pixmap.scaled(self.bg_width, self.bg_height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.scene.setBackgroundBrush(QBrush(scaled_pixmap))

    def _draw_grid(self):
        pen = QPen(QColor("black"))
        cell_color = QColor("lightgray")
        cell_color.setAlpha(196)
        brush = QBrush(cell_color)
        offset_x = (self.bg_width - self.grid_width) / 2
        offset_y = (self.bg_height - self.grid_height) / 2
        for row in range(self.rows):
            for col in range(self.cols):
                x = offset_x + col * self.cell_size
                y = offset_y + row * self.cell_size
                rect = QRectF(x, y, self.cell_size, self.cell_size)
                cell = QGraphicsRectItem(rect)
                cell.setPen(pen)
                cell.setBrush(brush)
                self.scene.addItem(cell)


    def update_from_ast(self, recipe_ast):
        for item in self.items.values():
            self.scene.removeItem(item)
        self.items.clear()

        offset_x = (self.bg_width - self.grid_width) / 2
        offset_y = (self.bg_height - self.grid_height) / 2

        for item in recipe_ast.get("input", []):
            position = item["position"]
            quantity = item["quantity"]
            material = item["material"]
            try:
                row, col = int(position[0]), int(position[1])
            except Exception as e:
                print(f"Invalid position format for item: {item}")
                continue

            base_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_dir, "..", "resources", "images", f"{material}.png").replace("\\", "/")
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                print(f"Image not found for material: {material}")
                continue

            pixmap = pixmap.scaled(self.cell_size - 10, self.cell_size - 10, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pixmap_item = QGraphicsPixmapItem(pixmap)
        
            x = offset_x + col * self.cell_size + (self.cell_size - pixmap.width()) / 2
            y = offset_y + row * self.cell_size + (self.cell_size - pixmap.height()) / 2
            pixmap_item.setPos(x, y)

            self.scene.addItem(pixmap_item)
            self.items[(row, col)] = pixmap_item
