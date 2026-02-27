@echo off
REM 构建 Inno Setup 安装包脚本

echo ========================================
echo YOLO 数据集预处理工具 - 构建安装包
echo ========================================
echo.

REM 检查是否已打包
if not exist "dist\YOLO数据集预处理工具\YOLO数据集预处理工具.exe" (
    echo [错误] 未找到打包文件！
    echo 请先运行 build_release.bat 进行打包
    pause
    exit /b 1
)

REM 检查 Inno Setup 是否安装
set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %ISCC% (
    echo [错误] 未找到 Inno Setup 编译器！
    echo 请安装 Inno Setup: https://jrsoftware.org/isdl.php
    pause
    exit /b 1
)

REM 创建 installer 输出目录
if not exist installer mkdir installer

REM 编译安装包
echo [1/2] 正在编译安装包...
%ISCC% installer_setup.iss

REM 检查结果
if not exist "installer\YOLO数据集预处理工具_v1.0.0_Setup.exe" (
    echo [错误] 安装包生成失败！
    pause
    exit /b 1
)

REM 完成
echo.
echo [2/2] 安装包生成完成！
echo.
echo ========================================
echo 安装包位置: installer\YOLO数据集预处理工具_v1.0.0_Setup.exe
echo ========================================
echo.
pause
