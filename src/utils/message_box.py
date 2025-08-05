from PyQt6.QtWidgets import QMessageBox, QWidget


def show_message(
    parent: QWidget, title: str, message: str, icon=QMessageBox.Icon.Information
):
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(icon)
    msg_box.setModal(True)
    msg_box.adjustSize()
    # Đưa message box ra giữa màn hình
    screen = msg_box.screen()
    if screen:
        screen_geometry = screen.geometry()
        msg_box_geometry = msg_box.frameGeometry()
        center_point = screen_geometry.center()
        msg_box_geometry.moveCenter(center_point)
        msg_box.move(msg_box_geometry.topLeft())
    msg_box.exec()
