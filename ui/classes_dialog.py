"""类别输入对话框"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit,
    QDialogButtonBox, QMessageBox
)
from PySide6.QtGui import QFont


class ClassesDialog(QDialog):
    """类别列表输入对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.classes = []
        self.init_ui()

    def init_ui(self):
        """初始化 UI"""
        self.setWindowTitle("输入类别列表")
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout(self)

        # 标题
        title = QLabel("输入类别列表")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # 说明
        desc = QLabel("请输入类别名称，每行一个：")
        desc.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc)

        # 文本输入框
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("例如：\nperson\ncar\nbike\ndog\ncat")
        self.text_edit.setStyleSheet("font-family: Consolas, monospace; font-size: 11pt;")
        layout.addWidget(self.text_edit)

        # 提示
        tip = QLabel(
            "💡 提示：\n"
            "• 空行将被自动忽略\n"
            "• 首尾空格将被自动去除\n"
            "• 重复的类别将被自动去重"
        )
        tip.setStyleSheet("color: #2196F3; font-size: 9pt; margin-top: 10px;")
        layout.addWidget(tip)

        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.button(QDialogButtonBox.Ok).setText("确认")
        button_box.button(QDialogButtonBox.Cancel).setText("取消")
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def validate_and_accept(self):
        """校验并接受"""
        text = self.text_edit.toPlainText()

        if not text or not text.strip():
            QMessageBox.warning(self, "输入错误", "类别列表不能为空")
            return

        # 处理类别：按行分割，去除空行和空格，去重
        lines = text.strip().split('\n')
        classes = []
        seen = set()

        for line in lines:
            cleaned = line.strip()
            if cleaned and cleaned not in seen:
                classes.append(cleaned)
                seen.add(cleaned)

        if not classes:
            QMessageBox.warning(self, "输入错误", "至少需要一个有效的类别")
            return

        # 保存结果
        self.classes = classes
        self.accept()
