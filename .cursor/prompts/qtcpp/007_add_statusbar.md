You are an expert Qt C++ UI designer and XML generator.

Create a Qt Designer `.ui` file named **main_statusbar.ui** inside `project/app/views/`.

This file defines a **status bar component** that follows the same design and naming conventions as other toolbar/UI components in the project (e.g. main_toolbar_form.ui).

The result must be a valid `.ui` XML file ready for use in Qt Designer and Qt C++.

---

## 🧱 Base Widget

- Class: `QWidget`
- Object name: `main_statusbar`
- Layout: `QHBoxLayout`
- Margins: 4 px
- Spacing: 6 px
- Minimum height: 28 px
- Size policy: Expanding width, Fixed height

---

## 🎛️ Status Bar Layout (Left → Right)

1. **QLabel**
   - objectName: `label_status`
   - text: `Ready`
   - tooltip: `Application status`
   - alignment: left
   - sizePolicy: Expanding horizontally, Fixed vertically

2. **QProgressBar**
   - objectName: `progressbar_status`
   - tooltip: `Shows operation progress`
   - minimum: 0
   - maximum: 100
   - value: 0
   - visible: false (default)
   - textVisible: true
   - sizePolicy: Fixed width (150px)
   - alignment: center vertically

3. **QSpacerItem**
   - Expanding horizontal spacer to push right-aligned widgets to the end

4. **QLabel**
   - objectName: `label_datetime`
   - text: `--:--`
   - tooltip: `Displays current time`
   - alignment: right
   - sizePolicy: Fixed width / Fixed height
   - minimum width: 80 px
   - font: monospace (if supported)

5. **QLabel**
   - objectName: `label_language_status`
   - text: `EN`
   - tooltip: `Currently active language`
   - alignment: right
   - fixed width: 40 px
   - frameShape: `QFrame::Box`
   - frameShadow: `QFrame::Sunken`
   - optional background: light gray for visibility

---

## 🎨 Visual Style

- Background: inherits from parent window
- Font: small (10–11 pt)
- Consistent margins and spacing
- Status text left-aligned, system information right-aligned
- All text labels use `self.tr()` for translatable strings

---

## 🧩 Technical Requirements

- Must be a **valid Qt Designer .ui XML file**
- Usable directly in Qt Designer and automatically processed by CMake's `CMAKE_AUTOUIC`, which generates `ui_main_statusbar.h` that should be included in the corresponding header file
- Include XML declaration and <ui version="4.0"> root element

Ensure all <layout>, <item>, <widget>, and <spacer> tags are correct

Do not include C++ code — only .ui XML

🧠 Naming Conventions
All widgets: snake_case with type prefix

Examples: label_status, progressbar_status, label_language_status

Signals (future use): e.g. on_progressbar_status_valueChanged()

Consistent with project-wide naming patterns

✅ Deliverable
Output the complete main_statusbar.ui XML content, ready to be opened and edited in Qt Designer.

It must:

Be automatically processed by CMake's `CMAKE_AUTOUIC`

Display all widgets aligned properly

Support translation (tr()-enabled text)

Match project visual standards