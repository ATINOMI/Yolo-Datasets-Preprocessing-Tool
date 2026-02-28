"""数据集配置数据模型"""

from typing import List, Optional
from models.step_state import StepState


class DatasetConfig:
    """数据集配置 - 存储整个工作流的状态数据"""

    def __init__(self):
        # Step 1: 原始图片导入
        self.raw_images_folder: Optional[str] = None
        self.processed_images: List[str] = []  # 处理后的图片列表
        self.image_count: int = 0

        # Step 2: 数据集目录结构
        self.dataset_parent_dir: Optional[str] = None
        self.dataset_name: str = ""
        self.dataset_root: Optional[str] = None  # 完整路径

        # Step 3: 数据划分
        self.train_ratio: float = 70.0
        self.val_ratio: float = 20.0
        self.test_ratio: float = 10.0
        self.random_seed: int = 42
        self.train_count: int = 0
        self.val_count: int = 0
        self.test_count: int = 0

        # Step 4: 类别管理
        self.classes: List[str] = []

        # Step 5: YAML 文件
        self.yaml_filename: str = "data.yaml"
        self.yaml_path: Optional[str] = None

        # Step 6: LabelImg 命令
        self.labelimg_commands: List[str] = []

        # 步骤状态管理
        self.steps = {
            1: StepState(1, "原始图片导入"),
            2: StepState(2, "数据集目录结构创建"),
            3: StepState(3, "数据划分"),
            4: StepState(4, "类别管理"),
            5: StepState(5, "YAML 文件生成"),
            6: StepState(6, "LabelImg 命令生成"),
        }

    def get_step(self, step_number: int) -> StepState:
        """获取指定步骤的状态"""
        return self.steps[step_number]

    def is_step_completed(self, step_number: int) -> bool:
        """检查指定步骤是否已完成"""
        return self.steps[step_number].is_completed()

    def mark_dependent_steps_need_regenerate(self, from_step: int):
        """
        标记依赖步骤需要重新生成

        Args:
            from_step: 从哪个步骤开始标记（包含该步骤之后的所有步骤）
        """
        for step_num in range(from_step + 1, 7):
            if self.steps[step_num].is_completed():
                self.steps[step_num].mark_need_regenerate()

    def to_dict(self) -> dict:
        """转换为字典（用于序列化）"""
        return {
            'raw_images_folder': self.raw_images_folder,
            'processed_images': self.processed_images,
            'image_count': self.image_count,
            'dataset_parent_dir': self.dataset_parent_dir,
            'dataset_name': self.dataset_name,
            'dataset_root': self.dataset_root,
            'train_ratio': self.train_ratio,
            'val_ratio': self.val_ratio,
            'test_ratio': self.test_ratio,
            'random_seed': self.random_seed,
            'train_count': self.train_count,
            'val_count': self.val_count,
            'test_count': self.test_count,
            'classes': self.classes,
            'yaml_filename': self.yaml_filename,
            'yaml_path': self.yaml_path,
            'labelimg_commands': self.labelimg_commands,
            'steps': {k: v.to_dict() for k, v in self.steps.items()}
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DatasetConfig':
        """从字典创建实例（用于反序列化）"""
        config = cls()

        # 基本数据
        config.raw_images_folder = data.get('raw_images_folder')
        config.processed_images = data.get('processed_images', [])
        config.image_count = data.get('image_count', 0)
        config.dataset_parent_dir = data.get('dataset_parent_dir')
        config.dataset_name = data.get('dataset_name', '')
        config.dataset_root = data.get('dataset_root')
        config.train_ratio = data.get('train_ratio', 70.0)
        config.val_ratio = data.get('val_ratio', 20.0)
        config.test_ratio = data.get('test_ratio', 10.0)
        config.random_seed = data.get('random_seed', 42)
        config.train_count = data.get('train_count', 0)
        config.val_count = data.get('val_count', 0)
        config.test_count = data.get('test_count', 0)
        config.classes = data.get('classes', [])
        config.yaml_filename = data.get('yaml_filename', 'data.yaml')
        config.yaml_path = data.get('yaml_path')
        config.labelimg_commands = data.get('labelimg_commands', [])

        # 步骤状态
        if 'steps' in data:
            for step_num, step_data in data['steps'].items():
                config.steps[int(step_num)] = StepState.from_dict(step_data)

        return config
