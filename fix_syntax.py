# Fix syntax error in ui_main.py - unterminated string literals

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the unterminated string literals in QLabel
content = content.replace(
    '''        # Graph 1 - Confidence Gauge (BIG: 500x140)
        self.graph1_label = QLabel("📊 Confidence Gauge

Detection confidence score (0-100%)

Analyzing...")
        self.graph1_label.setFixedHeight(140)
        self.graph1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graph1_label.setStyleSheet("QLabel { border: 3px solid #f59e0b; border-radius: 12px; background: #0f172a; color: #e2e8f0; font-size: 13px; padding: 15px; }")
        tab3_layout.addWidget(self.graph1_label)
        
        # Graph 2 - Pixel Distribution (BIG: 500x140)  
        self.graph2_label = QLabel("📈 Pixel Distribution

Histogram of pixel values in the image

Analyzing...")
        self.graph2_label.setFixedHeight(140)
        self.graph2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graph2_label.setStyleSheet("QLabel { border: 3px solid #ef4444; border-radius: 12px; background: #0f172a; color: #e2e8f0; font-size: 13px; padding: 15px; }")
        tab3_layout.addWidget(self.graph2_label)
        
        # Graph 3 - Model Statistics (BIG: 500x140)
        self.graph3_label = QLabel("📉 Model Statistics

Mean, Std, Min, Max values

Analyzing...")
        self.graph3_label.setFixedHeight(140)
        self.graph3_label.setAlignment(Qt.AlignmentFlag.AlignCenter)''',
    '''        # Graph 1 - Confidence Gauge (BIG: 500x140)
        self.graph1_label = QLabel("Graph 1: Confidence Gauge - Upload image to analyze")
        self.graph1_label.setFixedHeight(140)
        self.graph1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graph1_label.setStyleSheet("QLabel { border: 3px solid #f59e0b; border-radius: 12px; background: #0f172a; color: #e2e8f0; font-size: 13px; padding: 15px; }")
        tab3_layout.addWidget(self.graph1_label)
        
        # Graph 2 - Pixel Distribution (BIG: 500x140)  
        self.graph2_label = QLabel("Graph 2: Pixel Distribution - Histogram will appear here")
        self.graph2_label.setFixedHeight(140)
        self.graph2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graph2_label.setStyleSheet("QLabel { border: 3px solid #ef4444; border-radius: 12px; background: #0f172a; color: #e2e8f0; font-size: 13px; padding: 15px; }")
        tab3_layout.addWidget(self.graph2_label)
        
        # Graph 3 - Model Statistics (BIG: 500x140)
        self.graph3_label = QLabel("Graph 3: Model Statistics - Mean, Std, Min, Max")
        self.graph3_label.setFixedHeight(140)
        self.graph3_label.setAlignment(Qt.AlignmentFlag.AlignCenter)'''
)

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Syntax fixed!")
