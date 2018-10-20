# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='validator',
    version='0.1.0',
    description='XML Validation package for JJS.org',
    long_description=readme,
    author='Ian Vermes',
    author_email='ian.vermes@gmail.com',
    url='https://github.com/IanVermes/next_gen_xml/validation',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
