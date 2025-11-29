# Fancy Main Window

A Qt C++ application featuring:
- 3D animated background (rotating wireframe cube)
- Animated loader widget
- Main menu bar
- Fixed resolution: 1080x480

## Build Instructions

### Quick Build and Run

**Build and automatically run:**
```bash
cd app
./build.sh --run
```

**Build and prompt to run:**
```bash
cd app
./build.sh
```

**Clean build (removes build directory first):**
```bash
cd app
./build.sh --clean
```

**Show help:**
```bash
cd app
./build.sh --help
```

### Build Script Options

- `--run` or `-r`: Automatically run the application after building
- `--clean` or `-c`: Clean build directory before building
- `--help` or `-h`: Show help message

### Manual Build

```bash
cd app
mkdir -p build
cd build
cmake ..
make
```

### Run

```bash
cd app/build
./FancyApp
```

Or from the app directory:

```bash
cd app
./build/FancyApp
```

## Requirements

- Qt6 (Widgets, Core, OpenGL, OpenGLWidgets)
- CMake 3.16+
- C++17 compiler
- OpenGL support

## Project Structure

```
app/
├── CMakeLists.txt
├── main.cpp
├── build.sh
├── views/
│   ├── fancy_main_window.h
│   ├── fancy_main_window.cpp
│   ├── fancy_main_window.ui
│   ├── background_3d_widget.h
│   ├── background_3d_widget.cpp
│   ├── loader_widget.h
│   └── loader_widget.cpp
└── build/          (generated)
```

## Features

- **3D Background**: Rotating wireframe cube using QOpenGLWidget
- **Loader Animation**: Smooth rotating circular loader
- **Menu Bar**: File, Edit, Help menus with actions
- **Fixed Size**: Window locked at 1080x480 resolution

