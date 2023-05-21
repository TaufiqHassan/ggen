"""A setuptools based setup module for ggen"""
# -*- coding: utf-8 -*-

from codecs import open
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = [
    'xarray',
    'pandas',
    'setuptools',
    'scipy',
    'netCDF4',
    'nco',
    'tempest-remap'
]

setup(
    name='ggen',
    version='1.0.0',
    description="Package for generating grid meshes and performing conservative remapping",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Taufiq Hassan",
    author_email='taufiq.hassan@pnnl.gov',
    url='https://github.com/TaufiqHassan/ggen',
    entry_points={
        'console_scripts':[
            'ggen=ggen.main:main',
            ],
        },
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
)
