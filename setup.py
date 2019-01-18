#! coding: utf-8

from setuptools import find_packages
from setuptools import setup


setup(
    name='labrador',
    version='0.2.0',
    author='Eduardo Tenório',
    author_email='embatbr@gmail.com',
    license='WTFPL',
    packages=[
        'labrador',
        'labrador.connectors',
        'labrador.retrievers',
        'labrador.sinkers',
        'labrador.webapi'
    ],
    include_package_data=True,
    install_requires=[
        'boto3==1.9.80',
        'falcon==1.4.1',
        'google-cloud-bigquery==1.8.1',
        'gunicorn==19.9.0'
    ]
)
