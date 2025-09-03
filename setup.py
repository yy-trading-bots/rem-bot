from cx_Freeze import setup, Executable
import sys
import shutil
import os
import pathlib
import dateparser

sys.path.insert(0, os.path.abspath("src"))

base = None
executables = [Executable("src/main.py", base=base, target_name="rembot.exe")]

dateparser_pkg_dir = pathlib.Path(dateparser.__file__).parent
dateparser_data_dir = dateparser_pkg_dir / "data"

build_exe_options = {
    "packages": [
        "websockets",
        "talib",
        "requests",
        "urllib3",
        "dateparser",
        "dateparser.data",
        "dateparser.data.date_translation_data",
    ],
    "includes": [
        "websockets.legacy",
        "websockets.client",
        "websockets.server",
        "talib",
        "certifi",
        "requests",
        "urllib3",
        "dateparser.languages.loader",
        "dateparser.conf",
        "dateparser.date",
    ],
    "excludes": [],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": ["websockets", "talib", "dateparser"],
    "include_files": [
        ("src/settings.example.toml", "settings.toml"),
    ],
    "include_msvcr": True,
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
