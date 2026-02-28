"""右侧目录树视图 - 显示 YOLO 数据集目录结构"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTreeWidget,
    QTreeWidgetItem, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class TreeViewPanel(QWidget):
    """目录树视图面板"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)

        # 标题区域
        header_layout = QVBoxLayout()

        title = QLabel("数据集目录结构")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)

        # 模式提示
        mode_label = QLabel("● Preview Mode (预览模式)")
        mode_label.setStyleSheet("color: #888; font-size: 9pt;")

        header_layout.addWidget(title)
        header_layout.addWidget(mode_label)

        layout.addLayout(header_layout)

        # 树形视图
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("目录 / 文件")
        self.tree.setFrameShape(QFrame.Box)

        # 填充虚拟目录结构
        self.populate_preview_tree()

        layout.addWidget(self.tree)

    def populate_preview_tree(self):
        """填充预览目录结构"""
        self.tree.clear()

        # 根节点
        root = QTreeWidgetItem(self.tree, ["dataset_name/"])
        root.setExpanded(True)

        # images 目录
        images = QTreeWidgetItem(root, ["images/"])
        images.setExpanded(True)
        QTreeWidgetItem(images, ["train/"])
        QTreeWidgetItem(images, ["val/"])
        QTreeWidgetItem(images, ["test/"])

        # labels 目录
        labels = QTreeWidgetItem(root, ["labels/"])
        labels.setExpanded(True)
        QTreeWidgetItem(labels, ["train/"])
        QTreeWidgetItem(labels, ["val/"])
        QTreeWidgetItem(labels, ["test/"])
        QTreeWidgetItem(labels, ["classes.txt"])

        # YAML 文件
        QTreeWidgetItem(root, ["data.yaml"])
