'''
Created on September 19, 2016

@author: David Stocker
'''

from distutils.core import setup
setup(
  name = 'graphyne',
  packages = ['graphyne'],
  version = '1.1',
  description = "A fully native Python property graph database. It is designed to be easy to integrate into your Python projects, simple to use and very powerful.",
  author = 'David Stocker',
  author_email = 'mrdave991@gmail.com',
  url = 'https://github.com/davidhstocker/Graphyne',
  download_url = 'https://github.com/davidhstocker/Graphyne/tarball/1.1', 
  keywords = ['graph', 'propertygraph', 'property graph', 'graphdatabase', 'graph database'],
  install_requires=[
          'memetic',
      ],
  classifiers = [],
)
