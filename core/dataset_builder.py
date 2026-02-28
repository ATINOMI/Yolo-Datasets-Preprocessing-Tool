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

    @staticmethod
    def validate_existing_structure(dataset_root: str) -> Tuple[bool, str]:
        """
        验证目录是否为有效的 YOLO 数据集结构

        必需的目录结构:
            dataset_root/
            ├── images/
            │   ├── train/
            │   ├── val/
            │   └── test/
            └── labels/  (可选，不会导致失败)

        Args:
            dataset_root: 数据集根目录路径

        Returns:
            (True, "") 如果结构有效
            (False, "错误描述") 如果结构无效
        """
        # 检查目录是否存在
        if not os.path.exists(dataset_root):
            return False, f"目录不存在: {dataset_root}"

        if not os.path.isdir(dataset_root):
            return False, f"路径不是目录: {dataset_root}"

        # 检查必需的子目录
        required_paths = [
            ('images/train', os.path.join(dataset_root, 'images', 'train')),
            ('images/val', os.path.join(dataset_root, 'images', 'val')),
            ('images/test', os.path.join(dataset_root, 'images', 'test'))
        ]

        missing = []
        for display_path, full_path in required_paths:
            if not os.path.exists(full_path):
                missing.append(display_path)

        if missing:
            msg = "选择的目录不是有效的 YOLO 数据集\n\n缺少必需目录:\n"
            for path in missing:
                msg += f"  ✗ {path}\n"
            msg += "\n请选择包含标准 YOLO 目录结构的数据集"
            return False, msg

        return True, ""

    @staticmethod
    def find_max_image_index(dataset_root: str) -> Tuple[int, str]:
        """
        扫描所有子集中的图片，查找最大的4位编号

        编号模式: ####.{ext} 其中 #### 为 0001-9999

        Args:
            dataset_root: 数据集根目录路径

        Returns:
            (最大编号, "") 成功时
            (0, "错误信息") 失败时

        示例:
            数据集包含 0001.jpg, 0155.png → 返回 (155, "")
            空数据集 → 返回 (0, "")
        """
        try:
            import re
            # 匹配4位数字 + 支持的图片扩展名
            pattern = re.compile(r'^(\d{4})\.(jpg|jpeg|png|bmp|tiff|tif)$', re.IGNORECASE)

            max_idx = 0
            subsets = ['train', 'val', 'test']

            for subset in subsets:
                subset_path = DatasetBuilder.get_images_path(dataset_root, subset)
                if not os.path.exists(subset_path):
                    continue

                try:
                    filenames = os.listdir(subset_path)
                except OSError as e:
                    return 0, f"无法读取目录 {subset}: {str(e)}"

                for filename in filenames:
                    match = pattern.match(filename)
                    if match:
                        idx = int(match.group(1))
                        max_idx = max(max_idx, idx)

            return max_idx, ""

        except Exception as e:
            return 0, f"扫描图片编号失败: {str(e)}"
