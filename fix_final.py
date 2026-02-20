# Script to fix heatmap alignment, add confidence area with graphs, and auto-clear fields

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix AI Page - better layout with heatmap and result side by side
old_ai_page = '''    # === AI PAGE ===
    def ai_page(self):
        page = QWidget()
        page.setStyleSheet("background: #0a0e17;")
        layout = QVBoxLayout(page)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 10, 20, 10)
        
        layout.addWidget(QLabel("🤖 AI Steganography Detection", styleSheet="font-size: 24px; font-weight: bold; color: #8b5cf6;"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Upload section - centered
        center_layout = QVBoxLayout()
        center_layout.setSpacing(10)
        
        self.ai_label = QLabel("👆 Upload Image for Analysis")
        self.ai_label.setFixedSize(380, 250)
        self.ai_label.setStyleSheet("QLabel { border: 3px dashed #8b5cf6; border-radius: 15px; background: #0f172a; color: #c4b5fd; font-size: 16px; padding: 20px; }")
        center_layout.addWidget(self.ai_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Button row - centered
        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        
        self.upload_ai_btn = QPushButton("📁 Upload Image")
        self.upload_ai_btn.setFixedSize(140, 40)
        self.upload_ai_btn.setStyleSheet("QPushButton { background-color: #8b5cf6; color: white; border: 2px solid #6d28d9; border-radius: 20px; font-size: 14px; font-weight: bold; } QPushButton:hover { background-color: #6d28d9; }")
        self.upload_ai_btn.clicked.connect(self.upload_ai_image)
        
        self.analyze_btn = QPushButton("🔍 Analyze Image")
        self.analyze_btn.setFixedSize(140, 40)
        self.analyze_btn.setStyleSheet("QPushButton { background-color: #10b981; color: white; border: 2px solid #047857; border-radius: 20px; font-size: 14px; font-weight: bold; } QPushButton:hover { background-color: #047857; }")
        self.analyze_btn.clicked.connect(self.analyze_image_action)
        
        btn_row.addStretch(1)
        btn_row.addWidget(self.upload_ai_btn)
        btn_row.addWidget(self.analyze_btn)
        btn_row.addStretch(1)
        
        center_layout.addLayout(btn_row)
        layout.addLayout(center_layout)
        
        # Heatmap preview - centered
        self.heatmap_label = QLabel("LSB Heatmap will appear here")
        self.heatmap_label.setFixedSize(380, 250)
        self.heatmap_label.setStyleSheet("QLabel { border: 2px solid #6d28d9; border-radius: 12px; background: #1e293b; }")
        layout.addWidget(self.heatmap_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Results - centered
        self.result_label = QLabel("Upload image to begin analysis")
        self.result_label.setStyleSheet("QLabel { font-size: 18px; font-weight: bold; padding: 12px; border-radius: 10px; background: #1e293b; min-height: 50px; }")
        layout.addWidget(self.result_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return page'''

new_ai_page = '''    # === AI PAGE ===
    def ai_page(self):
        page = QWidget()
        page.setStyleSheet("background: #0a0e17;")
        layout = QVBoxLayout(page)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 10, 15, 10)
        
        layout.addWidget(QLabel("🤖 AI Steganography Detection", styleSheet="font-size: 22px; font-weight: bold; color: #8b5cf6;"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Upload section - centered
        upload_center = QVBoxLayout()
        upload_center.setSpacing(8)
        
        self.ai_label = QLabel("👆 Upload Image for Analysis")
        self.ai_label.setFixedSize(320, 200)
        self.ai_label.setStyleSheet("QLabel { border: 3px dashed #8b5cf6; border-radius: 12px; background: #0f172a; color: #c4b5fd; font-size: 14px; padding: 15px; }")
        upload_center.addWidget(self.ai_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Button row - centered
        btn_row = QHBoxLayout()
        btn_row.setSpacing(15)
        
        self.upload_ai_btn = QPushButton("📁 Upload Image")
        self.upload_ai_btn.setFixedSize(130, 38)
        self.upload_ai_btn.setStyleSheet("QPushButton { background-color: #8b5cf6; color: white; border: 2px solid #6d28d9; border-radius: 18px; font-size: 13px; font-weight: bold; } QPushButton:hover { background-color: #6d28d9; }")
        self.upload_ai_btn.clicked.connect(self.upload_ai_image)
        
        self.analyze_btn = QPushButton("🔍 Analyze Image")
        self.analyze_btn.setFixedSize(130, 38)
        self.analyze_btn.setStyleSheet("QPushButton { background-color: #10b981; color: white; border: 2px solid #047857; border-radius: 18px; font-size: 13px; font-weight: bold; } QPushButton:hover { background-color: #047857; }")
        self.analyze_btn.clicked.connect(self.analyze_image_action)
        
        btn_row.addStretch(1)
        btn_row.addWidget(self.upload_ai_btn)
        btn_row.addWidget(self.analyze_btn)
        btn_row.addStretch(1)
        
        upload_center.addLayout(btn_row)
        layout.addLayout(upload_center)
        
        # Heatmap and Results side by side - HORIZONTAL layout
        side_by_side = QHBoxLayout()
        side_by_side.setSpacing(15)
        side_by_side.setContentsMargins(10, 5, 10, 5)
        
        # Heatmap section
        heatmap_box = QVBoxLayout()
        heatmap_box.setSpacing(5)
        heatmap_title = QLabel("📊 LSB Heatmap Analysis")
        heatmap_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #8b5cf6;")
        heatmap_box.addWidget(heatmap_title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.heatmap_label = QLabel("No analysis yet")
        self.heatmap_label.setFixedSize(300, 180)
        self.heatmap_label.setStyleSheet("QLabel { border: 2px solid #6d28d9; border-radius: 10px; background: #1e293b; color: #94a3b8; font-size: 12px; }")
        heatmap_box.addWidget(self.heatmap_label, alignment=Qt.AlignmentFlag.AlignCenter)
        side_by_side.addLayout(heatmap_box, 1)
        
        # Confidence/Results section
        result_box = QVBoxLayout()
        result_box.setSpacing(5)
        result_title = QLabel("🎯 Detection Result")
        result_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #10b981;")
        result_box.addWidget(result_title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.result_label = QLabel("Upload image to begin")
        self.result_label.setFixedSize(300, 180)
        self.result_label.setStyleSheet("QLabel { font-size: 16px; font-weight: bold; padding: 15px; border-radius: 10px; background: #1e293b; color: #94a3b8; }")
        result_box.addWidget(self.result_label, alignment=Qt.AlignmentFlag.AlignCenter)
        side_by_side.addLayout(result_box, 1)
        
        layout.addLayout(side_by_side)
        
        return page'''

content = content.replace(old_ai_page, new_ai_page)

# Add auto-clear functionality after operations
# For image page - clear fields after hide
old_hide_image = '''    def hide_image_action(self):
        if not self.image_path or not self.msg_image.toPlainText():
            QMessageBox.warning(self, "Error", "Please upload an image and enter a message!")
            return
        
        key = self.key_image.text() or "defaultkey"
        output_path = QFileDialog.getSaveFileName(self, "Save Stego Image", "", "PNG (*.png)")[0]
        if output_path:
            if self.hide_message_image(self.image_path, self.msg_image.toPlainText(), key, output_path):
                QMessageBox.information(self, "Success", "Message hidden successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to hide message!")'''

new_hide_image = '''    def hide_image_action(self):
        if not self.image_path or not self.msg_image.toPlainText():
            QMessageBox.warning(self, "Error", "Please upload an image and enter a message!")
            return
        
        key = self.key_image.text() or "defaultkey"
        output_path = QFileDialog.getSaveFileName(self, "Save Stego Image", "", "PNG (*.png)")[0]
        if output_path:
            if self.hide_message_image(self.image_path, self.msg_image.toPlainText(), key, output_path):
                QMessageBox.information(self, "Success", "Message hidden successfully!")
                # Auto-clear fields after success
                self.msg_image.clear()
                self.key_image.clear()
            else:
                QMessageBox.critical(self, "Error", "Failed to hide message!")'''

content = content.replace(old_hide_image, new_hide_image)

# For image page - clear fields after extract
old_extract_image = '''    def extract_image_action(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "Please upload an image!")
            return
        
        key = self.key_image.text() or "defaultkey"
        message = self.extract_message_image(self.image_path, key)
        QMessageBox.information(self, "Extracted Message", message)'''

new_extract_image = '''    def extract_image_action(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "Please upload an image!")
            return
        
        key = self.key_image.text() or "defaultkey"
        message = self.extract_message_image(self.image_path, key)
        QMessageBox.information(self, "Extracted Message", message)
        # Auto-clear fields after extract
        self.key_image.clear()'''

content = content.replace(old_extract_image, new_extract_image)

# For video page - clear fields after hide
old_hide_video = '''    def hide_video_action(self):
        if not self.video_path:
            QMessageBox.warning(self, "Error", "Please upload a video!")
            return
        key = self.key_video.text() or "defaultkey"
        output_path = QFileDialog.getSaveFileName(self, "Save Stego Video", "", "MP4 (*.mp4)")[0]
        if output_path:
            if self.hide_message_video(self.video_path, self.msg_video.toPlainText(), key, output_path):
                QMessageBox.information(self, "Success", "Message hidden in video!")
            else:
                QMessageBox.critical(self, "Error", "Failed to process video!")'''

new_hide_video = '''    def hide_video_action(self):
        if not self.video_path:
            QMessageBox.warning(self, "Error", "Please upload a video!")
            return
        key = self.key_video.text() or "defaultkey"
        output_path = QFileDialog.getSaveFileName(self, "Save Stego Video", "", "MP4 (*.mp4)")[0]
        if output_path:
            if self.hide_message_video(self.video_path, self.msg_video.toPlainText(), key, output_path):
                QMessageBox.information(self, "Success", "Message hidden in video!")
                # Auto-clear fields after success
                self.msg_video.clear()
                self.key_video.clear()
            else:
                QMessageBox.critical(self, "Error", "Failed to process video!")'''

content = content.replace(old_hide_video, new_hide_video)

# For video page - clear fields after extract
old_extract_video = '''    def extract_video_action(self):
        if not self.video_path:
            QMessageBox.warning(self, "Error", "Please upload a video with hidden message!")
            return
        
        key = self.key_video.text() or "defaultkey"
        try:
            message = extract_message_from_video(self.video_path, key)
            QMessageBox.information(self, "Extracted Message", f"Message found:\\n\\n{message}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to extract message!\\n\\nPossible reasons:\\n- Wrong key\\n- No hidden message in this video\\n- Video format not supported\\n\\nError: {str(e)}")'''

new_extract_video = '''    def extract_video_action(self):
        if not self.video_path:
            QMessageBox.warning(self, "Error", "Please upload a video with hidden message!")
            return
        
        key = self.key_video.text() or "defaultkey"
        try:
            message = extract_message_from_video(self.video_path, key)
            QMessageBox.information(self, "Extracted Message", f"Message found:\\n\\n{message}")
            # Auto-clear key after extract
            self.key_video.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to extract message!\\n\\nPossible reasons:\\n- Wrong key\\n- No hidden message in this video\\n- Video format not supported\\n\\nError: {str(e)}")'''

content = content.replace(old_extract_video, new_extract_video)

# Fix window size - make it smaller to fit better
content = content.replace(
    'self.setFixedSize(1100, 750)',
    'self.setFixedSize(950, 680)'
)

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("All final fixes applied successfully!")
print("- Heatmap aligned side-by-side with results")
print("- Auto-clear fields after operations")
print("- Smaller window size for better fit")
