from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='nva.searchviewlet',
      version=version,
      description="Viewlet for search and check actual webcode",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['nva'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points={
         'fanstatic.libraries': [
            'nva.searchviewlet = nva.searchviewlet.resources:library',
            ],
         'z3c.autoinclude.plugin': 'target=uvcsite', 
      }
      )
