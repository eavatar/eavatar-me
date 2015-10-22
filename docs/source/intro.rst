Introduction
=====================

EAvatar ME, or Avame for short, is an event-driven agent for task automation.
It's designed with following scenarios in mind:

* Web scraping
* Service monitoring
* Cloud application integration

Basically speaking, Avame runs tasks which are assigned by the user.
A task is a unit of work that performs one action only.

Related tasks are grouped as a job for complicated workflow.
Incidentally, a job is the unit for submission and is described by a script.
The scripts are nothing but restrictive Python codes. Compared to regular Python codes,
a script do not support following features, just to name a few:

#. No 'import' statement
#. No while loop
#. No 'print' statement
#. Names start with double underscores are prohibited.
#. No function definition
#. No class definition

All these restrictions are to make scripts easier to write and read.
Other heavy-lifting actions are provided by modules and exposed to scripts.

Screenshot
-------------------

.. image:: _static/screenshot1.png
    :alt: EAvatar on Windows 7

Checkout Source Codes
-----------------------------

.. code-block:: bash

    git clone https://github.com/eavatar/eavatar-me.git
    cd eavatar-me

Dependencies
-----------------------------

All Python versions are 2.7.x.

Windows
^^^^^^^^^^

* PyWin32

Tested with Anaconda distribution only.

OS X
^^^^^^^^^

* PyObjc

Tested with Python installed via Homebrew.

Ubuntu
^^^^^^^^^

* PyGObject

Tested with system Python package.

Build the Distribution Package
------------------------------------

.. code-block:: bash

    pyinstaller pack/avame.spec --clean -y


Launch the Application
-----------------------------

Windows
^^^^^^^^^^^^

Launch the application from command line.
.. code-block:: bash

    dist\\avame\\avame.exe

OS X
^^^^^^^^^^^

Launch from the console
.. code-block:: bash

    ./dist/avame/avame

or run the app bundle:

.. code-block:: bash
    open dist/EAvatar.app

Ubuntu
^^^^^^^^^^^^^^

Launch from the console
.. code-block:: bash

    ./dist/avame/avame



License
^^^^^^^^^^^^

Apache license 2.0