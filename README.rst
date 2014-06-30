Carlae
======
A URL shortener for your domain.

Try out a `live demo <http://carlae.com>`_ to see Carlae in action.


Installation
------------
So you want to try this out on your own hardware? Follow the instructions below to install Carlae on your rig and start hacking!

.. note:: You'll need to following software and tools on your system to demo Carlae: **sqlite3**, **pip**.

#. [Optional] It is highly recommended you setup Carlae in a virtualenv. Here's how to create one:
TODO: `virtualenv` instructions
`conda` environment instructions.

#. Get the source
Download a zip or tar.gz of the source and extract to a directory of your choice. Do all of this from the command line by running the following commands:

```
curl -LO https://github.com/asobrien/carlae/archive/v0.0.1.tar.gz
tar -zxvf v0.0.1.tar.gz
cd carlae-0.0.1
```

#. Install carlae
Installation is straightforward.
```
cd /path/to/Carlae
python setup.py develop
```

#. Run script to install db
You need to install the tables and create an initial user.
Run the following to do so.

Open an interactive python shell (`$ python`) and execute the following:

```
>>> from carlae.utils import db
>>> db.initialize_db()  # creates tables
>>> db.create_user("user@emai.com", "strong_password")  # creates initial user, replace credentials
>>> exit()
```


#. Run carlae

Run the following command:
```
python carlae/main.py
```

And point your browser to http://0.0.0.0:5000 and you should see the site running.



That's it. Have fun and hack away!


Configuration
-------------
Configuration details to go here.




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