from setuptools import setup, find_packages
import os

version = '1.0.0'

tests_require = [
    'ftw.builder',
    'ftw.testbrowser',
    'ftw.testing',
    'plone.app.testing',
    'unittest2',
]


setup(name='ftw.redirector',
      version=version,
      description="Plone addon for redirects",
      long_description=open("README.rst").read() + "\n" + open(
          os.path.join("docs", "HISTORY.txt")).read(),

      classifiers=[
          "Environment :: Web Environment",
          'Framework :: Plone',
          'Framework :: Plone :: 4.3',
          "Intended Audience :: Developers",
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],

      keywords='ftw redirects redirector plone',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.redirector',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'collective.z3cform.datagridfield',
          'ftw.profilehook',
          'openpyxl',
          'plone.api',
          'plone.app.dexterity',
          'plone.dexterity',
          'plone.directives.form',
          'Plone',
          'setuptools',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """)
