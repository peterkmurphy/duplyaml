#!/usr/bin/env python
# The duplyaml YAML processor.
# The setup.py file.
# Used for setting up and installing duplyaml.


import sys
try:
    from setuptools import setup, Extension, Command
except ImportError:
    from distutils.core import setup, Extension, Command

import os

# Idea from https://github.com/simplejson/simplejson/blob/master/setup.py

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys, subprocess
        raise SystemExit(
            subprocess.call([sys.executable,
                             # Turn on deprecation warnings
                             '-Wd',
                             'duplyaml/tests/__init__.py']))

cmdclass = dict(test=TestCommand)
kw = dict(cmdclass=cmdclass)


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def readme():
    with open(os.path.join(__location__, 'README.rst')) as f:
        return f.read()

x = readme()

setup(name='duplyaml',
    version='0.1',
    description='A YAML processor for Python',
    url='https://github.com/peterkmurphy/duplyaml',
    author='Peter Murphy',
    author_email='peterkmurphy@gmail.com',
    license='MIT',
    packages=['duplyaml'],
    classifiers = [
        "Development Status :: 1 - Planning",
        "Environment :: Other Environment",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Other Audience",
        "Intended Audience :: System Administrators"
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Markup :: JSON",
        "Topic :: Text Processing :: Markup :: YAML",
      ],
      long_description=readme(),
      keywords='YAML JSON text parsing processing',
      include_package_data=True,
      zip_safe=False,
      **kw)
