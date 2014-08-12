Wjordpress
==========

Contents:

.. toctree::
   :maxdepth: 2

   prior_art
   quirks
   changelog


Since time immemorial, there has been effort after effort to make the Django
admin friendlier for writers to use as a CMS interface. The goal always being:
"Can we make Django as easy to use as WordPress?"

Well, instead of trying to make the Django admin ack like WordPress, why not
use WordPress and feed the data into Django? That is the goal of Wjordpress.


Installation
------------

Adding Wjordpress to your Django Project
''''''''''''''''''''''''''''''''''''''''

1. Install Wjordpress ``pip install wjordpress`` / update your requirements.
2. Add Wjordpress to your installed apps::

    INSTALLED_APPS = [
        # ... your other installed apps
        'wjordpress',
    ]

3. Initialize database tables using ``manage.py syncdb``. *Because the project
   is still in alpha, migrations have not been checked in.*

Setting Up Existing WordPress Site
''''''''''''''''''''''''''''''''''

1. Install the `JSON REST API`_ plugin
2. *(optional)* Install the HookPress_ plugin

.. _JSON REST API: http://wordpress.org/plugins/json-rest-api/
.. _HookPress: http://wordpress.org/plugins/hookpress/

Adding your first WordPress site
''''''''''''''''''''''''''''''''

1. In the Django Admin, add a Wjordpress Site
2. For the URL input, use the same url you'd use to browse to the site
3. Save. Whenever you save a site in admin, the most recent 10 posts will be
   pulled.
4. You can add additional WordPress sites so one Django site can integrate with
   many WordPress sites.


Next Steps
----------

Automatically keep the Django site up to date
'''''''''''''''''''''''''''''''''''''''''''''

If you installed the HookPress_ WordPress plugin, you can set up a
``save_post`` webhook that will ping the Django site to update whenever you
update a post. In the Django Admin change list for Wjordpress sites, there's a
column, "Hook", for the url to use as the webhook url. In the WordPress admin,
add a ``save_post`` hook to this url. Make sure the ``ID`` field is sent (this
happens by default).


Manually sync the Django site
'''''''''''''''''''''''''''''

Run the ``manage.py wjordpress_fetch`` management command.


Inspect communication between Django and WordPress
''''''''''''''''''''''''''''''''''''''''''''''''''

If you enabled logging when you added your WordPress site (this is on by
default), you can see what communication has occurred between the two in the
Django Admin at Wjordpress > Logs.


Embedding a WordPress site
''''''''''''''''''''''''''

Wjordpress comes with a templatetag so you can quickly insert a widget of
recent posts. If your WordPress site was called "Mollusk Life", in your Django
template HTML you would add something like::

    {% load wjidget from wjordpress %}
    {% wjidget "Mollusk Life" limit=5 %}

You need to add your own css to style the widget. All the css class names are
namespaced with the ``wjordpress-`` prefix.


Using Your Own Django Models
''''''''''''''''''''''''''''

If you want to sync WordPress content to your own models, you can write
``post_save`` signals. For an example, see the models_ and signals_ in the
example app.

.. _models: https://github.com/texastribune/wjordpress/blob/master/example_project/content/models.py
.. _signals: https://github.com/texastribune/wjordpress/blob/master/example_project/content/signals.py
