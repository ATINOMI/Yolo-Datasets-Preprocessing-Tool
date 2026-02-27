"""参数校验工具"""

from typing import List, Tuple


def validate_ratios(train: float, val: float, test: float) -> Tuple[bool, str]:
    """
    校验 train/val/test 比例

    Args:
        train: 训练集比例
        val: 验证集比例
        test: 测试集比例

    Returns:
        (是否有效, 错误消息)

    Example:
        >>> validate_ratios(70, 20, 10)
        (True, '')
        >>> validate_ratios(70, 20, 5)
        (False, '比例总和必须为 100，当前为 95.0')
    """
    # 检查是否为负数
    if train < 0 or val < 0 or test < 0:
        return False, "比例不能为负数"

    # 检查总和是否为 100
    total = train + val + test
    if abs(total - 100.0) > 0.01:  # 允许浮点误差
        return False, f"比例总和必须为 100，当前为 {total}"

    # 检查是否至少有一个非零
    if train == 0 and val == 0 and test == 0:
        return False, "至少需要一个非零比例"

    return True, ""


def validate_classes(text: str) -> Tuple[List[str], str]:
    """
    校验并清理类别文本

    Args:
        text: 多行类别文本

    Returns:
        (类别列表, 错误消息)

    处理规则：
        - 去除空行
        - 去除每行首尾空格
        - 去除重复类别
        - 保持顺序

    Example:
        >>> validate_classes("  person  \\n\\ncar\\nperson\\n")
        (['person', 'car'], '')
    """
    if not text or not text.strip():
        return [], "类别列表不能为空"

    # 按行分割
    lines = text.strip().split('\n')

    # 清理每一行：去除首尾空格，过滤空行
    classes = []
    seen = set()

    for line in lines:
        cleaned = line.strip()
        if cleaned and cleaned not in seen:
            classes.append(cleaned)
            seen.add(cleaned)

    if not classes:
        return [], "至少需要一个类别"

    return classes, ""


def validate_dataset_name(name: str) -> Tuple[bool, str]:
    """
    校验数据集名称

    Args:
        name: 数据集名称

    Returns:
        (是否有效, 错误消息)

    规则：
        - 不能为空
        - 不能包含非法字符（Windows 路径非法字符）
    """
    if not name or not name.strip():
        return False, "数据集名称不能为空"

    # Windows 非法字符
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
        if char in name:
            return False, f"数据集名称不能包含非法字符: {char}"

    return True, ""


def validate_yaml_filename(filename: str) -> Tuple[bool, str]:
    """
    校验 YAML 文件名

    Args:
        filename: YAML 文件名

    Returns:
        (是否有效, 错误消息)
    """
    if not filename or not filename.strip():
        return False, "YAML 文件名不能为空"

    # 检查扩展名
    if not filename.lower().endswith(('.yaml', '.yml')):
        return False, "YAML 文件名必须以 .yaml 或 .yml 结尾"

    # 检查非法字符
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
        if char in filename:
            return False, f"文件名不能包含非法字符: {char}"

    return True, ""
