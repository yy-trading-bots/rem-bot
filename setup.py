from cx_Freeze import setup, Executable
import sys
import shutil
import os

sys.path.insert(0, os.path.abspath("src"))

base = None

executables = [Executable("src/main.py", base=base, target_name="rembot.exe")]


def prepare_data_files(build_dir):
    src_example = os.path.join("src", "settings.example.toml")
    target = os.path.join(build_dir, "settings.toml")
    if os.path.exists(src_example):
        shutil.copy2(src_example, target)


build_exe_options = {
    "packages": [
        "websockets",
        "talib",
        "requests",
        "urllib3",
    ],
    "includes": [
        "websockets.legacy",
        "websockets.client",
        "websockets.server",
        "talib",
        "certifi",
        "requests",
        "urllib3",
    ],
    "excludes": [],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": ["dateparser", "websockets", "talib"],
    "include_files": [("src/settings.example.toml", "settings.toml")],
}

build_dir = "build"
if os.path.isdir(build_dir):
    shutil.rmtree(build_dir)

setup(
    name="rem-bot",
    version="0.1",
    description="rem-bot packaged with cx_Freeze",
    options={"build_exe": build_exe_options},
    executables=executables,
    script_args=["build"],
)

if __name__ == "__main__":
    build_root = None
    if os.path.isdir("build"):
        for entry in os.listdir("build"):
            if entry.startswith("exe"):
                build_root = os.path.join("build", entry)
                break
    if build_root:
        prepare_data_files(build_root)
