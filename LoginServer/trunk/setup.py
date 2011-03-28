from setuptools import setup, find_packages

version = '0.0'

setup(name='LoginServer',
      version=version,
      description="",
      long_description="""\
""",
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
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
                        'auth_pubtkt',
                        'M2Crypto',
                        # Add extra requirements here
                        ],
      entry_points={
          'fanstatic.libraries': [
              'loginserver = loginserver.resource:library',
          ]
      })
