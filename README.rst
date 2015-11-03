.. contents:: Table of Contents


Purpose
=======

This is a Plone addon which allows to manage redirects.
It allows to add new redirects which may point to internal
or external URLs.


Installation
============

Add the package as dependency to your setup.py:

.. code:: python

  setup(...
        install_requires=[
          ...
          'ftw.redirector',
        ])

or to your buildout configuration:

.. code:: ini

  [instance]
  eggs += ftw.redirector

and rerun buildout.

After restarting your Plone, install ftw.redirector through the Plone addons
control panel, quickinstaller or portal_setup.

After installing the addon, go to the Plone control panel for redirects in
order to add new redirects.

Links
=====

- Github: https://github.com/4teamwork/ftw.redirector
- Issues: https://github.com/4teamwork/ftw.redirector/issues
- Pypi: http://pypi.python.org/pypi/ftw.redirector
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.redirector

Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.redirector`` is licensed under GNU General Public License, version 2.
