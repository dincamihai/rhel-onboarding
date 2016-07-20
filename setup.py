
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='rhel-onboarding',
    version='0.1.0',
    author='Mihai Dinca',
    author_email='dincamihai@gmail.com',
    maintainer='Mihai Dinca',
    maintainer_email='dincamihai@gmail.com',
    license='MIT',
    url='https://github.com/dincamihai/rhel-onboarding',
    description='Make it easy to play with SuSE Manager and rhel minions',
    long_description='',
    packages=['onboarding'],
    install_requires=[
        'pytest-salt-containers',
        'docker-py',
        'fake-factory',
        'py'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'onboarding = onboarding.rhel',
        ],
    },
)
