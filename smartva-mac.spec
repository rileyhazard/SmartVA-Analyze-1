# -*- mode: python -*-
a = Analysis(['app.py'],
             hiddenimports=['wx'],
             hookspath=['pkg/hooks'],
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='SmartVA',
          debug=False,
          strip=None,
          upx=False,
          console=True,
          icon='pkg/icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               [('res/logo.png', 'smartva/res/logo.png', 'DATA')],
               [('res/about.html', 'smartva/res/about.html', 'DATA')],
               [('res/documentation.htm', 'smartva/res/documentation.htm', 'DATA')],
               [('res/documentation_files/header.htm', 'smartva/res/documentation_files/header.htm','DATA')],
               [('res/documentation_files/item0001.xml', 'smartva/res/documentation_files/item0001.xml','DATA')],
               [('res/documentation_files/props0002.xml', 'smartva/res/documentation_files/props0002.xml','DATA')],
               [('res/documentation_files/themedata.xml', 'smartva/res/documentation_files/themedata.xml','DATA')],
               [('res/documentation_files/image001.png', 'smartva/res/documentation_files/image001.png', 'DATA')],
               [('res/documentation_files/image002.png', 'smartva/res/documentation_files/image002.png', 'DATA')],
               [('res/documentation_files/image003.png', 'smartva/res/documentation_files/image003.png', 'DATA')],
               [('res/documentation_files/image004.png', 'smartva/res/documentation_files/image004.png', 'DATA')],
               [('res/documentation_files/image005.png', 'smartva/res/documentation_files/image005.png', 'DATA')],
               [('res/documentation_files/image006.png', 'smartva/res/documentation_files/image006.png', 'DATA')],
               [('res/documentation_files/image007.png', 'smartva/res/documentation_files/image007.png', 'DATA')],
               [('res/documentation_files/image008.png', 'smartva/res/documentation_files/image008.png', 'DATA')],
               [('res/documentation_files/image009.png', 'smartva/res/documentation_files/image009.png', 'DATA')],
               [('res/documentation_files/image010.png', 'smartva/res/documentation_files/image010.png', 'DATA')],
               [('res/documentation_files/image011.png', 'smartva/res/documentation_files/image011.png', 'DATA')],
               [('res/documentation_files/image012.png', 'smartva/res/documentation_files/image012.png', 'DATA')],
               [('res/documentation_files/image013.png', 'smartva/res/documentation_files/image013.png', 'DATA')],
               [('res/documentation_files/image014.png', 'smartva/res/documentation_files/image014.png', 'DATA')],
               [('res/documentation_files/image015.png', 'smartva/res/documentation_files/image015.png', 'DATA')],
               [('res/documentation_files/image016.png', 'smartva/res/documentation_files/image016.png', 'DATA')],
               [('res/documentation_files/image017.png', 'smartva/res/documentation_files/image017.png', 'DATA')],
               [('res/documentation_files/image018.png', 'smartva/res/documentation_files/image018.png', 'DATA')],
               [('res/documentation_files/image019.png', 'smartva/res/documentation_files/image019.png', 'DATA')],
               [('res/documentation_files/image020.png', 'smartva/res/documentation_files/image020.png', 'DATA')],
               [('tariffs-adult.csv', 'smartva/tariffs-adult.csv', 'DATA')],
               [('tariffs-child.csv', 'smartva/tariffs-child.csv', 'DATA')],
               [('tariffs-neonate.csv', 'smartva/tariffs-neonate.csv', 'DATA')],
               [('validated-adult.csv', 'smartva/validated-adult.csv', 'DATA')],
               [('validated-child.csv', 'smartva/validated-child.csv', 'DATA')],
               [('validated-neonate.csv', 'smartva/validated-neonate.csv', 'DATA')],
               [('adult_undetermined_weights-hce0.csv', 'smartva/adult_undetermined_weights-hce0.csv', 'DATA')],
               [('adult_undetermined_weights-hce1.csv', 'smartva/adult_undetermined_weights-hce1.csv', 'DATA')],
               [('child_undetermined_weights-hce0.csv', 'smartva/child_undetermined_weights-hce0.csv', 'DATA')],
               [('child_undetermined_weights-hce1.csv', 'smartva/child_undetermined_weights-hce1.csv', 'DATA')],
               [('neonate_undetermined_weights-hce0.csv', 'smartva/neonate_undetermined_weights-hce0.csv', 'DATA')],
               [('neonate_undetermined_weights-hce1.csv', 'smartva/neonate_undetermined_weights-hce1.csv', 'DATA')],
               strip=None,
               upx=False,
               name='SmartVA')
app = BUNDLE(coll,
             name='SmartVA.app',
             icon='pkg/icon.icns')