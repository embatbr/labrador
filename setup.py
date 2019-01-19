#! coding: utf-8

from setuptools import find_packages
from setuptools import setup


setup(
    name='labrador',
    version='1.0.0',
    author='Eduardo Tenório',
    author_email='embatbr@gmail.com',
    license='WTFPL',
    packages=[
        'labrador',
        'labrador.connectors',
        'labrador.retrievers',
        'labrador.sinkers'
    ],
    include_package_data=True,
    install_requires=[
        'boto3==1.9.80',
        'google-cloud-bigquery==1.8.1'
    ]
)
