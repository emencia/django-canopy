.. _virtualenv: https://virtualenv.pypa.io
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org
.. _Sphinx: http://www.sphinx-doc.org
.. _tox: http://tox.readthedocs.io
.. _livereload: https://livereload.readthedocs.io
.. _twine: https://twine.readthedocs.io

.. _development_intro:

===========
Development
===========

Development requirements
************************

django-canopy is developed with:

* *Test Development Driven* (TDD) using `Pytest`_;
* Respecting flake and pip8 rules using `Flake8`_;
* `Sphinx`_ for documentation with enabled `Napoleon`_ extension (using
  *Google style*);
* `tox`_ to run tests on various environments;

Every requirements are available in package extra requirements in section
``dev``.

.. _development_install:

System requirements
*******************

This will requires `Python`, `pip`_, `virtualenv`_, *GNU make* and a recent
*Node.js* already installed and some system packages for installing and running.

.. Note::
   Development environment use SQLite database, if you need another one you
   will need to install some more libraries and configurations on your own.

.. Warning::
   Package names may differ depending your system.

* Git;
* Python;
* ``python-dev``;
* ``python-virtualenv``;
* ``gettext``;
* ``gcc``;
* ``make``;
* ``libjpeg``;
* ``libcairo2``;
* ``zlib``;
* ``libfreetype``;

.. Hint::
   If your system does not have the right Python version as the default one, you should
   use something like `pyenv <https://github.com/pyenv/pyenv>`_ to install it and
   then use ``pyenv local`` to set the correct project Python version to use.

On Linux distribution
    You will install them from your common package manager like ``apt`` for Debian
    based distributions: ::

        apt install python-dev python-virtualenv gettext gcc make libjpeg libcairo2 zlib libfreetype

On macOS
    Recommended way is to use ``brew`` utility for system packages, some names
    can vary.

On Windows
    **Not supported**, you probably can install some needed stuff but with some
    works on your own.


Install for development
***********************

Once every requirements are installed, type: ::

    git clone https://github.com/emencia/django-canopy.git
    cd django-canopy
    make install frontend

django-canopy will be installed in editable mode from the
latest commit on master branch with some development tools.

Unittests
---------

Unittests are made to work on `Pytest`_, a shortcut in Makefile is available
to start them on your current development install: ::

    make tests

Tox
---

To ease development against multiple Python versions a tox configuration has
been added. You are strongly encouraged to use it to test your pull requests.

Just execute Tox: ::

    make tox

This will run tests for all configured Tox environments, it may takes some time so you
may use it only before releasing as a final check.

Documentation
-------------

You can easily build the documentation from one Makefile action: ::

    make docs

There is Makefile action ``livedocs`` to serve documentation and automatically
rebuild it when you change documentation files: ::

    make livedocs

Then go on ``http://localhost:8002/`` or your server machine IP with port 8002.

Note that you need to build the documentation at least once before using
``livedocs``.

Releasing
---------

Before releasing, you must ensure about quality, use the command below to run every
quality check tasks: ::

    make quality

If quality is correct and after you have correctly push all your commits
you can proceed to release: ::

    make release

This will build the package release and send it to Pypi with `twine`_.
You will have to
`configure your Pypi account <https://twine.readthedocs.io/en/latest/#configuration>`_
on your machine to avoid to input it each time.

Contribution
------------

* Every new feature or changed behavior must pass tests, Flake8 code quality
  and must be documented.
* Every feature or behavior must be compatible for all supported environment.
