Django Telekom BMP Integration
=====

> This app helps to integrate a Django app with the [Deutsche Telekom Business Marketplace](https://portal.telekomcloud.com). It is based mostly on the [Sample-Python-Application](https://github.com/AppDirect/Sample-Python-Application) example.


Quick start
-----------

1. Add `telekom_bmp` to your `INSTALLED_APPS` setting like this:
    ``` python
    INSTALLED_APPS = (
        ...
        'telekom_bmp',
    )
    ```

2. Set up a bunch of variables:

    ``` python
    # auth credentials
    TC_CONSUMER_KEY
    TC_CONSUMER_SECRET
    ```

    ``` python
    # classes that implement user and subscription relations
    TC_PAYLOAD_INTEGRATION
    TC_USER_INTEGRATION
    ```
   
    ``` python
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
    ```

2. Include the `telekom_bmp` URLconf in your project's `urls.py`:

    ``` python
    url(r'^telekom/', include('telekom_bmp.urls')),
    ```

3. Add the auth backend for OpenID:

    ``` python
    AUTHENTICATION_BACKENDS = (
        ...
        'telekom_bmp.backend.OpenIDBackend',   
        ...
    )
    ```

    If your user model is not the standard Django model you may want
    to use an extended backend based on this one.

4. Run `python manage.py syncdb` or `python manage.py migrate` when using
   migrations to create the necessary table models.


License
-----------

Copyright 2014 ezeep GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
