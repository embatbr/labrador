#! coding: utf-8

from setuptools import find_packages
from setuptools import setup


setup(
    name='labrador',
    version='0.1.0',
    author='Eduardo Tenório',
    author_email='embatbr@gmail.com',
    license='WTFPL',
    packages=[
        'labrador',
        'labrador.retrievers'
    ],
    include_package_data=True,
    install_requires=[
        'google-cloud-bigquery==1.8.1'
    ]
)