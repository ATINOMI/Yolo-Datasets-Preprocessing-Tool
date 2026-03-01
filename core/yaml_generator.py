"""YAML 文件生成器 - Step 5"""

import os
from typing import List, Tuple


class YAMLGenerator:
    """YOLO 训练配置 YAML 文件生成器"""

    @staticmethod
    def generate_yaml(
        dataset_root: str,
        classes: List[str],
        output_filename: str = "data.yaml"
    ) -> Tuple[str, str]:
        """
        生成 YOLO 训练 YAML 文件

        Args:
            dataset_root: 数据集根目录
            classes: 类别列表
            output_filename: YAML 文件名

        Returns:
            (YAML 文件路径, 错误消息)

        生成格式:
            path: <dataset_root_path>
            train: images/train
            val: images/val
            test: images/test

            names:
              - class_name_1
              - class_name_2
        """
        try:
            if not classes:
                return "", "类别列表不能为空"

            # YAML 文件路径
            yaml_path = os.path.join(dataset_root, output_filename)

            # 生成 YAML 内容
            lines = [
                f"path: {dataset_root}",
                "train: images/train",
                "val: images/val",
                "test: images/test",
                "",
                "names:"
            ]

            # 添加类别（使用列表格式）
            for class_name in classes:
                lines.append(f"  - {class_name}")

            # 写入文件
            with open(yaml_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            return yaml_path, ""

        except Exception as e:
            return "", f"生成 YAML 文件失败: {str(e)}"

    @staticmethod
    def write_classes_file(
        classes_file_path: str,
        classes: List[str]
    ) -> Tuple[bool, str]:
        """
        写入 classes.txt 文件

        Args:
            classes_file_path: classes.txt 文件路径
            classes: 类别列表

        Returns:
            (是否成功, 错误消息)
        """
        try:
            if not classes:
                return False, "类别列表不能为空"

            # 确保目录存在
            directory = os.path.dirname(classes_file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)

            # 写入文件（每行一个类别）
            with open(classes_file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(classes))

            return True, ""

        except Exception as e:
            return False, f"写入 classes.txt 失败: {str(e)}"
