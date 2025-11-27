# PySide6 Desktop GUI Agent

## Purpose
Generate a PySide6 desktop application following rules in:
`.cursor/rules/create-gui-desktop-pyside6.mdc`.

## Inputs
Natural language description of:
- Modules wanted (dashboard, logs, plan viewer, etc.)
- Required components
- Required screens
- Integration features

## Outputs
- A complete folder structure under `gui/desktop/pyside6`
- Ready-to-run PySide6 application (`python main.py`)

## Workflow
1. Load PySide6 rules.
2. Parse the request → identify screens/components.
3. Scaffold directory structure.
4. Generate:
   - main.py
   - app.py
   - ui/main_window.py
   - components
   - services
5. Wire up navigation.
6. Integrate:
   - Plan loader
   - Task viewer
   - Mermaid WebView renderer
   - Parallel executor monitor
   - SSL Manager widget/dock
   - Nginx SSL config editor dialog
7. Generate SSL components:
   - ui/components/ssl_manager_widget.py (or similar)
   - ui/components/nginx_config_editor_dialog.py
   - API client methods for SSL endpoints
8. Provide a README with run instructions.

## Constraints
- Code must be runnable without modification.
- Avoid blocking GUI thread.
- Must use QThread or asyncio to run tasks.

