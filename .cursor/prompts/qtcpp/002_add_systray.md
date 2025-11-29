# 🖥️ Cursor AI Prompt – Systray Improvement  

You are an **expert C++ and Qt developer**.  
The base project is already implemented (UI, structure, naming conventions, File→Exit action).  
Now extend it with a **System Tray (QSystemTrayIcon)** based on the [QtWidgets Systray Example](https://doc.qt.io/qt-6/qtwidgets-desktop-systray-example.html).  

---

## 🔧 Requirements  

### 1. Add System Tray Support  

- Implement `QSystemTrayIcon` in **main.cpp**.  
- Use an icon (default Qt icon if none is available).  
- Add a **QMenu** to the tray icon with:  
  - `Show/Hide` → toggle main window visibility.  
  - `Exit` → trigger `action_exit`.  

### 2. Behavior  

- Left-click tray icon → toggle main window visibility.  
- When main window is closed, **hide to tray instead of quitting**.  
- Application quits only when:  
  - "Exit" action is triggered from menu, or  
  - `action_exit` from File → Exit is triggered.  

### 3. Integration  

- Do not modify naming conventions.  
- Reuse `action_exit` from UI menu.  
- Ensure signals and slots follow the rules (`on_<sender>_<signal>`).  
- Keep systray logic inside `app/controllers/systray_controller.cpp` and `systray_controller.h` (not in UI file).  

### 4. Verification  

- Launch app → verify tray icon is visible.  
- Close window → it should hide to tray.  
- File → Exit and tray menu Exit → app quits.  
- Show/Hide works from tray.  

---

👉 Deliver the **updated main.cpp** with systray integration.  
Keep the existing project layout and naming rules.  
