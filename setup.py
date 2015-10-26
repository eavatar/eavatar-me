# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from setuptools import setup, find_packages

from ava import APP_NAME, __version__

setup(
    name=APP_NAME,
    version=__version__,
    description="An event-driven agent for task automation.",
    package_dir={'': 'src'},
    packages=find_packages(exclude=['**/tests/*']),
    include_package_data=True,

    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ava = avacli.main:main',
        ],
    },

    author="EAvatar Technology Ltd.",
    url="http://www.EAvatar.com",

)