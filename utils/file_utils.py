"""文件系统操作工具"""

import os
import shutil
import re
from typing import List


def safe_create_directory(path: str) -> None:
    """
    安全创建目录

    Args:
        path: 目录路径

    Raises:
        OSError: 创建失败时抛出异常
    """
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        raise OSError(f"创建目录失败: {path}\n错误: {str(e)}")


def safe_copy_file(src: str, dst: str) -> None:
    """
    安全复制文件

    Args:
        src: 源文件路径
        dst: 目标文件路径

    Raises:
        FileNotFoundError: 源文件不存在
        OSError: 复制失败时抛出异常
    """
    try:
        if not os.path.exists(src):
            raise FileNotFoundError(f"源文件不存在: {src}")

        # 确保目标目录存在
        dst_dir = os.path.dirname(dst)
        if dst_dir:
            safe_create_directory(dst_dir)

        shutil.copy2(src, dst)
    except (FileNotFoundError, OSError) as e:
        raise OSError(f"复制文件失败: {src} -> {dst}\n错误: {str(e)}")


def natural_sort_key(text: str) -> List:
    """
    自然排序的键函数

    Args:
        text: 待排序的文本

    Returns:
        用于排序的键列表

    Example:
        ['1.jpg', '2.jpg', '10.jpg'] 而不是 ['1.jpg', '10.jpg', '2.jpg']
    """
    def atoi(s):
        return int(s) if s.isdigit() else s.lower()

    return [atoi(c) for c in re.split(r'(\d+)', text)]


def natural_sort(file_list: List[str]) -> List[str]:
    """
    对文件列表进行自然排序

    Args:
        file_list: 文件路径列表

    Returns:
        排序后的文件列表

    Example:
        >>> natural_sort(['img10.jpg', 'img2.jpg', 'img1.jpg'])
        ['img1.jpg', 'img2.jpg', 'img10.jpg']
    """
    return sorted(file_list, key=natural_sort_key)


def get_file_extension(filename: str) -> str:
    """
    获取文件扩展名（小写，不含点）

    Args:
        filename: 文件名

    Returns:
        扩展名（小写）

    Example:
        >>> get_file_extension('image.JPG')
        'jpg'
    """
    return os.path.splitext(filename)[1].lower().lstrip('.')


def is_image_file(filename: str) -> bool:
    """
    判断是否为图片文件

    Args:
        filename: 文件名

    Returns:
        是否为支持的图片格式
    """
    supported_extensions = {'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif'}
    return get_file_extension(filename) in supported_extensions
