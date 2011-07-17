from setuptools import setup, find_packages

version = '0.0'

setup(name='ukh_userhandling',
      version=version,
      description="",
      long_description="""\
""",
      # Get strings from http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[],
      keywords="",
      author="",
      author_email="",
      url="",
      license="",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'grok',
                        'grokui.admin',
                        'fanstatic',
                        'zope.fanstatic',
                        'grokcore.startup',
                        'uvc.layout',
                        'megrok.menu',
                        # Add extra requirements here
                        ],
      entry_points={
          'fanstatic.libraries': [
              'ukh_userhandling = ukh_userhandling.resource:library',
          ]
      })
