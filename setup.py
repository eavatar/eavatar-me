# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import os
import codecs
from setuptools import setup, find_packages
from ava import APP_NAME, __version__


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


setup(
    name=APP_NAME,
    version=__version__,
    description="An event-driven agent for task automation.",
    long_description=read("README.rst"),
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['**/tests/**']),
    include_package_data=True,
    data_files=[('', ['src/ava_settings.py', 'src/ava_startup.py'])],

    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ava = avacli.main:main',
        ],
    },

    author="EAvatar Technology Ltd.",
    url="http://EAvatar.ME",
    license='Apache 2.0',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Environment :: MacOS X :: Cocoa",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: GTK",
        "Environment :: No Input/Output (Daemon)",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.7",
    ],
)
