import os
from setuptools import setup, find_packages

setup(
    name='co2-sensor',
    version=os.environ.get('APP_VERSION', '0.1.0'),
    description='CO2 sensor API for Raspberry Pi using mh_z19',
    author='Your Name',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Flask',
        'mh-z19',
        'PyYAML',
    ],
    entry_points={
        'console_scripts': [
            'co2-api = co2_api:app.run',
        ],
    },
)
