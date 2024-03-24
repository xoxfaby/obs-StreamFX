# Building
This document intends to guide you through the process of building StreamFX. It requires understanding of the tools used, and may require you to learn tools yourself before you can advance further in the guide. It is intended to be used by developers and contributors.

## Required Pre-Requisites / Dependencies
- [Git](https://git-scm.com/)
    - **Debian / Ubuntu**
      `sudo apt install git`
- [CMake](https://cmake.org/) 3.20 (or newer)
    - **Debian / Ubuntu**
      `sudo apt install cmake`
- A compatible Compiler:
    - **Windows**
      [Visual Studio](https://visualstudio.microsoft.com/vs/) 2022 or newer
    - **MacOS**
      Xcode 11.x (or newer) for x86_64
      Xcode 12.x (or newer) for arm64
    - **Debian / Ubuntu**
        - Essential Build Tools:
          `sudo apt install build-essential pkg-config checkinstall make ninja-build`
        - One of:
            - GCC 12 (or newer)
              `sudo apt install gcc-12 g++-12`
            - [LLVM](https://releases.llvm.org/) Clang 14 (or newer)
              `sudo bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"`
        - One of:
            - ld or gold
              `sudo apt install binutils`
            - [LLVM](https://releases.llvm.org/) lld
              `sudo bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"`
            - [mold](https://github.com/rui314/mold)
              `sudo apt install mold`
- [Homebrew](https://brew.sh/) (Required, for **MacOS** only)

## Building Bundled
The main method to build StreamFX is to first set up an OBS Studio copy and then integrate the StreamFX repository into it. It is recommended to first [Uninstall](Uninstallation) any currently installed versions of StreamFX to prevent conflicts, as OBS Studio may still attempt to load installed versions of StreamFX in addition to the one in the bundled build.

1. Clone StreamFX recursively with submodules into a directory of your choice.
  `git clone --recurse-submodules 'https://github.com/Xaymar/obs-StreamFX.git' .`
2. Navigate to the `third-party/obs-studio/UI/frontend-plugins` directory.
3. Add a symbolic link back to the StreamFX source code here.
    - **Windows (Powershell)**
      `New-Item -Path streamfx -ItemType SymbolicLink - Value ..\..\..\..\`
    - **Windows (Batch)**
      `mklink /J streamfx ..\..\..\..\`
    - **Debian / Ubuntu**
      `ln -s ../../../../ streamfx`
4. Open `CMakeLists.txt` in the same directory and append `add_subdirectory(streamfx)` to the end.
5. Navigate back to `third-party/obs-studio` and follow the follow the [OBS Studio build guide](https://obsproject.com/wiki/install-instructions). A short form of it is below.
    1. Check available CMake presets by running:
      `cmake --list-presets`
    2. Configure for one of the available presets with the command:
        - **Windows**
          `cmake --preset windows-x64`
        - **MacOS**
          `cmake --preset macos`
        - **Debian / Ubuntu (x86)**
          `cmake --preset linux-x86_64`
        - **Debian / Ubuntu (ARM)**
          `cmake --preset linux-aarch`
    3. Open the generated IDE file of your choice and start coding.
6. Done. StreamFX is now part of the build.

## Building Standalone
This method is primarily designed for Continuous Integration and is only used there, and as such requires a significantly more in depth experience with all used tools and projects. You are entirely on your own if you are so daring to choose this method. Here be dragons and stuff.

### Install Prerequisites / Dependencies
- [Qt](https://www.qt.io/) 6:
    - **Windows**  
      Handled by libobs.
	- **MacOS**  
	  Handled by libobs and the build script.
    - **Debian / Ubuntu:**  
      `sudo apt install qt6-base-dev qt6-base-private-dev qt6-image-formats-plugins qt6-wayland libqt6svg6-dev libglx-dev libgl1-mesa-dev`
- [CURL](https://curl.se/):
    - **Windows**  
      Handled by libobs.
	- **MacOS**  
	  Handled by libobs.
    - **Debian / Ubuntu:**  
      `sudo apt install curl libcurl4-openssl-dev`
- [FFmpeg](https://ffmpeg.org/) (Optional, for FFmpeg component only):
    - **Windows**  
      Handled by libobs.
	- **MacOS**  
	  Handled by libobs.
    - **Debian / Ubuntu**  
      `sudo apt install libavcodec-dev libavdevice-dev libavfilter-dev libavformat-dev libavutil-dev libswresample-dev libswscale-dev`
- [LLVM](https://releases.llvm.org/) (Optional, for clang-format and clang-tidy integration only):
	- **Windows**  
	  Install using the Windows installer.
	- **MacOS**  
	  Install using the MacOS installer, though usually not needed.
    - **Debian / Ubuntu**  
      `sudo bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)" all`
- [InnoSetup](https://jrsoftware.org/isinfo.php) (Optional, for **Windows** installer only)

### Steps
1. Open a `git` capable bash shell in your projects directory. (On Windows, git bash is enough).
2. Clone the project:  
  `git clone https://github.com/Xaymar/obs-StreamFX.git streamfx`
3. Install some required prerequisites:  
  `./tools/build.sh prerequisites`
4. Update submodules:  
  `./tools/build.sh fetch`
5. Apply patches:  
  `./tools/build.sh patch`
6. Build libOBS:  
  `./tools/build.sh libobs`
7. Build StreamFX:  
  `./tools/build.sh build`
8. Done.

It is still possible to build using cmake-gui, however it is not recommended anymore.

## CMake Options
The project is intended to be versatile and configurable, so we offer almost everything to be configured on a silver platter directly in CMake (if possible). If StreamFX detects that it is being built together with other projects, it will automatically prefix all options with `StreamFX_` to prevent collisions.

### Generic
- `GIT` (not prefixed)
  Path to the `git` binary on your system, for use with features that require git during configuration and generation.
- `VERSION`
  Set or override the version of the project with a custom one. Allowed formats are: SemVer 2.0.0, CMake.

### Code
- `ENABLE_CLANG`
  Enable integration of `clang-format` and `clang-tidy`
- `CLANG_PATH` (not prefixed, only with `ENABLE_CLANG`)
  Path to the `clang` installation containing `clang-format` and `clang-tidy`. Only used as a hint.
- `CLANG_FORMAT_PATH` and `CLANG_TIDY_PATH` (not prefixed)
  Path to `clang-format` and `clang-tidy` that will be used.

### Dependencies
- `LibObs_DIR`
  Path to the obs-studio libraries.
- `Qt5_DIR`, `Qt6_DIR` or `Qt_DIR` (autodetect)
  Path to Qt5 (OBS Studio 27.x and lower) or Qt6 (OBS Studio 28.x and higher).
- `FFmpeg_DIR`
  Path to compatible FFmpeg libraries and headers.
- `CURL_DIR`
  Path to compatible CURL libraries and headers.
- `AOM_DIR`
  Path to compatible AOM libraries and headers.

### Compiling
- `ENABLE_FASTMATH`
  Enable fast math optimizations if the compiler supports them. This trades precision for performance, and is usually good enough anyway.
- `ENABLE_LTO`
  Enable link time optimization for faster binaries in exchange for longer build times.
- `ENABLE_PROFILING`
  Enable CPU and GPU profiling code, this option reduces performance drastically.
- `TARGET_*`
  Specify which architecture target the generated binaries will use.

### Components
- `COMPONENT_<NAME>`
  Enable the component by the given name.

### Installing & Packaging
These options are only available in CI-Style mode.

- `CMAKE_INSTALL_PREFIX`
  The path in which installed content should be placed when building the `install` target.
- `STRUCTURE_PACKAGEMANAGER`
  If enabled will install files in a layout compatible with package managers.
- `STRUCTURE_UNIFIED`
  Enable to install files in a layout compatible with an OBS Studio plugin manager.
- `PACKAGE_NAME`
  The name of the packaged archive, excluding the prefix, suffix and extension.
- `PACKAGE_PREFIX`
  The path in which the packages should be placed.
- `PACKAGE_SUFFIX`
  The suffix to attach to the name, before the file extension. If left blank will attach the current version string to the package.
- `STRUCTURE_UNIFIED`
  Enable to replace the PACKAGE_ZIP target with a target that generates a single `.obs` file instead.

</details>
