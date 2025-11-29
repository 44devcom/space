#!/usr/bin/env bash
set -euo pipefail

# Build and run script for FancyApp

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${SCRIPT_DIR}/build"
APP_NAME="FancyApp"
EXECUTABLE="${BUILD_DIR}/${APP_NAME}"

echo "Building FancyApp..."
echo "Source directory: ${SCRIPT_DIR}"
echo "Build directory: ${BUILD_DIR}"
echo ""

# Create build directory
mkdir -p "${BUILD_DIR}"
cd "${BUILD_DIR}"

# Run CMake if needed
if [ ! -f "CMakeCache.txt" ]; then
    echo "Running CMake..."
    cmake ..
fi

# Build
echo "Building..."
make -j$(nproc 2>/dev/null || echo 4)

# Check if build was successful
if [ ! -f "${EXECUTABLE}" ]; then
    echo "Error: Executable not found at ${EXECUTABLE}"
    exit 1
fi

echo ""
echo "✅ Build successful!"
echo ""
echo "Starting ${APP_NAME}..."
echo ""

# Run the application
"${EXECUTABLE}"

