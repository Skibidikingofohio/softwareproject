# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mainapp\\flashcards.py'],
    pathex=[],
    binaries=[],
    datas=[('mainapp/flashcards.json', 'mainapp'), ('mainapp/stats.json', 'mainapp'), ('mainapp/quiz.py', 'mainapp'), ('mainapp/speak.py', 'mainapp'), ('mainapp/ui.py', 'mainapp')],
    hiddenimports=[],
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
    name='flashcards',
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
