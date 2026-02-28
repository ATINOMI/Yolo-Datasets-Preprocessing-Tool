"""图片处理器 - Step 1"""

import os
from typing import List, Tuple
from utils.file_utils import natural_sort, is_image_file, safe_copy_file


class ImageProcessor:
    """图片扫描、重命名、复制处理器"""

    @staticmethod
    def scan_images(folder_path: str) -> Tuple[List[str], str]:
        """
        扫描文件夹中的图片文件

        Args:
            folder_path: 文件夹路径

        Returns:
            (图片文件路径列表, 错误消息)
        """
        try:
            if not os.path.exists(folder_path):
                return [], f"文件夹不存在: {folder_path}"

            if not os.path.isdir(folder_path):
                return [], f"路径不是文件夹: {folder_path}"

            # 扫描所有文件
            all_files = []
            for filename in os.listdir(folder_path):
                filepath = os.path.join(folder_path, filename)
                if os.path.isfile(filepath) and is_image_file(filename):
                    all_files.append(filepath)

            if not all_files:
                return [], "文件夹中没有找到图片文件（支持的格式：jpg, jpeg, png, bmp, tiff）"

            # 自然排序
            sorted_files = natural_sort(all_files)

            return sorted_files, ""

        except Exception as e:
            return [], f"扫描图片失败: {str(e)}"

    @staticmethod
    def rename_and_copy(
        images: List[str],
        output_folder: str,
        start_index: int = 1
    ) -> Tuple[List[str], str]:
        """
        重命名并复制图片到目标文件夹

        Args:
            images: 原始图片路径列表（已排序）
            output_folder: 输出文件夹
            start_index: 起始编号（默认从 1 开始）

        Returns:
            (新图片路径列表, 错误消息)

        重命名格式: 0001.jpg, 0002.jpg, 0003.jpg, ...
        """
        try:
            # 创建输出文件夹
            os.makedirs(output_folder, exist_ok=True)

            new_images = []
            total = len(images)

            for i, src_path in enumerate(images, start=start_index):
                # 获取原始扩展名
                _, ext = os.path.splitext(src_path)
                if not ext:
                    ext = '.jpg'  # 默认扩展名

                # 生成新文件名：4 位数字 + 原扩展名
                new_filename = f"{i:04d}{ext.lower()}"
                dst_path = os.path.join(output_folder, new_filename)

                # 复制文件
                safe_copy_file(src_path, dst_path)
                new_images.append(dst_path)

            return new_images, ""

        except Exception as e:
            return [], f"重命名复制失败: {str(e)}"

    @staticmethod
    def process_images(
        folder_path: str,
        output_folder: str
    ) -> Tuple[List[str], int, str]:
        """
        完整的图片处理流程：扫描 → 重命名 → 复制

        Args:
            folder_path: 原始图片文件夹
            output_folder: 输出文件夹

        Returns:
            (处理后的图片路径列表, 图片数量, 错误消息)
        """
        # 扫描图片
        images, error = ImageProcessor.scan_images(folder_path)
        if error:
            return [], 0, error

        # 重命名并复制
        new_images, error = ImageProcessor.rename_and_copy(images, output_folder)
        if error:
            return [], 0, error

        return new_images, len(new_images), ""
