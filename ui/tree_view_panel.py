"""右侧目录树视图 - 显示 YOLO 数据集目录结构"""

import os
import subprocess
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTreeWidget,
    QTreeWidgetItem, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class TreeViewPanel(QWidget):
    """目录树视图面板"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # 状态存储
        self.dataset_root = None      # 数据集根路径
        self.dataset_name = None       # 数据集名称
        self.mode = None               # 'create' 或 'extend'
        self.root_item = None          # 根节点引用
        self.mode_label = None         # 模式标签引用
        self.init_ui()

    def init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)

        # 标题区域
        header_layout = QVBoxLayout()

        title = QLabel("数据集目录结构")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)

        # 模式提示（存储为实例属性）
        self.mode_label = QLabel("● Preview Mode (预览模式)")
        self.mode_label.setStyleSheet("color: #888; font-size: 9pt;")

        header_layout.addWidget(title)
        header_layout.addWidget(self.mode_label)

        layout.addLayout(header_layout)

        # 树形视图
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("目录 / 文件")
        self.tree.setFrameShape(QFrame.Box)

        # 禁用双击展开/折叠（避免与双击打开文件冲突）
        self.tree.setExpandsOnDoubleClick(False)

        # 增加缩进，让箭头区域更大更容易点击
        self.tree.setIndentation(30)  # 默认是 20，增加到 30

        # 连接双击事件
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)

        # 初始状态为空白（不再调用 populate_preview_tree）

        layout.addWidget(self.tree)

    def populate_preview_tree(self):
        """填充预览目录结构（保留但不使用，备用于演示模式）"""
        self.tree.clear()

        # 根节点
        root = QTreeWidgetItem(self.tree, ["dataset_name/"])
        root.setExpanded(True)

        # images 目录
        images = QTreeWidgetItem(root, ["images/"])
        images.setExpanded(True)
        QTreeWidgetItem(images, ["train/"])
        QTreeWidgetItem(images, ["val/"])
        QTreeWidgetItem(images, ["test/"])

        # labels 目录
        labels = QTreeWidgetItem(root, ["labels/"])
        labels.setExpanded(True)
        QTreeWidgetItem(labels, ["train/"])
        QTreeWidgetItem(labels, ["val/"])
        QTreeWidgetItem(labels, ["test/"])
        QTreeWidgetItem(labels, ["classes.txt"])

        # YAML 文件
        QTreeWidgetItem(root, ["data.yaml"])

    # ========== 新增：动态树构建方法 ==========

    def build_tree_extend(self, dataset_root: str):
        """
        扩展模式：扫描真实文件系统并构建树

        Args:
            dataset_root: 数据集根目录路径
        """
        self.tree.clear()
        self.dataset_root = dataset_root
        self.dataset_name = os.path.basename(dataset_root)
        self.mode = "extend"

        # 更新模式标签
        self.mode_label.setText("● Real Mode (真实结构)")
        self.mode_label.setStyleSheet("color: #4CAF50; font-size: 9pt;")

        # 创建根节点
        self.root_item = QTreeWidgetItem(self.tree, [self.dataset_name + "/"])
        self.root_item.setExpanded(True)
        self.root_item.setData(0, Qt.UserRole, dataset_root)

        # 递归扫描目录
        self._scan_directory(dataset_root, self.root_item)

    def build_tree_create_step2(self, dataset_name: str, dataset_root: str):
        """
        新建模式 Step 2：显示根节点和空文件夹结构

        Args:
            dataset_name: 数据集名称
            dataset_root: 数据集根路径
        """
        self.tree.clear()
        self.dataset_root = dataset_root
        self.dataset_name = dataset_name
        self.mode = "create"

        # 更新模式标签
        self.mode_label.setText("● Real Mode (真实结构)")
        self.mode_label.setStyleSheet("color: #4CAF50; font-size: 9pt;")

        # 创建根节点
        self.root_item = QTreeWidgetItem(self.tree, [dataset_name + "/"])
        self.root_item.setExpanded(True)
        self.root_item.setData(0, Qt.UserRole, dataset_root)

        # images/ 目录
        images_item = QTreeWidgetItem(self.root_item, ["images/"])
        images_item.setExpanded(True)
        images_path = os.path.join(dataset_root, "images")
        images_item.setData(0, Qt.UserRole, images_path)

        train_img_item = QTreeWidgetItem(images_item, ["train/"])
        train_img_item.setData(0, Qt.UserRole, os.path.join(images_path, "train"))

        val_img_item = QTreeWidgetItem(images_item, ["val/"])
        val_img_item.setData(0, Qt.UserRole, os.path.join(images_path, "val"))

        test_img_item = QTreeWidgetItem(images_item, ["test/"])
        test_img_item.setData(0, Qt.UserRole, os.path.join(images_path, "test"))

        # labels/ 目录
        labels_item = QTreeWidgetItem(self.root_item, ["labels/"])
        labels_item.setExpanded(True)
        labels_path = os.path.join(dataset_root, "labels")
        labels_item.setData(0, Qt.UserRole, labels_path)

        QTreeWidgetItem(labels_item, ["train/"]).setData(0, Qt.UserRole, os.path.join(labels_path, "train"))
        QTreeWidgetItem(labels_item, ["val/"]).setData(0, Qt.UserRole, os.path.join(labels_path, "val"))
        QTreeWidgetItem(labels_item, ["test/"]).setData(0, Qt.UserRole, os.path.join(labels_path, "test"))

        # temp/ 目录
        temp_item = QTreeWidgetItem(self.root_item, ["temp/"])
        temp_item.setData(0, Qt.UserRole, os.path.join(dataset_root, "temp"))

    def build_tree_create_step3(self, train_count: int, val_count: int, test_count: int):
        """
        新建模式 Step 3：添加图片数量提示（已弃用，使用 update_images_in_tree 替代）

        Args:
            train_count: train 图片数量
            val_count: val 图片数量
            test_count: test 图片数量
        """
        # 调用通用更新方法
        self.update_images_in_tree()

    def update_images_in_tree(self):
        """
        通用方法：更新预览树中 images/train、val、test 文件夹的图片信息
        扫描真实文件夹，显示图片数量和示例文件

        适用于新建模式和扩展模式的 Step 3
        """
        if not self.root_item or not self.dataset_root:
            return

        # 查找 images/ 节点
        images_item = self._find_item_by_text(self.root_item, "images/")
        if not images_item:
            return

        # 更新三个子集文件夹
        for subset in ['train', 'val', 'test']:
            subset_item = self._find_item_by_text(images_item, f"{subset}/")
            if not subset_item:
                continue

            # 清除该节点下的所有旧子节点
            subset_item.takeChildren()

            # 获取真实路径
            subset_path = subset_item.data(0, Qt.UserRole)
            if not subset_path or not os.path.exists(subset_path):
                continue

            # 扫描图片文件
            try:
                files = [f for f in os.listdir(subset_path)
                        if os.path.isfile(os.path.join(subset_path, f))
                        and f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'))]
                files.sort()  # 排序以保持一致性

                count = len(files)

                if count == 0:
                    # 无图片
                    hint = QTreeWidgetItem(subset_item, ["<暂无图片>"])
                    hint.setForeground(0, Qt.gray)
                    hint.setData(0, Qt.UserRole, subset_path)
                else:
                    # 添加数量提示
                    hint = QTreeWidgetItem(subset_item, [f"<共 {count} 张图片>"])
                    hint.setForeground(0, Qt.gray)
                    hint.setData(0, Qt.UserRole, subset_path)

                    # 添加前 5 张图片作为示例
                    max_preview = min(5, count)
                    for i in range(max_preview):
                        file_name = files[i]
                        file_path = os.path.join(subset_path, file_name)
                        file_item = QTreeWidgetItem(subset_item, [file_name])
                        file_item.setData(0, Qt.UserRole, file_path)

                    # 如果超过 5 张，显示省略提示
                    if count > 5:
                        more_hint = QTreeWidgetItem(subset_item, [f"... (还有 {count - 5} 张)"])
                        more_hint.setForeground(0, Qt.gray)
                        more_hint.setData(0, Qt.UserRole, subset_path)

            except Exception as e:
                # 扫描失败
                error_hint = QTreeWidgetItem(subset_item, [f"<扫描失败: {str(e)}>"])
                error_hint.setForeground(0, Qt.red)
                error_hint.setData(0, Qt.UserRole, subset_path)

    def build_tree_create_step4(self):
        """
        新建模式 Step 4：添加 classes.txt
        """
        if self.mode != "create" or not self.root_item:
            return

        # 查找 labels/ 节点
        labels_item = self._find_item_by_text(self.root_item, "labels/")
        if not labels_item:
            return

        # 添加 classes.txt
        classes_path = os.path.join(self.dataset_root, "labels", "classes.txt")
        classes_item = QTreeWidgetItem(labels_item, ["classes.txt"])
        classes_item.setData(0, Qt.UserRole, classes_path)

    def build_tree_create_step5(self, yaml_filename: str):
        """
        新建模式 Step 5：添加 YAML 文件

        Args:
            yaml_filename: YAML 文件名
        """
        if self.mode != "create" or not self.root_item:
            return

        # 在根节点下添加 YAML 文件
        yaml_path = os.path.join(self.dataset_root, yaml_filename)
        yaml_item = QTreeWidgetItem(self.root_item, [yaml_filename])
        yaml_item.setData(0, Qt.UserRole, yaml_path)

    def update_yaml_in_tree(self, new_yaml_filename: str, deleted_files: list = None):
        """
        更新预览树中的 YAML 文件节点（删除旧的，添加新的）

        Args:
            new_yaml_filename: 新的 YAML 文件名
            deleted_files: 被删除的旧 YAML 文件列表
        """
        if not self.root_item or not self.dataset_root:
            return

        # 1. 删除预览树中所有旧的 YAML 文件节点
        items_to_remove = []
        for i in range(self.root_item.childCount()):
            child = self.root_item.child(i)
            child_text = child.text(0)
            if child_text.lower().endswith('.yaml') or child_text.lower().endswith('.yml'):
                items_to_remove.append(child)

        for item in items_to_remove:
            index = self.root_item.indexOfChild(item)
            if index >= 0:
                self.root_item.takeChild(index)
                print(f"预览树中已删除旧 YAML 节点: {item.text(0)}")

        # 2. 添加新的 YAML 文件节点
        yaml_path = os.path.join(self.dataset_root, new_yaml_filename)
        yaml_item = QTreeWidgetItem(self.root_item, [new_yaml_filename])
        yaml_item.setData(0, Qt.UserRole, yaml_path)
        print(f"预览树中已添加新 YAML 节点: {new_yaml_filename}")

    # ========== 内部辅助方法 ==========

    def _scan_directory(self, dir_path: str, parent_item: QTreeWidgetItem):
        """
        递归扫描目录并填充树节点

        Args:
            dir_path: 要扫描的目录路径
            parent_item: 父节点
        """
        try:
            items = os.listdir(dir_path)
        except PermissionError:
            hint_item = QTreeWidgetItem(parent_item, ["<权限不足>"])
            hint_item.setForeground(0, Qt.red)
            return
        except Exception as e:
            hint_item = QTreeWidgetItem(parent_item, [f"<扫描失败: {str(e)}>"])
            hint_item.setForeground(0, Qt.red)
            return

        # 分离文件夹和文件
        folders = []
        files = []
        for item_name in items:
            item_path = os.path.join(dir_path, item_name)
            if os.path.isdir(item_path):
                folders.append((item_name, item_path))
            elif os.path.isfile(item_path):
                files.append((item_name, item_path))

        # 先添加文件夹（递归扫描）
        for folder_name, folder_path in sorted(folders):
            folder_item = QTreeWidgetItem(parent_item, [folder_name + "/"])
            folder_item.setData(0, Qt.UserRole, folder_path)
            self._scan_directory(folder_path, folder_item)

        # 再添加文件
        for file_name, file_path in sorted(files):
            file_item = QTreeWidgetItem(parent_item, [file_name])
            file_item.setData(0, Qt.UserRole, file_path)

    def _find_item_by_text(self, parent: QTreeWidgetItem, text: str) -> QTreeWidgetItem:
        """
        在父节点下查找指定文本的子节点

        Args:
            parent: 父节点
            text: 要查找的文本

        Returns:
            找到的节点，未找到返回 None
        """
        for i in range(parent.childCount()):
            child = parent.child(i)
            if child.text(0) == text:
                return child
        return None

    def _on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """
        双击事件处理器

        Args:
            item: 被双击的节点
            column: 列索引
        """
        path = item.data(0, Qt.UserRole)
        if not path:
            return

        # 判断是文件还是文件夹
        if os.path.isfile(path):
            # 文件：用默认程序打开
            self._open_file(path)
        elif os.path.isdir(path):
            # 文件夹：在资源管理器中打开
            self._open_in_explorer(path, select_file=False)
        else:
            # 路径不存在（如提示文本节点），尝试作为文件夹打开
            if path and os.path.exists(path):
                self._open_in_explorer(path, select_file=False)

    def _open_in_explorer(self, path: str, select_file: bool = False):
        """
        在 Windows 资源管理器中打开路径

        Args:
            path: 文件或文件夹路径
            select_file: 是否选中文件（仅当 path 是文件时有效）
        """
        try:
            # 规范化路径（将 / 转换为 \）
            path = os.path.normpath(path)

            if select_file and os.path.isfile(path):
                # 选中文件：使用 /select 参数（需要合并为一个参数）
                subprocess.Popen(['explorer', f'/select,{path}'])
            else:
                # 打开文件夹
                if os.path.isfile(path):
                    # 如果是文件但不选中，打开父文件夹
                    path = os.path.dirname(path)
                subprocess.Popen(['explorer', path])
        except Exception as e:
            print(f"打开资源管理器失败: {e}")

    def _open_file(self, path: str):
        """
        用默认程序打开文件

        Args:
            path: 文件路径
        """
        try:
            # 规范化路径
            path = os.path.normpath(path)
            # Windows 上使用 os.startfile 打开文件
            os.startfile(path)
        except Exception as e:
            print(f"打开文件失败: {e}")

