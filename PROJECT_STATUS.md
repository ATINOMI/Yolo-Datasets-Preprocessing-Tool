# Project Status

**Last Updated**: 2026-02-28
**Current Version**: 1.1.0 (Code Complete, Not Yet Packaged)
**Previous Stable Version**: 1.0.0 (Released 2026-02-27)
**Status**: ✅ Code Complete | ⏳ Packaging Pending

---

## Current State (v1.1.0)

### Completed Features

#### Core Workflow (Step 1-6)
- ✅ **Step 1**: Raw image import and scanning (jpg, jpeg, png, bmp, tiff)
- ✅ **Step 2**: Dataset directory structure creation with **dual modes**
  - **Create New Dataset**: Build from scratch, images numbered from 0001
  - **Extend Existing Dataset**: Add new images to existing dataset, auto-detect max index and continue numbering
- ✅ **Step 3**: Train/Val/Test split with configurable ratios (default: 70/20/10)
- ✅ **Step 4**: Class management with auto-loading of existing classes.txt (for extend mode)
- ✅ **Step 5**: YAML file generation (YOLO training config)
- ✅ **Step 6**: LabelImg command generation (with clipboard copy support)

#### New in v1.1.0
- ✅ **Mode Selection Dialog**: User chooses operation mode at Step 2
- ✅ **Dataset Structure Validation**: Validates existing YOLO dataset structure (images/train, images/val, images/test)
- ✅ **Smart Index Detection**: Scans all subsets (train/val/test) for maximum 4-digit image index
- ✅ **Collision-Free Numbering**: New images start from `max_index + 1`, preventing overwrite
- ✅ **Preview with Index Info**: Shows current max index and new image numbering range
- ✅ **Class Preloading**: Automatically loads existing classes.txt in extend mode
- ✅ **Backward Compatibility**: Original "create new dataset" workflow unchanged

### Technical Implementation
- **GUI Framework**: PySide6 6.6.3.1
- **Python Version**: 3.8.8+
- **Architecture**: MVC separation (ui/, core/, models/, utils/)
- **Error Handling**: All file operations wrapped with try/except
- **Path Safety**: All paths use os.path.join(), quoted in commands

---

## Verification Status

### v1.0.0 - Fully Verified ✅ (2026-02-27)

#### Functional Tests
- [x] Image scanning with 110 images
- [x] Directory structure creation in paths with spaces and parentheses
- [x] Data split (77 train / 22 val / 11 test)
- [x] Classes.txt generation with 4 classes
- [x] YAML file generation with correct format (list-based names)
- [x] LabelImg commands generation with proper argument order
- [x] Clipboard copy functionality for all 3 commands (train/val/test)

#### Packaging Tests
- [x] PyInstaller build completes without critical errors
- [x] Packaged executable runs without console window
- [x] All dependencies included in `_internal/` folder
- [x] Inno Setup installer builds successfully
- [x] Installer creates desktop shortcut and start menu entry

#### Build Artifacts (v1.0.0)
- **Green Version**: `release/YOLO数据集预处理工具_v1.0.0_绿色版.zip` (43 MB)
- **Installer**: *(Not generated in v1.0.0)*
- **Packaged App**: `dist/YOLO数据集预处理工具/` (onedir structure)

### v1.1.0 - Code Complete, Syntax Verified ✅ (2026-02-28)

#### Code Implementation Status
- [x] Core layer: `dataset_builder.py` - Added `validate_existing_structure()` and `find_max_image_index()`
- [x] UI layer: `mode_selection_dialog.py` - New mode selection dialog (85 lines)
- [x] UI layer: `main_window.py` - Refactored Step 2 into create/extend branches (~210 lines modified)
- [x] UI layer: `preview_dialog.py` - Added mode parameter and dynamic preview text (~25 lines modified)
- [x] UI layer: `classes_dialog.py` - Added existing_classes preloading (~15 lines modified)
- [x] Python syntax validation: All modified files compile without errors

#### Functional Tests (Not Yet Performed)
- [ ] Extend empty dataset (should start from 0001)
- [ ] Extend dataset with existing images (verify index continuation)
- [ ] Invalid directory selection (error handling)
- [ ] Mixed image extensions (.jpg, .png) detection
- [ ] Step 3-6 compatibility with extend mode
- [ ] Classes.txt preloading verification

#### Packaging Status (Not Yet Performed)
- [ ] PyInstaller build with new code
- [ ] Runtime testing of packaged executable
- [ ] Installer generation for v1.1.0

---

## Known Limitations

### Functional Constraints
- **Dataset Format**: YOLO format only (not compatible with COCO, Pascal VOC, etc.)
- **Image Indexing**: Maximum 9999 images per dataset (4-digit numbering)
- **Extend Mode Safety**: Only adds new images; does NOT modify/delete existing images
- **Split Behavior**: Step 3 splits ONLY new images in temp/, existing images unchanged

### Technical Constraints
- **Platform**: Windows-only packaging (PyInstaller + Inno Setup)
- **UI Language**: Chinese only (no i18n support)
- **Large Datasets**: No async processing for >1000 images (may cause UI freeze)

### Known Issues (Packaging-Related)
- ⚠️ DLL warnings during PyInstaller build (normal, does not affect functionality)
- ⚠️ Chinese language file not available in Inno Setup (using English installer UI)

---

## Critical Components (Do NOT Modify)

### 1. Command Generation Logic (`core/command_generator.py`)
- Argument order is CRITICAL: `labelimg "images_dir" "classes_file" "labels_dir"`
- Paths MUST be wrapped in double quotes for spaces/parentheses support
- DO NOT change unless labelimg itself changes its CLI interface

### 2. PyInstaller Configuration (`release.spec`)
- Using `onedir` mode (NOT onefile) for stability
- Excluding matplotlib, numpy, pandas, scipy to reduce size
- DO NOT switch to onefile mode without extensive testing

### 3. Button Click Handler (`ui/command_panel.py`)
- Using `functools.partial` to bind index parameter
- DO NOT use lambda functions (causes parameter binding issues)

### 4. File Path Handling
- All paths use `os.path.join()` for cross-platform compatibility
- All paths wrapped in quotes when generating shell commands
- DO NOT use string concatenation for paths

### 5. Workflow Constraints
- Step sequence: 1 → 2 → 3 → 4 → 5 → 6
- Each step checks prerequisites before execution
- DO NOT allow users to skip required steps

---

## Build Instructions

### Requirements
- Python 3.8+
- PySide6 (`pip install PySide6`)
- PyInstaller (`pip install pyinstaller`)
- Inno Setup 6 (for installer generation)

### Packaging Commands (For v1.1.0 Release)
```bash
# 1. Package application
pyinstaller release.spec

# 2. Test packaged executable
cd dist/YOLO数据集预处理工具/
YOLO数据集预处理工具.exe

# 3. Generate installer (requires Inno Setup)
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_setup.iss

# 4. Create portable ZIP
powershell -ExecutionPolicy Bypass -File create_portable.ps1
```

### Version Update Checklist
Before packaging v1.1.0, update:
- [ ] Version string in `installer_setup.iss` (line 4: `#define MyAppVersion "1.1.0"`)
- [ ] Output filename in `installer_setup.iss` (line 11)
- [ ] ZIP filename in `create_portable.ps1`
- [ ] Version history in this file (PROJECT_STATUS.md)

---

## Version History

### v1.1.0 (2026-02-28) - Code Complete
**New Features**:
- Dual-mode dataset creation (Create New / Extend Existing)
- Smart image index detection and continuation
- Dataset structure validation
- Classes.txt auto-loading in extend mode

**Modified Files**:
- `core/dataset_builder.py` (+108 lines)
- `ui/mode_selection_dialog.py` (NEW, 85 lines)
- `ui/main_window.py` (+210 lines, refactored Step 2)
- `ui/preview_dialog.py` (+25 lines, mode support)
- `ui/classes_dialog.py` (+15 lines, preloading)

**Status**: Code complete, syntax verified, functional testing pending

### v1.0.0 (2026-02-27) - Initial Release
- All 6 steps implemented and tested
- Packaging and installer verified
- Chinese path support confirmed
- Green version released (43 MB ZIP)

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
- Maintain backward compatibility with v1.0.0 workflows

### Testing Protocol
1. **Syntax Validation**: `python -m py_compile <file.py>`
2. **Functional Testing**: Complete Step 1-6 workflow with real images
3. **Packaging Testing**: Build with PyInstaller, test on clean Windows
4. **Regression Testing**: Verify original "create new" mode still works

---

## Optional Features (Not Implemented)

The following features were considered but **NOT implemented**:
- Draft save/load functionality (infrastructure exists in `utils/draft_manager.py`, not integrated)
- Real-time directory tree update after Step 2/3 completion
- Progress bar for large image folder processing
- Custom labelimg installation path configuration
- Batch processing for multiple datasets
- Async image processing for >1000 images
- Unit tests for core/ modules
- Internationalization (i18n) support

These are recorded for reference only, not as roadmap commitments.
