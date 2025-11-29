
# Qt C++ Project Initialization Guide

## 1️⃣ Project Structure

Create the following directory structure:

```
project/
└── app/
    ├── main.cpp
    ├── CMakeLists.txt
    └── views/
        ├── main_window.cpp
        ├── main_window.h
        └── main_window.ui
```

---

## 2️⃣ Naming Conventions

### Classes
- **CamelCase**, descriptive, clear
- Examples: `InitMainWindow`, `SettingsDialog`, `UserForm`

### Widgets (instance names)
- **snake_case** with widget type prefix
- Examples: `label_status`, `button_save`, `lineedit_username`, `combobox_options`

### Actions
- Format: `action_<verb>`
- Examples: `action_exit`, `action_save`, `action_open_file`

### Slots (manual + Designer auto-connected)
- Format: `on_<sendername>_<signal>()`
- Examples:
  - `on_button_save_clicked()`
  - `on_action_exit_triggered()`
  - `on_lineedit_username_textChanged()`

### Variables inside Slots
- Use **snake_case**, descriptive, meaningful
- Examples: `current_index`, `user_input`, `file_path`

**General Guidelines:**
- No abbreviations
- Signals unique per class
- Consistency across all files

---

## 3️⃣ UI File

**app/views/main_window.ui**

- Base widget: `QMainWindow`
- Menu bar → **File → Exit**
- Define one QAction in Designer:
  - `action_exit` (connected to File → Exit)

---

## 4️⃣ CMake Configuration

Create a `CMakeLists.txt` with:

```cmake
cmake_minimum_required(VERSION 3.16)
project(MyApp VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)

set(SOURCES
    main.cpp
    views/main_window.cpp
    views/main_window.h
    views/main_window.ui
)

qt_add_executable(MyApp ${SOURCES})
target_link_libraries(MyApp PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)
```

---

## 5️⃣ Build & Verification

Build the project with:

```bash
mkdir -p build
cd build
cmake ..
make
```

Run the application to verify it launches successfully:

```bash
./MyApp
```

---

## ✅ Notes

The `.ui` file is automatically processed by CMake's `CMAKE_AUTOUIC` setting, which generates `ui_main_window.h` that can be included in `main_window.h`.

Keep naming conventions consistent across Designer and C++ code.