from PyQt6.QtCore import QPointF, QRectF, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import (
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
)


class GraphicVideo(QGraphicsView):
    box_items_signal = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Tạo scene và gắn vào view
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Tối ưu hiển thị mượt
        self.setRenderHints(
            self.renderHints() | QPainter.RenderHint.SmoothPixmapTransform
        )
        self.setMinimumSize(QSize(800, 400))
        self.pixmap_item = None  # Ảnh hiện tại (frame)
        self.box_items = [None]  # Danh sách bounding boxes

        # --- Biến dùng để vẽ bằng chuột ---
        self.drawing = False
        self.origin = QPointF()
        self.current_rect = None

    def show_frame(self, frame):
        """Hiển thị 1 frame (QImage or QPixmap) lên view"""
        if isinstance(frame, QImage):
            pixmap = QPixmap.fromImage(frame)
        elif isinstance(frame, QPixmap):
            pixmap = frame
        else:
            raise ValueError("Unsupported frame type")

        # Nếu đã có ảnh cũ, cập nhật lại thay vì clear toàn bộ
        if self.pixmap_item:
            self.scene.removeItem(self.pixmap_item)

        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)
        self.pixmap_item.setZValue(-1)  # Đảm bảo ảnh luôn ở dưới box

        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def draw_box(self, x, y, w, h, color=Qt.GlobalColor.red, thickness=2):
        """Vẽ bounding box lên frame"""
        rect = QGraphicsRectItem(x, y, w, h)
        rect.setPen(QPen(color, thickness))
        self.scene.addItem(rect)
        self.box_items.append(rect)

    def clear_boxes(self):
        """Xóa toàn bộ bounding box đã vẽ"""
        for item in self.box_items:
            self.scene.removeItem(item)
        self.box_items = []

    # --- Xử lý chuột ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            current_pos = self.mapToScene(event.pos())
            image_rect = (
                self.pixmap_item.boundingRect() if self.pixmap_item else QRectF()
            )
            if (
                current_pos.x() < image_rect.left()
                or current_pos.x() > image_rect.right()
            ):
                return
            if (
                current_pos.y() < image_rect.top()
                or current_pos.y() > image_rect.bottom()
            ):
                return
            self.drawing = True
            self.origin = self.mapToScene(event.pos())
            self.current_rect = QGraphicsRectItem()
            self.current_rect.setPen(QPen(Qt.GlobalColor.red, 2))
            self.scene.addItem(self.current_rect)

    def mouseMoveEvent(self, event):
        if self.drawing and self.current_rect:
            current_pos = self.mapToScene(event.pos())
            image_rect = (
                self.pixmap_item.boundingRect() if self.pixmap_item else QRectF()
            )

            # Clamp current_pos vào trong ảnh
            x = min(max(current_pos.x(), image_rect.left()), image_rect.right())
            y = min(max(current_pos.y(), image_rect.top()), image_rect.bottom())

            clamped_pos = QPointF(x, y)
            rect = QRectF(self.origin, clamped_pos).normalized()
            self.current_rect.setRect(rect)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            if self.current_rect:
                self.clear_boxes()
                self.box_items.append(self.current_rect)
                self.box_items_signal.emit(self.current_rect)
                self.current_rect = None
