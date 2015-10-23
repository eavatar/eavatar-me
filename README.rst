EAvatar ME
###########################################

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
==========

.. image:: docs/source/_static/screenshot1.png
    :alt: EAvatar on Windows 7

Documentation
================

http://docs.eavatar.me

License
=======

Apache license 2.0