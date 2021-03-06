#!/usr/bin/env python3
import PyInstaller.__main__
import os
import site
import subprocess
from subprocess import PIPE

def get_default_python_path():
    if os.name == 'nt':
        pass
    elif os.name == 'posix':
        return '/usr/bin/python3'
    elif os.name == 'mac':
        pass

def get_default_python_site_packages():
    global_site_packages = []
    try:
        default_python_path = get_default_python_path()
        result = subprocess.run([default_python_path, "-c",'import site;  print(site.getsitepackages())'],stdout=subprocess.PIPE)
        global_site_packages = eval(result.stdout)
    except Exception as e:
        print(e)
    return global_site_packages


current_dir = os.path.dirname(os.path.realpath(__file__))
global_site_packages = get_default_python_site_packages()
venv_site_packages = site.getsitepackages()
total_paths_to_import = venv_site_packages + global_site_packages + [current_dir]
paths_variable = os.pathsep.join(total_paths_to_import)

PyInstaller.__main__.run([
    'analyzer.py',
    '--windowed',
    '--noconfirm',
    '--paths',
    paths_variable,
    '--add-data',
    'views/tree_view.glade'+os.pathsep+'views',
    '--add-data',
    'icons/analyzer_icon.jpeg'+os.pathsep+'icons/analyzer_icon.jpeg',
])