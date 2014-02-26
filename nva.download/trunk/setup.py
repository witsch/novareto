from setuptools import setup, find_packages
import os

version = '2.0'

setup(name='nva.download',
      version=version,
      description="A project to render a download view for folder contents",
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
          'uvc.api[plone]',
          # -*- Extra requirements: -*-
      ],
      entry_points={
         'z3c.autoinclude.plugin': 'target=plone', 
      }
      )
