Internals
===================

Event-driven, Non-blocking I/O
-------------------------------------

At the core of EAvatar, Gevent is used as the event-driven, non-blocking I/O engine.
With the lightweight concurrency support and thread-like programming model,
it a pleasure again to write asynchronous I/O codes.


Restrictive Execution of Python Codes
-------------------------------------------

In addition to mainly developed in Python, EAvatar also uses Python as the
domain-specific language(DSL) for describing jobs. A job is defined by a script in Python
with very limited subset of features enabled.

A script is parsed into an abstract syntax tree with `ast` module,
and then being walked through to detect
invalid constructs such as 'import', 'print', 'functiondef', etc.
Without complex constructs, it makes writing scripts more approachable for average users.

XML Parsing
------------------

One of the design goals of EAvatar is to support web scraping.
To this end, 'lxml' package is bundled for efficient XML/HTML parsing.