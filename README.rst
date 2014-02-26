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

   # auth credentials
   TC_CONSUMER_KEY
   TC_CONSUMER_SECRET

   # classes that implement user and subscription relations
   TC_PAYLOAD_INTEGRATION
   TC_USER_INTEGRATION

   # regarding python social auth
   SOCIAL_AUTH_PIPELINE = (
       'social.pipeline.social_auth.social_details',
       'social.pipeline.social_auth.social_uid', 
       # this part needs to be implemented
       '<your_app>.pipeline.load_user', 
       'social.pipeline.social_auth.auth_allowed',
       'social.pipeline.social_auth.social_user',
       'social.pipeline.social_auth.associate_user',
   )

2. Include the telekom_bmp URLconf in your project urls.py like this::

    url(r'^telekom/', include('telekom_bmp.urls')),

3. Add the auth backend for openid*::

   AUTHENTICATION_BACKENDS = (
       ...
       'telekom_bmp.backend.OpenIDBackend',   
       ...
   )

   * if you user model is not the standar django you may want
     to use an extended backend based on this one

4. Run `python manage.py syncdb`  or `python manage.py migrate` if using
   migrations to create the necessary tables models.

