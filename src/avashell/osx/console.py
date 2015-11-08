# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

"""
Ava console for Cocoa GUI
"""

import logging

from AppKit import *

from .cocoa import Delegate


logger = logging.getLogger(__name__)


class ConsoleDelegate(Delegate):

    def init(self):
        s = super(ConsoleDelegate, self).init()
        if s is None:
            return self

        return self

    def windowWillClose_(self, aNotification):
        logger.debug("Console window will close.")

    def windowShouldClose_(self, sender):
        logger.debug("Console window should close.")
        self.console.hide()
        return False


class Console(object):
    def __init__(self, shell):
        self._wnd = None
        self._shell = shell

        self._title = 'Ava Console'

        self.position = (100, 100)
        self.size = (640, 480)

        self.setup_ui()
        self._delegate = None

    def setup_ui(self):
        # OSX origin is bottom left of screen, and the screen might be
        # offset relative to other screens. Adjust for this.
        screen = NSScreen.mainScreen().visibleFrame()
        position = NSMakeRect(
            screen.origin.x + self.position[0],
            screen.size.height + screen.origin.y - self.position[1] - self.size[1],
            self.size[0],
            self.size[1]
        )
        self._wnd = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            position,
            NSTitledWindowMask | NSClosableWindowMask | NSResizableWindowMask,
            NSBackingStoreBuffered,
            False
        )
        self._wnd.setTitle_(self._title)
        # self._delegate = ConsoleDelegate.alloc().init()
        # self._delegate.console = self
        self._wnd.setDelegate_(self._shell.delegate)

        self._splitview = NSSplitView.alloc().init()
        self._splitview.setVertical_(False)
        self._splitview.setTranslatesAutoresizingMaskIntoConstraints_(False)

        self._subview1 = NSScrollView.alloc().init()
        self._subview1.setHasVerticalScroller_(True)
        self._subview1.setHasHorizontalScroller_(False)
        self._subview1.setAutohidesScrollers_(False)
        self._subview1.setBorderType_(NSBezelBorder)
        self._subview1.setTranslatesAutoresizingMaskIntoConstraints_(False)

        self._subview2 = NSScrollView.alloc().init()
        self._subview2.setHasVerticalScroller_(True)
        self._subview2.setHasHorizontalScroller_(False)
        self._subview2.setAutohidesScrollers_(False)
        self._subview2.setBorderType_(NSBezelBorder)
        self._subview2.setTranslatesAutoresizingMaskIntoConstraints_(False)

        self._text = NSTextView.alloc().init()


        self._text.setEditable_(True)
        self._text.setVerticallyResizable_(True)
        self._text.setHorizontallyResizable_(True)

        self._messages = NSTextView.alloc().init()


        self._messages.setEditable_(False)
        self._messages.setVerticallyResizable_(True)
        self._messages.setHorizontallyResizable_(True)

        self._subview1.setDocumentView_(self._messages)
        self._subview2.setDocumentView_(self._text)

        self._splitview.addSubview_(self._subview1)
        self._splitview.addSubview_(self._subview2)
        self._wnd.setContentView_(self._splitview)

        btn_frame = NSMakeRect(20, 20, 15, 5)
        submit_btn = NSButton.alloc().initWithFrame_(btn_frame)
        submit_btn.setTitle_('Submit')
        self._splitview.addSubview_(submit_btn)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self

        # Assign the widget to the same app as the window.
        self.content.app = self.app

        # Top level widnow items don't layout well with autolayout (especially when
        # they are scroll views); so revert to old-style autoresize masks for the
        # main content view.
        self._content._impl.setTranslatesAutoresizingMaskIntoConstraints_(True)

        self._wnd.setContentView_(self._content._impl)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        if self._title:
            self._wnd.setTitle_(self._title)
        else:
            self._wnd.setTitle_('')

    def show(self):
        self._wnd.orderFrontRegardless()
        # self._impl.visualizeConstraints_(self._impl.contentView.constraints())

    def hide(self):
        self._wnd.orderOut_(None)

    def on_close(self):
        pass


if __name__ == '__main__':
    console = Console(None)
    console.show()
    app = NSApplication.sharedApplication()
    app.activateIgnoringOtherApps_(True)
    app.run()
