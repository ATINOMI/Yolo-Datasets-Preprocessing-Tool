# Architecture Documentation

**Project**: YOLO Dataset Preprocessing Tool
**Last Updated**: 2026-02-27

---

## Project Structure

```
E:\yolo训练集助手\
├── main.py                          # Entry point
│
├── ui/                              # UI Layer (PySide6)
│   ├── __init__.py
│   ├── main_window.py               # Main window controller
│   ├── pipeline_panel.py            # Left: 6-step workflow panel
│   ├── tree_view_panel.py           # Right: directory tree view
│   ├── command_panel.py             # Bottom: labelimg commands
│   ├── preview_dialog.py            # Dry-run preview (Step 2)
│   ├── ratio_dialog.py              # Train/val/test ratio input
│   ├── split_preview_dialog.py      # Data split preview (Step 3)
│   └── classes_dialog.py            # Class names input (Step 4)
│
├── core/                            # Business Logic Layer
│   ├── __init__.py
│   ├── image_processor.py           # Step 1: Image scanning and renaming
│   ├── dataset_builder.py           # Step 2: Directory structure creation
│   ├── data_splitter.py             # Step 3: Train/val/test split
│   ├── yaml_generator.py            # Step 4/5: classes.txt and YAML generation
│   └── command_generator.py         # Step 6: LabelImg command generation
│
├── models/                          # Data Models
│   ├── __init__.py
│   ├── dataset_config.py            # Stores workflow state and data
│   └── step_state.py                # Step status management
│
├── utils/                           # Utility Functions
│   ├── __init__.py
│   ├── file_utils.py                # File operations (copy, create, natural sort)
│   ├── validator.py                 # Input validation (ratios, classes, filenames)
│   └── draft_manager.py             # Draft save/load (not integrated yet)
│
├── release.spec                     # PyInstaller config (onedir mode)
├── installer_setup.iss              # Inno Setup installer config
├── build_release.bat                # Build script
├── RELEASE.md                       # Release guide
└── RELEASE_SUMMARY.md               # Release summary
```

---

## Module Responsibilities

### UI Layer (`ui/`)

**Purpose**: Handle user interaction and display

**Responsibilities**:
- Render GUI components using PySide6
- Capture user input (button clicks, text input, folder selection)
- Call `core/` functions to execute business logic
- Display results and error messages to user

**Rules**:
- ✅ Can import from `core/`, `models/`, `utils/`
- ✅ Can use PySide6 widgets and dialogs
- ❌ MUST NOT contain business logic (no file operations, no data processing)
- ❌ MUST NOT directly access file system (use `core/` instead)

**Example**:
```python
# ✅ GOOD: UI calls core function
from core.image_processor import ImageProcessor

images, error = ImageProcessor.scan_images(folder_path)
if error:
    QMessageBox.warning(self, "Error", error)

# ❌ BAD: UI contains business logic
for file in os.listdir(folder_path):
    if file.endswith('.jpg'):
        # ... processing logic in UI
```

---

### Core Layer (`core/`)

**Purpose**: Implement business logic

**Responsibilities**:
- Process images (scan, rename, copy)
- Create directory structures
- Split data by ratio
- Generate configuration files
- Generate commands

**Rules**:
- ✅ Can import from `utils/`, `models/`
- ✅ Should return `(result, error_message)` tuples
- ❌ MUST NOT import from `ui/`
- ❌ MUST NOT use PySide6 widgets (no QMessageBox, QDialog, etc.)
- ❌ MUST NOT directly interact with user (return errors as strings)

**Error Handling Pattern**:
```python
# ✅ GOOD: Return error as string
def scan_images(folder_path: str) -> Tuple[List[str], str]:
    try:
        # ... logic
        return images, ""
    except Exception as e:
        return [], f"Scan failed: {str(e)}"

# ❌ BAD: Show error dialog in core
def scan_images(folder_path: str):
    try:
        # ... logic
    except Exception as e:
        QMessageBox.warning(None, "Error", str(e))  # WRONG!
```

---

### Models Layer (`models/`)

**Purpose**: Define data structures

**Responsibilities**:
- Store workflow state (`DatasetConfig`)
- Manage step status (`StepState`, `StepStatus`)
- Provide serialization methods (`to_dict()`, `from_dict()`)

**Rules**:
- ✅ Pure data classes
- ✅ Can have methods for state management
- ❌ MUST NOT import from `ui/` or `core/`
- ❌ MUST NOT contain business logic
- ❌ MUST NOT perform I/O operations

---

### Utils Layer (`utils/`)

**Purpose**: Provide reusable utility functions

**Responsibilities**:
- File operations (copy, create directories, natural sort)
- Input validation (ratios, class names, filenames)
- Draft management (serialize/deserialize)

**Rules**:
- ✅ Can import from `models/`
- ✅ Should be stateless and reusable
- ❌ MUST NOT import from `ui/` or `core/`
- ❌ MUST NOT contain workflow-specific logic

---

## Dependency Graph

```
┌─────────┐
│   UI    │ ← User interacts here
└────┬────┘
     │ imports
     ↓
┌─────────┐
│  Core   │ ← Business logic
└────┬────┘
     │ imports
     ↓
┌─────────┐     ┌─────────┐
│ Models  │     │  Utils  │ ← Data & utilities
└─────────┘     └─────────┘
```

**Rules**:
- ✅ Dependencies flow downward only
- ❌ Lower layers MUST NOT import from upper layers
- ❌ `core/` MUST NOT import from `ui/`
- ❌ `models/` and `utils/` MUST NOT import from `ui/` or `core/`

---

## Code Modification Rules

### 1. Adding New Features

**Before Adding**:
- Determine which layer the feature belongs to
- Check if existing modules can be reused
- Ensure no circular dependencies will be created

**Example**: Adding image format validation
- ✅ Add to `utils/validator.py` (utility function)
- ✅ Call from `core/image_processor.py` (business logic)
- ✅ Show error in `ui/main_window.py` (UI feedback)

### 2. Modifying UI

**Allowed**:
- Change widget layout and styling
- Add new input fields or buttons
- Modify dialog appearance

**Forbidden**:
- Adding file I/O in UI event handlers
- Implementing data processing logic in UI methods
- Storing business state in UI class attributes (use `DatasetConfig` instead)

### 3. Modifying Core Logic

**Before Changing**:
- Verify change does not break existing UI flows
- Test with real data (especially large datasets)
- Ensure error messages are user-friendly

**Critical Functions** (test thoroughly):
- `ImageProcessor.rename_and_copy()` - handles file renaming
- `DataSplitter.split_data()` - random seed must remain 42 for reproducibility
- `CommandGenerator.generate_commands()` - argument order is critical

### 4. Path Handling

**Rules**:
- ✅ Always use `os.path.join()` for path construction
- ✅ Wrap paths in double quotes when generating shell commands
- ✅ Test with paths containing spaces and Chinese characters
- ❌ Never use string concatenation for paths (`path + "/" + file`)
- ❌ Never use hardcoded path separators (`"C:\folder\file"`)

**Example**:
```python
# ✅ GOOD
images_dir = os.path.join(dataset_root, 'images', 'train')
cmd = f'labelimg "{images_dir}" "{classes_file}" "{labels_dir}"'

# ❌ BAD
images_dir = dataset_root + "/images/train"
cmd = f'labelimg {images_dir} {classes_file} {labels_dir}'  # Fails with spaces
```

---

## Testing Guidelines

### Manual Testing Checklist

**After UI Changes**:
- [ ] Run `python main.py` and verify no import errors
- [ ] Test all 6 steps sequentially
- [ ] Test with folder paths containing spaces and parentheses
- [ ] Test with Chinese folder paths

**After Core Logic Changes**:
- [ ] Test with 10 images (small dataset)
- [ ] Test with 100+ images (medium dataset)
- [ ] Test with empty folders (error handling)
- [ ] Verify generated files (classes.txt, data.yaml, commands)

**After Packaging Changes**:
- [ ] Run `pyinstaller release.spec`
- [ ] Test packaged executable from `dist/`
- [ ] Verify no missing DLLs or imports
- [ ] Test on a clean machine without Python installed

---

## Common Pitfalls

### 1. Lambda Function Parameter Binding
**Problem**: Using lambda in connect() causes parameter mismatch
```python
# ❌ WRONG
btn.clicked.connect(lambda: self.handle_click(index))

# ✅ CORRECT
from functools import partial
btn.clicked.connect(partial(self.handle_click, index))
```

### 2. Path Encoding
**Problem**: Windows paths with Chinese characters fail
```python
# ✅ Always use UTF-8
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
```

### 3. PyInstaller Packaging
**Problem**: Using onefile mode causes slow startup and antivirus issues
```python
# ✅ Use onedir mode
# In release.spec: exclude_binaries=True
```

### 4. LabelImg Command Order
**Problem**: Wrong argument order causes labelimg to fail
```python
# ❌ WRONG
cmd = f'labelimg {images_dir} {labels_dir} {classes_file}'

# ✅ CORRECT
cmd = f'labelimg "{images_dir}" "{classes_file}" "{labels_dir}"'
```

---

## Extension Points

### Safe to Extend
- Add new dialogs in `ui/` for new input types
- Add new processors in `core/` for new data operations
- Add new validators in `utils/` for new input types
- Add new fields to `DatasetConfig` for new data

### Unsafe to Modify
- Main workflow sequence (Step 1-6 order)
- PyInstaller spec file (unless necessary)
- Command generation format
- Random seed value (42) for reproducibility

---

## File Naming Conventions

- **UI files**: `<component>_<type>.py` (e.g., `ratio_dialog.py`, `pipeline_panel.py`)
- **Core files**: `<function>_<type>.py` (e.g., `image_processor.py`, `data_splitter.py`)
- **Dialog classes**: `<Name>Dialog` (e.g., `PreviewDialog`, `RatioDialog`)
- **Panel classes**: `<Name>Panel` (e.g., `PipelinePanel`, `CommandPanel`)

---

## Build and Release

### Development Build
```bash
python main.py
```

### Production Build
```bash
# 1. Package with PyInstaller
pyinstaller release.spec

# 2. Test packaged app
cd dist/YOLO数据集预处理工具
./YOLO数据集预处理工具.exe

# 3. Create portable version
powershell -Command "Compress-Archive -Path 'dist\YOLO数据集预处理工具' ..."

# 4. Create installer (requires Inno Setup)
"E:/Inno Setup 6/ISCC.exe" installer_setup.iss
```

### Build Output
- `dist/YOLO数据集预处理工具/` - Packaged application (onedir)
- `release/YOLO数据集预处理工具_v1.0.0_绿色版.zip` - Portable version
- `installer/YOLO数据集预处理工具_v1.0.0_Setup.exe` - Windows installer

---

## Emergency Fixes

### Program Won't Start After Packaging
1. Check `build/release/warn-release.txt` for critical warnings
2. Verify all imports work in `main.py`
3. Test with `console=True` in release.spec to see errors

### UI Layout Broken
1. Check for missing imports in UI files
2. Verify PySide6 version matches development environment
3. Test in Python directly before packaging

### Commands Not Working
1. Verify path quoting in `command_generator.py`
2. Test command string in actual terminal
3. Check for special characters in paths

---

## Summary

This architecture is designed for:
- **Maintainability**: Clear separation of concerns
- **Testability**: Business logic independent of UI
- **Extensibility**: Easy to add new steps or features
- **Stability**: Critical components clearly marked

**Golden Rule**: When in doubt, look at existing code patterns and follow them exactly.
