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


Usage
=====

After successfully installing the addon, go to the Plone control panel,
where a new "Redirect Configuration" link is added:

.. image:: https://raw.github.com/4teamwork/ftw.redirector/master/docs/controlpanel.png

Redirect rules can easily be managed by editing the configuration:

.. image:: https://raw.github.com/4teamwork/ftw.redirector/master/docs/edit-config.png


How it works
============

- The redirect config is a dexterity object (mainly for ``ftw.publisher`` compatibility).
- Redirects are only applied if no content is found (404).
- Redirect rules are applied top-down: top roles have higherpriority.
  The first matching rule is applied, later rules arenot considered.
- Redirects match when the request path starts with thesource path.
- Each rule requires a source path and a destination.
- The source path must start with a slash and should notbe the site root.
- The destination may be a path (starting with a slash)or an URL to an external site.

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
