# -*- coding: utf-8 -*-

from os.path import join, dirname
from setuptools import setup, find_packages


def read(*rnames):
    return open(join(dirname(__file__), *rnames)).read()

version = '1.0'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('src', 'nva', 'universalsearch', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )


setup(name='nva.universalsearch',
      version=version,
      description="Search multiple Plone sites via Solr",
      long_description=long_description,
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='cklinger',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/plone.example',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['nva'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'collective.solr',
        'z3c.jbot',
      ],
      extras_require=dict(test=[
        'collective.testcaselayer',
        'mr.laforge',
      ]),
      entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
      """,
      )
