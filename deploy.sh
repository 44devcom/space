#!/usr/bin/env bash
set -euo pipefail

# Deploy FancyApp to Android device

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${SCRIPT_DIR}/app"
BUILD_DIR="${APP_DIR}/build-android"
APK_DIR="${BUILD_DIR}/android-build/build/outputs/apk/release"
APK_NAME="android-build-release-unsigned.apk"
APK_PATH="${APK_DIR}/${APK_NAME}"
APP_NAME="FancyApp"
PACKAGE_NAME="org.qtproject.example.FancyApp"

echo "Deploying ${APP_NAME} to Android device..."
echo ""

# Check if adb is available
if ! command -v adb &> /dev/null; then
    echo "Error: adb not found. Please install Android SDK Platform Tools."
    echo "  Ubuntu/Debian: sudo apt-get install android-tools-adb"
    exit 1
fi

# Check if device is connected
DEVICES=$(adb devices | grep -v "List" | grep "device$" | wc -l)
if [ "$DEVICES" -eq 0 ]; then
    echo "Error: No Android device connected."
    echo "Please connect a device via USB and enable USB debugging."
    exit 1
fi

if [ "$DEVICES" -gt 1 ]; then
    echo "Warning: Multiple devices connected. Using first device."
fi

echo "✅ Android device detected"
echo ""

# Check if APK exists, if not, try to build it
if [ ! -f "${APK_PATH}" ]; then
    echo "APK not found at ${APK_PATH}"
    echo "Building Android APK..."
    echo ""
    
    cd "${BUILD_DIR}"
    
    # Check if CMake has been run
    if [ ! -f "CMakeCache.txt" ]; then
        echo "Error: Android build directory not configured."
        echo "Please build for Android first. Example:"
        echo "  cd ${BUILD_DIR}"
        echo "  cmake -DCMAKE_TOOLCHAIN_FILE=<Qt Android toolchain> ${APP_DIR}"
        exit 1
    fi
    
    # Build APK
    echo "Building APK..."
    make FancyApp_make_apk -j$(nproc 2>/dev/null || echo 4)
    
    if [ ! -f "${APK_PATH}" ]; then
        echo "Error: APK build failed. APK not found at ${APK_PATH}"
        exit 1
    fi
    
    echo "✅ APK built successfully"
    echo ""
fi

echo "APK found: ${APK_PATH}"
echo ""

# Uninstall existing app if present (optional, comment out if you want to keep data)
if adb shell pm list packages | grep -q "${PACKAGE_NAME}"; then
    echo "Uninstalling existing version..."
    adb uninstall "${PACKAGE_NAME}" || true
    echo ""
fi

# Install APK
echo "Installing APK to device..."
adb install -r "${APK_PATH}"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ APK installed successfully!"
    echo ""
    
    # Ask if user wants to launch the app
    read -p "Launch ${APP_NAME}? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Launching ${APP_NAME}..."
        adb shell am start -n "${PACKAGE_NAME}/.QtActivity" || \
        adb shell monkey -p "${PACKAGE_NAME}" -c android.intent.category.LAUNCHER 1
        echo "✅ App launched"
    fi
else
    echo ""
    echo "❌ Failed to install APK"
    exit 1
fi

