import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {'packages': [], 'excludes': []}
import os
os.environ['TCL_LIBRARY'] = 'D:\\Python\\Python36-32\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = 'D:\\Python\\Python36-32\\tcl\\tk8.6'
setup(
    name='示波器截图',
    version='1.0.0.0',
    description='示波器截图',
    options={'build_exe': build_exe_options},
    executables=[Executable('NAS.py')])
