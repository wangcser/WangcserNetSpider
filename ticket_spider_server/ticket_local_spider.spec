# -*- mode: python -*-

block_cipher = None


a = Analysis(['ticket_local_spider.py'],
             pathex=['E:\\02 Python\\01 crawl\\ticket_spider_server'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ticket_local_spider',
          debug=False,
          strip=False,
          upx=True,
          console=True )
