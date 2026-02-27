# PowerShell 脚本 - 创建绿色版 ZIP 压缩包

Write-Host "========================================"
Write-Host "YOLO 数据集预处理工具 - 创建绿色版"
Write-Host "========================================"
Write-Host ""

# 检查是否已打包
if (-not (Test-Path "dist\YOLO数据集预处理工具\YOLO数据集预处理工具.exe")) {
    Write-Host "[错误] 未找到打包文件！" -ForegroundColor Red
    Write-Host "请先运行: pyinstaller release.spec"
    Read-Host "按任意键退出"
    exit 1
}

# 创建 release 输出目录
if (-not (Test-Path "release")) {
    New-Item -ItemType Directory -Path "release" | Out-Null
}

# 压缩文件
$source = "dist\YOLO数据集预处理工具"
$destination = "release\YOLO数据集预处理工具_v1.0.0_绿色版.zip"

Write-Host "[1/2] 正在压缩文件..." -ForegroundColor Cyan
Write-Host "源目录: $source"
Write-Host "目标文件: $destination"
Write-Host ""

# 删除旧的压缩包
if (Test-Path $destination) {
    Remove-Item $destination -Force
}

# 压缩
try {
    Compress-Archive -Path $source -DestinationPath $destination -CompressionLevel Optimal
    Write-Host "[2/2] 压缩完成！" -ForegroundColor Green
}
catch {
    Write-Host "[错误] 压缩失败: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

# 显示结果
Write-Host ""
Write-Host "========================================"
Write-Host "绿色版已创建！"
Write-Host "========================================"
Write-Host ""
Write-Host "文件位置: $destination"

$zipFile = Get-Item $destination
Write-Host "文件大小: $([math]::Round($zipFile.Length / 1MB, 2)) MB"
Write-Host ""
Write-Host "使用说明:"
Write-Host "1. 将 ZIP 文件发送给用户"
Write-Host "2. 用户解压到任意位置"
Write-Host "3. 直接运行 YOLO数据集预处理工具.exe"
Write-Host ""
Write-Host "特点:"
Write-Host "- 无需安装"
Write-Host "- 绿色便携"
Write-Host "- 删除即卸载"
Write-Host ""

Read-Host "按任意键退出"
