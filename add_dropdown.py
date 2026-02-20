# Script to add dropdown menu for AI Detection task selection

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# First add QComboBox to imports
old_imports = '''from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QPushButton, 
                            QTextEdit, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, 
                            QMessageBox, QStackedWidget, QFrame, QSpacerItem, QSizePolicy)'''

new_imports = '''from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QPushButton, 
                            QTextEdit, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, 
                            QMessageBox, QStackedWidget, QFrame, QSpacerItem, QSizePolicy,
                            QComboBox)'''

content = content.replace(old_imports, new_imports)

# Replace the AI page with dropdown menu version
old_ai_page = '''    # === AI PAGE ===
    def ai_page(self):
        page = QWidget()
        page.setStyleSheet("background: #0a0e17;")
        layout = QVBoxLayout(page)
        layout.setSpacing(6)
        layout.setContentsMargins(12, 8, 12, 8)
        
        layout.addWidget(QLabel("🤖 AI Steganography Detection", styleSheet="font-size: 20px; font-weight: bold; color: #8b5cf6;"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Upload section
        upload_center = QVBoxLayout()
        upload_center.setSpacing(6)
        
        self.ai_label = QLabel("👆 Upload Image for Analysis")
        self.ai_label.setFixedSize(280, 160)
        self.ai_label.setStyleSheet("QLabel { border: 3px dashed #8b5cf6; border-radius: 10px; background: #0f172a; color: #c4b5fd; font-size: 12px; padding: 12px; }")
        upload_center.addWidget(self.ai_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Button row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        
        self.upload_ai_btn = QPushButton("📁 Upload Image")
        self.upload_ai_btn.setFixedSize(120, 34)
        self.upload_ai_btn.setStyleSheet("QPushButton { background-color: #8b5cf6; color: white; border: 2px solid #6d28d9; border-radius: 15px; font-size: 12px; font-weight: bold; } QPushButton:hover { background-color: #6d28d9; }")
        self.upload_ai_btn.clicked.connect(self.upload_ai_image)
        
        self.analyze_btn = QPushButton("🔍 Analyze Image")
        self.analyze_btn.setFixedSize(120, 34)
        self.analyze_btn.setStyleSheet("QPushButton { background-color: #10b981; color: white; border: 2px solid #047857; border-radius: 15px; font-size: 12px; font-weight: bold; } QPushButton:hover { background-color: #047857; }")
        self.analyze_btn.clicked.connect(self.analyze_image_action)
        
        btn_row.addStretch(1)
        btn_row.addWidget(self.upload_ai_btn)
        btn_row.addWidget(self.analyze_btn)
        btn_row.addStretch(1)
        
        upload_center.addLayout(btn_row)
        layout.addLayout(upload_center)
        
        # Heatmap and Results side by side
        side_by_side = QHBoxLayout()
        side_by_side.setSpacing(10)
        
        # Heatmap section
        heatmap_box = QVBoxLayout()
        heatmap_box.setSpacing(4)
        heatmap_title = QLabel("📊 LSB Heatmap")
        heatmap_title.setStyleSheet("font-size: 12px; font-weight: bold; color: #8b5cf6;")
        heatmap_box.addWidget(heatmap_title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.heatmap_label = QLabel("No analysis yet")
        self.heatmap_label.setFixedSize(250, 140)
        self.heatmap_label.setStyleSheet("QLabel { border: 2px solid #6d28d9; border-radius: 8px; background: #1e293b; color: #94a3b8; font-size: 11px; }")
        heatmap_box.addWidget(self.heatmap_label, alignment=Qt.AlignmentFlag.AlignCenter)
        side_by_side.addLayout(heatmap_box, 1)
        
        # Confidence/Results section
        result_box = QVBoxLayout()
        result_box.setSpacing(4)
        result_title = QLabel("🎯 Detection Result")
        result_title.setStyleSheet("font-size: 12px; font-weight: bold; color: #10b981;")
        result_box.addWidget(result_title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.result_label = QLabel("Upload image to begin")
        self.result_label.setFixedSize(250, 140)
        self.result_label.setStyleSheet("QLabel { font-size: 13px; font-weight: bold; padding: 10px; border-radius: 8px; background: #1e293b; color: #94a3b8; }")
        result_box.addWidget(self.result_label, alignment=Qt.AlignmentFlag.AlignCenter)
        side_by_side.addLayout(result_box, 1)
        
        layout.addLayout(side_by_side)
        
        # === GRAPHS SECTION ===
        graphs_box = QVBoxLayout()
        graphs_box.setSpacing(4)
        
        graphs_title = QLabel("📈 Analysis & Model Data")
        graphs_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #f59e0b;")
        graphs_box.addWidget(graphs_title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Graphs side by side
        graphs_row = QHBoxLayout()
        graphs_row.setSpacing(10)
        
        # Graph 1 - Confidence Gauge
        self.graph1_label = QLabel("Confidence Gauge")
        self.graph1_label.setFixedSize(200, 120)
        self.graph1_label.setStyleSheet("QLabel { border: 2px solid #f59e0b; border-radius: 8px; background: #1e293b; color: #e2e8f0; font-size: 11px; }")
        graphs_row.addWidget(self.graph1_label, 1)
        
        # Graph 2 - Pixel Distribution
        self.graph2_label = QLabel("Pixel Distribution")
        self.graph2_label.setFixedSize(200, 120)
        self.graph2_label.setStyleSheet("QLabel { border: 2px solid #ef4444; border-radius: 8px; background: #1e293b; color: #e2e8f0; font-size: 11px; }")
        graphs_row.addWidget(self.graph2_label, 1)
        
        # Graph 3 - Model Statistics
        self.graph3_label = QLabel("Model Statistics")
        self.graph3_label.setFixedSize(200, 120)
        self.graph3_label.setStyleSheet("QLabel { border: 2px solid #3b82f6; border-radius: 8px; background: #1e293b; color: #e2e8f0; font-size: 11px; }")
        graphs_row.addWidget(self.graph3_label, 1)
        
        graphs_box.addLayout(graphs_row)
        layout.addLayout(graphs_box)
        
        return page'''

new_ai_page = '''    # === AI PAGE ===
    def ai_page(self):
        page = QWidget()
        page.setStyleSheet("background: #0a0e17;")
        layout = QVBoxLayout(page)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 6, 10, 6)
        
        # Title with dropdown selector
        title_row = QHBoxLayout()
        title_row.setSpacing(10)
        
        title = QLabel("🤖 AI Steganography Detection")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #8b5cf6;")
        title_row.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(title_row)
        
        # Dropdown for task selection
        dropdown_row = QHBoxLayout()
        dropdown_row.setSpacing(10)
        
        task_label = QLabel("Select Task:", styleSheet="font-size: 12px; color: #94a3b8;")
        self.task_combo = QComboBox()
        self.task_combo.setFixedSize(200, 32)
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
            QComboBox:hover {
                border: 2px solid #a78bfa;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e293b;
                color: white;
                selection-background-color: #8b5cf6;
            }
        """)
        
        dropdown_row.addStretch(1)
        dropdown_row.addWidget(task_label)
        dropdown_row.addWidget(self.task_combo)
        dropdown_row.addStretch(1)
        
        layout.addLayout(dropdown_row)
        
        # Upload section
        upload_center = QVBoxLayout()
        upload_center.setSpacing(5)
        
        self.ai_label = QLabel("👆 Upload Image for Analysis")
        self.ai_label.setFixedSize(250, 140)
        self.ai_label.setStyleSheet("QLabel { border: 3px dashed #8b5cf6; border-radius: 10px; background: #0f172a; color: #c4b5fd; font-size: 11px; padding: 10px; }")
        upload_center.addWidget(self.ai_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Button row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        
        self.upload_ai_btn = QPushButton("📁 Upload Image")
        self.upload_ai_btn.setFixedSize(110, 30)
        self.upload_ai_btn.setStyleSheet("QPushButton { background-color: #8b5cf6; color: white; border: 2px solid #6d28d9; border-radius: 12px; font-size: 11px; font-weight: bold; } QPushButton:hover { background-color: #6d28d9; }")
        self.upload_ai_btn.clicked.connect(self.upload_ai_image)
        
        self.analyze_btn = QPushButton("🔍 Analyze")
        self.analyze_btn.setFixedSize(110, 30)
        self.analyze_btn.setStyleSheet("QPushButton { background-color: #10b981; color: white; border: 2px solid #047857; border-radius: 12px; font-size: 11px; font-weight: bold; } QPushButton:hover { background-color: #047857; }")
        self.analyze_btn.clicked.connect(self.analyze_image_action)
        
        btn_row.addStretch(1)
        btn_row.addWidget(self.upload_ai_btn)
        btn_row.addWidget(self.analyze_btn)
        btn_row.addStretch(1)
        
        upload_center.addLayout(btn_row)
        layout.addLayout(upload_center)
        
        # Heatmap and Results side by side
        side_by_side = QHBoxLayout()
        side_by_side.setSpacing(8)
        
        # Heatmap section
        heatmap_box = QVBoxLayout()
        heatmap_box.setSpacing(3)
        heatmap_title = QLabel("📊 LSB Heatmap")
        heatmap_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #8b5cf6;")
        heatmap_box.addWidget(heatmap_title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.heatmap_label = QLabel("No analysis yet")
        self.heatmap_label.setFixedSize(220, 120)
        self.heatmap_label.setStyleSheet("QLabel { border: 2px solid #6d28d9; border-radius: 8px; background: #1e293b; color: #94a3b8; font-size: 10px; }")
        heatmap_box.addWidget(self.heatmap_label, alignment=Qt.AlignmentFlag.AlignCenter)
        side_by_side.addLayout(heatmap_box, 1)
        
        # Confidence/Results section
        result_box = QVBoxLayout()
        result_box.setSpacing(3)
        result_title = QLabel("🎯 Detection Result")
        result_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #10b981;")
        result_box.addWidget(result_title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.result_label = QLabel("Select task & upload image")
        self.result_label.setFixedSize(220, 120)
        self.result_label.setStyleSheet("QLabel { font-size: 11px; font-weight: bold; padding: 8px; border-radius: 8px; background: #1e293b; color: #94a3b8; }")
        result_box.addWidget(self.result_label, alignment=Qt.AlignmentFlag.AlignCenter)
        side_by_side.addLayout(result_box, 1)
        
        layout.addLayout(side_by_side)
        
        # === GRAPHS SECTION ===
        graphs_box = QVBoxLayout()
        graphs_box.setSpacing(3)
        
        graphs_title = QLabel("📈 Analysis & Model Data")
        graphs_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #f59e0b;")
        graphs_box.addWidget(graphs_title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Graphs side by side
        graphs_row = QHBoxLayout()
        graphs_row.setSpacing(8)
        
        # Graph 1 - Confidence Gauge
        self.graph1_label = QLabel("Confidence Gauge")
        self.graph1_label.setFixedSize(180, 100)
        self.graph1_label.setStyleSheet("QLabel { border: 2px solid #f59e0b; border-radius: 6px; background: #1e293b; color: #e2e8f0; font-size: 10px; }")
        graphs_row.addWidget(self.graph1_label, 1)
        
        # Graph 2 - Pixel Distribution
        self.graph2_label = QLabel("Pixel Distribution")
        self.graph2_label.setFixedSize(180, 100)
        self.graph2_label.setStyleSheet("QLabel { border: 2px solid #ef4444; border-radius: 6px; background: #1e293b; color: #e2e8f0; font-size: 10px; }")
        graphs_row.addWidget(self.graph2_label, 1)
        
        # Graph 3 - Model Statistics
        self.graph3_label = QLabel("Model Statistics")
        self.graph3_label.setFixedSize(180, 100)
        self.graph3_label.setStyleSheet("QLabel { border: 2px solid #3b82f6; border-radius: 6px; background: #1e293b; color: #e2e8f0; font-size: 10px; }")
        graphs_row.addWidget(self.graph3_label, 1)
        
        graphs_box.addLayout(graphs_row)
        layout.addLayout(graphs_box)
        
        return page'''

content = content.replace(old_ai_page, new_ai_page)

# Update analyze function to handle different tasks
old_analyze = '''    def analyze_image_action(self):
        if not self.ai_path:
            QMessageBox.warning(self, "Error", "Please upload an image first!")
            return
        
        # Generate heatmap
        heatmap_pixmap = self.generate_heatmap(self.ai_path)
        if heatmap_pixmap:
            self.heatmap_label.setPixmap(heatmap_pixmap.scaled(250, 140, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        # Analyze
        result_text, color, confidence = self.analyze_cnn_with_details(self.ai_path)
        self.result_label.setText(result_text)
        self.result_label.setStyleSheet(f"QLabel {{ font-size: 14px; font-weight: bold; padding: 12px; border-radius: 8px; background: {color}; color: white; }}")
        
        # Generate graphs
        self.generate_analysis_graphs(self.ai_path, confidence)'''

new_analyze = '''    def analyze_image_action(self):
        if not self.ai_path:
            QMessageBox.warning(self, "Error", "Please upload an image first!")
            return
        
        # Get selected task
        selected_task = self.task_combo.currentText()
        
        # Generate heatmap
        heatmap_pixmap = self.generate_heatmap(self.ai_path)
        if heatmap_pixmap:
            self.heatmap_label.setPixmap(heatmap_pixmap.scaled(220, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        # Analyze based on selected task
        if "Steganalysis" in selected_task:
            result_text, color, confidence = self.analyze_cnn_with_details(self.ai_path)
        elif "LSB Heatmap" in selected_task:
            result_text, color, confidence = self.analyze_lsb_only(self.ai_path)
        elif "Statistical" in selected_task:
            result_text, color, confidence = self.analyze_statistical(self.ai_path)
        elif "Confidence" in selected_task:
            result_text, color, confidence = self.analyze_confidence(self.ai_path)
        else:  # Full Analysis
            result_text, color, confidence = self.analyze_full_report(self.ai_path)
        
        self.result_label.setText(result_text)
        self.result_label.setStyleSheet(f"QLabel {{ font-size: 11px; font-weight: bold; padding: 8px; border-radius: 8px; background: {color}; color: white; }}")
        
        # Generate graphs
        self.generate_analysis_graphs(self.ai_path, confidence)'''

content = content.replace(old_analyze, new_analyze)

# Add new analysis methods before analyze_cnn
old_analyze_cnn_start = '''    def analyze_cnn(self, image_path):
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)'''

new_methods = '''    # === TASK-SPECIFIC ANALYSIS METHODS ===
    
    def analyze_lsb_only(self, image_path):
        """LSB Heatmap Analysis Only"""
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            lsb = img & 1
            zero_pct = np.mean(lsb == 0) * 100
            one_pct = np.mean(lsb == 1) * 100
            
            result = f"📊 LSB Analysis\\n\\nLSB 0: {zero_pct:.1f}%\\nLSB 1: {one_pct:.1f}%\\nBalance: {min(zero_pct, one_pct):.1f}%"
            color = "#7c3aed"
            confidence = abs(zero_pct - 50)
            return result, color, confidence
        except:
            return "❌ Analysis failed", "#dc2626", 0
    
    def analyze_statistical(self, image_path):
        """Statistical Analysis Only"""
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            mean_val = np.mean(img)
            std_val = np.std(img)
            median_val = np.median(img)
            
            result = f"📈 Statistical Analysis\\n\\nMean: {mean_val:.1f}\\nStd Dev: {std_val:.1f}\\nMedian: {median_val:.1f}"
            color = "#059669"
            confidence = (std_val / 128) * 100
            return result, color, min(confidence, 100)
        except:
            return "❌ Analysis failed", "#dc2626", 0
    
    def analyze_confidence(self, image_path):
        """Confidence Evaluation Only"""
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            lsb = img & 1
            zero_pct = np.mean(lsb == 0) * 100
            
            confidence = min(abs(zero_pct - 50) * 2, 99)
            
            if confidence > 70:
                result = f"🎯 Confidence: HIGH\\n\\n{confidence:.1f}%\\n\\nStego Likely"
                color = "#dc2626"
            elif confidence > 40:
                result = f"🎯 Confidence: MEDIUM\\n\\n{confidence:.1f}%\\n\\nUncertain"
                color = "#f59e0b"
            else:
                result = f"🎯 Confidence: LOW\\n\\n{confidence:.1f}%\\n\\nClean Likely"
                color = "#16a34a"
            
            return result, color, confidence
        except:
            return "❌ Analysis failed", "#dc2626", 0
    
    def analyze_full_report(self, image_path):
        """Full Analysis Report"""
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            h, w = img.shape
            
            lsb = img & 1
            zero_pct = np.mean(lsb == 0) * 100
            one_pct = np.mean(lsb == 1) * 100
            
            mean_val = np.mean(img)
            std_val = np.std(img)
            min_val = np.min(img)
            max_val = np.max(img)
            
            balance = abs(zero_pct - 50)
            confidence = min(balance * 2, 99)
            
            if confidence > 70:
                status = "🔴 STEGO DETECTED"
                color = "#dc2626"
            else:
                status = "🟢 CLEAN"
                color = "#16a34a"
            
            result = f"{status}\\n\\n📊 Confidence: {confidence:.1f}%\\n📏 Size: {w}x{h}\\n📈 Mean: {mean_val:.1f}\\n📉 Std: {std_val:.1f}\\n🔢 LSB 0/1: {zero_pct:.0f}/{one_pct:.0f}%"
            
            return result, color, confidence
        except:
            return "❌ Analysis failed", "#dc2626", 0
    
    # === END TASK METHODS ===
    
    def analyze_cnn(self, image_path):
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)'''

content = content.replace(old_analyze_cnn_start, new_methods)

# Adjust window size
content = content.replace(
    'self.setFixedSize(1000, 750)',
    'self.setFixedSize(980, 720)'
)

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Dropdown menu added successfully!")
print("- Task selection dropdown with 5 options:")
print("  1. Steganalysis Detection")
print("  2. LSB Heatmap Analysis")
print("  3. Statistical Analysis")
print("  4. Confidence Evaluation")
print("  5. Full Analysis Report")
