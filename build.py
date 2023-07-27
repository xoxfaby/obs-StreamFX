# Copyright (C) 2023 XoXFaby

import requests
import os
import subprocess
import traceback
import shutil
import zipfile

def clone_repository(github_url, subfolder_name):
    folderpath = os.path.join("temp", subfolder_name)
    subprocess.run(['git', 'clone', '--recursive',
                   github_url, folderpath], check=True)
    

def build(*paths):
    llvmpath = ""
    obssourcepath = os.path.abspath("temp/obs-streamfx/third-party/obs-studio")
    obsbuildpath = os.path.abspath("temp/obs-streamfx/build/libobs")
    obsinstallpath = os.path.abspath("temp/obs-streamfx/build/libobs/install")

    fxsourcepath = os.path.abspath("temp/obs-streamfx/")
    fxbuildpath = os.path.abspath("temp/obs-streamfx/build/fx")
    fxinstallpath = os.path.abspath("temp/obs-streamfx/build/fx/install")

    packagebuildpath = os.path.abspath("temp/obs-streamfx/build/package")
    
    #cmake -S "$ROOT/third-party/obs-studio" -B "$ROOT/build/obs" -G "Visual Studio 17 2022" -A x64 -DCMAKE_SYSTEM_VERSION="10.0.20348.0" -DCMAKE_BUILD_TYPE="Release" -DCMAKE_INSTALL_PREFIX="$ROOT/build/obs/install" -DENABLE_PLUGINS=OFF -DENABLE_UI=OFF -DENABLE_SCRIPTING=OFF -DCMAKE_PREFIX_PATH="$OBS;$OBS_QT6"
    subprocess.run(['cmake', 
                    '-S', obssourcepath,
                    '-B', obsbuildpath,
                    '-G', 'Visual Studio 17 2022',
                    '-A', 'x64',
                    '-DCMAKE_SYSTEM_VERSION="10.0.20348.0"',
                    '-DCMAKE_BUILD_TYPE="Release"',
                    f'-DCMAKE_INSTALL_PREFIX={obsinstallpath}',
                    '-DENABLE_PLUGINS=OFF',
                    '-DENABLE_UI=OFF',
                    '-DENABLE_SCRIPTING=OFF',
                    f'-DCMAKE_PREFIX_PATH={";".join(paths)}"',
                    "-Wno-dev"
                   ])
    
    #cmake --build "$ROOT/build/obs" --config Release --target obs-frontend-api
    subprocess.run(['cmake', '--build', obsbuildpath, '--config Release', '--target obs-frontend-api'])
                    
    #cmake --install "$ROOT/build/obs" --config Release --component obs_libraries
    subprocess.run(['cmake', '--install', obsbuildpath,
                   '--config Release', '--component obs_libraries'])
    
    #cmake -S "$ROOT" -B "$ROOT/build/ci" -G "Visual Studio 17 2022" -A x64 -DCMAKE_SYSTEM_VERSION="10.0.20348.0" -DCMAKE_BUILD_TYPE="Release" -DCMAKE_INSTALL_PREFIX="$ROOT/build/ci/install" 
    #-DPACKAGE_NAME="streamfx-windows" -DPACKAGE_PREFIX="$ROOT/build/package" 
    # -DENABLE_CLANG=TRUE -DCLANG_PATH="$LLVM" -DENABLE_PROFILING=ON -Dlibobs_DIR="$ROOT/build/obs/install"
    #  -DQt_DIR="$OBS_QT6" -DFFmpeg_DIR="$OBS" -DCURL_DIR="$OBS". $LLVM
    subprocess.run(['cmake',
                    '-S', fxsourcepath,
                    '-B', fxbuildpath,
                    '-G', 'Visual Studio 17 2022',
                    '-A', 'x64',
                    '-DCMAKE_SYSTEM_VERSION="10.0.20348.0"',
                    '-DCMAKE_BUILD_TYPE="Release"',
                    f'-DCMAKE_INSTALL_PREFIX={fxinstallpath}',
                    '-DPACKAGE_NAME="streamfx-windows"',
                    f'-DPACKAGE_PREFIX={packagebuildpath}',
                    '-DENABLE_CLANG=TRUE',
                    #f'-DCLANG_PATH={llvmpath}',
                    "-DENABLE_PROFILING=ON",
                    f"-Dlibobs_DIR={obsinstallpath}",
                    f"-DFFmpeg_DIR={paths[0]}",
                    f"-DCURL_DIR={paths[0]}",
                    f"-DQt_DIR={paths[1]}",
                    "-Wno-dev"
                    ])

    #cmake --build "$ROOT/build/ci" --config RelWithDebInfo --target install
    subprocess.run(['cmake', '--build', fxbuildpath,
                    '--config RelWithDebInfo', '--target install'])
    
    inno = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    installerpath = os.path.abspath("temp/obs-streamfx/build/fx/installer.iss")
    
    #& "$INNO" /V10 "$ROOT\build\ci\"
    subprocess.run([inno, "/V10", installerpath])

def download_assets(github_user, github_repo, release_tag=None, filename=None, filenames=None):
    if release_tag:
        api_url = f'https://api.github.com/repos/{github_user}/{github_repo}/releases/tags/{release_tag}'
    else:
        api_url = f'https://api.github.com/repos/{github_user}/{github_repo}/releases/latest'
    response = requests.get(api_url)
    if response.status_code == 200:
        release_info = response.json()
        tag_name = release_info['tag_name']
        fileurls = [] 
        formatted_filenames = []
        if filename:
            formatted_filenames.append(filename.format(tag=tag_name))
        if filenames:
            for filename in filenames:
                formatted_filenames.append(filename.format(tag=tag_name))

        for asset in release_info['assets']:
            if asset['name'] in formatted_filenames:
                fileurls.append(
                    (asset['name'], asset['browser_download_url']))

        for filename, asset_url in fileurls:
            filepath = os.path.join("temp", filename)
            if (os.path.exists(filepath)):
                print(f"Skipping {filename} because it already exists.")
            else:
                with open(filepath, 'wb') as file:
                    print(f"Downloading {filename}")
                    fileresponse = requests.get(asset_url)
                    fileresponse.raise_for_status()
                    file.write(fileresponse.content)
                if filename.endswith(".zip"):
                    with zipfile.ZipFile(os.path.abspath(
                            filepath), 'r') as zip_ref:
                        zip_ref.extractall(filepath[:-4])
        return tag_name
    else:
        response.raise_for_status()


if __name__ == "__main__":
    github_url = 'https://github.com/xoxfaby/obs-StreamFX.git'
    subfolder_name = 'obs-streamfx'

    try:
        if(os.path.exists("temp")):
            print("Clearing old temp folder.")
            #shutil.rmtree("temp")
        #realos.makedirs("temp")

        try:
            clone_repository(github_url, subfolder_name)
        except: pass
        tag = download_assets("obsproject", "obs-deps", release_tag="2023-04-12",
                              filenames=["windows-deps-{tag}-x64.zip",
                                                        "windows-deps-qt6-{tag}-x64-Debug.zip"])
        
        depspath = os.path.abspath( f"temp/windows-deps-{tag}-x64")
        qtpath = os.path.abspath(f"temp/windows-deps-qt6-{tag}-x64-Debug")

        build(depspath, qtpath)

        #shutil.rmtree("temp")


    except Exception as e:
        traceback.print_exc()
