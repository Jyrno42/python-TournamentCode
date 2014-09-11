# -*- coding: utf-8 -*-

import os
from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
    name="python-TournamentCode",
    version="1.1.0",
    author="Jyrno Ader",
    author_email="jyrno42@gmail.com",
    description="LoL TournamentCode generation helper libary, can be easily used to set up different tournaments.",
    license="GPL v2",
    keywords="TournamentCode Riot LoL league legends django jyrno42",
    url="http://th3f0x.com",
    packages=['TournamentCode'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
)
