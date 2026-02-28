"""数据集操作模式选择对话框"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QRadioButton,
    QDialogButtonBox, QButtonGroup
)
from PySide6.QtGui import QFont


class ModeSelectionDialog(QDialog):
    """选择创建新数据集或扩展已有数据集"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mode = "create"  # 默认模式
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("选择操作模式")
        self.setMinimumWidth(480)

        layout = QVBoxLayout(self)

        # 标题
        title = QLabel("Step 2: 数据集目录结构")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # 说明文字
        desc = QLabel("请选择操作模式：")
        desc.setStyleSheet("color: #666; margin: 10px 0;")
        layout.addWidget(desc)

        # 单选按钮：创建新数据集
        self.btn_create = QRadioButton("创建新数据集")
        self.btn_create.setChecked(True)

        # 单选按钮：扩展已有数据集
        self.btn_extend = QRadioButton("扩展已有数据集")

        # 按钮组（确保互斥）
        button_group = QButtonGroup(self)
        button_group.addButton(self.btn_create)
        button_group.addButton(self.btn_extend)

        layout.addWidget(self.btn_create)
        create_hint = QLabel("    → 新建目录结构，图片从 0001 开始编号")
        create_hint.setStyleSheet("color: #999; font-size: 9pt;")
        layout.addWidget(create_hint)

        layout.addSpacing(10)

        layout.addWidget(self.btn_extend)
        extend_hint = QLabel("    → 选择已有数据集，新图片接续现有编号")
        extend_hint.setStyleSheet("color: #999; font-size: 9pt;")
        layout.addWidget(extend_hint)

        layout.addSpacing(20)

        # 对话框按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.button(QDialogButtonBox.Ok).setText("确认")
        button_box.button(QDialogButtonBox.Cancel).setText("取消")
        button_box.accepted.connect(self.on_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def on_accept(self):
        """用户点击确认"""
        self.mode = "create" if self.btn_create.isChecked() else "extend"
        self.accept()
