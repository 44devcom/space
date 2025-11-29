---
name: create-view-agent
description: "Generate Qt C++ view components (windows, dialogs, widgets) following Qt C++ MVC conventions and project structure."
inputSchema:
  type: object
  properties:
    viewName:
      type: string
      description: "Name of the view (e.g., 'settings', 'user-profile', 'connection-form')"
    viewType:
      type: string
      enum: ["window", "dialog", "widget", "page", "dock"]
      default: "dialog"
      description: "Type of view to create"
    layout:
      type: string
      enum: ["form", "vertical", "horizontal", "grid", "tabs"]
      default: "form"
      description: "Layout type for the view"
    mvc:
      type: boolean
      default: false
      description: "Generate full MVC (controller and model)"
    widgets:
      type: array
      items:
        type: string
      description: "List of widget types to include (e.g., ['table', 'chart', 'status'])"
    description:
      type: string
      description: "Description of the view's purpose"
stdin: true
---

# Create View Agent (Qt C++)

## Purpose

Generate complete Qt C++ view components (windows, dialogs, widgets, pages) following the rules defined in `.cursor/rules/qtcpp.mdc`.

The agent creates:
- Header file (`views/<view_name>_view.h`)
- Implementation file (`views/<view_name>_view.cpp`)
- UI file (`views/<view_name>_view.ui`)
- Optional: Controller (`controllers/<view_name>_controller.h/cpp`)
- Optional: Model (`models/<view_name>_model.h/cpp`)
- Updates `CMakeLists.txt` automatically

---

## Input Processing

### Step 1: Parse User Input

The agent accepts:
- Natural language description (e.g., "create a settings dialog with theme and language options")
- Structured input via JSON schema
- Command-line style arguments

### Step 2: Determine View Characteristics

From the input, determine:

1. **View Name**: Convert to snake_case (e.g., "user-profile" → "user_profile")
2. **View Type**: 
   - `window` → QMainWindow
   - `dialog` → QDialog
   - `widget` → QWidget
   - `page` → QWidget (for QStackedWidget)
   - `dock` → QDockWidget
3. **Layout Type**:
   - `form` → QFormLayout
   - `vertical` → QVBoxLayout
   - `horizontal` → QHBoxLayout
   - `grid` → QGridLayout
   - `tabs` → QTabWidget
4. **Widgets Needed**: Parse from description or explicit list
5. **MVC Pattern**: Determine if controller/model needed

---

## File Generation

### Step 3: Generate Header File

Create `views/<view_name>_view.h`:

```cpp
#ifndef <VIEW_NAME_UPPER>_VIEW_H
#define <VIEW_NAME_UPPER>_VIEW_H

#include <QWidget>
#include <QDialog>  // or QMainWindow, QDockWidget based on type
#include "ui_<view_name>_view.h"

class <ViewNameCamel>View : public QDialog  // or QMainWindow, QWidget
{
    Q_OBJECT

public:
    explicit <ViewNameCamel>View(QWidget *parent = nullptr);
    ~<ViewNameCamel>View();

    // Public getter methods (generated based on widgets)
    QString get_selected_value() const;
    bool get_checkbox_state() const;
    // ... more getters as needed

signals:
    void signal_save_<view_name>();
    void signal_cancel_<view_name>();
    void signal_<action_name>();

private slots:
    void on_button_save_clicked();
    void on_button_cancel_clicked();
    void on_<widget_name>_<signal>();

private:
    Ui::<ViewNameCamel>View *ui;
    void setup_connections();
    void load_defaults();
};

#endif // <VIEW_NAME_UPPER>_VIEW_H
```

**Naming Rules:**
- Class name: PascalCase (e.g., `SettingsView`, `UserProfileView`)
- Header guard: UPPER_SNAKE_CASE
- UI pointer: `ui` (lowercase)
- Methods: snake_case

### Step 4: Generate Implementation File

Create `views/<view_name>_view.cpp`:

```cpp
#include "<view_name>_view.h"
#include <QMessageBox>

<ViewNameCamel>View::<ViewNameCamel>View(QWidget *parent)
    : QDialog(parent)  // or QMainWindow, QWidget
    , ui(new Ui::<ViewNameCamel>View)
{
    ui->setupUi(this);
    setup_connections();
    load_defaults();
}

<ViewNameCamel>View::~<ViewNameCamel>View()
{
    delete ui;
}

void <ViewNameCamel>View::setup_connections()
{
    // Manual signal/slot connections if needed
    // Auto-connections handled by naming convention (on_<sender>_<signal>)
}

void <ViewNameCamel>View::load_defaults()
{
    // Initialize UI with default values
    // Populate comboboxes, set checkboxes, etc.
}

// Getter methods
QString <ViewNameCamel>View::get_selected_value() const
{
    return ui->combobox_field->currentText();
}

bool <ViewNameCamel>View::get_checkbox_state() const
{
    return ui->checkbox_field->isChecked();
}

// Slot implementations
void <ViewNameCamel>View::on_button_save_clicked()
{
    emit signal_save_<view_name>();
    accept();  // or close() for QMainWindow
}

void <ViewNameCamel>View::on_button_cancel_clicked()
{
    emit signal_cancel_<view_name>();
    reject();  // or close() for QMainWindow
}
```

### Step 5: Generate UI File

Create `views/<view_name>_view.ui` (XML format):

**For Dialog with Form Layout:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class><ViewNameCamel>View</class>
 <widget class="QDialog" name="<view_name>_dialog">
  <property name="windowTitle">
   <string><View Title></string>
  </property>
  <property name="minimumSize">
   <size>
    <width>320</width>
    <height>220</height>
   </size>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <item>
    <widget class="QWidget" name="content_widget">
     <layout class="QFormLayout" name="formlayout_main">
      <item row="0" column="0">
       <widget class="QLabel" name="label_field1">
        <property name="text">
         <string>Field 1:</string>
        </property>
       </widget>
      </item>
      <item row="0" column="1">
       <widget class="QLineEdit" name="lineedit_field1"/>
      </item>
      <!-- More form fields -->
     </layout>
    </widget>
   </item>
   <item>
    <widget class="QDialogButtonBox" name="buttonbox_<view_name>">
     <property name="standardButtons">
      <set>QDialogButtonBox::Cancel|QDialogButtonBox::Save</set>
     </property>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
```

**For Main Window:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class><ViewNameCamel>View</class>
 <widget class="QMainWindow" name="<view_name>_window">
  <property name="windowTitle">
   <string><Window Title></string>
  </property>
  <widget class="QWidget" name="central_widget">
   <layout class="QVBoxLayout" name="verticalLayout">
    <!-- Content here -->
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar"/>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
```

**Widget Naming Rules:**
- Object names: `snake_case` with type prefix
  - `button_save`, `button_cancel`
  - `lineedit_username`, `lineedit_password`
  - `combobox_language`, `combobox_theme`
  - `checkbox_enable`, `checkbox_autoload`
  - `table_data`, `list_items`
  - `label_status`, `label_title`

### Step 6: Generate Controller (if MVC requested)

Create `controllers/<view_name>_controller.h`:

```cpp
#ifndef <VIEW_NAME_UPPER>_CONTROLLER_H
#define <VIEW_NAME_UPPER>_CONTROLLER_H

#include <QObject>
#include "<view_name>_view.h"
#include "<view_name>_model.h"  // if model needed

class <ViewNameCamel>Controller : public QObject
{
    Q_OBJECT

public:
    explicit <ViewNameCamel>Controller(QObject *parent = nullptr);
    ~<ViewNameCamel>Controller();
    
    void show_view();
    <ViewNameCamel>View* get_view() const { return m_view; }

private slots:
    void on_save_clicked();
    void on_cancel_clicked();

private:
    <ViewNameCamel>View *m_view;
    <ViewNameCamel>Model *m_model;  // if model needed
    void setup_connections();
    void load_data();
};

#endif // <VIEW_NAME_UPPER>_CONTROLLER_H
```

Create `controllers/<view_name>_controller.cpp`:

```cpp
#include "<view_name>_controller.h"
#include <QMessageBox>

<ViewNameCamel>Controller::<ViewNameCamel>Controller(QObject *parent)
    : QObject(parent)
    , m_view(nullptr)
    , m_model(new <ViewNameCamel>Model(this))
{
    m_view = new <ViewNameCamel>View();
    setup_connections();
    load_data();
}

<ViewNameCamel>Controller::~<ViewNameCamel>Controller()
{
    if (m_view) {
        delete m_view;
    }
}

void <ViewNameCamel>Controller::show_view()
{
    if (m_view) {
        m_view->show();
    }
}

void <ViewNameCamel>Controller::setup_connections()
{
    connect(m_view, &<ViewNameCamel>View::signal_save_<view_name>, 
            this, &<ViewNameCamel>Controller::on_save_clicked);
    connect(m_view, &<ViewNameCamel>View::signal_cancel_<view_name>, 
            this, &<ViewNameCamel>Controller::on_cancel_clicked);
}

void <ViewNameCamel>Controller::load_data()
{
    // Load data from model and populate view
    // Example: m_view->set_theme(m_model->getTheme());
}

void <ViewNameCamel>Controller::on_save_clicked()
{
    // Get values from view
    // Save via model
    // Show success message
    QMessageBox::information(m_view, tr("Success"), tr("Settings saved."));
}

void <ViewNameCamel>Controller::on_cancel_clicked()
{
    m_view->close();
}
```

### Step 7: Generate Model (if MVC requested)

Create `models/<view_name>_model.h`:

```cpp
#ifndef <VIEW_NAME_UPPER>_MODEL_H
#define <VIEW_NAME_UPPER>_MODEL_H

#include <QObject>
#include <QJsonObject>
#include <QString>
#include <QVariant>

class <ViewNameCamel>Model : public QObject
{
    Q_OBJECT

public:
    explicit <ViewNameCamel>Model(QObject *parent = nullptr);
    ~<ViewNameCamel>Model();

    // Getter methods
    QVariant get(const QString &key) const;
    QString getTheme() const;
    QString getLanguage() const;
    bool getAutoload() const;

    // Setter methods
    void set(const QString &key, const QVariant &value);
    void setTheme(const QString &theme);
    void setLanguage(const QString &language);
    void setAutoload(bool autoload);

    // Persistence
    void save();
    void load();

private:
    QString m_filePath;
    QJsonObject m_data;
    void create_defaults();
};

#endif // <VIEW_NAME_UPPER>_MODEL_H
```

Create `models/<view_name>_model.cpp`:

```cpp
#include "<view_name>_model.h"
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QDebug>

<ViewNameCamel>Model::<ViewNameCamel>Model(QObject *parent)
    : QObject(parent)
    , m_filePath("<view_name>.json")
{
    load();
}

<ViewNameCamel>Model::~<ViewNameCamel>Model()
{
}

void <ViewNameCamel>Model::load()
{
    QFile file(m_filePath);
    if (!file.exists()) {
        create_defaults();
        save();
        return;
    }

    if (!file.open(QIODevice::ReadOnly)) {
        qWarning() << "Could not open" << m_filePath;
        create_defaults();
        return;
    }

    QByteArray data = file.readAll();
    QJsonDocument doc = QJsonDocument::fromJson(data);
    m_data = doc.object();
    file.close();
}

void <ViewNameCamel>Model::save()
{
    QFile file(m_filePath);
    if (!file.open(QIODevice::WriteOnly)) {
        qWarning() << "Could not write to" << m_filePath;
        return;
    }

    QJsonDocument doc(m_data);
    file.write(doc.toJson());
    file.close();
}

QVariant <ViewNameCamel>Model::get(const QString &key) const
{
    return m_data.value(key).toVariant();
}

void <ViewNameCamel>Model::set(const QString &key, const QVariant &value)
{
    m_data[key] = QJsonValue::fromVariant(value);
}

QString <ViewNameCamel>Model::getTheme() const
{
    return m_data.value("theme").toString("light");
}

void <ViewNameCamel>Model::setTheme(const QString &theme)
{
    m_data["theme"] = theme;
}

// ... more getter/setter methods

void <ViewNameCamel>Model::create_defaults()
{
    m_data["theme"] = "light";
    m_data["language"] = "en";
    m_data["autoload"] = true;
}
```

### Step 8: Update CMakeLists.txt

Add all generated files to `CMakeLists.txt`:

```cmake
set(SOURCES
    # ... existing sources ...
    views/<view_name>_view.cpp
    views/<view_name>_view.h
    views/<view_name>_view.ui
    # ... if MVC ...
    controllers/<view_name>_controller.cpp
    controllers/<view_name>_controller.h
    models/<view_name>_model.cpp
    models/<view_name>_model.h
)
```

---

## Common Patterns

### Settings Dialog Pattern

**Input:** `create-view-agent settings --type=dialog --layout=form`

**Generates:**
- QDialog with QVBoxLayout
- QTabWidget with QFormLayout
- Fields: combobox_theme, combobox_language, checkbox_*
- QDialogButtonBox (Save | Cancel)

### Main Window Pattern

**Input:** `create-view-agent main-window --type=window`

**Generates:**
- QMainWindow
- menubar, toolbar_main, statusbar
- Central widget with QVBoxLayout

### Form Widget Pattern

**Input:** `create-view-agent connection-form --type=widget --layout=form`

**Generates:**
- QWidget (for embedding)
- QFormLayout with connection fields
- lineedit_*, combobox_*, checkbox_*

### Toolbar Widget Pattern

**Input:** `create-view-agent main-toolbar --type=widget --layout=horizontal`

**Generates:**
- QWidget with QHBoxLayout
- Margins: 6px, Spacing: 4px
- button_*, frame_separator, spacer

---

## Validation

After generation, verify:

- [ ] All files follow naming conventions (snake_case for widgets, PascalCase for classes)
- [ ] UI file opens in Qt Designer
- [ ] CMakeLists.txt includes all sources
- [ ] Signals/slots follow `on_<sender>_<signal>` pattern
- [ ] Widget names use `snake_case` with type prefix
- [ ] Layout structure matches view type
- [ ] Controller connects view signals properly (if MVC)
- [ ] Model handles JSON persistence (if MVC)
- [ ] Translation strings wrapped in `tr()`

---

## Integration Checklist

When adding a new view:

1. **Files created** in correct directories (`views/`, `controllers/`, `models/`)
2. **CMakeLists.txt updated** with new sources
3. **Controller instantiated** in main.cpp (if MVC)
4. **View connected** to controller signals
5. **Translation strings** wrapped in `tr()`
6. **Default values** loaded in constructor
7. **Error handling** for file I/O (if model)

---

## Examples

### Example 1: Simple Settings Dialog

**Command:**
```
/create-view-agent settings
```

**Generates:**
- `views/settings_view.h/cpp/ui` (QDialog with form)
- Basic save/cancel functionality
- Standard form layout

### Example 2: Main Window

**Command:**
```
/create-view-agent main-window --type=window
```

**Generates:**
- `views/main_window.h/cpp/ui` (QMainWindow)
- menubar, toolbar, statusbar structure
- Central widget with layout

### Example 3: Full MVC

**Command:**
```
/create-view-agent user-profile --mvc
```

**Generates:**
- `views/user_profile_view.h/cpp/ui`
- `controllers/user_profile_controller.h/cpp`
- `models/user_profile_model.h/cpp`
- Full MVC integration

### Example 4: Custom Layout

**Command:**
```
/create-view-agent dashboard --type=window --layout=grid --widgets=table,chart,status
```

**Generates:**
- `views/dashboard_view.h/cpp/ui` (QMainWindow)
- QGridLayout with specified widgets
- Custom widget structure

