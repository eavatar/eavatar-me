Frequently Asked Questions
==================================

Where is my working folder for Avame?
------------------------------------------------------

Avame creates a per-user application folder when runs for the first time.
The location is dependent on the operating system, following are the typical paths:

* Mac OS X:
    ~/Library/Application Support/avame
* Mac OS X (POSIX):
    ~/.avame
* Ubuntu:
    ~/.config/avame
* Win 7 (roaming):
    C:\\Users\\<user>\\AppData\\Roaming\\avame
* Win 7 (not roaming):
    C:\\Users\\<user>\\AppData\\Local\\avame


How do I add auto-run jobs when Avame starts?
--------------------------------------------------

Simply add the script file (with extension .py) to the subfolder 'jobs' under the
Avame's working folder, and then restart Avame. It will be started if it's a correct script.

