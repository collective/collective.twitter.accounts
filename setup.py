# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '1.0.3'
long_description = open("README.rst").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='collective.twitter.accounts',
      version=version,
      description="Provide Twitter integration for a Plone Site",
      long_description=long_description,
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Franco Pellegrini',
      author_email='frapell@gmail.com',
      url='https://github.com/collective/collective.twitter.accounts',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective', 'collective.twitter'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'python-twitter',
        'plone.app.registry',
        ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
