#!/usr/bin/env python3
import os, shutil
from setuptools import setup

setup(name = 'mbti',
      version = '0.1',
      author = 'Denis Kasak',
      author_email = 'dkasak[at]termina.org.uk',
      description = ('Tools for Myers-Briggs types'),
      license = 'ISC',
      scripts = ['mbti.py'],
      entry_points = {
          "console_scripts" : ['mbti = mbti:main']
      }
)
