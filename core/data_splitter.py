"""数据划分器 - Step 3"""

import random
from typing import List, Tuple
import os
from utils.file_utils import safe_copy_file


class DataSplitter:
    """train / val / test 数据划分器"""

    @staticmethod
    def split_data(
        images: List[str],
        train_ratio: float,
        val_ratio: float,
        test_ratio: float,
        seed: int = 42
    ) -> Tuple[List[str], List[str], List[str], str]:
        """
        按比例划分数据集

        Args:
            images: 图片路径列表
            train_ratio: 训练集比例 (0-100)
            val_ratio: 验证集比例 (0-100)
            test_ratio: 测试集比例 (0-100)
            seed: 随机种子（保证可复现）

        Returns:
            (train_list, val_list, test_list, error_message)
        """
        try:
            if not images:
                return [], [], [], "图片列表为空"

            # 设置随机种子
            random.seed(seed)

            # 复制并打乱
            shuffled = images.copy()
            random.shuffle(shuffled)

            # 计算数量
            total = len(shuffled)
            train_count = int(total * train_ratio / 100)
            val_count = int(total * val_ratio / 100)
            # test_count 为剩余部分，确保总数不变

            # 划分
            train_list = shuffled[:train_count]
            val_list = shuffled[train_count:train_count + val_count]
            test_list = shuffled[train_count + val_count:]

            return train_list, val_list, test_list, ""

        except Exception as e:
            return [], [], [], f"数据划分失败: {str(e)}"

    @staticmethod
    def copy_images_to_subset(
        images: List[str],
        target_dir: str
    ) -> Tuple[int, str]:
        """
        复制图片到目标目录

        Args:
            images: 图片路径列表
            target_dir: 目标目录

        Returns:
            (成功复制的数量, 错误消息)
        """
        try:
            os.makedirs(target_dir, exist_ok=True)

            success_count = 0
            for img_path in images:
                filename = os.path.basename(img_path)
                dst_path = os.path.join(target_dir, filename)
                safe_copy_file(img_path, dst_path)
                success_count += 1

            return success_count, ""

        except Exception as e:
            return 0, f"复制图片失败: {str(e)}"
