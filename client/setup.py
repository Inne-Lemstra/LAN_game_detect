from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = ['multiprocessing'], excludes = [], include_files = ['all_the_games.txt'])
includefiles = ['all_the_games.txt']

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('getGameProcess.py', icon="icon.ico")
]

setup(
    name='getGamProcessTest',
    version = '0.1',
    description = 'A PyQt test Program',
    options = dict(build_exe = buildOptions),
    executables = executables
)