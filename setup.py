from setuptools import setup, find_packages
import sys, os

version = '1.0.4'

setup(name='webpreview',
      version=version,
      description="Extracts OpenGraph, TwitterCard and Schema properties from a webpage.",
      long_description=open('README.md').read(),
      classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
      ],
      keywords='OpenGraph TwitterCard Schema Facebook Twitter Google+',
      author='ludbek',
      author_email='sth.srn@gmail.com',
      url='https://github.com/ludbek/webpreview',
      license='LICENSE.txt',
      packages=find_packages(exclude=['test']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
        "requests==2.2.1",
        "beautifulsoup4==4.3.2",
      ],
      entry_points="""
        # -*- Entry points: -*-
        """,
      )
