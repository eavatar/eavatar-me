Development
===========


For developers who want to build Avame from source code, proper development
environments should be set up. According to the platform, the system requirements
and instructions are different.

Avame's source code is hosted on GitHub at https://github.com/eavatar/eavatar-me .
Therefore, Git is used for management of the source code.

`virtualenv` is used to have a relatively isolated Python runtime during development.
However, it becomes tricky due to the fact that Avame needs to access some packages that cannot be installed
via `pip`. So, event `virtualenv` is used, the `--system-site-packages` argument is set
for all supported platforms.


Refer to the section for the platform of your choice. Should you encountered any issues
, please file issues at https://github.com/eavatar/eavatar-me/issues


On Windows Platform
-------------------

System Requirements
^^^^^^^^^^^^^^^^^^^

+-------------------+------------------+
| Operating system  | CPU Architecture |
+===================+==================+
| Windows 7 Pro     | X86-64           |
+-------------------+------------------+

Git for Windows
^^^^^^^^^^^^^^^

To check out source codes on Windows platform, `Git for Windows` command line tool is needed.
Please download and install it from https://git-scm.com/download/win .

Please note that all command-line instructions are assumed to be run using the shell provided by
Git for Windows, which provides a Unix-like interface.

Python Distribution
^^^^^^^^^^^^^^^^^^^

The Python distribution for development on Windows platform is Anaconda Python 2.7.
Download it from https://www.continuum.io/downloads .


Get the Source Code
^^^^^^^^^^^^^^^^^^^

Use following command to check out the source code:

.. code-block:: bash

    git checkout https://github.com/eavatar/eavatar-me avame

It's assumed that source code is cloned to the local host at $WORKDIR directory.

Virtual Environment
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    virtualenv --system-site-packages env
    source env/Scripts/activate

It's assumed that command-line instructions in the following sections are run with the
virtual environment activated.

Installing Dependencies
^^^^^^^^^^^^^^^^^^^^^^^

Use following instruction to install

.. code-block:: bash

    pip install -r requirements/requirements_win32.txt

Avame needs `pywin32', 'lxml' packages on Windows platform, which should be already provided by
Anaconda Python Distribution.

Build the Binaries
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    pyinstaller pack\avame.spec --clean -y

The application binaries are located at $WORKDIR\dist\avame\.
You may use following instruction to launch it:

.. code-block:: bash

    .\dist\avame\avame.exe


On OS X Platform
----------------

System Requirements
^^^^^^^^^^^^^^^^^^^

+-------------------+------------------+
| Operating system  | CPU Architecture |
+===================+==================+
| OS X 10.10        | X86-64           |
+-------------------+------------------+

Python Distribution
^^^^^^^^^^^^^^^^^^^

OS X platform has built-in Python distribution, a Homebrew-managed version is used, however.
Assume `Homebrew <http://brew.sh/>`_ tool has already installed on the system, use following command to install
Python:

.. code-block:: bash

    brew install python

Virtual Environment
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    virtualenv --system-site-packages env
    source env/bin/activate

It's assumed that command-line instructions in the following sections are run with the
virtual environment activated.

Get the Source Code
^^^^^^^^^^^^^^^^^^^

Avame's source code is hosted on GitHub at https://github.com/eavatar/eavatar-me .
Therefore, Git is used for management of the source code.

Use following command to check out the source code:

.. code-block:: bash

    git checkout https://github.com/eavatar/eavatar-me avame

It's assumed that source code is cloned to the local host at $WORKDIR directory.


Installing Dependencies
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    pip install -r requirements/requirements_osx.txt

`lxml` package needs extra steps to install with following instructions:

.. code-block:: bash

    brew install libxml2
    pip install lxml

Build the Binaries
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    pyinstaller pack/avame.spec --clean -y

The application binaries are located at $WORKDIR/dist/avame/.
You may use following command to launch it:

.. code-block:: bash

    ./dist/avame/avame

In addition to the binaries, an application bundle for OS X is created and placed at
$WORKDIR/dist/EAvatar.app/ . An application bundle is a special directory on OS X,
which may be launched from the command line with following instruction:

.. code-block:: bash

    open ./dist/EAvatar.app

On Ubuntu Platform
-------------------

System Requirements
^^^^^^^^^^^^^^^^^^^

+-------------------+------------------+
| Operating system  | CPU Architecture |
+===================+==================+
| Ubuntu 14.04      | X86-64           |
+-------------------+------------------+

Python Distribution
^^^^^^^^^^^^^^^^^^^

Avame uses the system-bundled Python distribution for the development on Ubuntu platform.
Note that the version used is 2.7.6.

Virtual Environment
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    virtualenv --system-site-packages env
    source env/bin/activate

It's assumed that command-line instructions in the following sections are run with the
virtual environment activated.

Get the Source Code
^^^^^^^^^^^^^^^^^^^

Avame's source code is hosted on GitHub at https://github.com/eavatar/eavatar-me .
Therefore, Git is used for management of the source code.

Use following command to check out the source code:

.. code-block:: bash

    git checkout https://github.com/eavatar/eavatar-me avame

It's assumed that source code is cloned to the local host at $WORKDIR directory.

Installing Dependencies
^^^^^^^^^^^^^^^^^^^^^^^

Use following instructions to install Python and system packages:

.. code-block:: bash

    sudo apt-get install libxml2-dev libxslt1-dev python-dev python-lxml
    pip install -r requirements/requirements_gtk.txt

Build the Binaries
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    pyinstaller pack/avame.spec --clean -y

The application binaries are located at $WORKDIR/dist/avame/.
You may use following command to launch it:

.. code-block:: bash

    ./dist/avame/avame

