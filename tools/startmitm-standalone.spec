# -*- mode: python ; coding: utf-8 -*-
from zipfile import ZipFile
from os.path import basename as n
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import PYZ, EXE, COLLECT

from PyInstaller.utils.hooks import collect_data_files


startmitm_as = Analysis(
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

startmitm = EXE(
    PYZ(startmitm_as.pure, startmitm_as.zipped_data),
    startmitm_as.scripts,
    startmitm_as.binaries,
    startmitm_as.zipfiles,
    startmitm_as.datas,
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

mitmweb_as = Analysis(
    ["mitmweb.py"],
    pathex=[],
    binaries=[],
    datas=collect_data_files("mitmproxy"),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    excludes=["tcl", "tk", "tkinter"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)

mitmweb = EXE(
    PYZ(mitmweb_as.pure, mitmweb_as.zipped_data),
    mitmweb_as.scripts,
    mitmweb_as.binaries,
    mitmweb_as.zipfiles,
    mitmweb_as.datas,
    [],
    name="mitmweb",
    icon="NONE",
    debug=False,
    bootloader_ignore_signals=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
)

with ZipFile("startmitm-standalone.zip", "w") as f:
    f.write(startmitm.name, n(startmitm.name))
    f.write(mitmweb.name, n(mitmweb.name))
