"""YOLO 数据集预处理工具 - 程序入口"""

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """程序主入口"""
    app = QApplication(sys.argv)
    app.setApplicationName("YOLO Dataset Preprocessing Tool")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
