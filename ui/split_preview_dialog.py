"""数据拆分预览对话框"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit, QDialogButtonBox
)
from PySide6.QtGui import QFont


class SplitPreviewDialog(QDialog):
    """数据拆分 Dry-Run 预览对话框"""

    def __init__(self, train_count: int, val_count: int, test_count: int, parent=None):
        super().__init__(parent)
        self.train_count = train_count
        self.val_count = val_count
        self.test_count = test_count
        self.init_ui()

    def init_ui(self):
        """初始化 UI"""
        self.setWindowTitle("预览：数据拆分")
        self.setMinimumSize(500, 350)

        layout = QVBoxLayout(self)

        # 标题
        title = QLabel("📊 数据拆分预览")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # 说明
        desc = QLabel("以下是即将执行的数据拆分（当前为预览模式）：")
        desc.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc)

        # 预览内容
        preview_text = self.generate_preview_text()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(preview_text)
        text_edit.setStyleSheet("font-family: Consolas, monospace; background-color: #f5f5f5; font-size: 11pt;")
        layout.addWidget(text_edit)

        # 提示
        total = self.train_count + self.val_count + self.test_count
        tip = QLabel(f"⚠️ 将从 temp/ 文件夹复制 {total} 张图片到各子集文件夹")
        tip.setStyleSheet("color: #ff9800; font-weight: bold; margin-top: 10px;")
        tip.setWordWrap(True)
        layout.addWidget(tip)

        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.button(QDialogButtonBox.Ok).setText("确认拆分")
        button_box.button(QDialogButtonBox.Cancel).setText("取消")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def generate_preview_text(self) -> str:
        """生成预览文本"""
        total = self.train_count + self.val_count + self.test_count

        lines = [
            "数据拆分结果：",
            "",
            f"📁 images/train/",
            f"   └─ {self.train_count} 张图片 ({self.train_count / total * 100:.1f}%)",
            "",
            f"📁 images/val/",
            f"   └─ {self.val_count} 张图片 ({self.val_count / total * 100:.1f}%)",
            "",
            f"📁 images/test/",
            f"   └─ {self.test_count} 张图片 ({self.test_count / total * 100:.1f}%)",
            "",
            "─" * 50,
            f"总计: {total} 张图片",
            "",
            "说明：",
            "• 图片将按固定随机种子（42）打乱后划分",
            "• 原始图片（temp/ 文件夹）不会被删除",
            "• 每次执行结果相同（可复现）",
        ]

        return '\n'.join(lines)
