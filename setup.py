from setuptools import setup, find_packages, Extension
import os

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering :: Atmospheric Science"å
    ]

with open("README.rst", "r") as fp:
    long_description = fp.read()

setup(
    name="pyclmuapp",
    version="0.0.0",
    author="Junjie Yu",
    author_email="yjj1997@live.cn",
    url="https://github.com/envdes/pyclmuapp",
    description="Python package for CLMU-App",
    long_description=long_description,
    license="MIT",
    classifiers=classifiers,
    install_requires=['numpy', 'pandas', 'xarray', 'haversine', 'netcdf4', 'nc-time-axis', 'cdsapi'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyclmuapp=pyclmuapp._cli:main',
            #'clmuapp=pyclmuapp.infer:main',
        ],
    },
    package_data={'pyclmuapp': ['config/*', 
                                'config/cime_config/*',
                                'scripts/*', 
                                'usp/*', 
                                'usp/SourceMods/src.clm/*']}, # include all files in the config and scripts directory / specify the files to include file (MANIFEST.in)
    )