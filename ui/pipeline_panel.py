"""左侧步骤面板 - 显示 6 个处理步骤"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class StepCard(QFrame):
    """单个步骤卡片"""

    execute_clicked = Signal(int)  # 发射步骤编号

    def __init__(self, step_number: int, step_name: str, parent=None):
        super().__init__(parent)
        self.step_number = step_number
        self.step_name = step_name
        self.init_ui()

    def init_ui(self):
        """初始化 UI"""
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(1)
        self.setStyleSheet("""
            StepCard {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
            }
        """)

        layout = QVBoxLayout(self)

        # 顶部：步骤编号和名称
        top_layout = QHBoxLayout()

        # 步骤编号
        number_label = QLabel(f"Step {self.step_number}")
        number_label.setStyleSheet("color: #666; font-weight: bold;")

        # 状态图标（暂时显示圆点）
        self.status_label = QLabel("●")
        self.status_label.setStyleSheet("color: #ccc; font-size: 16px;")

        top_layout.addWidget(number_label)
        top_layout.addStretch()
        top_layout.addWidget(self.status_label)

        # 步骤名称
        name_label = QLabel(self.step_name)
        name_font = QFont()
        name_font.setPointSize(10)
        name_label.setFont(name_font)

        # 摘要信息（暂时为空）
        self.summary_label = QLabel("未完成")
        self.summary_label.setStyleSheet("color: #999; font-size: 9pt;")
        self.summary_label.setWordWrap(True)

        # 执行按钮
        self.execute_btn = QPushButton("执行")
        self.execute_btn.clicked.connect(lambda: self.execute_clicked.emit(self.step_number))
        self.execute_btn.setMaximumWidth(80)

        # 组装布局
        layout.addLayout(top_layout)
        layout.addWidget(name_label)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.execute_btn)

    def update_summary(self, text: str):
        """更新摘要信息"""
        self.summary_label.setText(text)

    def update_status(self, color: str):
        """
        更新状态图标颜色

        Args:
            color: 颜色值 (#ccc=未开始, #2196F3=已配置, #4CAF50=完成)
        """
        self.status_label.setStyleSheet(f"color: {color}; font-size: 16px;")


class PipelinePanel(QWidget):
    """步骤流程面板"""

    step_execute = Signal(int)  # 步骤执行信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.step_cards = {}
        self.init_ui()

    def init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)

        # 标题
        title = QLabel("处理流程")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)

        layout.addWidget(title)

        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        # 步骤容器
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(10)

        # 创建 6 个步骤卡片
        steps = [
            (1, "原始图片导入"),
            (2, "数据集目录结构创建"),
            (3, "数据划分 (train/val/test)"),
            (4, "类别管理 (classes.txt)"),
            (5, "YAML 文件生成"),
            (6, "LabelImg 命令生成"),
        ]

        for step_num, step_name in steps:
            card = StepCard(step_num, step_name)
            card.execute_clicked.connect(self.step_execute.emit)
            self.step_cards[step_num] = card
            container_layout.addWidget(card)

        container_layout.addStretch()

        scroll.setWidget(container)
        layout.addWidget(scroll)
