# -*- coding: utf-8 -*-

"""
This is a setup.py script for packaging plugin/extension.

Usage:
    python setup.py bdist_egg
"""


from setuptools import setup, find_packages

setup(
    name="avax.sample",
    version="0.1.0",
    description="A sample extension",
    zip_safe=True,
    packages=find_packages(),

    entry_points={
        'ava.extension': [
            'sample = avax.sample.ext:SampleExtension',
        ]
    }
)
