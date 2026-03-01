"""草稿保存/加载管理"""

import json
import os
from typing import Optional, Tuple
from models.dataset_config import DatasetConfig


class DraftManager:
    """草稿管理器"""

    @staticmethod
    def save_draft(config: DatasetConfig, filepath: str) -> None:
        """
        保存草稿到 JSON 文件

        Args:
            config: 数据集配置
            filepath: 保存路径

        Raises:
            OSError: 保存失败时抛出异常
        """
        try:
            # 确保目录存在
            directory = os.path.dirname(filepath)
            if directory:
                os.makedirs(directory, exist_ok=True)

            # 转换为字典并保存
            data = config.to_dict()

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            raise OSError(f"保存草稿失败: {str(e)}")

    @staticmethod
    def load_draft(filepath: str) -> DatasetConfig:
        """
        从 JSON 文件加载草稿

        Args:
            filepath: 文件路径

        Returns:
            数据集配置对象

        Raises:
            FileNotFoundError: 文件不存在
            ValueError: JSON 格式错误
            OSError: 其他读取错误
        """
        try:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"草稿文件不存在: {filepath}")

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 从字典恢复配置
            config = DatasetConfig.from_dict(data)
            return config

        except json.JSONDecodeError as e:
            raise ValueError(f"草稿文件格式错误: {str(e)}")
        except FileNotFoundError:
            raise
        except Exception as e:
            raise OSError(f"加载草稿失败: {str(e)}")

    @staticmethod
    def validate_draft_file(filepath: str) -> Tuple[bool, str]:
        """
        验证草稿文件是否有效

        Args:
            filepath: 文件路径

        Returns:
            (是否有效, 错误消息)
        """
        if not os.path.exists(filepath):
            return False, "文件不存在"

        if not filepath.lower().endswith('.json'):
            return False, "必须是 JSON 文件"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                json.load(f)
            return True, ""
        except json.JSONDecodeError:
            return False, "JSON 格式错误"
        except Exception as e:
            return False, f"读取文件失败: {str(e)}"
