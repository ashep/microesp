#!/bin/python
"""setup.py
"""
import io
import re
from setuptools import setup, find_packages

with io.open('README.rst', 'rt') as f:
    readme = f.read()

GITHUB_USER = 'ashep'
PKG_NAME = readme.split('\n')[0].lower()

with io.open('{}/__init__.py'.format(PKG_NAME), 'rt') as f:
    init_content = f.read()
    description = re.search(r"__description__ = '(.*?)'", init_content).group(1)
    author = re.search(r"__author__ = '(.*?)'", init_content).group(1)
    author_email = re.search(r"__email__ = '(.*?)'", init_content).group(1)
    lic = re.search(r"__license__ = '(.*?)'", init_content).group(1)
    version = re.search(r"__version__ = '(.*?)'", init_content).group(1)

setup(
    name=PKG_NAME,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=readme,
    long_description_content_type="text/x-rst",
    url='https://github.com/{}/{}'.format(GITHUB_USER, PKG_NAME),
    download_url='https://github.com/{}/{}/archive/master.zip'.format(GITHUB_USER, PKG_NAME),
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'adafruit-ampy==1.*',
    ],
    setup_requires=[],
    tests_require=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
