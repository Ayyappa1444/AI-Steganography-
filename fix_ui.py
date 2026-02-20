import os
import sys

# Read the current file
with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix button alignment - add spacing and centering
old_btn_layout = '''btn_layout = QHBoxLayout()
        self.hide_image_btn = QPushButton("🔒 Hide Message")
        self.extract_image_btn = QPushButton("🔓 Extract Message")
        self.hide_image_btn.setFixedHeight(60)
        self.extract_image_btn.setFixedHeight(60)'''

new_btn_layout = '''btn_layout = QHBoxLayout()
        btn_layout.setSpacing(25)
        btn_layout.setContentsMargins(60, 15, 60, 15)
        
        self.hide_image_btn = QPushButton("🔒 ENCRYPT & HIDE")
        self.extract_image_btn = QPushButton("🔓 DECRYPT & EXTRACT")
        self.hide_image_btn.setFixedHeight(60)
        self.hide_image_btn.setMinimumWidth(240)
        self.extract_image_btn.setFixedHeight(60)
        self.extract_image_btn.setMinimumWidth(240)'''

content = content.replace(old_btn_layout, new_btn_layout)

# Add stretch to center buttons for image page
old_buttons = '''btn_layout.addWidget(self.hide_image_btn)
        btn_layout.addWidget(self.extract_image_btn)
        layout.addLayout(btn_layout)
        
        return page'''

new_buttons = '''btn_layout.addStretch(1)
        btn_layout.addWidget(self.hide_image_btn)
        btn_layout.addWidget(self.extract_image_btn)
        btn_layout.addStretch(1)
        layout.addLayout(btn_layout)
        
        return page'''

content = content.replace(old_buttons, new_buttons)

# Also fix video buttons
old_video_btn = '''btn_layout = QHBoxLayout()
        self.hide_video_btn = QPushButton("🔒 Hide in Video")
        self.extract_video_btn = QPushButton("🔓 Extract from Video")
        for btn in [self.hide_video_btn, self.extract_video_btn]:
            btn.setFixedHeight(60)'''

new_video_btn = '''btn_layout = QHBoxLayout()
        btn_layout.setSpacing(25)
        btn_layout.setContentsMargins(60, 15, 60, 15)
        
        self.hide_video_btn = QPushButton("🔒 ENCRYPT & HIDE")
        self.extract_video_btn = QPushButton("🔓 DECRYPT & EXTRACT")
        self.hide_video_btn.setFixedHeight(60)
        self.hide_video_btn.setMinimumWidth(240)
        self.extract_video_btn.setFixedHeight(60)
        self.extract_video_btn.setMinimumWidth(240)'''

content = content.replace(old_video_btn, new_video_btn)

# Add stretch for video buttons
old_video_buttons = '''btn_layout.addWidget(self.hide_video_btn)
        btn_layout.addWidget(self.extract_video_btn)
        layout.addLayout(btn_layout)
        
        return page
    
    def upload_video'''

new_video_buttons = '''btn_layout.addStretch(1)
        btn_layout.addWidget(self.hide_video_btn)
        btn_layout.addWidget(self.extract_video_btn)
        btn_layout.addStretch(1)
        layout.addLayout(btn_layout)
        
        return page
    
    def upload_video'''

content = content.replace(old_video_buttons, new_video_buttons)

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("All fixes applied successfully!")
