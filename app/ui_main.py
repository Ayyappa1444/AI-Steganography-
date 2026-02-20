import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# app/ui_main.py - FULLY FUNCTIONAL + ALL FIXES + USER PROFILE
from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QPushButton, 
                            QTextEdit, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, 
                            QMessageBox, QStackedWidget, QFrame, QSpacerItem, QSizePolicy,
                            QComboBox, QScrollArea)
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QFont
from PyQt6.QtCore import Qt
import os
import numpy as np
from PIL import Image
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

# Import stego modules
from stego.image_stego import hide_message as hide_image_msg, extract_message as extract_image_msg
from stego.video_stego import hide_message_in_video, extract_message_from_video

# Import enhanced AI modules
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from ai.steganalysis_models import EnhancedSteganalysis, DCTSteganography, PerformanceMetrics
    from ai.cnn_steganalysis import SteganalysisCNN, EnsembleDetector
    ENHANCED_AI_AVAILABLE = True
except ImportError:
    ENHANCED_AI_AVAILABLE = False
    print("Enhanced AI modules not available")

class MainUI(QMainWindow):
    def __init__(self, username=None):
        super().__init__()
        self.username = username or "User"
        self.setWindowTitle("🎨 AI Steganography Suite v2.0")
        self.setFixedSize(1200, 800)
        self.image_path = None
        self.video_path = None
        self.ai_path = None
        self.image_page_ref = None
        self.video_page_ref = None
        self.ai_page_ref = None
        self.init_ui()
    
    def show_message(self, title, message, msg_type="info"):
        """Show custom styled message box"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        # Style based on message type
        if msg_type == "error":
            bg_color = "#7f1d1d"
            btn_color = "#dc2626"
            border_color = "#ef4444"
        elif msg_type == "warning":
            bg_color = "#78350f"
            btn_color = "#f59e0b"
            border_color = "#fbbf24"
        elif msg_type == "success":
            bg_color = "#14532d"
            btn_color = "#10b981"
            border_color = "#34d399"
        else:
            bg_color = "#1e3a5f"
            btn_color = "#3b82f6"
            border_color = "#60a5fa"
        
        msg_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {bg_color};
            }}
            QMessageBox QLabel {{
                color: #ffffff;
                font-size: 14px;
                padding: 15px;
                font-weight: bold;
            }}
            QMessageBox QPushButton {{
                background-color: {btn_color};
                color: white;
                border: 2px solid {border_color};
                border-radius: 8px;
                padding: 10px 30px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {border_color};
            }}
        """)
        
        if msg_type == "error":
            msg_box.setIcon(QMessageBox.Icon.Critical)
        elif msg_type == "warning":
            msg_box.setIcon(QMessageBox.Icon.Warning)
        elif msg_type == "success":
            msg_box.setIcon(QMessageBox.Icon.Information)
        else:
            msg_box.setIcon(QMessageBox.Icon.NoIcon)
        
        msg_box.exec()
    
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
        main_layout = QVBoxLayout(parent)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Top header with user profile and logout
        header = self.create_header()
        main_layout.addLayout(header)
        
        # Main content area (sidebar + stack)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        
        sidebar = self.create_sidebar()
        content_layout.addLayout(sidebar, 1)
        
        self.stack = QStackedWidget()
        self.stack.addWidget(self.image_page())
        self.stack.addWidget(self.video_page())
        self.stack.addWidget(self.ai_page())
        self.stack.addWidget(self.about_page())
        content_layout.addWidget(self.stack, 4)
        
        main_layout.addLayout(content_layout)
    
    def create_header(self):
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 5, 10, 5)
        
        # App title on the left
        app_title = QLabel("🎨 AI Steganography Suite")
        app_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #3b82f6;")
        header_layout.addWidget(app_title)
        
        header_layout.addStretch()
        
        # User profile section on the right - Enhanced with dropdown menu
        profile_frame = QFrame()
        profile_frame.setObjectName("profileFrame")
        profile_frame.setStyleSheet("""
            QFrame#profileFrame {
                background: #1e293b;
                border-radius: 20px;
                padding: 5px 15px;
            }
        """)
        profile_layout = QHBoxLayout(profile_frame)
        profile_layout.setSpacing(8)
        
        # User avatar
        avatar_label = QLabel("👤")
        avatar_label.setStyleSheet("font-size: 20px;")
        profile_layout.addWidget(avatar_label)
        
        # Username with user info
        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(0)
        user_info_layout.setContentsMargins(5, 0, 5, 0)
        
        username_label = QLabel(f"Welcome, {self.username}")
        username_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #10b981;")
        user_info_layout.addWidget(username_label)
        
        # User email/role
        user_detail = QLabel("Premium User")
        user_detail.setStyleSheet("font-size: 10px; color: #94a3b8;")
        user_info_layout.addWidget(user_detail)
        
        profile_layout.addLayout(user_info_layout)
        
        # User Menu Button (Activity & Store Activity)
        self.user_menu_btn = QPushButton("⚙️")
        self.user_menu_btn.setFixedSize(32, 32)
        self.user_menu_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        self.user_menu_btn.clicked.connect(self.show_user_menu)
        profile_layout.addWidget(self.user_menu_btn)
        
        # Logout button
        logout_btn = QPushButton("🚪")
        logout_btn.setFixedSize(32, 32)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        logout_btn.setToolTip("Logout")
        profile_layout.addWidget(logout_btn)
        
        header_layout.addWidget(profile_frame)
        
        return header_layout
    
    def show_user_menu(self):
        """Show user menu with Activity and Store Activity options"""
        from PyQt6.QtWidgets import QDialog, QListWidget, QListWidgetItem
        
        dialog = QDialog(self)
        dialog.setWindowTitle("User Menu")
        dialog.setFixedSize(320, 300)
        dialog.setStyleSheet("""
            QDialog {
                background: #1e293b;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)
        
        # User info header
        header = QLabel(f"👤 {self.username}")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #10b981; padding: 10px;")
        layout.addWidget(header)
        
        # Menu options
        menu_label = QLabel("Select Option:")
        menu_label.setStyleSheet("font-size: 12px; color: #94a3b8;")
        layout.addWidget(menu_label)
        
        menu_list = QListWidget()
        menu_list.setStyleSheet("""
            QListWidget {
                background: #0f172a;
                border: 2px solid #3b82f6;
                border-radius: 10px;
                padding: 5px;
                color: white;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 12px;
                border-radius: 8px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background: #3b82f6;
                color: white;
            }
            QListWidget::item:hover {
                background: #334155;
            }
        """)
        
        # Add menu items
        activity_item = QListWidgetItem("📊 Activity - View your usage history")
        activity_item.setData(1, "activity")
        menu_list.addItem(activity_item)
        
        store_activity_item = QListWidgetItem("💾 Store Activity - Save session data")
        store_activity_item.setData(1, "store")
        menu_list.addItem(store_activity_item)
        
        profile_item = QListWidgetItem("👤 Profile Settings")
        profile_item.setData(1, "profile")
        menu_list.addItem(profile_item)
        
        logout_item = QListWidgetItem("🚪 Logout")
        logout_item.setData(1, "logout")
        menu_list.addItem(logout_item)
        
        layout.addWidget(menu_list)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(35)
        close_btn.setStyleSheet("""
            QPushButton {
                background: #475569;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #64748b;
            }
        """)
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        # Handle menu selection
        def on_menu_selected(item):
            option = item.data(1)
            if option == "activity":
                dialog.close()
                self.show_activity()
            elif option == "store":
                dialog.close()
                self.store_activity()
            elif option == "profile":
                dialog.close()
                QMessageBox.information(self, "Profile", f"User: {self.username}\nRole: Premium User\nStatus: Active")
            elif option == "logout":
                dialog.close()
                self.logout()
        
        menu_list.itemClicked.connect(on_menu_selected)
        dialog.exec()
    
    def show_activity(self):
        """Show user activity history"""
        activity_info = f"""
        <div style='background: #0f172a; padding: 20px; border-radius: 10px; font-size: 14px; color: #e2e8f0;'>
        <h3 style='color: #10b981;'>📊 Your Activity</h3>
        <p><b>User:</b> {self.username}</p>
        <p><b>Session Started:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <p><b>Features Used:</b></p>
        <ul>
            <li>🖼️ Image Steganography</li>
            <li>🎥 Video Steganography</li>
            <li>🤖 AI Detection</li>
        </ul>
        <p><b>Status:</b> <span style='color: #10b981;'>Active</span></p>
        </div>
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("Activity")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(activity_info)
        msg.exec()
    
    def store_activity(self):
        """Store/save user activity"""
        activity_data = f"User: {self.username}\nDate: {datetime.now()}\nActivity: Session active"
        
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Activity", "", "Text Files (*.txt)")
        if save_path:
            try:
                with open(save_path, 'w') as f:
                    f.write(activity_data)
                QMessageBox.information(self, "Success", "Activity saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    def logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?", 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            # Reopen auth window
            from app.auth_window import AuthWindow
            from PyQt6.QtWidgets import QApplication
            import sys
            self.auth_window = AuthWindow()
            self.auth_window.show()
    
    def create_sidebar(self):
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(12)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        
        sidebar_widget = QFrame()
        sidebar_widget.setFixedWidth(280)
        sidebar_widget.setStyleSheet("QFrame { background: #0f172a; border-radius: 25px; }")
        sidebar_container = QVBoxLayout(sidebar_widget)
        sidebar_container.setSpacing(15)
        sidebar_container.setContentsMargins(20, 20, 20, 20)
        
        buttons = [
            ("🖼️ Image Stego", 0, "#3b82f6"), 
            ("🎥 Video Stego", 1, "#10b981"), 
            ("🤖 AI Detection", 2, "#8b5cf6"), 
            ("ℹ️ About", 3, "#6b7280")
        ]
        
        self.buttons = []
        for text, index, color in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(70)
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
    
    def analyze_cnn_with_details(self, image_path):
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            h, w = img.shape
            lsb = img & 1
            zero_pct = np.mean(lsb == 0) * 100
            one_pct = np.mean(lsb == 1) * 100
            mean_val = np.mean(img)
            std_val = np.std(img)
            balance = abs(zero_pct - 50)
            confidence = min(balance * 2, 95)
            
            if confidence > 70:
                result = f"🔴 STEGO DETECTED\n\nConfidence: {confidence:.1f}%"
                color = "#dc2626"
            else:
                result = f"🟢 CLEAN IMAGE\n\nConfidence: {100-confidence:.1f}%"
                color = "#16a34a"
            
            details = f"""<b>📋 Steganalysis Detection Report</b><br><br>
            <b>Result:</b> {'STEGO DETECTED' if confidence > 70 else 'CLEAN IMAGE'}<br>
            <b>Confidence Score:</b> {confidence:.1f}%<br>
            <b>Image Dimensions:</b> {w} x {h}<br>
            <b>LSB Distribution:</b> 0: {zero_pct:.1f}% | 1: {one_pct:.1f}%<br>
            <b>Mean Pixel Value:</b> {mean_val:.2f}<br>
            <b>Standard Deviation:</b> {std_val:.2f}<br>
            <b>Balance Score:</b> {balance:.2f}%"""
            
            return result, color, confidence, details
        except:
            return "❌ Analysis failed", "#dc2626", 0, "Error in analysis"
    
    # === IMAGE PAGE ===
    def image_page(self):
        page = QWidget()
        page.setStyleSheet("background: #0a0e17;")
        layout = QVBoxLayout(page)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 15, 20, 15)
        
        layout.addWidget(QLabel("🖼️ Image Steganography", styleSheet="font-size: 28px; font-weight: bold; color: #3b82f6;"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        preview_layout = QVBoxLayout()
        self.image_label = QLabel("👆 Upload Image")
        self.image_label.setFixedSize(400, 280)
        self.image_label.setStyleSheet("QLabel { border: 3px dashed #3b82f6; border-radius: 20px; background: #0f172a; color: #60a5fa; font-size: 20px; padding: 30px; }")
        preview_layout.addWidget(self.image_label)
        
        upload_btn = QPushButton("📁 Upload")
        upload_btn.setFixedSize(120, 45)
        upload_btn.setStyleSheet("QPushButton { background-color: #3b82f6; color: white; border: 2px solid #1e40af; border-radius: 22px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #1e40af; }")
        upload_btn.clicked.connect(self.upload_image)
        preview_layout.addWidget(upload_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(preview_layout)
        
        msg_layout = QHBoxLayout()
        msg_layout.addWidget(QLabel("💬 Message:", styleSheet="font-size: 14px; font-weight: bold; color: #3b82f6; min-width: 100px;"))
        self.msg_image = QTextEdit()
        self.msg_image.setFixedHeight(50)
        self.msg_image.setStyleSheet("QTextEdit { background-color: #1e293b; border: 2px solid #475569; border-radius: 12px; padding: 10px; font-size: 12px; }")
        msg_layout.addWidget(self.msg_image)
        layout.addLayout(msg_layout)
        
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("🔐 Key:", styleSheet="font-size: 14px; font-weight: bold; color: #3b82f6; min-width: 100px;"))
        self.key_image = QLineEdit()
        self.key_image.setFixedHeight(40)
        self.key_image.setStyleSheet("QLineEdit { background-color: #1e293b; border: 2px solid #475569; border-radius: 15px; padding: 12px; font-size: 13px; }")
        key_layout.addWidget(self.key_image)
        layout.addLayout(key_layout)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(25)
        btn_layout.setContentsMargins(60, 15, 60, 15)
        
        self.hide_image_btn = QPushButton("🔒 ENCRYPT & HIDE")
        self.extract_image_btn = QPushButton("🔓 DECRYPT & EXTRACT")
        self.hide_image_btn.setFixedHeight(50)
        self.hide_image_btn.setMinimumWidth(240)
        self.extract_image_btn.setFixedHeight(50)
        self.extract_image_btn.setMinimumWidth(240)
        self.hide_image_btn.clicked.connect(self.hide_image_action)
        self.extract_image_btn.clicked.connect(self.extract_image_action)
        
        self.hide_image_btn.setStyleSheet("QPushButton { background-color: #16a34a; color: white; border: 2px solid #15803d; border-radius: 25px; font-size: 14px; font-weight: bold; padding: 10px; } QPushButton:hover { background-color: #15803d; }")
        self.extract_image_btn.setStyleSheet("QPushButton { background-color: #f59e0b; color: white; border: 2px solid #d97706; border-radius: 25px; font-size: 14px; font-weight: bold; padding: 10px; } QPushButton:hover { background-color: #d97706; }")
        
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.hide_image_btn)
        btn_layout.addWidget(self.extract_image_btn)
        btn_layout.addStretch(1)
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
                self.msg_image.clear()
                self.key_image.clear()
            else:
                QMessageBox.critical(self, "Error", "Failed to hide message!")
    
    def extract_image_action(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "Please upload an image!")
            return
        
        key = self.key_image.text() or "defaultkey"
        message = self.extract_message_image(self.image_path, key)
        QMessageBox.information(self, "Extracted Message", message)
        self.key_image.clear()
    
    # === VIDEO PAGE ===
    def video_page(self):
        page = QWidget()
        page.setStyleSheet("background: #0a0e17;")
        layout = QVBoxLayout(page)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 15, 20, 15)
        
        layout.addWidget(QLabel("🎥 Video Steganography", styleSheet="font-size: 28px; font-weight: bold; color: #10b981;"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        preview_layout = QVBoxLayout()
        self.video_label = QLabel("👆 Upload Video")
        self.video_label.setFixedSize(400, 280)
        self.video_label.setStyleSheet("QLabel { border: 3px dashed #10b981; border-radius: 20px; background: #0f172a; color: #34d399; font-size: 20px; padding: 30px; }")
        preview_layout.addWidget(self.video_label)
        
        upload_btn = QPushButton("📁 Upload Video")
        upload_btn.setFixedSize(120, 40)
        upload_btn.setStyleSheet("QPushButton { background-color: #10b981; color: white; border: 2px solid #047857; border-radius: 22px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #047857; }")
        upload_btn.clicked.connect(self.upload_video)
        preview_layout.addWidget(upload_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(preview_layout)
        
        msg_layout = QHBoxLayout()
        msg_layout.addWidget(QLabel("💬 Message:", styleSheet="font-size: 14px; font-weight: bold; color: #10b981; min-width: 100px;"))
        self.msg_video = QTextEdit()
        self.msg_video.setFixedHeight(50)
        self.msg_video.setStyleSheet("QTextEdit { background-color: #1e293b; border: 2px solid #475569; border-radius: 12px; padding: 10px; font-size: 12px; }")
        msg_layout.addWidget(self.msg_video)
        layout.addLayout(msg_layout)
        
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("🔐 Key:", styleSheet="font-size: 14px; font-weight: bold; color: #10b981; min-width: 100px;"))
        self.key_video = QLineEdit()
        self.key_video.setFixedHeight(40)
        self.key_video.setStyleSheet("QLineEdit { background-color: #1e293b; border: 2px solid #475569; border-radius: 15px; padding: 12px; font-size: 13px; }")
        key_layout.addWidget(self.key_video)
        layout.addLayout(key_layout)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(25)
        btn_layout.setContentsMargins(60, 15, 60, 15)
        
        self.hide_video_btn = QPushButton("🔒 ENCRYPT & HIDE")
        self.extract_video_btn = QPushButton("🔓 DECRYPT & EXTRACT")
        self.hide_video_btn.setFixedHeight(50)
        self.hide_video_btn.setMinimumWidth(240)
        self.extract_video_btn.setFixedHeight(50)
        self.extract_video_btn.setMinimumWidth(240)
        
        self.hide_video_btn.clicked.connect(self.hide_video_action)
        self.extract_video_btn.clicked.connect(self.extract_video_action)
        
        self.hide_video_btn.setStyleSheet("QPushButton { background-color: #16a34a; color: white; border: 2px solid #15803d; border-radius: 25px; font-size: 14px; font-weight: bold; padding: 10px; } QPushButton:hover { background-color: #15803d; }")
        self.extract_video_btn.setStyleSheet("QPushButton { background-color: #f59e0b; color: white; border: 2px solid #d97706; border-radius: 25px; font-size: 14px; font-weight: bold; padding: 10px; } QPushButton:hover { background-color: #d97706; }")
        
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.hide_video_btn)
        btn_layout.addWidget(self.extract_video_btn)
        btn_layout.addStretch(1)
        layout.addLayout(btn_layout)
        
        return page
    
    def upload_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Videos (*.mp4 *.avi *.mov)")
        if file_path:
            self.video_path = file_path
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
                self.msg_video.clear()
                self.key_video.clear()
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
            self.key_video.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to extract message!\n\nError: {str(e)}")
    
    # === AI PAGE ===
    def ai_page(self):
        page = QWidget()
        page.setStyleSheet("background: #0a0e17;")
        
        main_split = QHBoxLayout(page)
        main_split.setSpacing(10)
        main_split.setContentsMargins(10, 8, 10, 8)
        
        # LEFT SIDE - Controls
        left_panel = QWidget()
        left_panel.setFixedWidth(350)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(4)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        title = QLabel("🤖 AI Steganography Detection")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #8b5cf6;")
        left_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        task_label = QLabel("Select Analysis Task:", styleSheet="font-size: 11px; color: #94a3b8;")
        left_layout.addWidget(task_label)
        
        self.task_combo = QComboBox()
        self.task_combo.setFixedHeight(32)
        self.task_combo.addItems([
            "🔍 Steganalysis Detection",
            "📊 LSB Heatmap Analysis", 
            "📈 Statistical Analysis",
            "🎯 Confidence Evaluation",
            "🖼️ Full Analysis Report"
        ])
        self.task_combo.setStyleSheet("""
            QComboBox {
                background-color: #1e293b;
                color: white;
                border: 2px solid #8b5cf6;
                border-radius: 8px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QComboBox:hover { border: 2px solid #a78bfa; }
            QComboBox::drop-down { border: none; width: 25px; }
            QComboBox QAbstractItemView {
                background-color: #1e293b;
                color: white;
                selection-background-color: #8b5cf6;
            }
        """)
        left_layout.addWidget(self.task_combo)
        
        self.ai_label = QLabel("👆 Upload Image for Analysis")
        self.ai_label.setFixedSize(320, 160)
        self.ai_label.setStyleSheet("QLabel { border: 3px dashed #8b5cf6; border-radius: 10px; background: #0f172a; color: #c4b5fd; font-size: 12px; padding: 10px; }")
        left_layout.addWidget(self.ai_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        
        self.upload_ai_btn = QPushButton("📁 Upload")
        self.upload_ai_btn.setFixedSize(100, 32)
        self.upload_ai_btn.setStyleSheet("QPushButton { background-color: #8b5cf6; color: white; border: 2px solid #6d28d9; border-radius: 12px; font-size: 11px; font-weight: bold; } QPushButton:hover { background-color: #6d28d9; }")
        self.upload_ai_btn.clicked.connect(self.upload_ai_image)
        
        self.analyze_btn = QPushButton("🔍 Analyze")
        self.analyze_btn.setFixedSize(100, 32)
        self.analyze_btn.setStyleSheet("QPushButton { background-color: #10b981; color: white; border: 2px solid #047857; border-radius: 12px; font-size: 11px; font-weight: bold; } QPushButton:hover { background-color: #047857; }")
        self.analyze_btn.clicked.connect(self.analyze_image_action)
        
        btn_row.addStretch(1)
        btn_row.addWidget(self.upload_ai_btn)
        btn_row.addWidget(self.analyze_btn)
        btn_row.addStretch(1)
        left_layout.addLayout(btn_row)
        
        self.heatmap_label = QLabel("Heatmap Preview")
        self.heatmap_label.setFixedSize(320, 140)
        self.heatmap_label.setStyleSheet("QLabel { border: 2px solid #6d28d9; border-radius: 8px; background: #1e293b; color: #94a3b8; font-size: 10px; }")
        left_layout.addWidget(self.heatmap_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.result_label = QLabel("Select task & upload image")
        self.result_label.setFixedSize(320, 60)
        self.result_label.setStyleSheet("QLabel { font-size: 11px; font-weight: bold; padding: 8px; border-radius: 8px; background: #1e293b; color: #94a3b8; }")
        left_layout.addWidget(self.result_label)
        
        main_split.addWidget(left_panel)
        
        # RIGHT SIDE - Results
        right_panel = QWidget()
        right_panel.setStyleSheet("background: #0f172a; border-radius: 15px;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(5)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        results_title = QLabel("📋 Analysis Results")
        results_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #10b981;")
        right_layout.addWidget(results_title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.results_stack = QStackedWidget()
        self.results_stack.setStyleSheet("background: #1e293b; border-radius: 10px;")
        
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.setContentsMargins(10, 10, 10, 10)
        self.tab_result = QLabel("No analysis performed yet.\n\nUpload an image and select a task to begin analysis.")
        self.tab_result.setStyleSheet("QLabel { font-size: 14px; font-weight: bold; padding: 20px; border-radius: 10px; background: #0f172a; color: #e2e8f0; line-height: 1.6; }")
        tab1_layout.addWidget(self.tab_result)
        self.results_stack.addWidget(tab1)
        
        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)
        self.tab_heatmap = QLabel("LSB Heatmap will appear here")
        self.tab_heatmap.setStyleSheet("QLabel { border: 2px solid #8b5cf6; border-radius: 10px; background: #0f172a; color: #94a3b8; font-size: 12px; }")
        tab2_layout.addWidget(self.tab_heatmap)
        self.results_stack.addWidget(tab2)
        
        tab3 = QWidget()
        tab3_layout = QVBoxLayout(tab3)
        tab3_layout.setSpacing(12)
        
        graphs_title = QLabel("📈 Analysis & Model Data")
        graphs_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #f59e0b; margin: 10px;")
        tab3_layout.addWidget(graphs_title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.graph1_label = QLabel("Graph 1: Confidence Gauge")
        self.graph1_label.setFixedHeight(150)
        self.graph1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graph1_label.setStyleSheet("QLabel { border: 3px solid #f59e0b; border-radius: 12px; background: #0f172a; color: #e2e8f0; font-size: 13px; padding: 15px; }")
        tab3_layout.addWidget(self.graph1_label)
        
        self.graph2_label = QLabel("Graph 2: Pixel Distribution")
        self.graph2_label.setFixedHeight(150)
        self.graph2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graph2_label.setStyleSheet("QLabel { border: 3px solid #ef4444; border-radius: 12px; background: #0f172a; color: #e2e8f0; font-size: 13px; padding: 15px; }")
        tab3_layout.addWidget(self.graph2_label)
        
        self.graph3_label = QLabel("Graph 3: Model Statistics")
        self.graph3_label.setFixedHeight(150)
        self.graph3_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graph3_label.setStyleSheet("QLabel { border: 3px solid #3b82f6; border-radius: 12px; background: #0f172a; color: #e2e8f0; font-size: 13px; padding: 15px; }")
        tab3_layout.addWidget(self.graph3_label)
        
        self.results_stack.addWidget(tab3)
        
        right_layout.addWidget(self.results_stack)
        
        tab_btns = QHBoxLayout()
        tab_btns.setSpacing(5)
        
        self.tab_btn1 = QPushButton("🎯 Result")
        self.tab_btn1.setFixedSize(80, 28)
        self.tab_btn1.setStyleSheet("QPushButton { background-color: #10b981; color: white; border-radius: 8px; font-size: 10px; }")
        self.tab_btn1.clicked.connect(lambda: self.results_stack.setCurrentIndex(0))
        
        self.tab_btn2 = QPushButton("📊 Heatmap")
        self.tab_btn2.setFixedSize(80, 28)
        self.tab_btn2.setStyleSheet("QPushButton { background-color: #8b5cf6; color: white; border-radius: 8px; font-size: 10px; }")
        self.tab_btn2.clicked.connect(lambda: self.results_stack.setCurrentIndex(1))
        
        self.tab_btn3 = QPushButton("📈 Graphs")
        self.tab_btn3.setFixedSize(80, 28)
        self.tab_btn3.setStyleSheet("QPushButton { background-color: #f59e0b; color: white; border-radius: 8px; font-size: 10px; }")
        self.tab_btn3.clicked.connect(lambda: self.results_stack.setCurrentIndex(2))
        
        tab_btns.addStretch(1)
        tab_btns.addWidget(self.tab_btn1)
        tab_btns.addWidget(self.tab_btn2)
        tab_btns.addWidget(self.tab_btn3)
        tab_btns.addStretch(1)
        
        right_layout.addLayout(tab_btns)
        
        main_split.addWidget(right_panel, 1)
        
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
        
        heatmap_pixmap = self.generate_heatmap(self.ai_path)
        if heatmap_pixmap:
            scaled_heatmap = heatmap_pixmap.scaled(320, 140, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.heatmap_label.setPixmap(scaled_heatmap)
            self.tab_heatmap.setPixmap(heatmap_pixmap.scaled(450, 280, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        result_text, color, confidence, details = self.analyze_cnn_with_details(self.ai_path)
        
        self.result_label.setText(result_text)
        self.result_label.setStyleSheet(f"QLabel {{ font-size: 11px; font-weight: bold; padding: 8px; border-radius: 8px; background: {color}; color: white; }}")
        
        self.tab_result.setText(result_text + "\n\n" + details)
        self.tab_result.setStyleSheet(f"QLabel {{ font-size: 14px; font-weight: bold; padding: 20px; border-radius: 10px; background: #0f172a; color: white; line-height: 1.6; }}")
        
        self.generate_analysis_graphs(self.ai_path, confidence)
    
    def generate_analysis_graphs(self, image_path, confidence):
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                return
            
            h, w = img.shape
            lsb = img & 1
            zero_pct = np.mean(lsb == 0) * 100
            one_pct = np.mean(lsb == 1) * 100
            mean_val = np.mean(img)
            std_val = np.std(img)
            min_val = np.min(img)
            max_val = np.max(img)
            
            # Graph 1 - Confidence Gauge
            fig1, ax1 = plt.subplots(figsize=(8, 3))
            bars1 = ax1.barh(['Detection'], [confidence], color='#8b5cf6', height=0.5)
            ax1.barh(['Detection'], [100-confidence], left=confidence, color='#374151', height=0.5)
            ax1.set_xlim(0, 100)
            ax1.set_title(f'Confidence Score: {confidence:.1f}%', fontsize=16, color='white', fontweight='bold')
            ax1.set_xlabel('Percentage', fontsize=14, color='white')
            ax1.tick_params(colors='white', labelsize=12)
            for spine in ax1.spines.values():
                spine.set_color('white')
            fig1.patch.set_facecolor('#1e293b')
            ax1.set_facecolor('#1e293b')
            ax1.text(confidence/2, 0, f'{confidence:.1f}%', ha='center', va='center', color='white', fontsize=14, fontweight='bold')
            plt.tight_layout()
            fig1.savefig('graph_confidence.png', dpi=150, bbox_inches='tight', facecolor='#1e293b')
            plt.close(fig1)
            
            # Graph 2 - Pixel Distribution
            fig2, ax2 = plt.subplots(figsize=(8, 3))
            ax2.hist(img.flatten(), bins=50, color='#ef4444', alpha=0.8, edgecolor='white')
            ax2.set_title('Pixel Value Distribution', fontsize=16, color='white', fontweight='bold')
            ax2.set_xlabel('Pixel Value (0-255)', fontsize=14, color='white')
            ax2.set_ylabel('Frequency', fontsize=14, color='white')
            ax2.tick_params(colors='white', labelsize=12)
            for spine in ax2.spines.values():
                spine.set_color('white')
            fig2.patch.set_facecolor('#1e293b')
            ax2.set_facecolor('#1e293b')
            plt.tight_layout()
            fig2.savefig('graph_distribution.png', dpi=150, bbox_inches='tight', facecolor='#1e293b')
            plt.close(fig2)
            
            # Graph 3 - Statistics
            fig3, ax3 = plt.subplots(figsize=(8, 3))
            stats_labels = ['Mean', 'Std Dev', 'Min', 'Max']
            stat_values = [mean_val, std_val, min_val, max_val]
            stat_percentages = [v/255*100 for v in stat_values]
            colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
            bars = ax3.bar(stats_labels, stat_percentages, color=colors, width=0.6, edgecolor='white')
            ax3.set_title('Image Statistics', fontsize=16, color='white', fontweight='bold')
            ax3.set_ylabel('Value (Normalized)', fontsize=14, color='white')
            ax3.tick_params(colors='white', labelsize=12)
            for spine in ax3.spines.values():
                spine.set_color('white')
            for bar, val, pct in zip(bars, stat_values, stat_percentages):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f'{val:.1f}', ha='center', va='bottom', color='white', fontsize=12, fontweight='bold')
            fig3.patch.set_facecolor('#1e293b')
            ax3.set_facecolor('#1e293b')
            ax3.set_ylim(0, max(stat_percentages) * 1.4)
            plt.tight_layout()
            fig3.savefig('graph_stats.png', dpi=150, bbox_inches='tight', facecolor='#1e293b')
            plt.close(fig3)
            
            conf_pix = QPixmap('graph_confidence.png')
            dist_pix = QPixmap('graph_distribution.png')
            stats_pix = QPixmap('graph_stats.png')
            
            conf_scaled = conf_pix.scaled(700, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            dist_scaled = dist_pix.scaled(700, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            stats_scaled = stats_pix.scaled(700, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
            self.graph1_label.setPixmap(conf_scaled)
            self.graph2_label.setPixmap(dist_scaled)
            self.graph3_label.setPixmap(stats_scaled)
            
        except Exception as e:
            print(f"Graph generation error: {e}")
    
    # === ABOUT PAGE ===
    def about_page(self):
        page = QWidget()
        page.setStyleSheet("background: #0a0e17;")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: #0a0e17; }")
        
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 15, 20, 15)
        
        title = QLabel("📖 AI Steganography Suite - Complete Documentation")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3b82f6; margin: 15px;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Sections...
        abstract = QLabel("""
        <div style='background: #1e293b; padding: 20px; border-radius: 12px; font-size: 14px; line-height: 1.8; color: #e2e8f0;'>
        <h2 style='color: #10b981;'>📝 Abstract</h2>
        <p>This project presents a comprehensive <b>AI Steganography Suite</b> - a modern desktop application that combines 
        <b>steganography</b> (the art of hiding data within other data) with <b>steganalysis</b> (detecting hidden data).</p>
        <p><b>Key Features:</b></p>
        <ul>
        <li>🖼️ Image Steganography with LSB embedding</li>
        <li>🎥 Video Steganography with frame-based embedding</li>
        <li>🤖 AI Detection with multiple analysis methods</li>
        <li>📊 Visual Heatmaps and Graph analysis</li>
        <li>🔐 Password-protected encryption</li>
        </ul>
        </div>
        """)
        abstract.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(abstract)
        
        howto = QLabel("""
        <div style='background: #1e293b; padding: 15px; border-radius: 10px; font-size: 13px; line-height: 1.6; color: #e2e8f0;'>
        <h2 style='color: #10b981;'>📖 How to Use</h2>
        <b>🖼️ Image Steganography:</b><br>
        1. Click "Upload" to select an image (PNG, JPG, BMP)<br>
        2. Enter your secret message in the text box<br>
        3. Set a secure key/password<br>
        4. Click "🔒 ENCRYPT & HIDE" button<br>
        5. Save the stego image to your desired location<br><br>
        
        <b>🎥 Video Steganography:</b><br>
        1. Click "Upload Video" to select a video file<br>
        2. Enter message and key/password<br>
        3. Click "🔒 ENCRYPT & HIDE" to embed<br>
        4. Save the stego video<br><br>
        
        <b>🤖 AI Detection:</b><br>
        1. Navigate to AI Detection page from sidebar<br>
        2. Select analysis task from dropdown menu<br>
        3. Upload image to analyze<br>
        4. Click "Analyze" button<br>
        5. View results in tabs (Result/Heatmap/Graphs)
        </div>
        """)
        howto.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(howto)
        
        footer = QLabel("""
        <div style='text-align: center; padding: 20px; color: #f59e0b; font-size: 14px;'>
        <b>🎨 AI Steganography Suite v2.0</b><br>
        Built with ❤️ using PyQt6, OpenCV, NumPy, Matplotlib<br>
        © 2024 | All Rights Reserved
        </div>
        """)
        footer.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(footer)
        
        scroll.setWidget(content_widget)
        
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
        
        return page

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec())
