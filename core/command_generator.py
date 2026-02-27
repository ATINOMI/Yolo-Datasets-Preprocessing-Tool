"""LabelImg 命令生成器 - Step 6"""

import os
from typing import List, Tuple


class CommandGenerator:
    """LabelImg 命令生成器"""

    @staticmethod
    def generate_commands(
        dataset_root: str,
        classes_file: str
    ) -> Tuple[List[str], str]:
        """
        生成 labelimg 命令

        Args:
            dataset_root: 数据集根目录
            classes_file: classes.txt 文件路径

        Returns:
            (命令列表 [train_cmd, val_cmd, test_cmd], 错误消息)

        命令格式:
            labelimg "图片目录" "类别文件" "标注保存目录"
        """
        try:
            commands = []

            for subset in ['train', 'val', 'test']:
                images_dir = os.path.join(dataset_root, 'images', subset)
                labels_dir = os.path.join(dataset_root, 'labels', subset)

                # 正确的参数顺序：图片目录 -> 类别文件 -> 标注保存目录
                # 所有路径用双引号包裹（处理空格和括号）
                cmd = f'labelimg "{images_dir}" "{classes_file}" "{labels_dir}"'
                commands.append(cmd)

            return commands, ""

        except Exception as e:
            return [], f"生成命令失败: {str(e)}"

