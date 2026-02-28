# Architecture Documentation

**Project**: YOLO Dataset Preprocessing Tool
**Last Updated**: 2026-02-28
**Current Version**: 1.1.0

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
│   ├── mode_selection_dialog.py     # Step 2: Create/Extend mode selection (NEW in v1.1.0)
│   ├── preview_dialog.py            # Dry-run preview (Step 2, supports both modes)
│   ├── ratio_dialog.py              # Train/val/test ratio input
│   ├── split_preview_dialog.py      # Data split preview (Step 3)
│   └── classes_dialog.py            # Class names input (Step 4, supports preloading)
│
├── core/                            # Business Logic Layer
│   ├── __init__.py
│   ├── image_processor.py           # Step 1: Image scanning and renaming
│   ├── dataset_builder.py           # Step 2: Directory creation, validation, index detection
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
│   └── draft_manager.py             # Draft save/load (infrastructure exists, not integrated)
│
├── release.spec                     # PyInstaller config (onedir mode)
├── installer_setup.iss              # Inno Setup installer config
├── build_release.bat                # Build script
├── RELEASE.md                       # Release guide
└── PROJECT_STATUS.md                # Current project status (v1.1.0)
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

**Files Overview**:
- `main_window.py`: Main controller, manages workflow state, coordinates Step 1-6 execution
- `mode_selection_dialog.py`: Step 2 mode selection (Create New / Extend Existing) **[NEW in v1.1.0]**
- `preview_dialog.py`: Shows directory structure and image renaming preview (supports both create and extend modes)
- `classes_dialog.py`: Class names input with preloading support for extend mode **[UPDATED in v1.1.0]**
- `ratio_dialog.py`: Train/val/test ratio input
- `split_preview_dialog.py`: Data split preview
- `command_panel.py`: Displays and copies LabelImg commands
- `pipeline_panel.py`: Left sidebar with 6-step workflow cards
- `tree_view_panel.py`: Right sidebar with directory tree view (placeholder)

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
- Create and validate directory structures
- Detect existing dataset index ranges
- Split data by ratio
- Generate configuration files
- Generate commands

**Rules**:
- ✅ Can import from `utils/`, `models/`
- ✅ Should return `(result, error_message)` tuples
- ❌ MUST NOT import from `ui/`
- ❌ MUST NOT use PySide6 widgets (no QMessageBox, QDialog, etc.)
- ❌ MUST NOT directly interact with user (return errors as strings)

**Files Overview**:
- `image_processor.py`: Scans images, renames to 4-digit format (0001.jpg, 0002.jpg...), supports custom start_index
- `dataset_builder.py`: **[UPDATED in v1.1.0]**
  - Creates YOLO directory structure (images/, labels/, train/val/test)
  - Validates existing dataset structure (`validate_existing_structure()`)
  - Finds maximum image index in existing datasets (`find_max_image_index()`)
  - Provides path helper methods (get_images_path, get_labels_path, get_classes_file_path)
- `data_splitter.py`: Splits images by ratio, copies to train/val/test directories
- `yaml_generator.py`: Generates classes.txt and data.yaml files
- `command_generator.py`: Generates LabelImg commands with proper argument order and quoting

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

**Files Overview**:
- `dataset_config.py`: Stores entire workflow state (image paths, dataset paths, ratios, classes, etc.)
- `step_state.py`: Manages individual step status (pending, in_progress, completed, need_regenerate)

**Note**: Currently, `main_window.py` directly stores state as instance variables instead of using `DatasetConfig`. The `DatasetConfig` class exists for potential draft save/load functionality (not yet integrated).

---

### Utils Layer (`utils/`)

**Purpose**: Provide reusable utility functions

**Responsibilities**:
- File operations (copy, create directories, natural sort)
- Input validation (ratios, class names, filenames)
- Draft management (serialize/deserialize, not integrated)

**Rules**:
- ✅ Can import from `models/`
- ✅ Should be stateless and reusable
- ❌ MUST NOT import from `ui/` or `core/`
- ❌ MUST NOT contain workflow-specific logic

**Files Overview**:
- `file_utils.py`: safe_create_directory(), safe_copy_file(), natural_sort(), is_image_file()
- `validator.py`: Validates ratios, class names, filenames
- `draft_manager.py`: Draft save/load infrastructure (exists but not integrated into main workflow)

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

## Workflow and Data Flow

### Main Workflow (6 Steps)

```
Step 1: Import Raw Images
  ↓ (scanned_images, image_count)
Step 2: Create/Extend Dataset
  ↓ (dataset_root, temp_folder)
Step 3: Split Data
  ↓ (train_images, val_images, test_images)
Step 4: Manage Classes
  ↓ (classes list)
Step 5: Generate YAML
  ↓ (yaml_path)
Step 6: Generate Commands
  ↓ (labelimg_commands)
```

### Step 2: Dual-Mode Architecture (NEW in v1.1.0)

**Mode Selection Flow**:
```
User clicks "Step 2"
  ↓
ModeSelectionDialog shows
  ↓
User selects mode
  ├─ "Create New Dataset"
  │    ↓
  │  execute_step2_create_new()
  │    ├─ Select parent directory
  │    ├─ Input dataset name
  │    ├─ Validate path not exists
  │    ├─ Preview structure
  │    ├─ Create directories (DatasetBuilder.create_structure)
  │    ├─ Copy images with start_index=1
  │    └─ Save dataset_root, temp_folder
  │
  └─ "Extend Existing Dataset"
       ↓
     execute_step2_extend_existing()
       ├─ Select existing dataset directory
       ├─ Validate structure (DatasetBuilder.validate_existing_structure)
       ├─ Find max index (DatasetBuilder.find_max_image_index)
       ├─ Preview with index info
       ├─ Ensure temp/ exists
       ├─ Copy images with start_index=max_index+1
       └─ Save dataset_root, temp_folder
```

**Key Architectural Decisions**:
1. **Branching at UI Layer**: `main_window.py` contains two separate methods (`_execute_step2_create_new()` and `_execute_step2_extend_existing()`)
2. **Code Isolation**: Original "create new" logic completely unchanged, new "extend" logic in separate method
3. **Core Reuse**: Both modes use `ImageProcessor.rename_and_copy()` with different `start_index` values
4. **Validation in Core**: Structure validation and index detection in `core/dataset_builder.py`, not UI
5. **Backward Compatibility**: Step 3-6 work identically for both modes (operate on `temp/` folder)

### Step 3-6 Compatibility

Both "create new" and "extend existing" modes converge after Step 2:
- **Step 3**: Reads from `temp/`, splits to train/val/test (only new images, existing images untouched)
- **Step 4**: Reads existing classes.txt if present, allows user to modify
- **Step 5**: Generates data.yaml using current dataset_root
- **Step 6**: Generates LabelImg commands using current dataset_root

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
- Storing business state in UI class attributes (use `DatasetConfig` instead, though currently state is in main_window.py)

### 3. Modifying Core Logic

**Before Changing**:
- Verify change does not break existing UI flows
- Test with real data (especially large datasets)
- Ensure error messages are user-friendly

**Critical Functions** (test thoroughly):
- `ImageProcessor.rename_and_copy()` - handles file renaming, `start_index` parameter is critical for extend mode
- `DatasetBuilder.find_max_image_index()` - regex pattern must match 4-digit numbering **[NEW in v1.1.0]**
- `DatasetBuilder.validate_existing_structure()` - must check all required directories **[NEW in v1.1.0]**
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
- [ ] Test all 6 steps sequentially (create new mode)
- [ ] Test all 6 steps sequentially (extend existing mode) **[NEW in v1.1.0]**
- [ ] Test with folder paths containing spaces and parentheses
- [ ] Test with Chinese folder paths

**After Core Logic Changes**:
- [ ] Test with 10 images (small dataset)
- [ ] Test with 100+ images (medium dataset)
- [ ] Test with empty folders (error handling)
- [ ] Test extend mode with existing dataset (verify index continuation) **[NEW in v1.1.0]**
- [ ] Test extend mode with empty dataset (should start from 0001) **[NEW in v1.1.0]**
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

### 5. Extend Mode Index Detection **[NEW in v1.1.0]**
**Problem**: Not scanning all subsets (train/val/test) causes index collision
```python
# ❌ WRONG: Only checking train/
max_idx = find_max_in_directory(train_dir)

# ✅ CORRECT: Checking all subsets
for subset in ['train', 'val', 'test']:
    subset_path = get_images_path(dataset_root, subset)
    # scan and update max_idx
```

---

## Extension Points

### Safe to Extend
- Add new dialogs in `ui/` for new input types
- Add new processors in `core/` for new data operations
- Add new validators in `utils/` for new input types
- Add new fields to `DatasetConfig` for new data (if draft functionality is integrated)
- Add new modes to Step 2 (e.g., "Merge Datasets") following the dual-mode pattern **[NEW in v1.1.0]**

### Unsafe to Modify
- Main workflow sequence (Step 1-6 order and dependencies)
- PyInstaller spec file (unless necessary)
- Command generation format (LabelImg expects specific argument order)
- Random seed value (42) for reproducibility
- Image numbering format (4-digit, 0001-9999) **[CRITICAL for v1.1.0 extend mode]**
- Regex pattern in `find_max_image_index()` **[CRITICAL for v1.1.0]**

---

## Critical Architectural Constraints (v1.1.0)

### 1. Image Numbering System
- **Format**: 4-digit with leading zeros (0001.jpg, 0002.jpg, ..., 9999.jpg)
- **Maximum**: 9999 images per dataset
- **Extension Preservation**: Original extension converted to lowercase (.jpg, .png, etc.)
- **Collision Avoidance**: `find_max_image_index()` scans ALL subsets (train/val/test) to find max

### 2. Extend Mode Safety
- **Read-Only on Existing Data**: Extend mode NEVER modifies existing images in train/val/test
- **Temp Folder Isolation**: New images copied to temp/ only, user must run Step 3 to distribute
- **Index Continuation**: New images always start from `max_index + 1`, verified in preview
- **Structure Validation**: `validate_existing_structure()` ensures dataset is valid before extending

### 3. Backward Compatibility
- **Create New Mode**: Original v1.0.0 logic completely unchanged, extracted to `_execute_step2_create_new()`
- **Step 3-6 Agnostic**: Downstream steps work identically for both create and extend modes
- **State Storage**: Both modes save same variables (`dataset_root`, `temp_folder`), no mode tracking needed

### 4. UI-Core Separation (Enforced)
- **Mode Selection**: UI layer only (`ModeSelectionDialog`, `main_window.py` branching logic)
- **Validation**: Core layer only (`DatasetBuilder.validate_existing_structure()`)
- **Index Detection**: Core layer only (`DatasetBuilder.find_max_image_index()`)
- **Error Display**: UI shows errors returned from core as strings, never generated in core

---

## File Naming Conventions

- **UI files**: `<component>_<type>.py` (e.g., `ratio_dialog.py`, `pipeline_panel.py`, `mode_selection_dialog.py`)
- **Core files**: `<function>_<type>.py` (e.g., `image_processor.py`, `data_splitter.py`)
- **Dialog classes**: `<Name>Dialog` (e.g., `PreviewDialog`, `RatioDialog`, `ModeSelectionDialog`)
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
powershell -ExecutionPolicy Bypass -File create_portable.ps1

# 4. Create installer (requires Inno Setup)
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_setup.iss
```

### Build Output
- `dist/YOLO数据集预处理工具/` - Packaged application (onedir)
- `release/YOLO数据集预处理工具_v1.1.0_绿色版.zip` - Portable version
- `installer/YOLO数据集预处理工具_v1.1.0_Setup.exe` - Windows installer

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

### Extend Mode Index Collision **[NEW in v1.1.0]**
1. Verify `find_max_image_index()` scans all three subsets (train/val/test)
2. Check regex pattern matches 4-digit format correctly
3. Test with mixed extensions (.jpg, .png, .bmp)
4. Verify preview shows correct start index before copying

---

## Summary

This architecture is designed for:
- **Maintainability**: Clear separation of concerns across ui/core/models/utils layers
- **Testability**: Business logic independent of UI, all errors returned as strings
- **Extensibility**: New features can follow existing patterns (e.g., dual-mode in Step 2)
- **Stability**: Critical components clearly marked, backward compatibility enforced
- **Safety**: Extend mode never modifies existing data, all operations previewed before execution

**Golden Rule**: When in doubt, look at existing code patterns and follow them exactly.

**Version History**:
- **v1.0.0** (2026-02-27): Initial release with 6-step workflow
- **v1.1.0** (2026-02-28): Added dual-mode Step 2 (Create New / Extend Existing), backward compatible
