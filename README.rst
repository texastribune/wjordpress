Wjordpress
==========

.. image:: https://travis-ci.org/texastribune/wjordpress.png
   :target: https://travis-ci.org/texastribune/wjordpress
.. image:: https://coveralls.io/repos/texastribune/wjordpress/badge.png
   :target: https://coveralls.io/r/texastribune/wjordpress

Wjordpress is a reusable app for Django_ that allows you to use WordPress_ as
your editing interface and use Django_ for your presentation. You an also hook
multiple WordPress sites to a single Django project.

.. _Django: https://www.djangoproject.com/
.. _WordPress: http://wordpress.org/

You choose your level of integration. You can do a one time import, periodic
sync, manual sync, or near real-time updates using a web hook.

You can also start using WordPress content immediately without writing any
urls, views, or templates with the built in templatetag.


See the `ReadTheDocs site <http://wjordpress.readthedocs.org/en/latest/>`_ for
more.


Scenarios
---------

**Easy peasy lemon squeezy**:

1. Setup a link to a WordPress site
2. Write views_ and templates_ to display WordPress content

This is how the `reference project`_ syncs with `my blog`_

.. _views: https://github.com/texastribune/wjordpress/blob/master/example_project/viewer/views.py
.. _templates: https://github.com/texastribune/wjordpress/tree/master/example_project/templates
.. _reference project: http://wjordpress.herokuapp.com/
.. _my blog: http://www.crccheck.com/blog/

**Bring your own models**:

1. Setup a link to a WordPress site
2. Create a ``post_save`` signal on the Wjordpress models to sync to your own
   content models
3. Write a view and template to display your content models


----

How to pronounce "Wjordpress": http://youtu.be/tmyGrk99uzM
