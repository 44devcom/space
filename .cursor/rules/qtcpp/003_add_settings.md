# Cursor AI Prompt: Add Settings MVC with UI Compilation + Form Layout Structure

You are extending the existing Qt C++ app project.  
Add a Settings system implemented using QtModel – QtController – QtView, with a structured form-based UI.

**Follow all steps and rules carefully.**

## 🎯 Goals

Create the following new files in the proper folders:

- `app/models/settings_model.cpp`
- `app/models/settings_model.h`
- `app/controllers/settings_controller.cpp`
- `app/controllers/settings_controller.h`
- `app/views/settings_view.cpp`
- `app/views/settings_view.h`
- `app/views/settings_view.ui`
- `app/defaults.json`

### Requirements

- The `.ui` file is automatically processed by CMake's `CMAKE_AUTOUIC`
- The MVC pattern is correctly followed
- The settings system loads automatically at app startup
- The view uses a structured layout with form sections

## 🧱 Project Structure Update

```
project/
└── app/
    ├── main.cpp
    ├── CMakeLists.txt
    ├── models/
    │   ├── settings_model.cpp
    │   └── settings_model.h
    ├── controllers/
    │   ├── settings_controller.cpp
    │   └── settings_controller.h
    ├── views/
    │   ├── main_window.cpp
    │   ├── main_window.h
    │   ├── main_window.ui
    │   ├── settings_view.ui
    │   ├── settings_view.cpp
    │   └── settings_view.h
    └── defaults.json          # auto-created if missing
```

## 🪟 UI File Specification: settings_view.ui

Design the Settings Dialog in Qt Designer (XML `.ui`).

### 🧩 Base Widget

- **Type:** QDialog (or QDockWidget if needed)
- **Object name:** `settings_dialog`
- **Window title:** Settings
- **Layout:** QVBoxLayout (main)
- **Minimum size:** 320x220

### 🧱 Layout Hierarchy

```
Root Layout → QVBoxLayout
├── QTabWidget (objectName: tabwidget_settings)
│   ├── Tab 1: General
│   └── Tab 2: Advanced (reserved, can be empty)
└── QDialogButtonBox
    ├── Object name: buttonbox_settings
    ├── Standard buttons: Save | Cancel
    ├── Orientation: Horizontal
    └── Alignment: Right
```

### Inside "General" Tab

- **Layout:** QFormLayout
- **Object name:** `formlayout_general`
- **Spacing:** 8 px
- **Margins:** 6 px

#### Field Groups

**Theme**
- **Label:** Theme
- **Widget:** `combobox_theme`
- **Type:** QComboBox
- **Items:** Light, Dark

**Language**
- **Label:** Language
- **Widget:** `combobox_language`
- **Type:** QComboBox
- **Items:** English (en), Hungarian (hu)

**Autoload**
- **Label:** Load settings on startup
- **Widget:** `checkbox_autoload`
- **Type:** QCheckBox
- **Checked:** True by default

**Notifications (Optional)**
- **Label:** Enable notifications
- **Widget:** `checkbox_notifications`
- **Type:** QCheckBox
- **Default:** True

### 🎨 UI Rules

- **Widget naming:** snake_case + type prefix  
  e.g., `combobox_language`, `checkbox_autoload`
- **Use Form Layout** for grouped fields
- **Use QVBoxLayout** for dialog structure (tabs + buttons)
- **Ensure translatable labels** (via `self.tr()` in Python)

## 🧰 Compilation

The `.ui` file is automatically processed by CMake's `CMAKE_AUTOUIC`, which generates `ui_settings_view.h` that should be included in `settings_view.h`.

## 🧠 MVC Implementation Rules

### 1️⃣ SettingsModel (`settings_model.cpp` and `settings_model.h`)

- Reads/writes `defaults.json`
- Creates file if missing with defaults:

```json
{
  "theme": "light",
  "language": "en",
  "autoload": true,
  "notifications": true
}
```

- Exposes `get()` and `set()` methods for all keys

### 2️⃣ SettingsController (`settings_controller.cpp` and `settings_controller.h`)

- Loads the model at startup
- Populates the view with saved values
- Connects signals from the view (save/cancel)
- Writes changes back to JSON via the model

### 3️⃣ SettingsView (`settings_view.cpp`, `settings_view.h` + `.ui`)

- Includes the auto-generated `ui_settings_view.h` from the `.ui` file
- Exposes signals such as:
  - `signal_save_settings`
  - `signal_cancel_settings`
- Provides helper methods:
  - `get_selected_theme()`
  - `get_selected_language()`
  - `get_autoload_state()`

## 🏗️ Integration in main.cpp

- Include `settings_view.h` and `settings_controller.h`
- Initialize both before showing the main window
- Ensure settings load before other components (e.g., language translator)
- Add a menu or toolbar button in `main_window.ui`:
  - `action_settings` → opens the dialog

## 🧾 Update CMakeLists.txt

Add all source files to the `SOURCES` variable:

```cmake
set(SOURCES
    main.cpp
    views/main_window.cpp
    views/main_window.h
    views/main_window.ui
    views/settings_view.cpp
    views/settings_view.h
    views/settings_view.ui
    models/settings_model.cpp
    models/settings_model.h
    controllers/settings_controller.cpp
    controllers/settings_controller.h
)
```

## ✅ Build & Verification

### Run Commands

```bash
mkdir -p build
cd build
cmake ..
make
./MyApp
```

### Verification Checklist

- [ ] `defaults.json` exists and loads defaults
- [ ] Settings dialog opens and displays values
- [ ] Changing settings updates the JSON file
- [ ] Values persist across app restarts