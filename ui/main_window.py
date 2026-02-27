"""YOLO 数据集预处理工具 - 主窗口"""

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QFileDialog, QMessageBox, QInputDialog, QDialog
)
from PySide6.QtCore import Qt

from ui.pipeline_panel import PipelinePanel
from ui.tree_view_panel import TreeViewPanel
from ui.command_panel import CommandPanel
from ui.preview_dialog import PreviewDialog
from ui.ratio_dialog import RatioDialog
from ui.split_preview_dialog import SplitPreviewDialog
from ui.classes_dialog import ClassesDialog
from core.image_processor import ImageProcessor
from core.dataset_builder import DatasetBuilder
from core.data_splitter import DataSplitter
from core.yaml_generator import YAMLGenerator
from core.command_generator import CommandGenerator


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        # Step 1 数据
        self.raw_images_folder = None  # 原始图片文件夹路径
        self.scanned_images = []  # 扫描到的图片列表
        self.image_count = 0  # 图片数量

        # Step 2 数据
        self.dataset_parent_dir = None  # 数据集父目录
        self.dataset_name = ""  # 数据集名称
        self.dataset_root = None  # 数据集根路径
        self.temp_folder = None  # 临时文件夹路径（存放重命名后的图片）

        # Step 3 数据
        self.train_ratio = 70.0
        self.val_ratio = 20.0
        self.test_ratio = 10.0
        self.train_images = []
        self.val_images = []
        self.test_images = []

        # Step 4 数据
        self.classes = []

        # Step 5 数据
        self.yaml_filename = "data.yaml"
        self.yaml_path = None

        self.init_ui()

    def init_ui(self):
        """初始化 UI"""
        self.setWindowTitle("YOLO Dataset Preprocessing Tool")
        self.setGeometry(100, 100, 1200, 800)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局（垂直）
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 上部：工作区（左右分割）
        splitter = QSplitter(Qt.Horizontal)

        # 左侧：步骤面板
        self.pipeline_panel = PipelinePanel()
        self.pipeline_panel.step_execute.connect(self.on_step_execute)

        # 右侧：目录树视图
        self.tree_view_panel = TreeViewPanel()

        splitter.addWidget(self.pipeline_panel)
        splitter.addWidget(self.tree_view_panel)

        # 设置分割比例（左：右 = 2:3）
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)

        main_layout.addWidget(splitter, stretch=7)

        # 下部：命令面板
        self.command_panel = CommandPanel()
        main_layout.addWidget(self.command_panel, stretch=3)

    def on_step_execute(self, step_number: int):
        """
        步骤执行槽函数

        Args:
            step_number: 步骤编号 (1-6)
        """
        if step_number == 1:
            self.execute_step1()
        elif step_number == 2:
            self.execute_step2()
        elif step_number == 3:
            self.execute_step3()
        elif step_number == 4:
            self.execute_step4()
        elif step_number == 5:
            self.execute_step5()
        elif step_number == 6:
            self.execute_step6()
        else:
            # 其他步骤暂时无功能
            print(f"Step {step_number} 执行按钮被点击（暂无功能）")

    def execute_step1(self):
        """执行 Step 1：选择原始图片文件夹 + 扫描图片"""
        # 打开文件夹选择对话框
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择原始图片文件夹",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )

        # 用户取消选择
        if not folder:
            return

        # 验证路径
        if not os.path.exists(folder):
            QMessageBox.warning(self, "路径无效", f"选择的路径不存在:\n{folder}")
            return

        if not os.path.isdir(folder):
            QMessageBox.warning(self, "路径无效", f"选择的路径不是文件夹:\n{folder}")
            return

        # 扫描图片
        images, error = ImageProcessor.scan_images(folder)

        if error:
            QMessageBox.warning(self, "扫描失败", error)
            return

        if not images:
            QMessageBox.warning(
                self,
                "未找到图片",
                "文件夹中没有找到图片文件\n\n支持的格式：jpg, jpeg, png, bmp, tiff, tif"
            )
            return

        # 保存数据
        self.raw_images_folder = folder
        self.scanned_images = images
        self.image_count = len(images)

        # 更新 UI
        card = self.pipeline_panel.step_cards[1]
        summary_text = f"路径: {folder}\n找到 {self.image_count} 张图片"
        card.update_summary(summary_text)
        card.update_status("#2196F3")  # 蓝色表示已配置

        print(f"Step 1: 已选择文件夹: {folder}")
        print(f"Step 1: 扫描到 {self.image_count} 张图片")

    def execute_step2(self):
        """执行 Step 2：创建数据集目录结构 + 重命名图片"""
        # 检查 Step 1 是否完成
        if not self.scanned_images:
            QMessageBox.warning(
                self,
                "前置条件未满足",
                "请先完成 Step 1（原始图片导入）"
            )
            return

        # 1. 选择数据集父目录
        parent_dir = QFileDialog.getExistingDirectory(
            self,
            "选择数据集父目录",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )

        if not parent_dir:
            return

        # 2. 输入数据集名称
        dataset_name, ok = QInputDialog.getText(
            self,
            "输入数据集名称",
            "数据集名称:",
            text="my_dataset"
        )

        if not ok or not dataset_name.strip():
            return

        dataset_name = dataset_name.strip()

        # 3. 计算数据集根路径
        dataset_root = os.path.join(parent_dir, dataset_name)

        # 检查是否已存在
        if os.path.exists(dataset_root):
            QMessageBox.warning(
                self,
                "路径已存在",
                f"路径已存在，请选择其他位置或名称:\n{dataset_root}"
            )
            return

        # 4. 准备 dry-run 预览数据
        preview_images = []
        for i, img_path in enumerate(self.scanned_images, 1):
            old_name = os.path.basename(img_path)
            _, ext = os.path.splitext(img_path)
            new_name = f"{i:04d}{ext.lower()}"
            preview_images.append((old_name, new_name))

        # 5. 显示 dry-run 预览对话框
        dialog = PreviewDialog(dataset_root, self.image_count, preview_images, self)
        if dialog.exec() != QDialog.Accepted:
            print("用户取消了操作")
            return

        # 6. 执行创建
        try:
            # 创建目录结构
            _, error = DatasetBuilder.create_structure(parent_dir, dataset_name)
            if error:
                QMessageBox.critical(self, "创建失败", error)
                return

            # 创建 temp 文件夹
            temp_folder = os.path.join(dataset_root, "temp")
            os.makedirs(temp_folder, exist_ok=True)

            # 重命名并复制图片
            _, error = ImageProcessor.rename_and_copy(
                self.scanned_images,
                temp_folder,
                start_index=1
            )

            if error:
                QMessageBox.critical(self, "复制失败", error)
                return

            # 保存数据
            self.dataset_parent_dir = parent_dir
            self.dataset_name = dataset_name
            self.dataset_root = dataset_root
            self.temp_folder = temp_folder

            # 更新 UI
            card = self.pipeline_panel.step_cards[2]
            summary_text = f"数据集: {dataset_root}\n已复制 {self.image_count} 张图片到 temp/"
            card.update_summary(summary_text)
            card.update_status("#4CAF50")  # 绿色表示已完成

            QMessageBox.information(
                self,
                "创建成功",
                f"数据集目录结构已创建:\n{dataset_root}\n\n"
                f"已将 {self.image_count} 张图片重命名并复制到 temp/ 文件夹"
            )

            print(f"Step 2: 数据集已创建: {dataset_root}")
            print(f"Step 2: 图片已复制到: {temp_folder}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建过程中出现错误:\n{str(e)}")

    def execute_step3(self):
        """执行 Step 3：train / val / test 数据拆分"""
        # 检查 Step 2 是否完成
        if not self.dataset_root or not self.temp_folder:
            QMessageBox.warning(
                self,
                "前置条件未满足",
                "请先完成 Step 2（数据集目录结构创建）"
            )
            return

        # 1. 弹出比例输入对话框
        ratio_dialog = RatioDialog(self)
        if ratio_dialog.exec() != QDialog.Accepted:
            print("用户取消了比例配置")
            return

        # 获取比例
        train_ratio = ratio_dialog.train_ratio
        val_ratio = ratio_dialog.val_ratio
        test_ratio = ratio_dialog.test_ratio

        # 2. 获取 temp/ 文件夹中的图片
        temp_images = []
        for filename in os.listdir(self.temp_folder):
            filepath = os.path.join(self.temp_folder, filename)
            if os.path.isfile(filepath):
                temp_images.append(filepath)

        if not temp_images:
            QMessageBox.warning(self, "错误", "temp/ 文件夹中没有图片")
            return

        # 3. 划分数据
        train_list, val_list, test_list, error = DataSplitter.split_data(
            temp_images,
            train_ratio,
            val_ratio,
            test_ratio,
            seed=42
        )

        if error:
            QMessageBox.critical(self, "拆分失败", error)
            return

        # 4. 显示 dry-run 预览
        preview_dialog = SplitPreviewDialog(
            len(train_list),
            len(val_list),
            len(test_list),
            self
        )
        if preview_dialog.exec() != QDialog.Accepted:
            print("用户取消了拆分")
            return

        # 5. 执行复制
        try:
            # 复制到 train
            train_dir = DatasetBuilder.get_images_path(self.dataset_root, 'train')
            _, error = DataSplitter.copy_images_to_subset(train_list, train_dir)
            if error:
                raise Exception(f"复制到 train 失败: {error}")

            # 复制到 val
            val_dir = DatasetBuilder.get_images_path(self.dataset_root, 'val')
            _, error = DataSplitter.copy_images_to_subset(val_list, val_dir)
            if error:
                raise Exception(f"复制到 val 失败: {error}")

            # 复制到 test
            test_dir = DatasetBuilder.get_images_path(self.dataset_root, 'test')
            _, error = DataSplitter.copy_images_to_subset(test_list, test_dir)
            if error:
                raise Exception(f"复制到 test 失败: {error}")

            # 保存数据
            self.train_ratio = train_ratio
            self.val_ratio = val_ratio
            self.test_ratio = test_ratio
            self.train_images = train_list
            self.val_images = val_list
            self.test_images = test_list

            # 更新 UI
            card = self.pipeline_panel.step_cards[3]
            summary_text = (
                f"比例: {train_ratio:.0f}% / {val_ratio:.0f}% / {test_ratio:.0f}%\n"
                f"Train: {len(train_list)} 张 | Val: {len(val_list)} 张 | Test: {len(test_list)} 张"
            )
            card.update_summary(summary_text)
            card.update_status("#4CAF50")  # 绿色表示已完成

            QMessageBox.information(
                self,
                "拆分成功",
                f"数据已成功拆分:\n\n"
                f"Train: {len(train_list)} 张图片\n"
                f"Val: {len(val_list)} 张图片\n"
                f"Test: {len(test_list)} 张图片"
            )

            print(f"Step 3: 数据拆分完成")
            print(f"  Train: {len(train_list)} 张")
            print(f"  Val: {len(val_list)} 张")
            print(f"  Test: {len(test_list)} 张")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"拆分过程中出现错误:\n{str(e)}")

    def execute_step4(self):
        """执行 Step 4：类别管理（生成 classes.txt）"""
        # 检查 Step 3 是否完成
        if not self.train_images:
            QMessageBox.warning(
                self,
                "前置条件未满足",
                "请先完成 Step 3（数据划分）"
            )
            return

        # 1. 弹出类别输入对话框
        dialog = ClassesDialog(self)
        if dialog.exec() != QDialog.Accepted:
            print("用户取消了类别输入")
            return

        # 获取类别列表
        classes = dialog.classes

        # 2. 写入 classes.txt
        try:
            classes_file = DatasetBuilder.get_classes_file_path(self.dataset_root)
            success, error = YAMLGenerator.write_classes_file(classes_file, classes)

            if not success:
                QMessageBox.critical(self, "保存失败", error)
                return

            # 保存数据
            self.classes = classes

            # 更新 UI
            card = self.pipeline_panel.step_cards[4]
            preview_classes = ", ".join(classes[:3])
            if len(classes) > 3:
                preview_classes += f", ... ({len(classes) - 3} 个更多)"
            summary_text = f"{len(classes)} 个类别: {preview_classes}"
            card.update_summary(summary_text)
            card.update_status("#4CAF50")  # 绿色表示已完成

            QMessageBox.information(
                self,
                "类别保存成功",
                f"已保存 {len(classes)} 个类别到:\n{classes_file}"
            )

            print(f"Step 4: 类别已保存: {classes}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存类别时出现错误:\n{str(e)}")

    def execute_step5(self):
        """执行 Step 5：生成 YAML 文件"""
        # 检查 Step 4 是否完成
        if not self.classes:
            QMessageBox.warning(
                self,
                "前置条件未满足",
                "请先完成 Step 4（类别管理）"
            )
            return

        # 1. 输入 YAML 文件名
        filename, ok = QInputDialog.getText(
            self,
            "输入 YAML 文件名",
            "YAML 文件名:",
            text="data.yaml"
        )

        if not ok or not filename.strip():
            return

        filename = filename.strip()

        # 校验文件名
        if not (filename.lower().endswith('.yaml') or filename.lower().endswith('.yml')):
            QMessageBox.warning(
                self,
                "文件名无效",
                "YAML 文件名必须以 .yaml 或 .yml 结尾"
            )
            return

        # 2. 生成 YAML 文件
        try:
            yaml_path, error = YAMLGenerator.generate_yaml(
                self.dataset_root,
                self.classes,
                filename
            )

            if error:
                QMessageBox.critical(self, "生成失败", error)
                return

            # 保存数据
            self.yaml_filename = filename
            self.yaml_path = yaml_path

            # 更新 UI
            card = self.pipeline_panel.step_cards[5]
            summary_text = f"YAML 文件: {yaml_path}"
            card.update_summary(summary_text)
            card.update_status("#4CAF50")  # 绿色表示已完成

            QMessageBox.information(
                self,
                "YAML 文件生成成功",
                f"YAML 文件已生成:\n{yaml_path}"
            )

            print(f"Step 5: YAML 文件已生成: {yaml_path}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成 YAML 文件时出现错误:\n{str(e)}")

    def execute_step6(self):
        """执行 Step 6：生成 LabelImg 命令"""
        # 检查 Step 5 是否完成
        if not self.yaml_path:
            QMessageBox.warning(
                self,
                "前置条件未满足",
                "请先完成 Step 5（YAML 文件生成）"
            )
            return

        try:
            # 生成命令
            classes_file = DatasetBuilder.get_classes_file_path(self.dataset_root)
            commands, error = CommandGenerator.generate_commands(
                self.dataset_root,
                classes_file
            )

            if error:
                QMessageBox.critical(self, "生成失败", error)
                return

            # 显示命令到命令面板
            self.command_panel.set_commands(commands)

            # 更新 UI
            card = self.pipeline_panel.step_cards[6]
            summary_text = "命令已生成"
            card.update_summary(summary_text)
            card.update_status("#4CAF50")  # 绿色表示已完成

            QMessageBox.information(
                self,
                "命令生成成功",
                "LabelImg 命令已生成并显示在底部命令面板\n\n"
                "点击\"复制\"按钮可复制命令到剪贴板"
            )

            print(f"Step 6: LabelImg 命令已生成")
            for i, cmd in enumerate(commands):
                print(f"  {['Train', 'Val', 'Test'][i]}: {cmd}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成命令时出现错误:\n{str(e)}")




