#!usr/bin/python

# Copyright 2021 AIR Institute
# See LICENSE for details.


import io
from setuptools import setup, find_packages


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


def read_requeriments_file(filename):
    with io.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            yield line.strip()


setup(
    name='co2-mqtt-deepint-connector',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/air-institute/co2-mqtt-deepint-connector',
    download_url='https://github.com/air-institute/co2-mqtt-deepint-connector/archive/master.zip',
    license='GNU Affero General Public License v3',
    author='AIR Institute',
    author_email='franpintosantos@air-institute.com',
    description=' ',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=list(read_requeriments_file('requirements.txt')),
    entry_points={
        'console_scripts': [
            'co2-mqtt-deepint-connector=co2_mqtt_deepint_connector.cli:run'
        ],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Intended Audience :: Developers"
    ],
    keywords='MQTT, Deep Intelligence, connector',
    python_requires='>=3',
    project_urls={
        'Bug Reports': 'https://github.com/air-institute/co2-mqtt-deepint-connector/issues',
        'Source': 'https://github.com/air-institute/co2-mqtt-deepint-connector',
        'Documentation': 'https://github.com/air-institute/co2-mqtt-deepint-connector'
    },
)