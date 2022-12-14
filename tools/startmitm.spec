# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import PYZ, EXE

from PyInstaller.utils.hooks import collect_data_files


a = Analysis(
    ["startmitm.py"],
    pathex=[],
    binaries=[],
    datas=collect_data_files("lamda"),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    excludes=["tcl", "tk", "tkinter"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)

exe = EXE(
    PYZ(a.pure, a.zipped_data),
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="startmitm",
    icon=["startmitm.ico"],
    debug=False,
    bootloader_ignore_signals=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
)