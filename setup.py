#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from setuptools import setup

with open('requirements.txt', 'r') as fh:
    dependencies = [l.strip() for l in fh]

setup(name='upass',
      version='0.2.0',
      description='Console UI for pass.',
      keywords='upass',
      author='Chris Warrick',
      author_email='chris@chriswarrick.com',
      url='https://github.com/Kwpolska/upass',
      license='3-clause BSD',
      long_description=io.open('./docs/README.rst', 'r', encoding='utf-8').read(),
      platforms='any',
      zip_safe=False,
      include_package_data=True,
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 3 - Alpha',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6'],
      packages=['upass'],
      install_requires=dependencies,
      extras_require={
            ':python_version == "2.7"': ['configparser']
      },
      entry_points={
          'console_scripts': [
              'upass = upass.__main__:main',
          ]
      },
      )
