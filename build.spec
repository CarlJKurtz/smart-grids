# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
    ('assets/smart_grids-icon.png', 'assets'),
    ('assets/splashscreen.png', 'assets'),
    ]

a = Analysis(
    ['main.py'],
    datas=added_files,
    pathex=[],
    binaries=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='SmartGrids.app',
    icon='./assets/smart_grids-icon.png',
    bundle_identifier=None,
    version='1.3.0',
    info_plist={
        'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeName': 'grid',
                    'LSItemContentTypes': ['com.example.grid'],
                    'LSHandlerRank': 'Owner'
                    }
                ]
    }

)
