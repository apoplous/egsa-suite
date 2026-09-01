# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = (
    collect_submodules("ezdxf")
    + collect_submodules("pyproj")
    + [
        "hatt_coefficients",
        "kml.current_point",
        "kml.fly_to",
        "kml.network_link",
        "kml.polygon",
        "kml.saved_points",
        "services.file_service",
        "services.google_earth_service",
        "services.http_server",
        "utils.platform_utils",
    ]
)

datas = [
    ("assets", "assets"),
]
datas += collect_data_files("pyproj")

a = Analysis(
    ["geotoolsgr.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="EGSA_Suite",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version="version_info.txt",
)
