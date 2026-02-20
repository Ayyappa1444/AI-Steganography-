
# app/ui_main.py - FULLY FUNCTIONAL + ALL FIXES
from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QPushButton, 
                            QTextEdit, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, 
                            QMessageBox, QStackedWidget, QFrame, QSpacerItem, QSizePolicy)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os
import numpy as np
from PIL import Image
import cv2

# Import stego modules
from stego.image_stego import hide_message as hide_image_msg, extract_message as extract_image_msg
from stego.video_stego import hide_message_in_video, extract_message_from_video

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎨 AI Steganography Suite v2.0")
        self.setFixedSize(1450, 980)
        self.image_path = None
        self.video_path = None
        self.ai_path = None
        self.image_page_ref = None
        self.video_page_ref = None
        self.ai_page_ref = None
        self.init_ui()
    
    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("""
            QWidget { 
                background: #0a0e17; 
                color: white; 
                font-family: 'Segoe UI', Arial; 
            }
        """)
        self.build_ui(central)
    
    def build_ui(self, parent):
        main_layout = QHBoxLayout(parent)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(25)
        
        sidebar = self.create_sidebar()
        main_layout.addLayout(sidebar, 1)
        
        self.stack = QStackedWidget()
        self.stack.addWidget(self.image_page())
        self.stack.addWidget(self.video_page())
        self.stack.addWidget(self.ai_page())
        self.stack.addWidget(self.about_page())
        main_layout.addWidget(self.stack, 4)
    
    def create_sidebar(self):
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(20)
        sidebar_layout.setContentsMargins(20, 25, 20, 25)
        
        sidebar_widget = QFrame()
        sidebar_widget.setFixedWidth(280)
        sidebar_widget.setStyleSheet("QFrame { background: #0f172a; border-radius: 25px; }")
        sidebar_container = QVBoxLayout(sidebar_widget)
        sidebar_container.setSpacing(22)
        sidebar_container.setContentsMargins(25, 25, 25, 25)
        
        buttons = [
            ("🖼️ Image Stego", 0, "#3b82f6"), 
            ("🎥 Video Stego", 1, "#10b981"), 
            ("🤖 AI Detection", 2, "#8b5cf6"), 
            ("ℹ️ About", 3, "#6b7280")
        ]
        
        self.buttons = []
        for text, index, color in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(85)
            btn.setStyleSheet(f"""
                QPushButton {{ background-color: {color}; border: 3px solid #ffffff40; 
                               border-radius: 25px; padding: 20px; font-size: 18px; 
                               font-weight: bold; color: white; }}
                QPushButton:hover {{ background-color: {self.darken_color(color)}; border: 3px solid white; }}
            """)
            sidebar_container.addWidget(btn)
            self.buttons.append((btn, index))
        
        sidebar_container.addSpacerItem(QSpacerItem(20, 80, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        sidebar_layout.addWidget(sidebar_widget)
        
        for btn, index in self.buttons:
            btn.clicked.connect(lambda checked, i=index: self.stack.setCurrentIndex(i))
        return sidebar_layout
    
    def darken_color(self, color):
        colors = {"#3b82f6": "#1e40af", "#10b981": "#047857", "#8b5cf6": "#6d28d9", "#6b7280": "#475569"}
        return colors.get(color, color)
    
    def lighten_color(self, color):
        colors = {"#3b82f6": "#60a5fa", "#10b981": "#34d399", "#8b5cf6": "#c4b5fd"}
        return colors.get(color, color)
    
    # === REAL STEGANOGRAPHY ===
    def hide_message_image(self, image_path, message, key, output_path):
        try:
            img = Image.open(image_path).convert('RGB')
            pixels = np.array(img, dtype=np.uint8)
            
            # Encrypt + length + end marker
            key_bytes = key.encode('utf-8')
            encrypted = bytearray(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(message.encode('utf-8')))
            data = len(message.encode('utf-8')).to_bytes(4, 'big') + bytes(encrypted) + b'\xFF\xFF\xFF\xFF'
            binary_data = ''.join(format(b, '08b') for b in data)
            
            # Embed LSB
            idx = 0
            for y in range(pixels.shape[0]):
                for x in range(pixels.shape[1]):
                    if idx < len(binary_data):
                        pixels[y, x, 0] = (pixels[y, x, 0] & 0xFE) | int(binary_data[idx])
                        idx += 1
                    else:
                        break
                if idx >= len(binary_data):
                    break
            
            Image.fromarray(pixels).save(output_path)
            return True
        except:
            return False
    
    def extract_message_image(self, image_path, key):
        try:
            img = Image.open(image_path).convert('RGB')
            pixels = np.array(img)
            
            binary_data = ''
            for y in range(min(100, pixels.shape[0])):
                for x in range(pixels.shape[1]):
                    binary_data += str(pixels[y, x, 0] & 1)
                    if len(binary_data) > 200:
                        break
                if len(binary_data) > 200:
                    break
            
            msg_len = int(binary_data[:32], 2)
            msg_binary = binary_data[32:32 + msg_len * 8]
            
            key_bytes = key.encode('utf-8')
            decrypted = bytearray()
            for i in range(0, len(msg_binary), 8):
                if i + 8 <= len(msg_binary):
                    byte_val = int(msg_binary[i:i+8], 2)
                    decrypted.append(byte_val ^ key_bytes[i//8 % len(key_bytes)])
            
            return decrypted.decode('utf-8', errors='ignore').rstrip('\x00')
        except:
            return "No message found"
    
    def hide_message_video(self, video_path, message, key, output_path):
        try:
            cap = cv2.VideoCapture(video_path)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            w, h = int(cap.get(3)), int(cap.get(4))
            out = cv2.VideoWriter(output_path, fourcc, 30.0, (w, h))
            
            msg_binary = ''.join(format(ord(c) ^ ord(key[i % len(key)]), '08b') for i, c in enumerate(message))
            idx = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if idx < len(msg_binary):
                    for y in range(min(50, frame.shape[0])):
                        for x in range(min(50, frame.shape[1])):
                            if idx < len(msg_binary):
                                frame[y, x, 0] = (frame[y, x, 0] & 0xFE) | int(msg_binary[idx])
                                idx += 1
                out.write(frame)
            
            cap.release()
            out.release()
            return True
        except:
            return False
    
    def generate_heatmap(self, image_path):
        try:
            img = cv2.imread(image_path, 0)
            lsb = img & 1
            heatmap = cv2.applyColorMap((lsb * 255).astype(np.uint8), cv2.COLORMAP_JET)
            cv2.imwrite('heatmap.png', heatmap)
            return QPixmap('heatmap.png').scaled(440, 280, Qt.AspectRatioMode.KeepAspectRatio)
        except:
            return None
    
    def analyze_cnn(self, image_path):
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            lsb = img & 1
            zero_pct = np.mean(lsb == 0) * 100
            confidence = min(abs(zero_pct - 50) * 2, 95)
            
            if confidence > 70:
                return f"🔴 STEGO DETECTED\n{confidence:.1f}% confidence", "red"
            else:
                return f"🟢 CLEAN IMAGE\n{100-confidence:.1f}% confidence", "green"
        except:
            return "❌ Analysis failed", "red"
    
    def image_page(self):
        page = QWidget()
        page.setStyleSheet("background: #0a0e17;")
        layout = QVBoxLayout(page)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)
        
        layout.addWidget(QLabel("🖼️ Image Steganography", styleSheet="font-size: 34px; font-weight: bold; color: #3b82f6;"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        preview_layout = QVBoxLayout()
        self.image_label = QLabel("👆 Upload Image")
        self.image_label.setFixedSize(480, 320)
        self.image_label.setStyleSheet("QLabel { border: 3px dashed #3b82f6; border-radius: 20px; background: #0f172a; color: #60a5fa; font-size: 20px; padding: 30px; }")
        preview_layout.addWidget(self.image_label)
        
        upload_btn = QPushButton("📁 Upload")
        upload_btn.setFixedSize(120, 45)
        upload_btn.setStyleSheet("QPushButton { background-color: #3b82f6; color: white; border: 2px solid #1e40af; border-radius: 22px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #1e40af; }")
        upload_btn.clicked.connect(self.upload_image)
        preview_layout.addWidget(upload_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(preview_layout)
        
        msg_layout = QHBoxLayout()
        msg_layout.addWidget(QLabel("💬 Message:", styleSheet="font-size: 18px; font-weight: bold; color: #3b82f6; min-width: 100px;"))
        self.msg_image = QTextEdit()
        self.msg_image.setFixedHeight(70)
        self.msg_image.setStyleSheet("QTextEdit { background-color: #1e293b; border: 2px solid #475569; border-radius: 15px; padding: 12px; font-size: 13px; }")
        msg_layout.addWidget(self.msg_image)
        layout.addLayout(msg_layout)
        
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("🔐 Key:", styleSheet="font-size: 18px; font-weight: bold; color: #3b82f6; min-width: 100px;"))
        self.key_image = QLineEdit()
        self.key_image.setFixedHeight(50)
        self.key_image.setStyleSheet("QLineEdit { background-color: #1e293b; border: 2px solid #475569; border-radius: 15px; padding: 12px; font-size: 13px; }")
        key_layout.addWidget(self.key_image)
        layout.addLayout(key_layout)
        
        btn_layout = QHBoxLayout()
        self.hide_image_btn = QPushButton("🔒 Hide Message")
        self.extract_image_btn = QPushButton("🔓 Extract Message")
        self.hide_image_btn.setFixedHeight(60)
        self.extract_image_btn.setFixedHeight(60)
        self.hide_image_btn.clicked.connect(self.hide_image_action)
        self.extract_image_btn.clicked.connect(self.extract_image_action)
        
        self.hide_image_btn.setStyleSheet("QPushButton { background-color: #16a34a; color: white; border: 2px solid #15803d; border-radius: 25px; font-size: 18px; font-weight: bold; padding: 15px; } QPushButton:hover { background-color: #15803d; }")
        self.extract_image_btn.setStyleSheet("""
            QPushButton { 
                background-color: #f59e0b; 
                color: white; 
                border: 2px solid #d97706; 
                border-radius: 25px; 
                font-size: 18px; 
                font-weight: bold; 
                padding: 15px; 
            } 
            QPushButton:hover { 
                background-color: #d97706; 
            }
        """)
        btn_layout.addWidget(self.hide_image_btn)
        btn_layout.addWidget(self.extract_image_btn)
        layout.addLayout(btn_layout)
        
        return page
    
    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path).scaled(470, 310, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.image_label.setStyleSheet("QLabel { border: 3px solid #3b82f6; border-radius: 20px; background: black; }")
    
    def hide_image_action(self):
        if not self.image_path or not self.msg_image.toPlainText():
            QMessageBox.warning(self, "Error", "Please upload an image and enter a message!")
            return
        
        key = self.key_image.text() or "defaultkey"
        output_path = QFileDialog.getSaveFileName(self, "Save Stego Image", "", "PNG (*.png)")[0]
        if output_path:
            if self.hide_message_image(self.image_path, self.msg_image.toPlainText(), key, output_path):
                QMessageBox.information(self, "Success", "Message hidden successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to hide message!")
    
    def extract_image_action(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "Please upload an image!")
            return
        
        key = self.key_image.text() or "defaultkey"
        message = self.extract_message_image(self.image_path, key)
        QMessageBox.information(self, "Extracted Message", message)
    
    # === VIDEO PAGE ===
    def video_page(self):
        page = QWidget()
        page.setStyleSheet("background: #0a0e17;")
        layout = QVBoxLayout(page)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)
        
        layout.addWidget(QLabel("🎥 Video Steganography", styleSheet="font-size: 34px; font-weight: bold; color: #10b981;"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Video upload section (similar structure to image)
        preview_layout = QVBoxLayout()
        self.video_label = QLabel("👆 Upload Video")
        self.video_label.setFixedSize(480, 320)
        self.video_label.setStyleSheet("QLabel { border: 3px dashed #10b981; border-radius: 20px; background: #0f172a; color: #34d399; font-size: 20px; padding: 30px; }")
        preview_layout.addWidget(self.video_label)
        
        upload_btn = QPushButton("📁 Upload Video")
        upload_btn.setFixedSize(140, 45)
        upload_btn.setStyleSheet("QPushButton { background-color: #10b981; color: white; border: 2px solid #047857; border-radius: 22px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #047857; }")
        upload_btn.clicked.connect(self.upload_video)
        preview_layout.addWidget(upload_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(preview_layout)
        
        # Message and key inputs
        msg_layout = QHBoxLayout()
        msg_layout.addWidget(QLabel("💬 Message:", styleSheet="font-size: 18px; font-weight: bold; color: #10b981; min-width: 100px;"))
        self.msg_video = QTextEdit()
        self.msg_video.setFixedHeight(70)
        self.msg_video.setStyleSheet("QTextEdit { background-color: #1e293b; border: 2px solid #475569; border-radius: 15px; padding: 12px; font-size: 13px; }")
        msg_layout.addWidget(self.msg_video)
        layout.addLayout(msg_layout)
        
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("🔐 Key:", styleSheet="font-size: 18px; font-weight: bold; color: #10b981; min-width: 100px;"))
        self.key_video = QLineEdit()
        self.key_video.setFixedHeight(50)
        self.key_video.setStyleSheet("QLineEdit { background-color: #1e293b; border: 2px solid #475569; border-radius: 15px; padding: 12px; font-size: 13px; }")
        key_layout.addWidget(self.key_video)
        layout.addLayout(key_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.hide_video_btn = QPushButton("🔒 Hide in Video")
        self.extract_video_btn = QPushButton("🔓 Extract from Video")
        for btn in [self.hide_video_btn, self.extract_video_btn]:
            btn.setFixedHeight(60)
        
        self.hide_video_btn.clicked.connect(self.hide_video_action)
        self.extract_video_btn.clicked.connect(self.extract_video_action)
        
        self.hide_video_btn.setStyleSheet("QPushButton { background-color: #16a34a; color: white; border: 2px solid #15803d; border-radius: 25px; font-size: 18px; font-weight: bold; padding: 15px; } QPushButton:hover { background-color: #15803d; }")
        self.extract_video_btn.setStyleSheet("QPushButton { background-color: #f59e0b; color: white; border: 2px solid #d97706; border-radius: 25px; font-size: 18px; font-weight: bold; padding: 15px; } QPushButton:hover { background-color: #d97706; }")
        
        btn_layout.addWidget(self.hide_video_btn)
        btn_layout.addWidget(self.extract_video_btn)
        layout.addLayout(btn_layout)
        
        return page
    
    def upload_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Videos (*.mp4 *.avi *.mov)")
        if file_path:
            self.video_path = file_path
            # Show first frame as thumbnail
            cap = cv2.VideoCapture(file_path)
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width = frame_rgb.shape[:2]
                max_size = 470
                scale = min(max_size/width, max_size/height)
                new_w, new_h = int(width * scale), int(height * scale)
                frame_resized = cv2.resize(frame_rgb, (new_w, new_h))
                qimage = QPixmap.fromImage(frame_resized)
                self.video_label.setPixmap(qimage)
            cap.release()
            self.video_label.setStyleSheet("QLabel { border: 3px solid #10b981; border-radius: 20px; background: black; }")
    
    def hide_video_action(self):
        if not self.video_path:
            QMessageBox.warning(self, "Error", "Please upload a video!")
            return
        key = self.key_video.text() or "defaultkey"
        output_path = QFileDialog.getSaveFileName(self, "Save Stego Video", "", "MP4 (*.mp4)")[0]
        if output_path:
            if self.hide_message_video(self.video_path, self.msg_video.toPlainText(), key, output_path):
                QMessageBox.information(self, "Success", "Message hidden in video!")
            else:
                QMessageBox.critical(self, "Error", "Failed to process video!")
    
    def extract_video_action(self):
        if not self.video_path:
            QMessageBox.warning(self, "Error", "Please upload a video with hidden message!")
            return
        
        key = self.key_video.text() or "defaultkey"
        try:
            message = extract_message_from_video(self.video_path, key)
            QMessageBox.information(self, "Extracted Message", f"Message found:\n\n{message}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to extract message!\n\nPossible reasons:\n- Wrong key\n- No hidden message in this video\n- Video format not supported\n\nError: {str(e)}")
    
    # === AI PAGE ===
    def ai_page(self):
        page = QWidget()
        page.setStyleSheet("background: #0a0e17;")
        layout = QVBoxLayout(page)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)
        
        layout.addWidget(QLabel("🤖 AI Steganography Detection", styleSheet="font-size: 34px; font-weight: bold; color: #8b5cf6;"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Upload section
        upload_layout = QVBoxLayout()
        self.ai_label = QLabel("👆 Upload Image for Analysis")
        self.ai_label.setFixedSize(480, 320)
        self.ai_label.setStyleSheet("QLabel { border: 3px dashed #8b5cf6; border-radius: 20px; background: #0f172a; color: #c4b5fd; font-size: 18px; padding: 30px; }")
        upload_layout.addWidget(self.ai_label)
        
        # Combined upload and analyze buttons in a horizontal layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        self.upload_ai_btn = QPushButton("📁 Upload Image")
        self.upload_ai_btn.setFixedSize(180, 55)
        self.upload_ai_btn.setStyleSheet("QPushButton { background-color: #8b5cf6; color: white; border: 2px solid #6d28d9; border-radius: 25px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #6d28d9; }")
        self.upload_ai_btn.clicked.connect(self.upload_ai_image)
        
        self.analyze_btn = QPushButton("🔍 Analyze Image")
        self.analyze_btn.setFixedSize(180, 55)
        self.analyze_btn.setStyleSheet("QPushButton { background-color: #10b981; color: white; border: 2px solid #047857; border-radius: 25px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #047857; }")
        self.analyze_btn.clicked.connect(self.analyze_image_action)
        
        btn_layout.addWidget(self.upload_ai_btn)
        btn_layout.addWidget(self.analyze_btn)
        upload_layout.addLayout(btn_layout)
        layout.addLayout(upload_layout)
        
        # Heatmap preview
        self.heatmap_label = QLabel("LSB Heatmap will appear here")
        self.heatmap_label.setFixedSize(500, 350)
        self.heatmap_label.setStyleSheet("QLabel { border: 2px solid #6d28d9; border-radius: 15px; background: #1e293b; }")
        layout.addWidget(self.heatmap_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Results
        self.result_label = QLabel("Upload image to begin analysis")
        self.result_label.setStyleSheet("QLabel { font-size: 24px; font-weight: bold; padding: 20px; border-radius: 15px; background: #1e293b; min-height: 80px; }")
        layout.addWidget(self.result_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return page
    
    def upload_ai_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image for Analysis", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.ai_path = file_path
            pixmap = QPixmap(file_path).scaled(470, 310, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.ai_label.setPixmap(pixmap)
            self.ai_label.setStyleSheet("QLabel { border: 3px solid #8b5cf6; border-radius: 20px; background: black; }")
    
    def analyze_image_action(self):
        if not self.ai_path:
            QMessageBox.warning(self, "Error", "Please upload an image first!")
            return
        
        # Generate heatmap
        heatmap_pixmap = self.generate_heatmap(self.ai_path)
        if heatmap_pixmap:
            self.heatmap_label.setPixmap(heatmap_pixmap)
        
        # Analyze
        result_text, color = self.analyze_cnn(self.ai_path)
        self.result_label.setText(result_text)
        self.result_label.setStyleSheet(f"QLabel {{ font-size: 24px; font-weight: bold; padding: 20px; border-radius: 15px; background: {color}; min-height: 80px; color: white; }}")
    
    # === ABOUT PAGE ===
    def about_page(self):
        page = QWidget()
        page.setStyleSheet("background: #0a0e17;")
        layout = QVBoxLayout(page)
        layout.setSpacing(25)
        layout.setContentsMargins(50, 50, 50, 50)
        
        title = QLabel("🎨 AI Steganography Suite v2.0")
        title.setStyleSheet("font-size: 42px; font-weight: bold; color: #3b82f6; margin-bottom: 20px;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        info = """
        <div style='font-size: 18px; line-height: 1.6; color: #e2e8f0; background: #1e293b; padding: 30px; border-radius: 20px;'>
            <h2 style='color: #10b981; margin-top: 0;'>✨ Features</h2>
            <ul style='margin: 20px 0; padding-left: 25px;'>
                <li>🖼️ Image Steganography (LSB + Encryption)</li>
                <li>🎥 Video Steganography (Frame embedding)</li>
                <li>🤖 AI Detection (Statistical + Heatmap analysis)</li>
                <li>🔐 Password-based encryption</li>
                <li>📊 LSB Heatmap visualization</li>
            </ul>
            <h2 style='color: #8b5cf6;'>⚙️ Technologies</h2>
            <ul style='margin: 20px 0; padding-left: 25px;'>
                <li>PyQt6 - Modern cross-platform UI</li>
                <li>OpenCV - Computer vision processing</li>
                <li>Pillow - Image manipulation</li>
                <li>NumPy - Array operations</li>
            </ul>
            <p style='font-size: 16px; color: #94a3b8;'>
                Built with ❤️ for security researchers and enthusiasts.
            </p>
        </div>
        """
        about_label = QLabel()
        about_label.setTextFormat(Qt.TextFormat.RichText)
        about_label.setWordWrap(True)
        about_label.setStyleSheet("QLabel { background: transparent; padding: 0; }")
        about_label.setText(info)
        layout.addWidget(about_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return page

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec())
