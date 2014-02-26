=====
Django telekomcloud bussiness market place integration
=====

This is an app that helps to integrate a django app with the telekom
bussiness market place (MP from now on)


Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "telekom_bmp" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'telekom_bmp',
    )

2. There are a bunch of variables to set up like::

   TC_CONSUMER_KEY
   TC_CONSUMER_SECRET
   TC_SUBSCRIPTION_INTEGRATION
   TC_USER_INTEGRATION


2. Include the telekom_bmp URLconf in your project urls.py like this::

    url(r'^telekom/', include('telekom_bmp.urls')),

3. Run `python manage.py syncdb`  or `python manage.py migrate` if using
   migrations to create the necessary tables models.

