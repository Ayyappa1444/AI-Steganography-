# Script to fix AI page layout and About page content

import re

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix AI Page Layout
old_ai_page = '''    # === AI PAGE ===
    def ai_page(self):
        page = QWidget()
        page.setStyleSheet("background: #0a0e17;")
        layout = QVBoxLayout(page)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 15, 20, 15)
        
        layout.addWidget(QLabel("🤖 AI Steganography Detection", styleSheet="font-size: 28px; font-weight: bold; color: #8b5cf6;"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Upload section
        upload_layout = QVBoxLayout()
        self.ai_label = QLabel("👆 Upload Image for Analysis")
        self.ai_label.setFixedSize(400, 280)
        self.ai_label.setStyleSheet("QLabel { border: 3px dashed #8b5cf6; border-radius: 20px; background: #0f172a; color: #c4b5fd; font-size: 18px; padding: 30px; }")
        upload_layout.addWidget(self.ai_label)
        
        # Combined upload and analyze buttons in a horizontal layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        self.upload_ai_btn = QPushButton("📁 Upload Image")
        self.upload_ai_btn.setFixedSize(150, 45)
        self.upload_ai_btn.setStyleSheet("QPushButton { background-color: #8b5cf6; color: white; border: 2px solid #6d28d9; border-radius: 25px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #6d28d9; }")
        self.upload_ai_btn.clicked.connect(self.upload_ai_image)
        
        self.analyze_btn = QPushButton("🔍 Analyze Image")
        self.analyze_btn.setFixedSize(150, 45)
        self.analyze_btn.setStyleSheet("QPushButton { background-color: #10b981; color: white; border: 2px solid #047857; border-radius: 25px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #047857; }")
        self.analyze_btn.clicked.connect(self.analyze_image_action)
        
        btn_layout.addWidget(self.upload_ai_btn)
        btn_layout.addWidget(self.analyze_btn)
        upload_layout.addLayout(btn_layout)
        layout.addLayout(upload_layout)
        
        # Heatmap preview
        self.heatmap_label = QLabel("LSB Heatmap will appear here")
        self.heatmap_label.setFixedSize(400, 280)
        self.heatmap_label.setStyleSheet("QLabel { border: 2px solid #6d28d9; border-radius: 15px; background: #1e293b; }")
        layout.addWidget(self.heatmap_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Results
        self.result_label = QLabel("Upload image to begin analysis")
        self.result_label.setStyleSheet("QLabel { font-size: 24px; font-weight: bold; padding: 20px; border-radius: 15px; background: #1e293b; min-height: 80px; }")
        layout.addWidget(self.result_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return page'''

new_ai_page = '''    # === AI PAGE ===
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

content = content.replace(old_ai_page, new_ai_page)

# Fix About Page Content - enhance with more information
old_about_info = '''
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
'''

new_about_info = '''
        info = """
        <div style='font-size: 15px; line-height: 1.6; color: #e2e8f0; background: #1e293b; padding: 25px; border-radius: 18px;'>
            <h2 style='color: #10b981; margin-top: 0; font-size: 22px;'>✨ Features</h2>
            <ul style='margin: 15px 0; padding-left: 20px;'>
                <li>🖼️ <b>Image Steganography</b> - LSB + AES Encryption</li>
                <li>🎥 <b>Video Steganography</b> - Frame embedding with encryption</li>
                <li>🤖 <b>AI Detection</b> - Statistical + Deep Learning analysis</li>
                <li>🔐 <b>Password Protection</b> - Fernet symmetric encryption</li>
                <li>📊 <b>LSB Heatmap</b> - Visual analysis of hidden data</li>
                <li>📈 <b>PSNR/MSE Metrics</b> - Image quality measurement</li>
            </ul>
            <h2 style='color: #8b5cf6; font-size: 22px;'>⚙️ Technologies</h2>
            <ul style='margin: 15px 0; padding-left: 20px;'>
                <li>🔵 <b>PyQt6</b> - Modern cross-platform GUI framework</li>
                <li>🟢 <b>OpenCV</b> - Computer vision & video processing</li>
                <li>🟡 <b>Pillow</b> - Image manipulation & processing</li>
                <li>🔷 <b>NumPy</b> - High-performance array operations</li>
                <li>🔒 <b>Cryptography</b> - AES-128 encryption</li>
                <li>🧠 <b>TensorFlow/Keras</b> - Deep learning detection</li>
            </ul>
            <h2 style='color: #f59e0b; font-size: 22px;'>📖 How to Use</h2>
            <ul style='margin: 15px 0; padding-left: 20px;'>
                <li><b>Encode:</b> Upload image/video → Enter message → Set key → Click ENCRYPT & HIDE</li>
                <li><b>Decode:</b> Upload stego file → Enter same key → Click DECRYPT & EXTRACT</li>
                <li><b>Analyze:</b> Upload image → Click Analyze → View heatmap & confidence</li>
            </ul>
            <h2 style='color: #ef4444; font-size: 22px;'>⚠️ Disclaimer</h2>
            <p style='font-size: 14px; color: #94a3b8;'>
                This tool is for educational & research purposes only. 
                Always comply with applicable laws and regulations.
            </p>
            <p style='font-size: 16px; color: #f59e0b; margin-top: 20px;'>
                Built with ❤️ for security researchers and enthusiasts.<br>
                Version 2.0 | © 2024
            </p>
        </div>
        """
'''

content = content.replace(old_about_info, new_about_info)

# Also fix the about page margins
content = content.replace(
    'layout.setContentsMargins(30, 30, 30, 30)',
    'layout.setContentsMargins(25, 20, 25, 20)'
)

content = content.replace(
    "title.setStyleSheet(\"font-size: 42px; font-weight: bold; color: #3b82f6; margin-bottom: 20px;\")",
    "title.setStyleSheet(\"font-size: 32px; font-weight: bold; color: #3b82f6; margin-bottom: 15px;\")"
)

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("AI page and About page fixed successfully!")
