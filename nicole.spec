# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Añade la línea para incluir archivos y carpetas
a = Analysis(['nicole.py'],
             pathex=['C:\\ruta\\a\\tu\\proyecto'], # Reemplaza con la ruta de tu carpeta
             binaries=[],
             datas=[('brain_icon.ico', '.'),
                    ('brain_icon.png', '.'),
                    ('eye_closed.png', '.'),
                    ('eye_open.png', '.'),
                    ('help_icon.png', '.'),
                    ('INSTRUCCIONES.txt', '.'),
                    ('isrrootx1.pem', '.'),
                    ('License.txt', '.'),
                    ('n.py', '.'),
                    ('requirements.txt', '.'),
                    ('.env', '.')], 
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='nicole',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False, # Cambia a True si es una app de consola
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='nicole')