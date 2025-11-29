---
name: create-view
description: "Quickly generate a basic Qt C++ view component (header, implementation, UI file)."
inputSchema:
  type: string
stdin: true
---

# Create View Command (Qt C++)

## Purpose

Quickly generate a basic Qt C++ view with minimal configuration. For advanced features, use `create-view-agent`.

This command creates:
- `views/<view_name>_view.h`
- `views/<view_name>_view.cpp`
- `views/<view_name>_view.ui`
- Updates `CMakeLists.txt`

---

## Usage

```
/create-view <view_name>
```

**Examples:**
- `/create-view settings` → creates `settings_view.h/cpp/ui`
- `/create-view user-profile` → creates `user_profile_view.h/cpp/ui`
- `/create-view connection-form` → creates `connection_form_view.h/cpp/ui`

---

## Default Behavior

The command generates a **QDialog** with:
- **Layout:** QVBoxLayout → QFormLayout
- **Buttons:** QDialogButtonBox (Save | Cancel)
- **Minimum size:** 320x220
- **Basic structure:** Ready for form fields

---

## Generated Files

### Header File (`views/<view_name>_view.h`)

```cpp
#ifndef <VIEW_NAME_UPPER>_VIEW_H
#define <VIEW_NAME_UPPER>_VIEW_H

#include <QDialog>
#include "ui_<view_name>_view.h"

class <ViewNameCamel>View : public QDialog
{
    Q_OBJECT

public:
    explicit <ViewNameCamel>View(QWidget *parent = nullptr);
    ~<ViewNameCamel>View();

signals:
    void signal_save_<view_name>();
    void signal_cancel_<view_name>();

private slots:
    void on_button_save_clicked();
    void on_button_cancel_clicked();

private:
    Ui::<ViewNameCamel>View *ui;
};

#endif // <VIEW_NAME_UPPER>_VIEW_H
```

### Implementation File (`views/<view_name>_view.cpp`)

```cpp
#include "<view_name>_view.h"

<ViewNameCamel>View::<ViewNameCamel>View(QWidget *parent)
    : QDialog(parent)
    , ui(new Ui::<ViewNameCamel>View)
{
    ui->setupUi(this);
}

<ViewNameCamel>View::~<ViewNameCamel>View()
{
    delete ui;
}

void <ViewNameCamel>View::on_button_save_clicked()
{
    emit signal_save_<view_name>();
    accept();
}

void <ViewNameCamel>View::on_button_cancel_clicked()
{
    emit signal_cancel_<view_name>();
    reject();
}
```

### UI File (`views/<view_name>_view.ui`)

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
      <!-- Add form fields here -->
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

---

## Naming Conventions

- **View name:** Converted to snake_case (e.g., "user-profile" → "user_profile")
- **Class name:** PascalCase (e.g., "user_profile" → "UserProfileView")
- **Header guard:** UPPER_SNAKE_CASE (e.g., "USER_PROFILE_VIEW_H")
- **UI object name:** snake_case with suffix (e.g., "user_profile_dialog")

---

## CMakeLists.txt Update

Automatically adds to `CMakeLists.txt`:

```cmake
set(SOURCES
    # ... existing sources ...
    views/<view_name>_view.cpp
    views/<view_name>_view.h
    views/<view_name>_view.ui
)
```

---

## Workflow

1. **Parse view name** from input
2. **Convert naming** (snake_case, PascalCase, etc.)
3. **Generate header file** with basic structure
4. **Generate implementation file** with constructor/destructor and slots
5. **Generate UI file** with QDialog and QFormLayout
6. **Update CMakeLists.txt** with new sources
7. **Return success message** with file paths

---

## When to Use

Use `create-view` for:
- ✅ Quick dialog creation
- ✅ Simple forms
- ✅ Basic views without complex requirements
- ✅ Rapid prototyping

Use `create-view-agent` for:
- ⚙️ Custom view types (window, widget, dock)
- ⚙️ Custom layouts (grid, tabs, horizontal)
- ⚙️ MVC pattern (controller + model)
- ⚙️ Complex widget requirements
- ⚙️ Advanced customization

---

## Example Output

**Input:**
```
/create-view settings
```

**Output:**
```
✅ Created view files:
   - views/settings_view.h
   - views/settings_view.cpp
   - views/settings_view.ui
   - Updated CMakeLists.txt

Ready to customize! Add form fields to the UI file.
```

---

## Next Steps

After generation:
1. Open `views/<view_name>_view.ui` in Qt Designer
2. Add form fields (lineedit, combobox, checkbox, etc.)
3. Follow widget naming: `snake_case` with type prefix
4. Add getter methods to header if needed
5. Connect signals in your controller

---

## Validation

The command ensures:
- ✅ View name is valid (no spaces, special chars)
- ✅ Files don't already exist (warns if they do)
- ✅ CMakeLists.txt is updated correctly
- ✅ Naming conventions are followed

