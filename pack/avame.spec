# -*- mode: python -*-
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

app_name = 'avame'
exe_name = 'avame'
console = False
run_strip = False
extra_binaries = []

app_path = os.path.abspath('.')

src_path = os.path.join(app_path, 'src')
res_path = os.path.join(app_path, 'res')
pod_path = os.path.join(app_path, 'pod')
lib_path = os.path.join(app_path, 'plat.libs')
web_path = os.path.join(app_path, 'webfront')


if sys.platform == 'win32':
    exe_name = exe_name + '.exe'
    run_upx = False
    console = False
    script = os.path.join(app_path, 'src', 'avashell', 'shell_win32.py')
    extra_binaries.append( ('libsodium.dll', os.path.join(lib_path, 'libsodium.dll'), 'BINARY'))

elif sys.platform.startswith('linux'):
    run_strip = True
    run_upx = True
    script = os.path.join(app_path, 'src', 'avashell', 'shell_gtk.py')
    extra_binaries.append( ('libsodium.so', os.path.join(lib_path, 'libsodium.so.13.1.0'), 'BINARY' ))

elif sys.platform.startswith('darwin'):
    console=True
    run_upx = False
    run_strip = True
    script = os.path.join(app_path, 'src', 'avashell', 'shell_osx.py')
    extra_binaries.append( ('libsodium.dylib',  os.path.join(lib_path, 'libsodium.dylib'), 'BINARY') )

else:
    print("Unsupported operating system")
    sys.exit(-1)

# for copying data file according to PyInstaller's recipe
def Datafiles(*filenames, **kw):
    import os

    def datafile(path, strip_path=True):
        parts = path.split('/')
        path = name = os.path.join(*parts)
        if strip_path:
            name = os.path.basename(path)
        return name, path, 'DATA'

    strip_path = kw.get('strip_path', True)
    return TOC(
        datafile(filename, strip_path=strip_path)
        for filename in filenames
        if os.path.isfile(filename))

# declared the extra script files to be added
shfiles = Datafiles('src/ava_settings.py', 'src/ava_startup.py')


a = Analysis([script],
             pathex=[src_path],
             binaries=None,
             datas=None,
             hiddenimports=['avame.user','avame.schedule', 'ava_startup'],
             hookspath=None,
             runtime_hooks=None,
             excludes=['PySide.QtNetwork', 'PyQt4', 'Tkinter', 'ttk', 'wx'])

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          a.dependencies,
          exclude_binaries=True,
          name=exe_name,
          debug=False,
          strip=run_strip,
          upx=run_upx,
          icon= os.path.join(res_path, 'icon.ico'),
          console=console)


coll = COLLECT(exe,
               a.binaries + extra_binaries,
               a.zipfiles,
               Tree(pod_path, 'pod', excludes=['*.pyc', '*.mdb', '*.db']),
               Tree(res_path, 'res', excludes=['*.pyc']),
               Tree(web_path, 'webfront', excludes=['*_dev.*', 'tests', 'node_modules']),
               a.datas,
               shfiles,          # add script files to the collection.
               strip=run_strip,
               upx=run_upx,
               name=app_name)

if sys.platform.startswith('darwin'):
    app = BUNDLE(coll,
                name='EAvatar.app',
                appname=exe_name,
                icon=os.path.join(res_path, 'icon.icns'),
                info_plist={
                    'LSUIElement': '1',
                    'LSBackgroundOnly': '0',
                })