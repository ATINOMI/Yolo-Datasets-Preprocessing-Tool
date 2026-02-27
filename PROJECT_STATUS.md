# Project Status

**Last Updated**: 2026-02-27
**Version**: 1.0.0
**Status**: ✅ Production Ready

---

## Current State

### Completed Features
- ✅ **Step 1**: Raw image import and scanning (jpg, jpeg, png, bmp, tiff)
- ✅ **Step 2**: YOLO directory structure creation + image renaming (0001.jpg, 0002.jpg...)
- ✅ **Step 3**: Train/Val/Test split with configurable ratios (default: 70/20/10)
- ✅ **Step 4**: Class management (generates `labels/classes.txt`)
- ✅ **Step 5**: YAML file generation (YOLO training config)
- ✅ **Step 6**: LabelImg command generation (with clipboard copy support)

### Technical Implementation
- **GUI Framework**: PySide6 6.6.3.1
- **Python Version**: 3.8.8
- **Packaging**: PyInstaller 6.19.0 (onedir mode, NOT onefile)
- **Installer**: Inno Setup 6.7.1

### Build Artifacts
- **Green Version**: `release/YOLO数据集预处理工具_v1.0.0_绿色版.zip` (43 MB)
- **Installer**: `installer/YOLO数据集预处理工具_v1.0.0_Setup.exe` (30 MB)
- **Packaged App**: `dist/YOLO数据集预处理工具/` (onedir structure)

---

## Last Verified (2026-02-27)

### Functional Tests ✅
- [x] Image scanning with 110 images
- [x] Directory structure creation in paths with spaces and parentheses
- [x] Data split (77 train / 22 val / 11 test)
- [x] Classes.txt generation with 4 classes
- [x] YAML file generation with correct format (list-based names)
- [x] LabelImg commands generation with proper argument order
- [x] Clipboard copy functionality for all 3 commands (train/val/test)

### Packaging Tests ✅
- [x] PyInstaller build completes without critical errors
- [x] Packaged executable runs without console window
- [x] All dependencies included in `_internal/` folder
- [x] Inno Setup installer builds successfully
- [x] Installer creates desktop shortcut and start menu entry

### Known Issues
- ⚠️ DLL warnings during packaging (normal, does not affect functionality)
- ⚠️ Chinese language file not available in Inno Setup (using English only)

---

## Next Planned Changes

### Potential Features (Not Implemented Yet)
- [ ] Draft save/load functionality (utils/draft_manager.py exists but not integrated)
- [ ] Real-time directory tree update after Step 2/3 completion
- [ ] Progress bar for large image folder processing
- [ ] Custom labelimg installation path configuration
- [ ] Batch processing for multiple datasets

### Refactoring Considerations
- [ ] Consider async image processing for >1000 images
- [ ] Add unit tests for core/ modules
- [ ] Internationalization (i18n) support

---

## Do NOT Change

### Critical Components (Stable and Working)
1. **Command Generation Logic** (`core/command_generator.py`)
   - Argument order is CRITICAL: `labelimg "images_dir" "classes_file" "labels_dir"`
   - Paths MUST be wrapped in double quotes for spaces/parentheses support
   - DO NOT change unless labelimg itself changes its CLI interface

2. **PyInstaller Configuration** (`release.spec`)
   - Using `onedir` mode (NOT onefile) for stability
   - Excluding matplotlib, numpy, pandas, scipy to reduce size
   - DO NOT switch to onefile mode without extensive testing

3. **Button Click Handler** (`ui/command_panel.py`)
   - Using `functools.partial` to bind index parameter
   - DO NOT use lambda functions (causes parameter binding issues)

4. **File Paths**
   - All paths use `os.path.join()` for cross-platform compatibility
   - All paths wrapped in quotes when generating shell commands
   - DO NOT use string concatenation for paths

5. **Data Flow**
   - Main workflow: Step 1 → Step 2 → Step 3 → Step 4 → Step 5 → Step 6
   - Each step checks prerequisites before execution
   - DO NOT allow users to skip required steps

---

## Development Environment

### Required Tools
- Python 3.8+
- PySide6 (`pip install PySide6`)
- PyInstaller (`pip install pyinstaller`)
- Inno Setup 6 (for installer generation)

### Build Commands
```bash
# Package application
pyinstaller release.spec

# Generate installer (requires Inno Setup)
"E:/Inno Setup 6/ISCC.exe" installer_setup.iss

# Create portable ZIP
powershell -Command "Compress-Archive -Path 'dist\YOLO数据集预处理工具' -DestinationPath 'release\YOLO数据集预处理工具_v1.0.0_绿色版.zip' -Force"
```

---

## Contact / Handover Notes

### For Future Maintainers
- This project uses **staged development approach** (阶段开发)
- Each feature was implemented and verified independently
- UI and core logic are strictly separated
- All file operations use try/except with user-friendly error messages

### Code Modification Rules
- Read `ARCHITECTURE.md` before making ANY changes
- Test packaging after every UI change
- Verify labelimg command format after modifying command_generator.py
- Always use dry-run preview dialogs for destructive operations

---

## Version History

### v1.0.0 (2026-02-27)
- Initial release
- All 6 steps implemented and tested
- Packaging and installer verified
- Chinese path support confirmed
