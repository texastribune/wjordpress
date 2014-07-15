Wjordpress
==========

Wjordpress is a reusable app for Django_ that allows you to use WordPress_ as
your editing interface and Django_ for your presentation.

With Wjordpress, you can interact with WordPress content as if it were entered
in the Django admin. Wjordpress does not pretend to be WordPress and does not
provide any presentation. After the initial link, it's a "Fire-and-forget"
system. The Wjordpress Django admin interface is not something you'll have to
mess with on a daily basis.

.. _Django: https://www.djangoproject.com/
.. _WordPress: http://wordpress.org/


WordPress Setup
---------------

Once you have a WordPress site setup, you need to make sure it has the `JSON
REST API`_ plugin installed and activated. That's it! If you want real-time
updates, you'll need the HookPress_ plugin *TODO*.

.. _JSON REST API: http://wordpress.org/plugins/json-rest-api/
.. _HookPress: http://wordpress.org/plugins/hookpress/


Django Setup
------------

**Install into your environment**::

    # pip install wjordpress  # TODO
    pip install https://github.com/texastribune/wjordpress/archive/master.tar.gz

**Install into your Django project**::

    INSTALLED_APPS = [
        # ... your other installed apps
        'wjordpress',
    ]

**Create the database tables**::

    # python manage.py migrate wjordpress  # TODO
    python manage.py syncdb

**Add a WordPress site**:

In your Django admin, add a new site in ``Wjordpress -> Sites``:

.. image:: images/admin.png

Just enter the url to the WordPress blog and save.


Scenarios
---------

**Easy peasy lemon squeezy**:

1. Setup a link to a WordPress site
2. Write a view and template to display WordPress content

**Bring your own models**:

1. Setup a link to a WordPress site
2. Create a ``post_save`` signal on the Wjordpress models to sync to your own
   content models
3. Write a view and template to display your content models
