#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(name='pywigner',
      version='0.0.1',
      description='Wigner distribution',
      url='https://github.com/ljbkusters/python-wigner-distribution',
      author='Luc Kusters',
      author_email='luc.kusters@rwth-aachen.de',
      license='MIT License',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
            "numpy",
            "scipy",
          ],
      )
