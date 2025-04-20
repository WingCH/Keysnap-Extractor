from setuptools import setup

APP = ['extract_keyframes_gui.py']
DATA_FILES = []
OPTIONS = {
    'packages': ['cv2', 'numpy', 'PIL'],
    'includes': ['tkinter'],
    'iconfile': 'app_icon.png',
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
