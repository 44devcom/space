You are an expert Qt C++ UI designer and XML generator.

Create a Qt Designer `.ui` file named **main_toolbar_form.ui** inside `project/app/views/`.  
This file defines a standalone toolbar component with a language switcher dropdown.

Follow all specifications below exactly.

---

## 🧱 Base Widget

- Class: `QWidget`
- Object name: `main_toolbar_form`
- Layout: `QHBoxLayout`
- Margins: 6 px
- Spacing: 4 px
- Minimum height: 40 px
- Size policy: Expanding width, Fixed height

---

## 🎛️ Toolbar Widgets (Left → Right)

1. **QPushButton**
   - objectName: `button_new`
   - text: `New`
   - tooltip: `Create a new item`
   - icon: `QStyle::SP_FileIcon`
   - flat: true

2. **QPushButton**
   - objectName: `button_open`
   - text: `Open`
   - tooltip: `Open an existing file`
   - icon: `QStyle::SP_DirOpenIcon`
   - flat: true

3. **QPushButton**
   - objectName: `button_save`
   - text: `Save`
   - tooltip: `Save current work`
   - icon: `QStyle::SP_DialogSaveButton`
   - flat: true

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
   - flat: true

6. **QSpacerItem**
   - expanding spacer (horizontal)
   - pushes next elements to the far right

---

## 🌍 Language Switcher (Right-Aligned Section)

7. **QLabel**
   - objectName: `label_language`
   - text: `Language:`
   - tooltip: `Select interface language`
   - font: bold
   - sizePolicy: Fixed width / Fixed height
   - small left margin (4 px)

8. **QComboBox**
   - objectName: `combobox_language`
   - tooltip: `Switch interface language`
   - fixed width: 120 px
   - items:
     - English (data: `en`)
     - Magyar (data: `hu`)
   - default: English
   - signal: `currentIndexChanged(int)`
   - this combo box will be connected later to `on_combobox_language_currentIndexChanged()` in the main window

---

## 🎨 Visual Style & Layout

- All buttons use icon size = 24x24 px
- Flat button style for clean toolbar look
- Layout alignment: left
- Toolbar height fixed at 40 px
- Right side (language section) visually balanced using spacer before label
- Use consistent 4 px spacing between widgets

---

## 🧩 Technical Requirements

- Must be a valid Qt Designer `.ui` XML file
- Usable in Qt Designer directly
- Automatically processed by CMake's `CMAKE_AUTOUIC`, which generates `ui_main_toolbar_form.h` that should be included in the corresponding header file
- Use <ui version="4.0"> root element

Proper <layout>, <widget>, and <spacer> structure

Include correct objectName attributes for all widgets

✅ Deliverable
Output the complete main_toolbar_form.ui XML file, ready for use and promotion in other UIs.

It must:

Open correctly in Qt Designer

Maintain alignment and spacing

Use valid widget hierarchy and Qt attributes

Be translatable (texts wrapped in tr() automatically by Designer)

yaml
Copy code
