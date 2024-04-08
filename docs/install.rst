.. _install_intro:

=======
Install
=======

Install package in your environment : ::

    pip install django-canopy

For development usage see :ref:`development_install`.

Configuration from scratch
**************************

Enable application stack
------------------------

Add it to your installed Django apps in settings : ::

    INSTALLED_APPS = (
        ...
        "django.forms",
        # Add required DjangoCMS applications here
        # ...
        # Required Canopy form application stack
        "captcha",
        "phonenumber_field",
        "crispy_forms",
        "crispy_bootstrap5",
        "canopy",
    )

.. Note::

    * ``django.forms`` is not required but `recommended <https://docs.djangoproject.com/en/stable/ref/forms/renderers/#templatessetting>`_;
    * See `DjangoCMS documentation <https://docs.django-cms.org/en/latest/introduction/01-install.html#adding-django-cms-to-an-existing-django-project>`_
      to know what to add;
    * ``crispy_bootstrap5`` maybe avoided, however it still a package requirement;


Configure behaviors and options from settings
---------------------------------------------

There is many settings depending applications, in order:

DjangoCMS
    There is just too much possible scenario to describe, check the
    `DjangoCMS documentation <https://docs.django-cms.org/en/latest/introduction/01-install.html#adding-django-cms-to-an-existing-django-project>`_
    for details.

Captcha
    We recommend at least to define the captcha lifespan with: ::

        CAPTCHA_TIMEOUT = 5

    Captcha code will be available for 5 minutes.

    There is many more settings you may want to customize, see
    `Django simple captcha documentation <https://django-simple-captcha.readthedocs.io/en/latest/advanced.html#configuration-toggles>`_.

Phonenumber
    For a simple configuration you may allow for any format in international syntax: ::

        PHONENUMBER_DEFAULT_FORMAT = "INTERNATIONAL"
        PHONENUMBER_DB_FORMAT = "INTERNATIONAL"

    This will allows for ``+33 1 12 34 56 78`` or ``+1 604-401-1234,987`` but not
    ``01 12 34 56 78`` or ``6044011234``.

    Or you can use a more specific format and syntax following the `foo documentation <https://django-phonenumber-field.readthedocs.io/en/latest/reference.html#settings>`_.

    As an example, to only allows for french format in nationa syntax you would do: ::

        PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"
        PHONENUMBER_DB_FORMAT = "NATIONAL"
        PHONENUMBER_DEFAULT_REGION = "FR"

    This will allows for ``01 12 34 56 78`` or ``+33 1 12 34 56 78`` but not
    ``+1 604-401-1234`` or ``6044011234``.

Crispy forms
    If you are using Bootstrap5, you just need to add this: ::

        CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

        CRISPY_TEMPLATE_PACK = "bootstrap5"

    Check
    `Crispy form template pack documentation <https://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs>`_ for more details.

Canopy form itself
    Load default settings: ::

        from canopy.settings import *

    Then overrides the :ref:`settings_intro` you need.


Mount application URLs
----------------------

Then mount applications URLs: ::

    urlpatterns = [
        ...
        path("canopy/", include("canopy.urls")),
        path("code-check/", include("captcha.urls")),
    ]

The first one is for Canopy form itself and the second one is used to reload captcha.
You can change their path if needed.


Apply migrations
----------------

Once everything is done, you can apply database migrations.

Sandbox
*******

Repository contains a sandbox that is a simple Django project with everything
configured to just work, it can be an easy way to try Canopy form.

For this you need to get the repository and install it locally in development mode, see
documentation :ref:`development_install` for details.
