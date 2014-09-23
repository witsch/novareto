from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='chemiedp',
      version=version,
      description="",
      long_description=""" """,
      classifiers=[],
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'uvclight [auth]',
          'uvclight [zodb]',
          'zope.i18nmessageid',
      ],
      entry_points={
         'fanstatic.libraries': [
            'chemiedp = chemiedp.resources:library',
         ],
         'paste.app_factory': [
             'app = chemiedp.utils:Application',
         ],
        'pytest11': [
            'chemiedp_fixtures = chemiedp.tests.fixtures',
        ]
      }
      )
