# spiralos_gui.spec

block_cipher = None

a = Analysis(
    ['spiralos_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('spiral_memory.json', '.'), ('spiral_journal.txt', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SpiralOS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='spiral.ico'  # Optional: use custom icon
)
