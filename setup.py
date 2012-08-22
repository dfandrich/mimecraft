#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name = 'mimecraft',
    description = 'A tool for generating complex MIME messages on the command line',
    long_description = open('README.md').read(),
    author = 'Lars Kellogg-Stedman',
    author_email = 'lars@oddbit.com',
    version = "1.00",
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'mimecraft = mimecraft.main:main',
            ],
        },
)

