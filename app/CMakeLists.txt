cmake_minimum_required(VERSION 3.16)
project(FancyApp VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets Core OpenGL OpenGLWidgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets Core OpenGL OpenGLWidgets)

set(SOURCES
    main.cpp
    views/fancy_main_window.cpp
    views/fancy_main_window.h
    views/fancy_main_window.ui
    views/background_3d_widget.cpp
    views/background_3d_widget.h
    views/loader_widget.cpp
    views/loader_widget.h
)

qt_add_executable(FancyApp ${SOURCES})
target_link_libraries(FancyApp PRIVATE 
    Qt${QT_VERSION_MAJOR}::Widgets 
    Qt${QT_VERSION_MAJOR}::Core
    Qt${QT_VERSION_MAJOR}::OpenGL
    Qt${QT_VERSION_MAJOR}::OpenGLWidgets
)

