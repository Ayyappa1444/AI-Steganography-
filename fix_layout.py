# Script to fix UI layout - move buttons up and improve visibility

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: Reduce spacing in main layouts to make GUI more compact and visible
# Change the main layout spacing
content = content.replace(
    'main_layout.setSpacing(25)',
    'main_layout.setSpacing(15)'
)

# Change content margins
content = content.replace(
    'main_layout.setContentsMargins(15, 15, 15, 15)',
    'main_layout.setContentsMargins(10, 10, 10, 10)'
)

# Make page layouts more compact
content = content.replace(
    'layout.setSpacing(20)',
    'layout.setSpacing(12)'
)

content = content.replace(
    'layout.setContentsMargins(30, 20, 30, 20)',
    'layout.setContentsMargins(20, 15, 20, 15)'
)

# Make about page more compact
content = content.replace(
    'layout.setContentsMargins(50, 50, 50, 50)',
    'layout.setContentsMargins(30, 30, 30, 30)'
)

# Reduce sidebar spacing
content = content.replace(
    'sidebar_layout.setSpacing(20)',
    'sidebar_layout.setSpacing(10)'
)

content = content.replace(
    'sidebar_layout.setContentsMargins(20, 25, 20, 25)',
    'sidebar_layout.setContentsMargins(15, 20, 15, 20)'
)

# Make sidebar buttons smaller
content = content.replace(
    'btn.setFixedHeight(85)',
    'btn.setFixedHeight(70)'
)

# Reduce sidebar button spacing
content = content.replace(
    'sidebar_container.setSpacing(22)',
    'sidebar_container.setSpacing(15)'
)

content = content.replace(
    'sidebar_container.setContentsMargins(25, 25, 25, 25)',
    'sidebar_container.setContentsMargins(20, 20, 20, 20)'
)

# Make preview labels smaller
content = content.replace(
    'self.image_label.setFixedSize(480, 320)',
    'self.image_label.setFixedSize(400, 280)'
)

content = content.replace(
    'self.video_label.setFixedSize(480, 320)',
    'self.video_label.setFixedSize(400, 280)'
)

content = content.replace(
    'self.ai_label.setFixedSize(480, 320)',
    'self.ai_label.setFixedSize(400, 280)'
)

# Make heatmap smaller
content = content.replace(
    'self.heatmap_label.setFixedSize(500, 350)',
    'self.heatmap_label.setFixedSize(400, 280)'
)

# Reduce button height
content = content.replace(
    'self.hide_image_btn.setFixedHeight(60)',
    'self.hide_image_btn.setFixedHeight(50)'
)

content = content.replace(
    'self.extract_image_btn.setFixedHeight(60)',
    'self.extract_image_btn.setFixedHeight(50)'
)

content = content.replace(
    'self.hide_video_btn.setFixedHeight(60)',
    'self.hide_video_btn.setFixedHeight(50)'
)

content = content.replace(
    'self.extract_video_btn.setFixedHeight(60)',
    'self.extract_video_btn.setFixedHeight(50)'
)

# Reduce text edit height
content = content.replace(
    'self.msg_image.setFixedHeight(70)',
    'self.msg_image.setFixedHeight(50)'
)

content = content.replace(
    'self.msg_video.setFixedHeight(70)',
    'self.msg_video.setFixedHeight(50)'
)

# Reduce line edit height
content = content.replace(
    'self.key_image.setFixedHeight(50)',
    'self.key_image.setFixedHeight(40)'
)

content = content.replace(
    'self.key_video.setFixedHeight(50)',
    'self.key_video.setFixedHeight(40)'
)

# Reduce upload button size
content = content.replace(
    'upload_btn.setFixedSize(140, 45)',
    'upload_btn.setFixedSize(120, 40)'
)

content = content.replace(
    'upload_btn.setFixedSize(160, 45)',
    'upload_btn.setFixedSize(140, 40)'
)

# Fix result label height
content = content.replace(
    'self.result_label.setStyleSheet(f"QLabel {{ font-size: 24px; font-weight: bold; padding: 20px; border-radius: 15px; background: {color}; min-height: 80px; color: white; }}"',
    'self.result_label.setStyleSheet(f"QLabel {{ font-size: 20px; font-weight: bold; padding: 15px; border-radius: 12px; background: {color}; min-height: 60px; color: white; }}"'
)

# Reduce title font sizes
content = content.replace(
    'styleSheet="font-size: 34px; font-weight: bold;',
    'styleSheet="font-size: 28px; font-weight: bold;'
)

content = content.replace(
    'styleSheet="font-size: 42px; font-weight: bold; color: #3b82f6; margin-bottom: 20px;"',
    'styleSheet="font-size: 32px; font-weight: bold; color: #3b82f6; margin-bottom: 15px;"'
)

# Reduce label font sizes
content = content.replace(
    'styleSheet="font-size: 18px; font-weight: bold;',
    'styleSheet="font-size: 14px; font-weight: bold;'
)

# Make input text smaller
content = content.replace(
    'self.msg_image.setStyleSheet("QTextEdit { background-color: #1e293b; border: 2px solid #475569; border-radius: 15px; padding: 12px; font-size: 13px; }"',
    'self.msg_image.setStyleSheet("QTextEdit { background-color: #1e293b; border: 2px solid #475569; border-radius: 12px; padding: 10px; font-size: 12px; }"'
)

content = content.replace(
    'self.msg_video.setStyleSheet("QTextEdit { background-color: #1e293b; border: 2px solid #475569; border-radius: 15px; padding: 12px; font-size: 13px; }"',
    'self.msg_video.setStyleSheet("QTextEdit { background-color: #1e293b; border: 2px solid #475569; border-radius: 12px; padding: 10px; font-size: 12px; }"'
)

# Fix button fonts
content = content.replace(
    'font-size: 18px; font-weight: bold; padding: 15px;',
    'font-size: 14px; font-weight: bold; padding: 10px;'
)

# Reduce AI button size
content = content.replace(
    'self.upload_ai_btn.setFixedSize(180, 55)',
    'self.upload_ai_btn.setFixedSize(150, 45)'
)

content = content.replace(
    'self.analyze_btn.setFixedSize(180, 55)',
    'self.analyze_btn.setFixedSize(150, 45)'
)

# Change window size to be smaller and fit better
content = content.replace(
    'self.setFixedSize(1450, 980)',
    'self.setFixedSize(1100, 750)'
)

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Layout fixed successfully!")
