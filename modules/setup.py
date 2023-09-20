from setuptools import setup

APP = ['main.py']
DATA_FILES = []
PACKAGES = ['pro_publica.py', 'excel.py']
INSTALL_REQUIRES = ['PySimpleGUI', 'pandas', 'requests', 'beautifulsoup4']

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': {'packages': PACKAGES}},
    install_requires=INSTALL_REQUIRES,
    setup_requires=['py2app'],
)
