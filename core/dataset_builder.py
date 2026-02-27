"""数据集目录结构构建器 - Step 2"""

import os
from typing import Tuple
from utils.file_utils import safe_create_directory


class DatasetBuilder:
    """YOLO 数据集目录结构构建器"""

    STRUCTURE = {
        'images': ['train', 'val', 'test'],
        'labels': ['train', 'val', 'test']
    }

    @staticmethod
    def validate_not_exists(path: str) -> Tuple[bool, str]:
        """
        验证路径是否不存在

        Args:
            path: 路径

        Returns:
            (是否有效, 错误消息)
        """
        if os.path.exists(path):
            return False, f"路径已存在，请选择其他位置或名称: {path}"
        return True, ""

    @staticmethod
    def create_structure(parent_dir: str, dataset_name: str) -> Tuple[str, str]:
        """
        创建 YOLO 标准目录结构

        目录结构:
            dataset_name/
             ├─ images/
             │   ├─ train/
             │   ├─ val/
             │   └─ test/
             └─ labels/
                 ├─ train/
                 ├─ val/
                 ├─ test/
                 └─ classes.txt

        Args:
            parent_dir: 父目录路径
            dataset_name: 数据集名称

        Returns:
            (数据集根路径, 错误消息)
        """
        try:
            # 数据集根目录
            dataset_root = os.path.join(parent_dir, dataset_name)

            # 检查是否已存在
            valid, error = DatasetBuilder.validate_not_exists(dataset_root)
            if not valid:
                return "", error

            # 创建主目录结构
            for main_dir, sub_dirs in DatasetBuilder.STRUCTURE.items():
                main_path = os.path.join(dataset_root, main_dir)
                safe_create_directory(main_path)

                # 创建子目录
                for sub_dir in sub_dirs:
                    sub_path = os.path.join(main_path, sub_dir)
                    safe_create_directory(sub_path)

            # 创建 classes.txt（空文件）
            classes_file = os.path.join(dataset_root, 'labels', 'classes.txt')
            with open(classes_file, 'w', encoding='utf-8') as f:
                f.write("")

            return dataset_root, ""

        except Exception as e:
            return "", f"创建目录结构失败: {str(e)}"

    @staticmethod
    def get_images_path(dataset_root: str, subset: str) -> str:
        """
        获取图片目录路径

        Args:
            dataset_root: 数据集根目录
            subset: 子集名称 ('train', 'val', 'test')

        Returns:
            完整路径
        """
        return os.path.join(dataset_root, 'images', subset)

    @staticmethod
    def get_labels_path(dataset_root: str, subset: str) -> str:
        """
        获取标签目录路径

        Args:
            dataset_root: 数据集根目录
            subset: 子集名称 ('train', 'val', 'test')

        Returns:
            完整路径
        """
        return os.path.join(dataset_root, 'labels', subset)

    @staticmethod
    def get_classes_file_path(dataset_root: str) -> str:
        """
        获取 classes.txt 文件路径

        Args:
            dataset_root: 数据集根目录

        Returns:
            完整路径
        """
        return os.path.join(dataset_root, 'labels', 'classes.txt')
