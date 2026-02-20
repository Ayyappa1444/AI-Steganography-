# main.py - Entry point with Authentication
from PyQt6.QtWidgets import QApplication
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.auth_window import AuthWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())
