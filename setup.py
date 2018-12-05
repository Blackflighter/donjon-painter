#!/usr/bin/env python

import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='donjon-painter',
    version='0.9.2',
    author='Korvin Roganov',
    author_email='qualimerjudith@gmail.com',
    license='GPLv3',
    description='Graphical map translator for donjon\'s Random Dungeon Generator TSV files.',
    long_description=long_description,
    url='https://github.com/Blackflighter/donjon-painter',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_dir={'donjon-painter': 'donjon_painter'},
    entry_points={
        'console_scripts': [
            'donjon-painter = donjon_painter.painter:main'
        ]
    },
    python_requires='>=3.5',
    install_requires=[
        'Pillow'
    ],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent"
    ])
