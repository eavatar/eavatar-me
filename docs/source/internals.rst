Internals
=========

Event-driven, Non-blocking I/O
------------------------------

At the core of EAvatar, Gevent is used as the event-driven, non-blocking I/O engine.
With the lightweight concurrency support and thread-like programming model,
it a pleasure again to write asynchronous I/O codes.


Restrictive Execution of Python Codes
-------------------------------------

In addition to mainly developed in Python, EAvatar also uses Python as the
domain-specific language(DSL) for describing jobs. A job is defined by a script in Python
with very limited subset of features enabled.

A script is parsed into an abstract syntax tree with `ast` module,
and then being walked through to detect
invalid constructs such as 'import', 'print', 'functiondef', etc.
Without complex constructs, it makes writing scripts more approachable for average users.

How Avame integrated with desktop environments
----------------------------------------------

The main user interface for Avame is a so-called system tray icon or status icon on the
desktop environment. Trying to avoid the bloated cross-platform GUI frameworks like QT,
it takes a very different way to provide the desktop UI.

No cross-platform GUI frameworks are used for the desktop environments,
an environment-by-environment integration is used instead.

* On Windows platform, Win32 API is used via `PyWin32` package.

* On OS X platform, Cocoa is used via `PyObjc` package.

* On Ubuntu platform, GTK3 is used via `PyGObject` package.

A cross-platform web-based user interface is supported for user interactions that are more
complex. To this end, Avame launches the default web browser when web UI is required.