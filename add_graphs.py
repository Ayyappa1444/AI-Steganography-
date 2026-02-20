# Script to add graph sections for data and model analysis

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# First, add matplotlib import at the top
# Find the import section and add matplotlib
old_imports = '''from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os
import numpy as np
from PIL import Image
import cv2'''

new_imports = '''from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QFont
from PyQt6.QtCore import Qt
import os
import numpy as np
from PIL import Image
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime'''

content = content.replace(old_imports, new_imports)

# Replace the AI page with graph sections
old_ai_page = '''    # === AI PAGE ===
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

new_ai_page = '''    # === AI PAGE ===
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

content = content.replace(old_ai_page, new_ai_page)

# Now update the analyze_image_action to generate graphs
old_analyze = '''    def analyze_image_action(self):
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
        self.result_label.setStyleSheet(f"QLabel {{ font-size: 20px; font-weight: bold; padding: 15px; border-radius: 12px; background: {color}; min-height: 60px; color: white; }}")'''

new_analyze = '''    def analyze_image_action(self):
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

content = content.replace(old_analyze, new_analyze)

# Add the new methods for detailed analysis and graph generation
# Find the existing analyze_cnn method and add the enhanced version
old_analyze_cnn = '''    def analyze_cnn(self, image_path):
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            lsb = img & 1
            zero_pct = np.mean(lsb == 0) * 100
            confidence = min(abs(zero_pct - 50) * 2, 95)
            
            if confidence > 70:
                return f"🔴 STEGO DETECTED\\n{confidence:.1f}% confidence", "red"
            else:
                return f"🟢 CLEAN IMAGE\\n{100-confidence:.1f}% confidence", "green"
        except:
            return "❌ Analysis failed", "red"'''

new_analyze_cnn = '''    def analyze_cnn(self, image_path):
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            lsb = img & 1
            zero_pct = np.mean(lsb == 0) * 100
            confidence = min(abs(zero_pct - 50) * 2, 95)
            
            if confidence > 70:
                return f"🔴 STEGO DETECTED\\n{confidence:.1f}% confidence", "red"
            else:
                return f"🟢 CLEAN IMAGE\\n{100-confidence:.1f}% confidence", "green"
        except:
            return "❌ Analysis failed", "red"
    
    def analyze_cnn_with_details(self, image_path):
        """Enhanced analysis with detailed statistics"""
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            h, w = img.shape
            
            # LSB analysis
            lsb = img & 1
            zero_pct = np.mean(lsb == 0) * 100
            one_pct = np.mean(lsb == 1) * 100
            
            # Pixel value statistics
            mean_val = np.mean(img)
            std_val = np.std(img)
            min_val = np.min(img)
            max_val = np.max(img)
            
            # Calculate confidence
            balance = abs(zero_pct - 50)
            confidence = min(balance * 2, 99)
            
            if confidence > 70:
                result = f"🔴 STEGO DETECTED\\n\\nConfidence: {confidence:.1f}%\\nLSB 0: {zero_pct:.1f}% | LSB 1: {one_pct:.1f}%\\nMean: {mean_val:.1f} | Std: {std_val:.1f}"
                color = "#dc2626"
            else:
                result = f"🟢 CLEAN IMAGE\\n\\nConfidence: {100-confidence:.1f}%\\nLSB 0: {zero_pct:.1f}% | LSB 1: {one_pct:.1f}%\\nMean: {mean_val:.1f} | Std: {std_val:.1f}"
                color = "#16a34a"
            
            self.last_analysis = {
                'confidence': confidence,
                'zero_pct': zero_pct,
                'one_pct': one_pct,
                'mean': mean_val,
                'std': std_val,
                'min': min_val,
                'max': max_val,
                'width': w,
                'height': h
            }
            
            return result, color, confidence
        except Exception as e:
            return f"❌ Analysis failed\\n{str(e)}", "#dc2626", 0
    
    def generate_analysis_graphs(self, image_path, confidence):
        """Generate analysis graphs"""
        try:
            # Get stored analysis data
            data = getattr(self, 'last_analysis', None)
            if not data:
                return
            
            # Graph 1 - Confidence Gauge (bar chart)
            fig1, ax1 = plt.subplots(figsize=(3, 1.8))
            ax1.barh(['Confidence'], [confidence], color='#8b5cf6', height=0.4)
            ax1.barh(['Confidence'], [100-confidence], left=confidence, color='#374151', height=0.4)
            ax1.set_xlim(0, 100)
            ax1.set_title(f'Confidence: {confidence:.1f}%', fontsize=10, color='white')
            ax1.tick_params(colors='white', labelsize=8)
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['bottom'].set_color('white')
            ax1.spines['left'].set_visible(False)
            fig1.patch.set_facecolor('#1e293b')
            ax1.set_facecolor('#1e293b')
            ax1.tick_params(colors='white')
            plt.tight_layout()
            fig1.savefig('graph_confidence.png', dpi=80, bbox_inches='tight')
            plt.close(fig1)
            
            # Graph 2 - Pixel Distribution (histogram)
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            fig2, ax2 = plt.subplots(figsize=(3, 1.8))
            ax2.hist(img.flatten(), bins=50, color='#ef4444', alpha=0.7)
            ax2.set_title('Pixel Distribution', fontsize=10, color='white')
            ax2.tick_params(colors='white', labelsize=8)
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['bottom'].set_color('white')
            ax2.spines['left'].set_color('white')
            fig2.patch.set_facecolor('#1e293b')
            ax2.set_facecolor('#1e293b')
            ax2.tick_params(colors='white')
            plt.tight_layout()
            fig2.savefig('graph_distribution.png', dpi=80, bbox_inches='tight')
            plt.close(fig2)
            
            # Graph 3 - Model Statistics
            fig3, ax3 = plt.subplots(figsize=(3, 1.8))
            stats = ['Mean', 'Std', 'Min', 'Max']
            values = [data['mean']/255*100, data['std']/255*100, data['min']/255*100, data['max']/255*100]
            colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
            ax3.bar(stats, values, color=colors, width=0.6)
            ax3.set_title('Image Statistics (%)', fontsize=10, color='white')
            ax3.tick_params(colors='white', labelsize=8)
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
            ax3.spines['bottom'].set_color('white')
            ax3.spines['left'].set_color('white')
            fig3.patch.set_facecolor('#1e293b')
            ax3.set_facecolor('#1e293b')
            ax3.tick_params(colors='white')
            plt.tight_layout()
            fig3.savefig('graph_stats.png', dpi=80, bbox_inches='tight')
            plt.close(fig3)
            
            # Load and display graphs
            self.graph1_label.setPixmap(QPixmap('graph_confidence.png').scaled(200, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.graph2_label.setPixmap(QPixmap('graph_distribution.png').scaled(200, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.graph3_label.setPixmap(QPixmap('graph_stats.png').scaled(200, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            
        except Exception as e:
            print(f"Graph generation error: {e}")'''

content = content.replace(old_analyze_cnn, new_analyze_cnn)

# Make window bigger to accommodate graphs
content = content.replace(
    'self.setFixedSize(950, 680)',
    'self.setFixedSize(1000, 750)'
)

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Graph sections added successfully!")
print("- Confidence Gauge graph")
print("- Pixel Distribution histogram")
print("- Model Statistics chart")
print("- Enhanced analysis with detailed statistics")
