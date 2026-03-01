# Architecture Documentation

**Project**: YOLO Dataset Preprocessing Tool
**Last Updated**: 2026-03-01
**Current Version**: 1.2.1

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
│   ├── tree_view_panel.py           # Right: directory tree view (dynamic, interactive) [UPDATED v1.2.0-1.2.1]
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
└── PROJECT_STATUS.md                # Current project status (v1.2.1)
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
- Manage preview tree visual state and user interactions **[v1.2.0-1.2.1]**

**Rules**:
- ✅ Can import from `core/`, `models/`, `utils/`
- ✅ Can use PySide6 widgets and dialogs
- ❌ MUST NOT contain business logic (no file operations, no data processing)
- ❌ MUST NOT directly access file system (use `core/` instead, except for tree display scanning)

**Files Overview**:
- `main_window.py`: Main controller, manages workflow state, coordinates Step 1-6 execution, tracks dataset_mode **[UPDATED v1.2.0]**
- `tree_view_panel.py`: **[UPDATED v1.2.0-1.2.1]** Dynamic directory tree with progressive building and file system interaction
  - Blank on startup (no hardcoded preview)
  - Progressive build in create mode (Step 2 → Step 5)
  - Real file system scanning in extend mode (Step 2)
  - Universal image folder update at Step 3 (both modes) **[v1.2.1]**
  - Double-click to open files/folders
  - Custom indentation (30px) for easier arrow clicking
  - Disabled double-click expansion to avoid conflicts
- `mode_selection_dialog.py`: Step 2 mode selection (Create New / Extend Existing) **[NEW in v1.1.0]**
- `preview_dialog.py`: Shows directory structure and image renaming preview (supports both create and extend modes)
- `classes_dialog.py`: Class names input with preloading support for extend mode **[UPDATED in v1.1.0]**
- `ratio_dialog.py`: Train/val/test ratio input
- `split_preview_dialog.py`: Data split preview
- `command_panel.py`: Displays and copies LabelImg commands
- `pipeline_panel.py`: Left sidebar with 6-step workflow cards

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
  ↓ (dataset_root, temp_folder, dataset_mode)
Step 3: Split Data + Update Tree [UPDATED v1.2.1]
  ↓ (train_images, val_images, test_images)
  ↓ Tree scans real folders and displays image info
Step 4: Manage Classes
  ↓ (classes list)
Step 5: Generate YAML (deletes old YAML files first)
  ↓ (yaml_path)
Step 6: Generate Commands
  ↓ (labelimg_commands)
```

### Step 2: Dual-Mode Architecture (v1.1.0)

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
  │    ├─ Set dataset_mode = "create" [v1.2.0]
  │    ├─ Save dataset_root, temp_folder
  │    └─ Update preview tree (Step 2 structure) [v1.2.0]
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
       ├─ Set dataset_mode = "extend" [v1.2.0]
       ├─ Save dataset_root, temp_folder
       └─ Update preview tree (full file system scan) [v1.2.0]
```

**Key Architectural Decisions**:
1. **Branching at UI Layer**: `main_window.py` contains two separate methods (`_execute_step2_create_new()` and `_execute_step2_extend_existing()`)
2. **Code Isolation**: Original "create new" logic completely unchanged, new "extend" logic in separate method
3. **Core Reuse**: Both modes use `ImageProcessor.rename_and_copy()` with different `start_index` values
4. **Validation in Core**: Structure validation and index detection in `core/dataset_builder.py`, not UI
5. **Backward Compatibility**: Step 3-6 work identically for both modes (operate on `temp/` folder)
6. **Preview Tree Integration**: UI tracks mode and calls appropriate tree update methods **[v1.2.0]**

### Preview Tree Dynamic Build (v1.2.0-1.2.1)

**Create Mode - Progressive Build**:
```
Step 2 completes
  ↓
tree_view_panel.build_tree_create_step2(dataset_name, dataset_root)
  └─ Creates root node: "dataset_name/"
  └─ Creates virtual folder structure:
       ├─ images/
       │   ├─ train/
       │   ├─ val/
       │   └─ test/
       ├─ labels/
       │   ├─ train/
       │   ├─ val/
       │   └─ test/
       └─ temp/
  └─ Updates mode label to "Real Mode" (green)

Step 3 completes [UPDATED v1.2.1]
  ↓
tree_view_panel.update_images_in_tree()
  └─ For each subset (train, val, test):
       ├─ Clears old child nodes (takeChildren)
       ├─ Scans real folder: os.listdir() + filter by image extensions
       ├─ Sorts filenames for consistency
       ├─ Displays:
       │   ├─ <共 N 张图片> (gray hint, count)
       │   ├─ First 5 image filenames (clickable file nodes)
       │   └─ ... (还有 X 张) (gray hint, if count > 5)
       └─ Handles empty folders: <暂无图片>

Step 4 completes
  ↓
tree_view_panel.build_tree_create_step4()
  └─ Adds under labels/:
       └─ classes.txt

Step 5 completes
  ↓
tree_view_panel.update_yaml_in_tree(new_yaml_filename, deleted_files)
  └─ Removes all old .yaml/.yml nodes from root
  └─ Adds new YAML node to root:
       └─ data.yaml
```

**Extend Mode - Mixed Strategy** **[UPDATED v1.2.1]**:
```
Step 2 completes
  ↓
tree_view_panel.build_tree_extend(dataset_root)
  └─ Creates root node: "existing_dataset/"
  └─ Recursively scans file system using _scan_directory():
       ├─ Lists all files and folders
       ├─ Separates folders and files
       ├─ Adds folder nodes first (recursive)
       ├─ Adds file nodes last (sorted)
       └─ Stores real file paths in Qt.UserRole
  └─ Updates mode label to "Real Mode" (green)

Step 3 completes [NEW v1.2.1]
  ↓
tree_view_panel.update_images_in_tree()
  └─ Same behavior as create mode:
       ├─ Clears train/val/test child nodes
       ├─ Re-scans folders for accurate counts
       ├─ Displays: count hint + first 5 examples + ellipsis
       └─ Ensures tree consistency with file system

Step 4-5 complete
  └─ YAML update only (same as create mode)
```

**Interactive Features**:
```
User double-clicks file node (e.g., 0001.jpg, classes.txt)
  ↓
_on_item_double_clicked(item, column)
  ↓
Retrieves path from item.data(0, Qt.UserRole)
  ↓
Detects it's a file (os.path.isfile)
  ↓
_open_file(path)
  └─ Normalizes path (os.path.normpath)
  └─ Opens with default program (os.startfile)

User double-clicks folder node (e.g., train/) or hint node (e.g., <共 50 张图片>)
  ↓
_on_item_double_clicked(item, column)
  ↓
Retrieves path from item.data(0, Qt.UserRole)
  ↓
Detects it's a folder (os.path.isdir)
  ↓
_open_in_explorer(path, select_file=False)
  └─ Normalizes path (os.path.normpath)
  └─ Opens in Explorer (subprocess.Popen(['explorer', path]))
```

### Step 3 Tree Update Logic (v1.2.1)

**Unified Behavior for Both Modes**:
```python
def update_images_in_tree(self):
    """Update image folder display after Step 3"""
    # Find images/ node
    images_item = find("images/")

    # For each subset: train, val, test
    for subset in ['train', 'val', 'test']:
        subset_item = find(f"{subset}/")

        # Clear old children
        subset_item.takeChildren()

        # Get real path
        subset_path = subset_item.data(Qt.UserRole)

        # Scan folder
        files = [f for f in os.listdir(subset_path)
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'))]
        files.sort()

        count = len(files)

        if count == 0:
            # Add hint: <暂无图片>
            add_hint("<暂无图片>", gray)
        else:
            # Add count hint: <共 N 张图片>
            add_hint(f"<共 {count} 张图片>", gray)

            # Add first 5 examples
            for i in range(min(5, count)):
                add_file_node(files[i], clickable)

            # Add ellipsis if more
            if count > 5:
                add_hint(f"... (还有 {count - 5} 张)", gray)
```

**Why This Design**:
1. **Accuracy**: Always scans real folders, not relying on passed parameters
2. **Consistency**: Both create and extend modes behave identically at Step 3
3. **Performance**: Limits display to 5 examples, avoiding thousands of nodes
4. **User Experience**: Shows enough info without cluttering the tree

### Step 3-6 Compatibility

Both "create new" and "extend existing" modes converge after Step 2:
- **Step 3**: Reads from `temp/`, splits to train/val/test (only new images, existing images untouched)
  - **Both modes**: Update tree with real scanned image info **[v1.2.1]**
- **Step 4**: Reads existing classes.txt if present, allows user to modify
  - Create mode: Adds classes.txt node to tree
  - Extend mode: Tree remains unchanged (classes.txt already exists)
- **Step 5**: **[v1.2.0]** Deletes all old YAML files, generates new one
  - Both modes: Updates tree by removing old YAML nodes and adding new one
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
- Update tree display logic in `tree_view_panel.py` **[v1.2.0-1.2.1]**

**Forbidden**:
- Adding file I/O in UI event handlers (except tree display scanning)
- Implementing data processing logic in UI methods
- Storing business state in UI class attributes (use `DatasetConfig` instead, though currently state is in main_window.py)

### 3. Modifying Core Logic

**Before Changing**:
- Verify change does not break existing UI flows
- Test with real data (especially large datasets)
- Ensure error messages are user-friendly

**Critical Functions** (test thoroughly):
- `ImageProcessor.rename_and_copy()` - handles file renaming, `start_index` parameter is critical for extend mode
- `DatasetBuilder.find_max_image_index()` - regex pattern must match 4-digit numbering **[v1.1.0]**
- `DatasetBuilder.validate_existing_structure()` - must check all required directories **[v1.1.0]**
- `DataSplitter.split_data()` - random seed must remain 42 for reproducibility
- `CommandGenerator.generate_commands()` - argument order is critical

### 4. Path Handling

**Rules**:
- ✅ Always use `os.path.join()` for path construction
- ✅ Wrap paths in double quotes when generating shell commands
- ✅ Test with paths containing spaces and Chinese characters
- ✅ Normalize paths before passing to subprocess (os.path.normpath) **[v1.2.0]**
- ❌ Never use string concatenation for paths (`path + "/" + file`)
- ❌ Never use hardcoded path separators (`"C:\folder\file"`)

**Example**:
```python
# ✅ GOOD
images_dir = os.path.join(dataset_root, 'images', 'train')
cmd = f'labelimg "{images_dir}" "{classes_file}" "{labels_dir}"'

# ✅ GOOD (v1.2.0 - for subprocess)
path = os.path.normpath(path)
subprocess.Popen(['explorer', path])

# ❌ BAD
images_dir = dataset_root + "/images/train"
cmd = f'labelimg {images_dir} {classes_file} {labels_dir}'  # Fails with spaces
```

### 5. Tree Widget Modifications **[v1.2.0-1.2.1]**

**Critical Settings**:
- `setExpandsOnDoubleClick(False)` - Prevents double-click conflict with file opening
- `setIndentation(30)` - Increases arrow click area (default is 20)
- `setData(0, Qt.UserRole, path)` - MUST store real paths for double-click handler

**Double-Click Behavior**:
```python
# ✅ CORRECT: Separate file and folder handling
if os.path.isfile(path):
    os.startfile(path)  # Open with default program
elif os.path.isdir(path):
    subprocess.Popen(['explorer', path])  # Open in Explorer

# ❌ WRONG: Using /select, parameter incorrectly
subprocess.Popen(['explorer', '/select,', path])  # Fails! Must be single param
```

**Image Folder Update** **[v1.2.1]**:
```python
# ✅ CORRECT: Clear old nodes, scan real folder
subset_item.takeChildren()  # Remove all children
files = [f for f in os.listdir(path) if is_image(f)]
files.sort()

# ❌ WRONG: Using passed parameters without scanning
add_hint(f"<已有 {train_count} 张图片>")  # May be outdated!
```

---

## Testing Guidelines

### Manual Testing Checklist

**After UI Changes**:
- [ ] Run `python main.py` and verify no import errors
- [ ] Test all 6 steps sequentially (create new mode)
- [ ] Test all 6 steps sequentially (extend existing mode)
- [ ] Test preview tree progressive build (create mode) **[v1.2.0]**
- [ ] Test preview tree file system scan (extend mode) **[v1.2.0]**
- [ ] Test preview tree Step 3 update (both modes) **[v1.2.1]**
- [ ] Test double-click on files (opens default program) **[v1.2.0]**
- [ ] Test double-click on folders (opens Explorer) **[v1.2.0]**
- [ ] Test double-click on example images (opens image viewer) **[v1.2.1]**
- [ ] Test arrow expansion/collapse (independent of double-click) **[v1.2.0]**
- [ ] Test with folder paths containing spaces and parentheses
- [ ] Test with Chinese folder paths

**After Core Logic Changes**:
- [ ] Test with 10 images (small dataset)
- [ ] Test with 100+ images (medium dataset)
- [ ] Test with empty folders (error handling)
- [ ] Test extend mode with existing dataset (verify index continuation)
- [ ] Test extend mode with empty dataset (should start from 0001)
- [ ] Verify generated files (classes.txt, data.yaml, commands)

**After Tree Widget Changes** **[v1.2.0-1.2.1]**:
- [ ] Test tree is blank on startup
- [ ] Test progressive build shows correct nodes at each step
- [ ] Test file system scan shows all files and folders
- [ ] Test Step 3 shows accurate image counts (not stale data) **[v1.2.1]**
- [ ] Test Step 3 shows first 5 examples correctly **[v1.2.1]**
- [ ] Test Step 3 shows ellipsis for large datasets **[v1.2.1]**
- [ ] Test Step 3 handles empty folders with hint **[v1.2.1]**
- [ ] Test double-click opens correct files/folders
- [ ] Test with large datasets (>1000 files, verify 2-3 second scan time acceptable)
- [ ] Test YAML replacement removes old nodes and adds new one

**After Packaging Changes**:
- [ ] Run `pyinstaller release.spec`
- [ ] Test packaged executable from `dist/`
- [ ] Verify no missing DLLs or imports
- [ ] Test on a clean machine without Python installed
- [ ] Test tree double-click still works in packaged app **[v1.2.0]**
- [ ] Test tree Step 3 update works in packaged app **[v1.2.1]**

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

### 5. Extend Mode Index Detection **[v1.1.0]**
**Problem**: Not scanning all subsets (train/val/test) causes index collision
```python
# ❌ WRONG: Only checking train/
max_idx = find_max_in_directory(train_dir)

# ✅ CORRECT: Checking all subsets
for subset in ['train', 'val', 'test']:
    subset_path = get_images_path(dataset_root, subset)
    # scan and update max_idx
```

### 6. Subprocess Parameter Formatting **[v1.2.0]**
**Problem**: Incorrect /select, parameter format causes Explorer to fail
```python
# ❌ WRONG: Split into separate parameters
subprocess.Popen(['explorer', '/select,', path])

# ✅ CORRECT: Merge into single parameter
subprocess.Popen(['explorer', f'/select,{path}'])

# ✅ ALSO CORRECT: Just open folder
subprocess.Popen(['explorer', os.path.normpath(path)])
```

### 7. Double-Click Expansion Conflict **[v1.2.0]**
**Problem**: Double-click both expands node and opens file
```python
# ❌ WRONG: Default QTreeWidget behavior conflicts
# (no setExpandsOnDoubleClick call)

# ✅ CORRECT: Disable double-click expansion
self.tree.setExpandsOnDoubleClick(False)
```

### 8. Tree Node Path Storage **[v1.2.0]**
**Problem**: Paths not stored or stored incorrectly
```python
# ❌ WRONG: Path only in label text
item = QTreeWidgetItem(parent, ["classes.txt"])

# ✅ CORRECT: Path stored in UserRole
item = QTreeWidgetItem(parent, ["classes.txt"])
item.setData(0, Qt.UserRole, "/path/to/classes.txt")
```

### 9. Step 3 Tree Update with Stale Data **[v1.2.1]**
**Problem**: Using passed parameters instead of scanning real folders
```python
# ❌ WRONG: May show outdated counts
def build_tree_step3(train_count, val_count, test_count):
    add_hint(f"<已有 {train_count} 张图片>")  # Not accurate!

# ✅ CORRECT: Always scan real folders
def update_images_in_tree():
    files = [f for f in os.listdir(subset_path) if is_image(f)]
    count = len(files)  # Accurate count
    add_hint(f"<共 {count} 张图片>")
```

### 10. Not Clearing Old Tree Nodes **[v1.2.1]**
**Problem**: Old nodes accumulate, causing duplicate or incorrect display
```python
# ❌ WRONG: Appending to existing children
subset_item.addChild(new_hint)  # Old hints remain!

# ✅ CORRECT: Clear before adding
subset_item.takeChildren()  # Remove all old children
subset_item.addChild(new_hint)  # Now add fresh data
```

---

## Extension Points

### Safe to Extend
- Add new dialogs in `ui/` for new input types
- Add new processors in `core/` for new data operations
- Add new validators in `utils/` for new input types
- Add new fields to `DatasetConfig` for new data (if draft functionality is integrated)
- Add new modes to Step 2 (e.g., "Merge Datasets") following the dual-mode pattern **[v1.1.0]**
- Add new tree interaction features (e.g., right-click menu, icons) in `tree_view_panel.py` **[v1.2.0]**
- Modify tree display strategy (e.g., show 10 examples instead of 5) **[v1.2.1]**

### Unsafe to Modify
- Main workflow sequence (Step 1-6 order and dependencies)
- PyInstaller spec file (unless necessary)
- Command generation format (LabelImg expects specific argument order)
- Random seed value (42) for reproducibility
- Image numbering format (4-digit, 0001-9999) **[CRITICAL for v1.1.0 extend mode]**
- Regex pattern in `find_max_image_index()` **[CRITICAL for v1.1.0]**
- Tree widget expansion/click behavior settings **[CRITICAL for v1.2.0 interactions]**
- Path normalization before subprocess calls **[CRITICAL for v1.2.0 Explorer opening]**
- Step 3 tree update strategy (must scan real folders) **[CRITICAL for v1.2.1 accuracy]**

---

## Critical Architectural Constraints

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

### 3. Preview Tree Behavior **[v1.2.0-1.2.1]**
- **Initial State**: Completely blank, no hardcoded preview structure
- **Create Mode**: Progressive building, no full file system scanning
  - Nodes added at Steps 2, 3, 4, 5
  - Paths constructed virtually using `os.path.join()`
  - Step 3: Scans only train/val/test folders for image counts **[v1.2.1]**
- **Extend Mode**: Mixed strategy
  - Step 2: Full file system scan (recursive)
  - Step 3: Re-scans train/val/test folders (same as create mode) **[v1.2.1]**
  - All paths are real file system paths
- **Image Display**: **[v1.2.1]**
  - Count hint: `<共 N 张图片>`
  - First 5 examples as file nodes
  - Ellipsis: `... (还有 X 张)` if count > 5
  - Empty hint: `<暂无图片>` if count = 0
- **Double-Click Safety**: Disabled built-in expansion to avoid conflict with file opening
- **Path Storage**: All paths stored in `Qt.UserRole`, never in visible text

### 4. Step 3 Image Folder Update **[v1.2.1]**
- **Always Re-scan**: Never trust passed parameters, always scan real folders
- **Clear Before Update**: `takeChildren()` to remove old nodes before adding new ones
- **File Filtering**: Only include files with image extensions (.jpg, .jpeg, .png, .bmp, .tiff, .tif)
- **Sorting**: Always sort filenames for consistent display order
- **Universal Behavior**: Both create and extend modes use the same update logic

### 5. Step 5 YAML Management **[v1.2.0]**
- **Cleanup First**: Deletes ALL .yaml/.yml files in dataset root before generating new one
- **Tree Synchronization**: Updates preview tree in both create and extend modes
- **User Notification**: Success dialog shows deleted files if any existed
- **Idempotency**: Can be executed multiple times safely (each time replaces previous YAML)

### 6. Backward Compatibility
- **Create New Mode**: Original v1.0.0 logic completely unchanged, extracted to `_execute_step2_create_new()`
- **Step 3-6 Agnostic**: Downstream steps work identically for both create and extend modes
- **State Storage**: Both modes save same variables (`dataset_root`, `temp_folder`), mode tracked separately **[v1.2.0]**

### 7. UI-Core Separation (Enforced)
- **Mode Selection**: UI layer only (`ModeSelectionDialog`, `main_window.py` branching logic)
- **Validation**: Core layer only (`DatasetBuilder.validate_existing_structure()`)
- **Index Detection**: Core layer only (`DatasetBuilder.find_max_image_index()`)
- **Tree Display**: UI layer only (`tree_view_panel.py`) **[v1.2.0-1.2.1]**
- **File Scanning for Display**: UI layer only (tree display purposes, not business logic) **[v1.2.1]**
- **File Opening**: UI layer only (Windows-specific `os.startfile`, `subprocess.Popen`) **[v1.2.0]**
- **Error Display**: UI shows errors returned from core as strings, never generated in core

---

## File Naming Conventions

- **UI files**: `<component>_<type>.py` (e.g., `ratio_dialog.py`, `pipeline_panel.py`, `mode_selection_dialog.py`, `tree_view_panel.py`)
- **Core files**: `<function>_<type>.py` (e.g., `image_processor.py`, `data_splitter.py`)
- **Dialog classes**: `<Name>Dialog` (e.g., `PreviewDialog`, `RatioDialog`, `ModeSelectionDialog`)
- **Panel classes**: `<Name>Panel` (e.g., `PipelinePanel`, `CommandPanel`, `TreeViewPanel`)

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
- `release/YOLO数据集预处理工具_v1.2.1_绿色版.zip` - Portable version
- `installer/YOLO数据集预处理工具_v1.2.1_Setup.exe` - Windows installer

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

### Extend Mode Index Collision **[v1.1.0]**
1. Verify `find_max_image_index()` scans all three subsets (train/val/test)
2. Check regex pattern matches 4-digit format correctly
3. Test with mixed extensions (.jpg, .png, .bmp)
4. Verify preview shows correct start index before copying

### Tree Double-Click Not Working **[v1.2.0]**
1. Verify `setExpandsOnDoubleClick(False)` is called in tree initialization
2. Check paths are stored in `Qt.UserRole` (use debugger or print statements)
3. Test path normalization: `os.path.normpath(path)` before subprocess call
4. Verify subprocess parameter format: `['explorer', f'/select,{path}']` (merged, not split)
5. Check file exists: `os.path.exists(path)` before opening

### Tree Not Updating After Step Execution **[v1.2.0]**
1. Verify `dataset_mode` is set correctly in Step 2 ("create" or "extend")
2. Check tree update methods are called with correct conditions
3. Verify `self.root_item` exists before calling update methods
4. Check `_find_item_by_text()` returns valid nodes (not None)

### Tree Shows Outdated Image Counts **[v1.2.1]**
1. Verify `update_images_in_tree()` is called after Step 3 completes
2. Check that `takeChildren()` is called to clear old nodes
3. Test that `os.listdir()` scans the correct folder paths
4. Verify file filtering includes all image extensions
5. Check that nodes store correct paths in `Qt.UserRole`

### Tree Shows Duplicate Nodes **[v1.2.1]**
1. Verify `takeChildren()` is called before adding new nodes
2. Check that Step 3 is not called multiple times without clearing
3. Test with create mode and extend mode separately

---

## Summary

This architecture is designed for:
- **Maintainability**: Clear separation of concerns across ui/core/models/utils layers
- **Testability**: Business logic independent of UI, all errors returned as strings
- **Extensibility**: New features can follow existing patterns (e.g., dual-mode in Step 2, progressive tree in v1.2.0)
- **Stability**: Critical components clearly marked, backward compatibility enforced
- **Safety**: Extend mode never modifies existing data, all operations previewed before execution
- **Interactivity**: Preview tree provides direct file system access while maintaining clean architecture **[v1.2.0]**
- **Accuracy**: Tree always reflects actual file system state, not stale cached data **[v1.2.1]**

**Golden Rule**: When in doubt, look at existing code patterns and follow them exactly.

**Version History**:
- **v1.0.0** (2026-02-27): Initial release with 6-step workflow
- **v1.1.0** (2026-02-28): Added dual-mode Step 2 (Create New / Extend Existing), backward compatible
- **v1.2.0** (2026-03-01): Added preview tree dynamic build and file system interaction, YAML smart replacement
- **v1.2.1** (2026-03-01): Unified Step 3 tree update for both modes, real folder scanning for accurate counts, example display strategy
