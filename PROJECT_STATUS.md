# Project Status

**Last Updated**: 2026-03-01
**Current Version**: 1.2.1 (Code Complete, Verified)
**Previous Stable Version**: 1.1.0 (Released 2026-02-28)
**Status**: ✅ Code Complete | ✅ Functionally Verified

---

## Current State (v1.2.1)

### Completed Features

#### Core Workflow (Step 1-6)
- ✅ **Step 1**: Raw image import and scanning (jpg, jpeg, png, bmp, tiff)
- ✅ **Step 2**: Dataset directory structure creation with **dual modes**
  - **Create New Dataset**: Build from scratch, images numbered from 0001
  - **Extend Existing Dataset**: Add new images to existing dataset, auto-detect max index and continue numbering
- ✅ **Step 3**: Train/Val/Test split with configurable ratios (default: 70/20/10)
  - **Tree Update**: Both create and extend modes update preview tree after split
- ✅ **Step 4**: Class management with auto-loading of existing classes.txt (for extend mode)
- ✅ **Step 5**: YAML file generation with **smart replacement** (deletes old YAML files, generates new one)
- ✅ **Step 6**: LabelImg command generation (with clipboard copy support)

#### Preview Tree (v1.2.0-1.2.1)
- ✅ **Initial Blank State**: Preview tree is empty on application startup
- ✅ **Progressive Build (Create Mode)**: Tree nodes added step-by-step
  - Step 2: Shows root node + empty folder structure
  - Step 3: Scans real folders, displays image count + first 5 examples per subset
  - Step 4: Adds classes.txt node in labels/
  - Step 5: Adds/updates YAML file node in root
- ✅ **Dynamic Update (Extend Mode)**: Tree updates reflect real file system
  - Step 2: Scans and displays complete file system structure
  - Step 3: Re-scans train/val/test folders, updates image information **[NEW v1.2.1]**
  - Step 4-5: Updates YAML node only
- ✅ **Image Display Strategy**: **[OPTIMIZED v1.2.1]**
  - Shows `<共 N 张图片>` count hint for each subset
  - Displays first 5 image filenames as examples
  - Shows `... (还有 X 张)` ellipsis for large datasets
  - Supports empty folders with `<暂无图片>` hint
- ✅ **Interactive Features**:
  - Double-click file → Opens with default program (e.g., .jpg in image viewer, .txt in Notepad)
  - Double-click folder → Opens in Windows Explorer
  - Single-click arrow → Expand/collapse node
  - Increased indentation (30px) for easier arrow clicking
- ✅ **Mode Indicator**: Label changes from "Preview Mode" (gray) to "Real Mode" (green)
- ✅ **YAML Management**: Step 5 deletes all old YAML files before generating new one, updates tree accordingly

#### Established in v1.1.0
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
- **File Operations**: os.startfile() for opening files, subprocess.Popen() for Explorer
- **Tree Widget**: QTreeWidget with custom indentation (30px) and disabled double-click expansion
- **File Scanning**: os.listdir() + filter for image extensions, sorted for consistency

---

## Verification Status

### v1.2.1 - Code Complete, Functionally Verified ✅ (2026-03-01)

#### Code Implementation Status
- [x] UI layer: `tree_view_panel.py` - Replaced build_tree_create_step3() with universal update_images_in_tree() (~50 lines modified)
- [x] UI layer: `main_window.py` - Removed mode condition in Step 3, always update tree (~5 lines modified)
- [x] Python syntax validation: All modified files compile without errors
- [x] Runtime testing: Application runs without crashes

#### Functional Tests
- [x] Create mode Step 3: Tree updates with real scanned image info (count + examples)
- [x] Extend mode Step 3: Tree re-scans and updates train/val/test folders
- [x] Image count accuracy: Verified count matches actual files in folder
- [x] Example display: Shows first 5 images correctly
- [x] Ellipsis display: Shows "... (还有 X 张)" for folders with >5 images
- [x] Empty folder handling: Shows "<暂无图片>" for empty subsets
- [x] Double-click on example images: Opens with default program
- [x] Double-click on count hint: Opens folder in Explorer
- [x] Tree consistency: Verified tree matches file system after Step 3

#### Packaging Status (Not Yet Performed)
- [ ] PyInstaller build with v1.2.1 code
- [ ] Runtime testing of packaged executable
- [ ] Installer generation for v1.2.1

### v1.2.0 - Fully Verified ✅ (2026-03-01)

#### Functional Tests
- [x] Preview tree blank on startup
- [x] Create mode: Progressive tree building (Step 2 → Step 5)
- [x] Extend mode: Real file system scanning at Step 2
- [x] Double-click file opens with default program
- [x] Double-click folder opens in Windows Explorer
- [x] Arrow expansion/collapse works independently of double-click
- [x] YAML file replacement: Deletes old, generates new, updates tree
- [x] Mode indicator updates from "Preview Mode" to "Real Mode"

### v1.1.0 - Fully Verified ✅ (2026-02-28)

#### Functional Tests
- [x] Mode selection dialog works correctly
- [x] Create new dataset workflow (Step 1-6)
- [x] Extend existing dataset workflow (Step 1-6)
- [x] Index detection across all subsets (train/val/test)
- [x] Classes.txt preloading in extend mode
- [x] Collision-free image numbering

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

---

## Known Limitations

### Functional Constraints
- **Dataset Format**: YOLO format only (not compatible with COCO, Pascal VOC, etc.)
- **Image Indexing**: Maximum 9999 images per dataset (4-digit numbering)
- **Extend Mode Safety**: Only adds new images; does NOT modify/delete existing images
- **Split Behavior**: Step 3 splits ONLY new images in temp/, existing images unchanged
- **Preview Tree Performance**: Large datasets (10000+ files) may take 2-3 seconds to scan
- **Example Limit**: Only shows first 5 images per subset to avoid tree clutter **[v1.2.1]**

### Technical Constraints
- **Platform**: Windows-only packaging (PyInstaller + Inno Setup)
- **File Opening**: Uses Windows-specific APIs (os.startfile, explorer.exe)
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

### 5. Tree Node Path Storage (`ui/tree_view_panel.py`)
- Paths stored in `QTreeWidgetItem.setData(0, Qt.UserRole, path)`
- Used by double-click handler to open correct files/folders
- DO NOT store paths as plain text in node labels

### 6. YAML File Management (Step 5)
- Always deletes ALL .yaml/.yml files before generating new one
- Prevents accumulation of old configuration files
- Updates preview tree in both create and extend modes

### 7. Image Folder Scanning (Step 3) **[v1.2.1]**
- Always re-scans train/val/test folders to get accurate counts
- Filters files by image extension (.jpg, .jpeg, .png, .bmp, .tiff, .tif)
- Sorts filenames for consistent display order
- DO NOT rely on passed parameters, always scan real folders

### 8. Workflow Constraints
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

### Packaging Commands (For v1.2.1 Release)
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
Before packaging v1.2.1, update:
- [ ] Version string in `installer_setup.iss` (line 4: `#define MyAppVersion "1.2.1"`)
- [ ] Output filename in `installer_setup.iss` (line 11)
- [ ] ZIP filename in `create_portable.ps1`
- [ ] Version history in this file (PROJECT_STATUS.md)

---

## Version History

### v1.2.1 (2026-03-01) - Preview Tree Step 3 Optimization
**Improvements**:
- Step 3 tree update now applies to BOTH create and extend modes
- Scans real folders to get accurate image counts (not relying on parameters)
- Displays image information: count hint + first 5 examples + ellipsis
- Handles empty folders gracefully with `<暂无图片>` hint
- Ensures tree consistency with actual file system after data split

**Modified Files**:
- `ui/tree_view_panel.py` (~50 lines modified, replaced build_tree_create_step3 with update_images_in_tree)
- `ui/main_window.py` (~5 lines modified, removed mode condition)

**Status**: Code complete, functionally verified, packaging pending

### v1.2.0 (2026-03-01) - Preview Tree Dynamic Build
**New Features**:
- Preview tree progressive building (create mode: Step 2 → Step 5)
- Preview tree real file system scanning (extend mode: Step 2)
- Double-click to open files/folders in Explorer
- Increased arrow click area (indentation: 30px)
- YAML file smart replacement (deletes old, generates new)
- Mode indicator (Preview Mode → Real Mode)

**Modified Files**:
- `ui/tree_view_panel.py` (+~280 lines, complete rewrite)
- `ui/main_window.py` (+~30 lines, tree update integration)

**Status**: Code complete, functionally verified, packaging pending

### v1.1.0 (2026-02-28) - Extend Existing Dataset
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

**Status**: Code complete, functionally verified

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
3. **Tree Interaction Testing**: Test double-click on files/folders, expansion/collapse
4. **Tree Consistency Testing**: Verify tree matches file system after Step 3 **[v1.2.1]**
5. **Packaging Testing**: Build with PyInstaller, test on clean Windows
6. **Regression Testing**: Verify original "create new" mode still works

---

## Optional Features (Not Implemented)

The following features were considered but **NOT implemented**:
- Draft save/load functionality (infrastructure exists in `utils/draft_manager.py`, not integrated)
- Right-click context menu on tree nodes (e.g., "Refresh", "Open in VS Code")
- Progress bar for large image folder processing
- Custom labelimg installation path configuration
- Batch processing for multiple datasets
- Async image processing for >1000 images
- Unit tests for core/ modules
- Internationalization (i18n) support
- Tree node icons (folder icon, file type icons)
- Search/filter functionality in preview tree
- Showing ALL images in tree (limited to 5 examples for performance)
- Real-time tree refresh during file operations

These are recorded for reference only, not as roadmap commitments.
