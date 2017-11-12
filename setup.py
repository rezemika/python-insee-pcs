# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
import insee_pcs

setup(
    name=insee_pcs.__appname__,
    version=insee_pcs.__version__,
    packages=find_packages(),
    author="rezemika",
    author_email="reze.mika@gmail.com",
    description="A set of tools to use the 'Professions et Catégories Socioprofessionnelles' system of INSEE (a French statistical agency).",
    long_description=open('README.md').read(),
    install_requires=["peewee"],
    include_package_data=True,
    url='http://github.com/rezemika/python-insee-pcs',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Natural Language :: French",
        "Topic :: Utilities",
        "Topic :: Database"
    ]
)
