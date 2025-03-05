import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui import MainWindow
from utils import get_resource_path


def main():
    app = QApplication(sys.argv)

    # Set application icon using resource path
    icon_path = get_resource_path(os.path.join("assets", "app_icon.png"))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
