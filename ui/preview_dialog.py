"""Dry-Run 预览对话框"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QDialogButtonBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class PreviewDialog(QDialog):
    """Dry-Run 预览对话框"""

    def __init__(self, dataset_root: str, image_count: int, preview_images: list,
                 parent=None, mode="create", extra_info=""):
        """
        Args:
            dataset_root: 数据集根目录
            image_count: 图片数量
            preview_images: [(原文件名, 新文件名), ...] 列表
            parent: 父窗口
            mode: "create" 或 "extend"
            extra_info: 扩展模式下的额外信息（如最大编号）
        """
        super().__init__(parent)
        self.dataset_root = dataset_root
        self.image_count = image_count
        self.preview_images = preview_images
        self.mode = mode
        self.extra_info = extra_info
        self.init_ui()

    def init_ui(self):
        """初始化 UI"""
        self.setWindowTitle("预览：即将创建的内容")
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout(self)

        # 标题
        title = QLabel("📋 Dry-Run 预览")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # 说明
        desc = QLabel("以下内容将被创建（当前为预览模式，未实际创建）：")
        desc.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc)

        # 预览内容
        preview_text = self.generate_preview_text()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(preview_text)
        text_edit.setStyleSheet("font-family: Consolas, monospace; background-color: #f5f5f5;")
        layout.addWidget(text_edit)

        # 提示
        tip = QLabel(f"⚠️ 将复制 {self.image_count} 张图片到临时文件夹，原始图片不受影响")
        tip.setStyleSheet("color: #ff9800; font-weight: bold; margin-top: 10px;")
        tip.setWordWrap(True)
        layout.addWidget(tip)

        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.button(QDialogButtonBox.Ok).setText("确认创建")
        button_box.button(QDialogButtonBox.Cancel).setText("取消")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def generate_preview_text(self) -> str:
        """生成预览文本"""
        lines = []

        if self.mode == "extend":
            # 扩展模式：显示数据集路径和编号信息
            lines.append(f"扩展数据集: {self.dataset_root}")
            lines.append("")
            lines.append(self.extra_info.strip())  # 显示最大编号和起始编号
            lines.append("")
            lines.append(f"新增图片重命名（共 {self.image_count} 张）：")
        else:
            # 创建模式：显示完整目录结构（保持原有逻辑）
            lines.append(f"数据集根目录: {self.dataset_root}")
            lines.append("")
            lines.append("目录结构:")
            lines.append("├─ images/")
            lines.append("│   ├─ train/")
            lines.append("│   ├─ val/")
            lines.append("│   └─ test/")
            lines.append("├─ labels/")
            lines.append("│   ├─ train/")
            lines.append("│   ├─ val/")
            lines.append("│   ├─ test/")
            lines.append("│   └─ classes.txt")
            lines.append("├─ temp/  ← 重命名后的图片将存放于此")
            lines.append("└─ data.yaml")
            lines.append("")
            lines.append(f"图片重命名（共 {self.image_count} 张）：")

        # 共同部分：显示前10张图片的重命名预览
        for i, (old_name, new_name) in enumerate(self.preview_images[:10], 1):
            lines.append(f"  {old_name} → {new_name}")

        if len(self.preview_images) > 10:
            lines.append(f"  ... （还有 {len(self.preview_images) - 10} 张）")

        return '\n'.join(lines)
