@echo off
REM YOLO Dataset Preprocessing Tool - 正式打包脚本
REM 使用 onedir 模式打包

echo ========================================
echo YOLO 数据集预处理工具 - 正式打包
echo ========================================
echo.

REM 清理旧的构建文件
echo [1/4] 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM 执行打包
echo.
echo [2/4] 开始打包（onedir 模式）...
pyinstaller release.spec

REM 检查打包结果
echo.
echo [3/4] 检查打包结果...
if not exist "dist\YOLO数据集预处理工具\YOLO数据集预处理工具.exe" (
    echo [错误] 打包失败，未找到 exe 文件！
    pause
    exit /b 1
)

REM 打包完成
echo.
echo [4/4] 打包完成！
echo.
echo ========================================
echo 打包结果位于: dist\YOLO数据集预处理工具\
echo 主程序: YOLO数据集预处理工具.exe
echo ========================================
echo.
echo 下一步: 运行 build_installer.bat 创建安装包
echo.
pause
