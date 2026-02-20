from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog,
    QTextEdit, QVBoxLayout, QHBoxLayout,
    QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt


class VideoUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Steganography")
        self.setFixedSize(900, 600)
        self.setStyleSheet("background:#0f172a; color:white;")

        self.video_path = None
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)

        self.video_label = QLabel("No Video Selected")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("border:2px dashed #38bdf8; padding:30px;")

        upload_btn = QPushButton("Upload Video")
        upload_btn.setStyleSheet("background:#2563eb; padding:12px; border-radius:8px;")
        upload_btn.clicked.connect(self.upload_video)

        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Secret message")

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Secret key")

        btns = QHBoxLayout()

        hide_btn = QPushButton("Hide & Save")
        hide_btn.setStyleSheet("background:#16a34a; padding:12px; border-radius:8px;")
        hide_btn.clicked.connect(self.hide_data)

        extract_btn = QPushButton("Extract")
        extract_btn.setStyleSheet("background:#f59e0b; padding:12px; border-radius:8px;")
        extract_btn.clicked.connect(self.extract_data)

        btns.addWidget(hide_btn)
        btns.addWidget(extract_btn)

        layout.addWidget(self.video_label)
        layout.addWidget(upload_btn)
        layout.addWidget(self.text_box)
        layout.addWidget(self.key_input)
        layout.addLayout(btns)

    def upload_video(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Video", "", "Videos (*.mp4 *.avi)"
        )
        if path:
            self.video_path = path
            self.video_label.setText(path.split("/")[-1])

    def hide_data(self):
        from stego.video_stego import hide_video_message

        if not self.video_path:
            QMessageBox.warning(self, "Error", "Upload video first")
            return

        msg = self.text_box.toPlainText().strip()
        key = self.key_input.text().strip()

        if not msg or not key:
            QMessageBox.warning(self, "Error", "Message and key required")
            return

        save, _ = QFileDialog.getSaveFileName(
            self, "Save Video", "", "MP4 (*.mp4)"
        )

        if save:
            hide_video_message(self.video_path, msg, key, save)
            QMessageBox.information(self, "Success", "Message hidden")
            self.text_box.clear()
            self.key_input.clear()

    def extract_data(self):
        from stego.video_stego import extract_video_message

        try:
            msg = extract_video_message(self.video_path, self.key_input.text())
            self.text_box.setPlainText(msg)
            self.text_box.setReadOnly(True)
        except Exception as e:
            QMessageBox.warning(self, "Failed", str(e))
