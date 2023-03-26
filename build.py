from PyInstaller.__main__ import run
import os

workpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build', 'workpath')
distpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')

datas = [(r'C:\Users\umutk\Desktop\Projects\TypeScript - JS\JumpCutterGUI\venv\Lib\site-packages\moviepy\audio\io\ffmpeg_audiowriter.py', '.'),
         (r'C:\Users\umutk\Desktop\Projects\TypeScript - JS\JumpCutterGUI\venv\Lib\site-packages\PyInstaller', '.'),
         (r"C:\Users\umutk\Desktop\Projects\TypeScript - JS\JumpCutterGUI\venv\Lib\site-packages", '.')
        ]

run([
    'jump_cutter_main.py',
    '--onefile',
    '--noconsole',
    f'--workpath={workpath}',
    f'--distpath={distpath}',
    '--icon=icon.ico',
    *[f'--add-data={src};{dst}' for src, dst in datas],
])
