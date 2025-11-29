# Cursor AI Prompt: Add Connection Manager MVC (Connections Tab in Settings Dialog)

You are extending the existing Qt C++ app project.  
Enhance the existing Settings system by adding a Connection Manager MVC (Model–Controller–View).  
The Connections tab will appear inside the existing Settings dialog (`settings_view.ui`).

**Follow all steps and structure carefully.**

## 🎯 Goals

Add new MVC components:

- `app/models/connection_model.cpp`
- `app/models/connection_model.h`
- `app/controllers/connection_controller.cpp`
- `app/controllers/connection_controller.h`
- `app/views/connection_view.cpp`
- `app/views/connection_view.h`
- `app/views/connection_view.ui`

### Requirements

- Integrate the connection manager UI as a tab inside `settings_view.ui` (not a separate window)
- The tab name: **"Connections"**
- The `.ui` files are automatically processed by CMake's `CMAKE_AUTOUIC`
- Ensure a persistent data file: `app/connections.json` (auto-created if missing)

## 🧱 Project Structure Update

```
project/
└── app/
    ├── main.cpp
    ├── CMakeLists.txt
    ├── models/
    │   ├── settings_model.cpp
    │   ├── settings_model.h
    │   ├── connection_model.cpp
    │   └── connection_model.h
    ├── controllers/
    │   ├── settings_controller.cpp
    │   ├── settings_controller.h
    │   ├── connection_controller.cpp
    │   └── connection_controller.h
    ├── views/
    │   ├── main_window.cpp
    │   ├── main_window.h
    │   ├── main_window.ui
    │   ├── settings_view.ui
    │   ├── settings_view.cpp
    │   ├── settings_view.h
    │   ├── connection_view.ui
    │   ├── connection_view.cpp
    │   └── connection_view.h
    ├── defaults.json
    └── connections.json         # auto-created if missing
```

## 🪟 UI: Connection Manager Form (`connection_view.ui`)

Design this UI in Qt Designer.

### 🧩 Base Widget

- **Type:** QWidget
- **Object name:** `connection_form`
- **Layout:** QVBoxLayout
- **Purpose:** Embedded directly into `settings_view.ui` under a "Connections" tab

### 🧱 Layout Hierarchy

```
Root Layout → QVBoxLayout
├── QGroupBox — "Connection Details"
│   └── Layout: QFormLayout
│       ├── Connection Type → QComboBox (combobox_connection_type)
│       ├── Host → QLineEdit (lineedit_host)
│       ├── Port → QLineEdit (lineedit_port)
│       ├── Username → QLineEdit (lineedit_username)
│       └── Password → QLineEdit (lineedit_password)
├── QHBoxLayout — action buttons row
│   ├── button_test_connection
│   ├── button_save_connection
│   └── button_remove_connection
├── QTableWidget — for listing saved connections
│   └── Object name: table_connections
└── QSpacerItem — at bottom (vertical expanding)
```

### Form Fields

| Label | Widget | Object Name | Notes |
|-------|--------|-------------|-------|
| Connection Type | QComboBox | `combobox_connection_type` | Items: FTP, SQL |
| Host | QLineEdit | `lineedit_host` | Placeholder: e.g., localhost |
| Port | QLineEdit | `lineedit_port` | Input mask: integer only |
| Username | QLineEdit | `lineedit_username` | |
| Password | QLineEdit | `lineedit_password` | Echo mode: Password |

### Action Buttons

- **`button_test_connection`** → Text: "Test Connection"
- **`button_save_connection`** → Text: "Save Connection"
- **`button_remove_connection`** → Text: "Remove Selected"
- **All buttons right-aligned**

### Table Configuration

- **Object name:** `table_connections`
- **Columns:** Type, Host, Port, Username
- **Read-only rows**
- **Supports selection** for edit/remove
- **Stretch last column**

## 🧩 Integration into Settings Dialog

1. Open `settings_view.ui`
2. Inside the main QTabWidget (`objectName: tabwidget_settings`), add a new tab:
   - **Tab name:** Connections
   - **Tab content:** Promote a QWidget to the generated `connection_view.ui` (or include via QWidget placeholder named `widget_connections`)

### Tab Order

1. General
2. Connections
3. Advanced (optional)

## 🧰 Compilation

The `.ui` files are automatically processed by CMake's `CMAKE_AUTOUIC`, which generates `ui_connection_view.h` and `ui_settings_view.h` that should be included in their respective header files.

## 🧠 Implementation Rules

### 1️⃣ ConnectionModel (`connection_model.cpp` and `connection_model.h`)

- Reads/writes `connections.json`
- Auto-creates file if missing with example:

```json
[
  {
    "type": "FTP",
    "host": "localhost",
    "port": 21,
    "username": "user",
    "password": "pass"
  }
]
```

- Provides methods:
  - `list_connections()`
  - `add_connection(data)`
  - `update_connection(index, data)`
  - `remove_connection(index)`
- Returns data in safe dictionary form (hide passwords by default)

### 2️⃣ ConnectionController (`connection_controller.cpp` and `connection_controller.h`)

- Loads model at startup
- Populates `table_connections` with stored entries
- Connects UI signals:
  - `button_save_connection.clicked` → `save_connection()`
  - `button_remove_connection.clicked` → `remove_connection()`
  - `button_test_connection.clicked` → `test_connection()`

#### Handles "Test Connection"

- **FTP:** test via Qt's network classes or a C++ FTP library
- **SQL:** test via Qt's SQL module (`QSqlDatabase`)
- Displays success/failure message via `QMessageBox`

### 3️⃣ ConnectionView (`connection_view.ui` + `connection_view.cpp` and `connection_view.h`)

- Exposes custom signals:
  - `signal_save_connection`
  - `signal_test_connection`
  - `signal_remove_connection`
- Provides getters for all form fields:
  - `get_connection_type()`
  - `get_host()`
  - `get_port()`
  - `get_username()`
  - `get_password()`
- Provides `populate_table(connections: list)` and `clear_fields()` methods

## 🔗 Integration Flow

In `settings_controller.cpp`:

- Include and initialize `ConnectionController` and `ConnectionView`
- Embed the `connection_form` (from `connection_view.ui`) inside the "Connections" tab
- Connect its signals to controller methods
- Ensure updates to `connections.json` are reflected immediately

## 🧾 Build Config (`CMakeLists.txt`)

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
    views/connection_view.cpp
    views/connection_view.h
    views/connection_view.ui
    models/settings_model.cpp
    models/settings_model.h
    models/connection_model.cpp
    models/connection_model.h
    controllers/settings_controller.cpp
    controllers/settings_controller.h
    controllers/connection_controller.cpp
    controllers/connection_controller.h
)
```

## ⚡ Build & Verification

### Run Commands

```bash
mkdir -p build
cd build
cmake ..
make
./MyApp
```

### Verification Checklist

- [ ] `connections.json` auto-created with defaults
- [ ] Settings dialog has Connections tab
- [ ] Adding/removing/editing works
- [ ] "Test Connection" validates credentials
- [ ] Changes persist to JSON and reload on restart

## ✅ Expected Result

- **Unified Settings dialog** with a Connections tab
- **Full MVC separation**
- **Persistent storage** (`connections.json`)
- **Reusable and translatable UI**
- **Buttons and table fully functional**
- **Integrated and compiled** with CMake's `CMAKE_AUTOUIC`