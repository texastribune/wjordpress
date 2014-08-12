Wjordpress
==========

.. image:: https://travis-ci.org/texastribune/wjordpress.png
   :target: https://travis-ci.org/texastribune/wjordpress
.. image:: https://coveralls.io/repos/texastribune/wjordpress/badge.png
   :target: https://coveralls.io/r/texastribune/wjordpress

Wjordpress is a reusable app for Django_ that allows you to use WordPress_ as
your editing interface and Django_ for your presentation.

With Wjordpress, you can interact with WordPress content as if it had been
entered in the Django admin. Wjordpress does not pretend to be WordPress and
does not provide any presentation. After the initial link, it's a "Fire-and-
forget" system. The Wjordpress Django admin interface is not something you'll
have to mess with on a daily basis. Changes made in WordPress will
automatically

.. _Django: https://www.djangoproject.com/
.. _WordPress: http://wordpress.org/


See the `ReadTheDocs site <http://wjordpress.readthedocs.org/en/latest/>`_ for
the latest docs.


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
