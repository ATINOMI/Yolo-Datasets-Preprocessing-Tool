"""步骤状态管理模块"""

from enum import Enum
from typing import Optional


class StepStatus(Enum):
    """步骤状态枚举"""
    NOT_STARTED = "not_started"        # 未开始
    IN_PROGRESS = "in_progress"        # 进行中
    COMPLETED = "completed"            # 已完成
    NEED_REGENERATE = "need_regenerate"  # 需要重新生成


class StepState:
    """单个步骤的状态管理"""

    def __init__(self, step_number: int, step_name: str):
        """
        初始化步骤状态

        Args:
            step_number: 步骤编号 (1-6)
            step_name: 步骤名称
        """
        self.step_number = step_number
        self.step_name = step_name
        self.status = StepStatus.NOT_STARTED
        self.summary = ""  # 参数摘要
        self.error_message: Optional[str] = None

    def start(self):
        """标记步骤为进行中"""
        self.status = StepStatus.IN_PROGRESS
        self.error_message = None

    def complete(self, summary: str = ""):
        """
        标记步骤为已完成

        Args:
            summary: 参数摘要信息
        """
        self.status = StepStatus.COMPLETED
        self.summary = summary
        self.error_message = None

    def mark_need_regenerate(self):
        """标记需要重新生成"""
        self.status = StepStatus.NEED_REGENERATE

    def fail(self, error_message: str):
        """
        标记步骤失败

        Args:
            error_message: 错误信息
        """
        self.status = StepStatus.NOT_STARTED
        self.error_message = error_message

    def reset(self):
        """重置步骤状态"""
        self.status = StepStatus.NOT_STARTED
        self.summary = ""
        self.error_message = None

    def is_completed(self) -> bool:
        """检查是否已完成"""
        return self.status == StepStatus.COMPLETED

    def get_status_display(self) -> str:
        """获取状态显示文本"""
        status_map = {
            StepStatus.NOT_STARTED: "未完成",
            StepStatus.IN_PROGRESS: "进行中...",
            StepStatus.COMPLETED: "已完成",
            StepStatus.NEED_REGENERATE: "需重新生成"
        }
        return status_map.get(self.status, "未知")

    def to_dict(self) -> dict:
        """转换为字典（用于序列化）"""
        return {
            'step_number': self.step_number,
            'step_name': self.step_name,
            'status': self.status.value,
            'summary': self.summary,
            'error_message': self.error_message
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'StepState':
        """从字典创建实例（用于反序列化）"""
        step = cls(data['step_number'], data['step_name'])
        step.status = StepStatus(data['status'])
        step.summary = data.get('summary', '')
        step.error_message = data.get('error_message')
        return step
