Carlae
======
A URL shortener for your domain.

**ARCHIVE NOTICE: This repository is no longer under active development. The code here is compatible with python2, no effort has been made to make it work with python3.**

Try out a ~~live demo~~ to see Carlae in action.


Installation
------------
So you want to try this out on your own hardware? Follow the instructions below to install Carlae on your rig and start hacking!

    | You'll need to following software and tools on your system to demo Carlae: **sqlite3** & **pip**.


1. [Optional] Create `virtualenv`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is highly recommended you setup Carlae in a virtualenv. See `these instructions <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ to get one up and running.

If you're using the `Anaconda python distribution <https://store.continuum.io/cshop/anaconda/>`_, you'll need to create a new environment like so:

.. code-block:: base
    
    conda create -n carlae-app pip
    
This will create a virualenv with a *python* interpreter, *pip*, *setuptools*, *sqlite3*, and few other dependencies. Now activate it:

.. code-block:: bash

    source activate carlae-app
    
and proceed with the installation instructions.
    


2. Get the source
~~~~~~~~~~~~~~~~~
Download a `zip`_ or `tar.gz`_ of the source and extract to a directory of your choice. Do all of this from the command line by running the following commands:

.. code-block:: bash

    curl -LO https://github.com/asobrien/carlae/archive/v0.0.2.tar.gz
    tar -zxvf v0.0.2.tar.gz
    cd carlae-0.0.2


3. Install Carlae
~~~~~~~~~~~~~~~~~
Installation is straightforward.

.. code-block:: bash

    cd /path/to/Carlae
    python setup.py develop


4. Run initialization scripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You need to install the tables and create an initial user.
Run the following to do so.

Open an interactive python shell (:code:`$ python`) and execute the following:

.. code-block:: python

    from carlae.utils import db
    db.initialize_db()  # creates tables
    db.create_user("user@email.com", "strong_password")  # creates initial user, replace credentials
    exit()



5. Run Carlae
~~~~~~~~~~~~~
Run the following command:

.. code-block:: bash

    python carlae/main.py


And point your browser to http://0.0.0.0:5000 and you should see the site running.


That's it. Have fun and hack away!



Configuration
-------------
Configuration details to follow.


Issues
------

File bugs, issues, problems, etc., on the `issue tracker <https://github.com/asobrien/carlae/issues>`_.

Dependencies
------------
See `requirements.txt <src/requirements.txt>`_ for a complete list of dependencies.

Carlae is built upon the `Flask`_ framework and utilizes various extensions. The UI is built upon `Bootstrap`_. Interfacing with the database is via `SQLAlchemy`_.




License
-------
Carlae is released under the terms of the `MIT license`_.

The MIT license is simple and very unrestrictive. See the `LICENSE <LICENSE>`_ file for the complete terms.


.. _Flask: http://flask.pocoo.org/
.. _Bootstrap: http://getbootstrap.com/
.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _MIT license: http://en.wikipedia.org/wiki/MIT_License
.. _zip: https://github.com/asobrien/carlae/archive/v0.0.2.zip
.. _tar.gz: https://github.com/asobrien/carlae/archive/v0.0.2.tar.gz
