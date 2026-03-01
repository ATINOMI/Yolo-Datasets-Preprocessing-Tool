"""比例输入对话框"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QDialogButtonBox, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QDoubleValidator


class RatioDialog(QDialog):
    """train / val / test 比例输入对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.train_ratio = 70.0
        self.val_ratio = 20.0
        self.test_ratio = 10.0
        self.init_ui()

    def init_ui(self):
        """初始化 UI"""
        self.setWindowTitle("配置数据集划分比例")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # 标题
        title = QLabel("配置 Train / Val / Test 比例")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # 说明
        desc = QLabel("请输入数据集划分比例（总和必须为 100）：")
        desc.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc)

        # 表单
        form_layout = QFormLayout()

        # Train 输入框
        self.train_input = QLineEdit("70")
        self.train_input.setValidator(QDoubleValidator(0.0, 100.0, 2))
        form_layout.addRow("Train 比例 (%):", self.train_input)

        # Val 输入框
        self.val_input = QLineEdit("20")
        self.val_input.setValidator(QDoubleValidator(0.0, 100.0, 2))
        form_layout.addRow("Val 比例 (%):", self.val_input)

        # Test 输入框
        self.test_input = QLineEdit("10")
        self.test_input.setValidator(QDoubleValidator(0.0, 100.0, 2))
        form_layout.addRow("Test 比例 (%):", self.test_input)

        layout.addLayout(form_layout)

        # 提示
        tip = QLabel("💡 提示：随机种子固定为 42，确保结果可复现")
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
        try:
            train = float(self.train_input.text())
            val = float(self.val_input.text())
            test = float(self.test_input.text())

            # 校验
            if train < 0 or val < 0 or test < 0:
                QMessageBox.warning(self, "输入错误", "比例不能为负数")
                return

            total = train + val + test
            if abs(total - 100.0) > 0.01:
                QMessageBox.warning(
                    self,
                    "比例错误",
                    f"比例总和必须为 100，当前为 {total}"
                )
                return

            # 保存结果
            self.train_ratio = train
            self.val_ratio = val
            self.test_ratio = test

            self.accept()

        except ValueError:
            QMessageBox.warning(self, "输入错误", "请输入有效的数字")
