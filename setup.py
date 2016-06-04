from distutils.core import setup

setup(
    name='cura2slic3r',
    version='0.1',
    description='Converts Cura slicer profile do Slic3r profile',
    author='ra100',
    author_email='git@ra100.net',
    url='https://github.com/ra100/curaToSlic3rProfile',
    packages = ['package'],
    scripts=['cura2slic3r']
)