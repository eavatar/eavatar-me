Introduction
=====================

EAvatar ME, or Avame for short, is an event-driven agent for task automation.
It's designed with following scenarios in mind:

* Web scraping
* Web functional tests
* Network service monitoring
* Cloud application integration

Basically speaking, Avame runs tasks on behalf of the user in the background.

A task is a unit of work that performs one action only.
Related tasks are grouped as a job for complicated workflow.
Incidentally, a job is the unit for submission and is described by a script.
The scripts are nothing but restrictive Python code. Compared to regular Python code,
a script do not support following features, just to name a few:

#. No import statement
#. No while loop
#. No print statement
#. Names start with double underscores are prohibited.
#. No function definition
#. No class definition

All these restrictions are to make scripts easier to write and read.
Other heavy-lifting actions are provided by modules and exposed to scripts.

The source code of Avame project is released with Apache license 2.0