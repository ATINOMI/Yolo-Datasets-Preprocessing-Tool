"""底部命令面板 - 显示 LabelImg 命令"""

from functools import partial
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QFrame, QMessageBox, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class CommandPanel(QWidget):
    """命令显示面板"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.command_boxes = []
        self.copy_buttons = []
        self.init_ui()

    def init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)

        # 标题
        title = QLabel("LabelImg 命令")
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title.setFont(title_font)

        layout.addWidget(title)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # 创建 3 个命令框
        subsets = ["train", "val", "test"]
        for i, subset in enumerate(subsets):
            cmd_layout = QHBoxLayout()

            # 标签
            label = QLabel(f"{subset.upper()}:")
            label.setMinimumWidth(60)
            label.setStyleSheet("font-weight: bold;")

            # 文本框（只读）
            text_box = QTextEdit()
            text_box.setReadOnly(True)
            text_box.setMaximumHeight(60)
            text_box.setPlaceholderText(f"labelimg 命令将在数据集生成后显示...")
            text_box.setStyleSheet("background-color: #f5f5f5;")
            self.command_boxes.append(text_box)

            # 复制按钮
            copy_btn = QPushButton("复制")
            copy_btn.setMaximumWidth(80)
            copy_btn.setEnabled(False)  # 初始禁用
            # 使用 partial 绑定参数
            copy_btn.clicked.connect(partial(self.copy_command, i))
            self.copy_buttons.append(copy_btn)

            cmd_layout.addWidget(label)
            cmd_layout.addWidget(text_box)
            cmd_layout.addWidget(copy_btn)

            layout.addLayout(cmd_layout)

    def set_commands(self, commands: list):
        """
        设置命令文本

        Args:
            commands: 命令列表 [train_cmd, val_cmd, test_cmd]
        """
        for i, cmd in enumerate(commands):
            if i < len(self.command_boxes):
                self.command_boxes[i].setText(cmd)
                # 启用对应的复制按钮
                if i < len(self.copy_buttons):
                    self.copy_buttons[i].setEnabled(True)

    def copy_command(self, index: int):
        """
        复制指定命令到剪贴板

        Args:
            index: 命令索引 (0=train, 1=val, 2=test)
        """
        if index < len(self.command_boxes):
            command = self.command_boxes[index].toPlainText()
            if command:
                clipboard = QApplication.clipboard()
                clipboard.setText(command)
                QMessageBox.information(
                    self,
                    "复制成功",
                    "命令已复制到剪贴板"
                )

