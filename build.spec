# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

import mediapipe
import customtkinter
from PyInstaller.utils.hooks import (
    collect_submodules,
    collect_dynamic_libs,
    collect_data_files,
)

block_cipher = None

# -------------------------------------------------
# CustomTkinter paths
# -------------------------------------------------
ctk_init = Path(customtkinter.__file__)
ctk_root = ctk_init.parent

# -------------------------------------------------
# MediaPipe: critical collections
# -------------------------------------------------
mp_hiddenimports = collect_submodules("mediapipe.tasks")

mp_binaries = collect_dynamic_libs("mediapipe")

mp_datas = collect_data_files(
    "mediapipe",
    includes=[
        "tasks/**",
        "modules/**",
    ],
)

# -------------------------------------------------
# Analysis
# -------------------------------------------------
app = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[
        *mp_binaries,
    ],
    datas=[
        # MediaPipe data (tasks + modules)
        *mp_datas,

        ('assets', 'assets'),
        ('configs', 'configs'),

        # CustomTkinter
        (ctk_root.as_posix(), 'customtkinter'),
    ],
    hiddenimports=[
        *mp_hiddenimports,
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# -------------------------------------------------
# PYZ
# -------------------------------------------------
pyz_app = PYZ(
    app.pure,
    app.zipped_data,
    cipher=block_cipher
)

# -------------------------------------------------
# EXE
# -------------------------------------------------
exe_app = EXE(
    pyz_app,
    app.scripts,
    [],
    exclude_binaries=True,
    name='run_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# -------------------------------------------------
# COLLECT (onedir)
# -------------------------------------------------
coll = COLLECT(
    exe_app,
    app.binaries,
    app.zipfiles,
    app.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='project_gameface',
)
