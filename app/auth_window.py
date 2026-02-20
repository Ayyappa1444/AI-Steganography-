# Authentication Window - Login and Registration
from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QPushButton, 
                            QLineEdit, QVBoxLayout, QHBoxLayout, QMessageBox,
                            QFrame, QGraphicsOpacityEffect, QDialog, QSizePolicy)
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QTimer
import hashlib
import os

# Simple user database (in production, use a real database)
USERS_FILE = "users.dat"

class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 AI Steganography Suite - Login")
        self.setFixedSize(450, 580)
        self.main_window = None
        self.init_ui()
        self.load_users()
    
    def load_users(self):
        """Load users from file"""
        self.users = {}
        if os.path.exists(USERS_FILE):
            try:
                with open(USERS_FILE, 'r') as f:
                    for line in f:
                        parts = line.strip().split(':')
                        if len(parts) == 2:
                            self.users[parts[0]] = parts[1]
            except:
                self.users = {}
    
    def save_users(self):
        """Save users to file"""
        with open(USERS_FILE, 'w') as f:
            for username, password in self.users.items():
                f.write(f"{username}:{password}\n")
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        # Background gradient
        central.setStyleSheet("""
            QWidget { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f172a, stop:1 #1e293b); 
            }
        """)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Center container
        center_widget = QWidget()
        center_widget.setFixedWidth(380)
        center_widget.setStyleSheet("background: transparent;")
        center_layout = QVBoxLayout(center_widget)
        center_layout.setSpacing(12)
        center_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("🎨 AI Steganography Suite")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #3b82f6;
                padding: 8px;
            }
        """)
        center_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Secure Data Hiding & Detection")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #94a3b8;
                padding-bottom: 10px;
            }
        """)
        center_layout.addWidget(subtitle)
        
        # Login Frame
        login_frame = QFrame()
        login_frame.setStyleSheet("""
            QFrame {
                background: #1e293b;
                border-radius: 16px;
                border: 1px solid #334155;
            }
        """)
        login_layout = QVBoxLayout(login_frame)
        login_layout.setSpacing(10)
        login_layout.setContentsMargins(25, 20, 25, 20)
        
        # Login Title
        login_title = QLabel("🔑 Login to Account")
        login_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #10b981;
                padding: 5px;
            }
        """)
        login_layout.addWidget(login_title)
        
        # Username Field - Full width, aligned
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #e2e8f0; font-size: 12px; font-weight: bold;")
        login_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(40)
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: #0f172a;
                border: 2px solid #475569;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
        """)
        login_layout.addWidget(self.username_input)
        
        # Password Field - Full width, aligned
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #e2e8f0; font-size: 12px; font-weight: bold;")
        login_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setFixedHeight(40)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: #0f172a;
                border: 2px solid #475569;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
        """)
        login_layout.addWidget(self.password_input)
        
        # Login Button - Full width
        login_btn = QPushButton("🚀 Login")
        login_btn.setFixedHeight(42)
        login_btn.setStyleSheet("""
            QPushButton {
                background: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 5px;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        login_btn.clicked.connect(self.login)
        login_layout.addWidget(login_btn)
        
        # Divider
        divider_layout = QHBoxLayout()
        divider_layout.setSpacing(8)
        
        left_line = QFrame()
        left_line.setFixedHeight(1)
        left_line.setStyleSheet("background: #475569;")
        left_line.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        or_label = QLabel("OR")
        or_label.setStyleSheet("color: #64748b; font-size: 10px;")
        
        right_line = QFrame()
        right_line.setFixedHeight(1)
        right_line.setStyleSheet("background: #475569;")
        right_line.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        divider_layout.addWidget(left_line)
        divider_layout.addWidget(or_label)
        divider_layout.addWidget(right_line)
        login_layout.addLayout(divider_layout)
        
        # Register Button - Full width
        register_btn = QPushButton("📝 Create New Account")
        register_btn.setFixedHeight(40)
        register_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #3b82f6;
                border: 2px solid #3b82f6;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #3b82f6;
                color: white;
            }
        """)
        register_btn.clicked.connect(self.show_register)
        login_layout.addWidget(register_btn)
        
        # Forgot Password Button
        forgot_btn = QPushButton("🔐 Forgot Password?")
        forgot_btn.setFixedHeight(32)
        forgot_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #f59e0b;
                border: none;
                border-radius: 8px;
                font-size: 11px;
                font-weight: bold;
                margin-top: 3px;
            }
            QPushButton:hover {
                color: #fbbf24;
                text-decoration: underline;
            }
        """)
        forgot_btn.clicked.connect(self.show_forgot_password)
        login_layout.addWidget(forgot_btn)
        
        center_layout.addWidget(login_frame)
        
        # Footer
        footer = QLabel("© 2024 AI Steganography Suite")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #64748b; font-size: 10px; padding: 10px;")
        center_layout.addWidget(footer)
        
        main_layout.addWidget(center_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Store for reference
        self.login_frame = login_frame
    
    def login(self):
        """Handle login"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.show_message("⚠️ Error", "Please enter username and password!", "error")
            return
        
        # Check credentials
        hashed = self.hash_password(password)
        
        if username in self.users and self.users[username] == hashed:
            # Login successful - pass username to main window
            self.open_main(username)
        else:
            self.show_message("❌ Login Failed", "Invalid username or password!", "error")
            self.password_input.clear()
    
    def open_main(self, username):
        """Open main application with logged in username"""
        from app.ui_main import MainUI
        self.main_window = MainUI(username=username)
        self.main_window.show()
        self.close()
    
    def show_register(self):
        """Show registration dialog"""
        dialog = RegisterDialog(self)
        dialog.exec()
    
    def show_forgot_password(self):
        """Show forgot password dialog"""
        dialog = ForgotPasswordDialog(self)
        dialog.exec()
    
    def show_message(self, title, message, msg_type="info"):
        """Show custom styled message box"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1e293b;
            }
            QMessageBox QLabel {
                color: #ffffff;
                font-size: 14px;
                padding: 15px;
                font-weight: bold;
            }
            QMessageBox QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 30px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QMessageBox QPushButton:hover {
                background-color: #2563eb;
            }
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


class ForgotPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("🔐 Reset Password")
        self.setFixedSize(380, 380)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog { 
                background: #1e293b; 
            }
        """)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Title
        title = QLabel("🔐 Reset Password")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #f59e0b;
                padding: 5px;
            }
        """)
        layout.addWidget(title)
        
        # Info text
        info = QLabel("Enter your username and new password to reset.")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setWordWrap(True)
        info.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #94a3b8;
                padding: 3px;
            }
        """)
        layout.addWidget(info)
        
        # Username Field
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #e2e8f0; font-size: 11px; font-weight: bold;")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(36)
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: #0f172a;
                border: 2px solid #475569;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 12px;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #f59e0b;
            }
        """)
        layout.addWidget(self.username_input)
        
        # New Password Field
        new_password_label = QLabel("New Password")
        new_password_label.setStyleSheet("color: #e2e8f0; font-size: 11px; font-weight: bold;")
        layout.addWidget(new_password_label)
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setFixedHeight(36)
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_input.setStyleSheet("""
            QLineEdit {
                background: #0f172a;
                border: 2px solid #475569;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 12px;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #f59e0b;
            }
        """)
        layout.addWidget(self.new_password_input)
        
        # Confirm Password Field
        confirm_label = QLabel("Confirm New Password")
        confirm_label.setStyleSheet("color: #e2e8f0; font-size: 11px; font-weight: bold;")
        layout.addWidget(confirm_label)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setFixedHeight(36)
        self.confirm_input.setPlaceholderText("Confirm new password")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setStyleSheet("""
            QLineEdit {
                background: #0f172a;
                border: 2px solid #475569;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 12px;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #f59e0b;
            }
        """)
        layout.addWidget(self.confirm_input)
        
        # Security Question
        question_label = QLabel("Security: What is this application?")
        question_label.setStyleSheet("color: #e2e8f0; font-size: 11px; font-weight: bold;")
        layout.addWidget(question_label)
        
        self.answer_input = QLineEdit()
        self.answer_input.setFixedHeight(36)
        self.answer_input.setPlaceholderText("Type: Steganography")
        self.answer_input.setStyleSheet("""
            QLineEdit {
                background: #0f172a;
                border: 2px solid #475569;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 12px;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #f59e0b;
            }
        """)
        layout.addWidget(self.answer_input)
        
        # Buttons layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        # Reset Button
        reset_btn = QPushButton("🔄 Reset")
        reset_btn.setFixedHeight(38)
        reset_btn.setStyleSheet("""
            QPushButton {
                background: #f59e0b;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #d97706;
            }
        """)
        reset_btn.clicked.connect(self.reset_password)
        
        # Cancel Button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(38)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #94a3b8;
                border: 2px solid #475569;
                border-radius: 8px;
                font-size: 12px;
            }
            cancel_btn:hover {
                color: white;
                border-color: #64748b;
            }
        """)
        cancel_btn.clicked.connect(self.close)
        
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
    
    def show_message(self, title, message, msg_type="info"):
        """Show custom styled message box"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1e293b;
            }
            QMessageBox QLabel {
                color: #ffffff;
                font-size: 14px;
                padding: 15px;
                font-weight: bold;
            }
            QMessageBox QPushButton {
                background-color: #f59e0b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 30px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QMessageBox QPushButton:hover {
                background-color: #d97706;
            }
        """)
        
        if msg_type == "error":
            msg_box.setIcon(QMessageBox.Icon.Critical)
        elif msg_type == "warning":
            msg_box.setIcon(QMessageBox.Icon.Warning)
        else:
            msg_box.setIcon(QMessageBox.Icon.Information)
        
        msg_box.exec()
    
    def reset_password(self):
        """Handle password reset"""
        username = self.username_input.text().strip()
        new_password = self.new_password_input.text()
        confirm = self.confirm_input.text()
        answer = self.answer_input.text().strip()
        
        # Validation
        if not username or not new_password or not answer:
            self.show_message("⚠️ Error", "Please fill all fields!", "warning")
            return
        
        if len(new_password) < 4:
            self.show_message("⚠️ Error", "Password must be at least 4 characters!", "warning")
            return
        
        if new_password != confirm:
            self.show_message("⚠️ Error", "Passwords do not match!", "warning")
            self.confirm_input.clear()
            return
        
        # Simple security question check
        if answer.lower() != "steganography":
            self.show_message("❌ Error", "Incorrect answer!\nHint: This is about hiding data.", "error")
            return
        
        # Check if user exists
        if not hasattr(self.parent_window, 'users') or username not in self.parent_window.users:
            self.show_message("❌ Error", "Username not found!", "error")
            return
        
        # Reset password
        hashed = self.parent_window.hash_password(new_password)
        self.parent_window.users[username] = hashed
        self.parent_window.save_users()
        
        self.show_message("✅ Success", "Password reset successfully!", "success")
        self.close()


class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("📝 Register")
        self.setFixedSize(360, 400)
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet("""
            QDialog { 
                background: #1e293b; 
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Title
        title = QLabel("Create New Account")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #8b5cf6;
                padding: 5px;
            }
        """)
        layout.addWidget(title)
        
        # Username
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #e2e8f0; font-size: 11px; font-weight: bold;")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(36)
        self.username_input.setPlaceholderText("Choose a username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: #0f172a;
                border: 2px solid #475569;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 12px;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #8b5cf6;
            }
        """)
        layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #e2e8f0; font-size: 11px; font-weight: bold;")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setFixedHeight(36)
        self.password_input.setPlaceholderText("Choose a password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: #0f172a;
                border: 2px solid #475569;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 12px;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #8b5cf6;
            }
        """)
        layout.addWidget(self.password_input)
        
        # Confirm Password
        confirm_label = QLabel("Confirm Password")
        confirm_label.setStyleSheet("color: #e2e8f0; font-size: 11px; font-weight: bold;")
        layout.addWidget(confirm_label)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setFixedHeight(36)
        self.confirm_input.setPlaceholderText("Confirm your password")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setStyleSheet("""
            QLineEdit {
                background: #0f172a;
                border: 2px solid #475569;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 12px;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #8b5cf6;
            }
        """)
        layout.addWidget(self.confirm_input)
        
        # Buttons layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        # Register Button
        register_btn = QPushButton("✅ Register")
        register_btn.setFixedHeight(38)
        register_btn.setStyleSheet("""
            QPushButton {
                background: #8b5cf6;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #7c3aed;
            }
        """)
        register_btn.clicked.connect(self.register)
        
        # Cancel Button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(38)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #94a3b8;
                border: 2px solid #475569;
                border-radius: 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                color: white;
                border-color: #64748b;
            }
        """)
        cancel_btn.clicked.connect(self.close)
        
        btn_layout.addWidget(register_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
    
    def show_message(self, title, message, msg_type="info"):
        """Show custom styled message box"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1e293b;
            }
            QMessageBox QLabel {
                color: #ffffff;
                font-size: 14px;
                padding: 15px;
                font-weight: bold;
            }
            QMessageBox QPushButton {
                background-color: #8b5cf6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 30px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QMessageBox QPushButton:hover {
                background-color: #7c3aed;
            }
        """)
        
        if msg_type == "error":
            msg_box.setIcon(QMessageBox.Icon.Critical)
        elif msg_type == "warning":
            msg_box.setIcon(QMessageBox.Icon.Warning)
        else:
            msg_box.setIcon(QMessageBox.Icon.Information)
        
        msg_box.exec()
    
    def register(self):
        """Handle registration"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        if not username or not password:
            self.show_message("⚠️ Error", "Please fill all fields!", "warning")
            return
        
        if len(username) < 3:
            self.show_message("⚠️ Error", "Username must be at least 3 characters!", "warning")
            return
        
        if len(password) < 4:
            self.show_message("⚠️ Error", "Password must be at least 4 characters!", "warning")
            return
        
        if password != confirm:
            self.show_message("⚠️ Error", "Passwords do not match!", "warning")
            self.confirm_input.clear()
            return
        
        # Check if user exists
        if hasattr(self.parent_window, 'users') and username in self.parent_window.users:
            self.show_message("❌ Error", "Username already exists!", "error")
            return
        
        # Save user
        hashed = self.parent_window.hash_password(password)
        self.parent_window.users[username] = hashed
        self.parent_window.save_users()
        
        self.show_message("✅ Success", "Account created successfully!", "success")
        self.close()
