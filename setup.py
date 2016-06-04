from setuptools import setup

setup(
    name='cura2slic3r',
    version='0.1',
    description='Converts Cura slicer profile do Slic3r profile',
    author='Rastislav Svarba (ra100)',
    author_email='git@ra100.net',
    url='https://github.com/ra100/curaToSlic3rProfile',
    license='GPLv3+',
    packages = ['package'],
    scripts=['cura2slic3r'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Utilities',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 2.7',
    ],
)