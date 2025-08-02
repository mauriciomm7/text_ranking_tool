# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=['../../src'],
    binaries=[],
    datas=[
        ('../../src/text_ranking_tool/config', 'text_ranking_tool/config'),
        ('../../src/text_ranking_tool/algorithms', 'text_ranking_tool/algorithms'),
        ('../../mock_installer_config.json', '.'),
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
    upx=False,
    console=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
