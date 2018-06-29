# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\HugoConstantinopolos\\Documents\\GitHub\\Simple_Chat\\udp_simpleChat\\client.py'],
             pathex=['C:\\Users\\HugoConstantinopolos\\AppData\\Local\\Programs\\Python\\Python36-32\\Scripts'],
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
          name='client',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
