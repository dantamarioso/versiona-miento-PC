# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['nicole.py'],
    pathex=['C:\\Users\\SENA\\Downloads\\test\\Source'],
    binaries=[],
    datas=[
        ('brain_icon.ico', '.'),
        ('brain_icon.png', '.'),
        ('License.txt', '.'),
        ('.env', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='nicole',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Cambia a True si es una app de consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='brain_icon.ico',  # Usa el ícono para el ejecutable
)