#!template/venv/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='Template',
    version='0.1.dev',
    author='frennkie',
    author_email='mail@rhab.de',
    maintainer='frennkie',
    url='https://github.com/frennkie/template',
    description='Template for my Python projects',
    long_description=open('README.md').read(),
    packages=['template', 'template/modules', 'template/tests'],
    scripts=['bin/start_project_from_template.sh'],
    license='MIT',
    install_requires=[],
)
