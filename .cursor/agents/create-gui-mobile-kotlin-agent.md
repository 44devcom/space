# Kotlin Android GUI Agent

## Purpose
Generate an Android app in Kotlin using Jetpack Compose.

## Workflow
1. Load Kotlin GUI rules.
2. Generate Android project structure.
3. Create:
   - MainActivity.kt
   - Navigation host
   - Screens (Dashboard, Plan, Task, Logs, SSL & Certificates, etc.)
   - ViewModels with coroutines
   - Retrofit client
4. Integrate API calls:
   - plan list
   - plan detail
   - run plan
   - logs stream
   - SSL APIs:
     - GET /api/ssl/status
     - POST /api/ssl/enable
     - POST /api/ssl/renew
     - POST /api/ssl/reload-nginx
5. Generate SSL screen:
   - SSL & Certificates composable screen
   - SSL status display
   - Action buttons (Enable, Renew, Reload)
   - Error/success snackbars
6. Provide `build.gradle.kts` boilerplate.
7. Provide AndroidManifest.xml.

## Output
A ready-to-import Android Studio project.

