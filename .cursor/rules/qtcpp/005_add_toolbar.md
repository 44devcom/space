You are an expert Qt C++ UI designer and XML architect.

Your task: create and integrate a reusable toolbar component into the main window UI of a Qt C++ project.

Follow this specification **exactly**.

---

## 🧩 Purpose

You will create:
1. A new UI file named `main_toolbar.ui`
2. Modify or generate `main_window.ui` so that it loads or embeds the toolbar

Both files must be Qt Designer–compatible `.ui` XML files.

---

## 1️⃣ Create `main_toolbar.ui`

**File:** `app/views/main_toolbar.ui`

**Base widget:** `QWidget`  
**Object name:** `main_toolbar`  
**Layout:** `QHBoxLayout`  
**Properties:**
- margin: 6 px  
- spacing: 4 px  
- minimum height: 40 px  
- horizontal expanding, fixed vertical size policy  

**Widgets (left → right):**

1. **QPushButton**
   - objectName: `button_new`
   - text: `New`
   - tooltip: `Create a new item`
   - icon: `QStyle::SP_FileIcon`

2. **QPushButton**
   - objectName: `button_open`
   - text: `Open`
   - tooltip: `Open an existing file`
   - icon: `QStyle::SP_DirOpenIcon`

3. **QPushButton**
   - objectName: `button_save`
   - text: `Save`
   - tooltip: `Save current work`
   - icon: `QStyle::SP_DialogSaveButton`

4. **QFrame (Separator)**
   - objectName: `frame_separator`
   - shape: `QFrame::VLine`
   - shadow: `QFrame::Sunken`
   - fixed width: 2 px

5. **QPushButton**
   - objectName: `button_refresh`
   - text: `Refresh`
   - tooltip: `Reload or refresh content`
   - icon: `QStyle::SP_BrowserReload`

6. **QSpacerItem**
   - expanding spacer at the end to push items left

**Button Properties:**
- flat = true  
- iconSize = 24x24  
- layout alignment = left  

**Naming conventions:**  
- All widgets: snake_case with type prefix  
- Example: `button_save`, `frame_separator`

---

## 2️⃣ Integrate into `main_window.ui`

**File:** `app/views/main_window.ui`

**Base widget:** `QMainWindow`  
**Object name:** `MainWindow`  
**Central widget:** `QWidget` with objectName `central_widget`  
**Layout:** `QVBoxLayout`

### Components:
1. **Menu Bar**
   - Object name: `menubar`
   - Menu: `menu_file` → contains one QAction:
     - objectName: `action_exit`
     - text: `Exit`

2. **Toolbar Integration**
   - Add a `QToolBar` (objectName: `toolbar_main`)
   - Inside, **promote a QWidget** to reference `main_toolbar.ui`
     - This toolbar will load the contents of `main_toolbar.ui`
     - In Designer: `<widget class="QWidget" name="main_toolbar">`
   - Ensure the promoted widget uses class `main_toolbar` and header `main_toolbar.h` (Designer placeholder; can be ignored in Python)

3. **Central Widget**
   - Contains a `QLabel` named `label_status`
   - Text: `Ready`

---

## 3️⃣ Technical Notes

- Ensure XML structure is fully valid.
- The generated `.ui` files must open directly in **Qt Designer** and are automatically processed by CMake's `CMAKE_AUTOUIC`, which generates `ui_main_window.h` and `ui_main_toolbar.h` that should be included in their respective header files.
  
Add necessary <connection> tags if needed for signals/slots (can be placeholders).

Do not include any C++ code — only .ui XML content.

4️⃣ Deliverables

✅ Output two files:

main_toolbar.ui — self-contained toolbar component

main_window.ui — main window embedding the toolbar and menu bar

Both must be complete, valid .ui XML files.

Each file should have comments or clear XML naming so future developers can easily identify their purpose.