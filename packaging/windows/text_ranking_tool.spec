# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=['../../src'],  # ← Go back two levels to find src
    binaries=[],
    datas=[
        ('../../src/text_ranking_tool/config', 'text_ranking_tool/config'),      # ← Back to project root
        ('../../src/text_ranking_tool/algorithms', 'text_ranking_tool/algorithms'), # ← Back to project root
        ('../../mock_installer_config.json', '.'),                              # ← Back to project root
    ],
    hiddenimports=[
        'pandas', 
        'numpy', 
        'rich', 
        'scipy.stats',
        'text_ranking_tool',
        'text_ranking_tool.main',
        'text_ranking_tool.algorithms.recursive_median.recursive_median_core',
        'text_ranking_tool.algorithms.tournament.tournament_core',
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

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TextRankingTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # ← Also changed to False for better performance as discussed
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
