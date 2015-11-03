Writing Scripts
###############

What are Scripts
----------------

To tell Avame to do your jobs, you need to tell Avame how to do it imperatively.
The instructions are expressed as a script in Python-like programming language.
It sounds scary at the first place to writing scripts in a programming language
for regular users. It ends up not so hard at all.

Differences from Regular Code
-----------------------------

The syntax is intentionally very limited so that it's more approachable than full-featured
Python codes. The document is not intended to describe all the syntax as it's a proper
subset of Python's. Compared to regular Python, following are removed features:

#. No import statement
#. No while control loop
#. No print statement
#. Names start with double underscores are prohibited, e.g. '__class__'.
#. No function definition
#. No class definition


Common Libraries
----------------
It's not supported to import modules for scripts, so some standard
libraries from Python runtime are selected and made available.
The modules provided:

#. datetime
#. collections
#. calendar
#. heapq
#. bisect
#. array
#. queue or Queue
#. string
#. re
#. math
#. random
#. json
#. base64
#. binascii
#. hashlib
#. hmac

In addition to standard libraries, `lxml` is available for XML/HTML parsing.

Perform Actions
---------------

Besides the common libraries, scripts can perform various actions,
each of which are explicitly registered functions and are intended for use by scripts.

The syntax to invoke an action is like follow:

.. code:: python

    ava.do(action_name, **kwargs)

, where `action_name` is in a format like 'mod_name.func_name'. For example,
'imap.check_gmail' is the action name from `imap` module to check GMail.

`ava.do` function returns a task object whose essential methods are:

#. result(blocked=True, timeout=None)
    Wait for the task to finish and return the result (or raise an exception).
    By default, the method blocks the caller. But can be made to work asynchronously.
    If `blocked` is False and the task is not stopped, a `Timeout` exception is raised.
    If `timeout` parameter is given, a `Timeout` exception will be raised if expired.


#. stopped()
    Check if the task is finished or failed without blocking.

#. finished()
    Check if the task is completed successfully.

#. failed()
    Check if the task failed.


The execution of an action is represented as a task. Multiple tasks can be issued
concurrently. At times, it's needed to wait for tasks to finish. To coordinate
tasks, a script may use following method to wait for tasks.

.. code:: python

    ava.wait(tasks, timeout=10)

,where `tasks` is a list of task objects; `timeout` is a timeout interval in seconds.
There is an additional argument `count` which specify how many tasks to wait for before
returning.


Built-in Actions
----------------

User Module
^^^^^^^^^^^

* user.notify
    Notify owner with a message and title.

Request Module
^^^^^^^^^^^^^^

Make methods from `requests` library available as actions.

* requests.head

* requests.get

* requests.put

* requests.patch

* requests.delete

* requests.post

Loop Control
------------

The only supported loop control for scripts is `for` statement.
`for` loop is usually used to iterate a finite number of elements.
In case a indefinite loop is needed, following construct can be used:

.. code:: python

    for it in ava.schedule:
        ...

`ava.schedule` is a special generator that returns counting number from 1 for
each iteration. By default, the interval between intervals are 1 minute.
Following are more examples:

1-minute interval
^^^^^^^^^^^^^^^^^

.. code:: python

    for it in ava.schedule.every(1).minute

5-minute interval
^^^^^^^^^^^^^^^^^

.. code:: python

    for it in ava.schedule.every(5).minutes

There are other supported interval units like `second`,`seconds`, `hour`, `hours`, `day` and `days`.

The total number of looping can also be control by providing a `counts` value.
For example:

.. code:: python

    for it in ava.schedule.count(5).every().minute:
        ...

Above code snippet loops 5 times and waits for 1 minute before an iteration.


Example
-------

Following script is for checking a GMail account with IMAP protocol every minute:

.. code:: python

    last_unseen = 0

    for it in ava.schedule.every(1).minute:
        check_task = ava.do('imap.check_gmail',
                            username='username@gmail.com',
                            password='password')

        messages, unseen = check_task.result()
        if unseen > 0 and unseen != last_unseen:
            last_unseen = unseen
            ava.do('user.notify',
                   message="You got %d new messages." % unseen,
                   title="You Got Mails from GMail")

