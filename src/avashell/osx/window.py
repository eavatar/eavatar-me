# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from Foundation import *
from AppKit import *


class WindowDelegate(NSObject):
    def windowWillClose_(self, notification):
        self.__dict__['interface'].on_close()

    ######################################################################
    # Toolbar delegate methods
    ######################################################################


class Window(object):
    def __init__(self, title=None, position=(100, 100), size=(640, 480), toolbar=None):
        self._impl = None
        self._app = None
        self._toolbar = None

        self.position = position
        self.size = size

        self.startup()

        self.title = title
        self.toolbar = toolbar

        print("Window created!")

    def startup(self):
        # OSX origin is bottom left of screen, and the screen might be
        # offset relative to other screens. Adjust for this.
        screen = NSScreen.mainScreen().visibleFrame()
        position = NSMakeRect(
            screen.origin.x + self.position[0],
            screen.size.height + screen.origin.y - self.position[1] - self.size[1],
            self.size[0],
            self.size[1]
        )
        self._impl = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            position,
            NSTitledWindowMask | NSClosableWindowMask | NSResizableWindowMask | NSMiniaturizableWindowMask,
            NSBackingStoreBuffered,
            False
        )
        self._impl.setFrame_display_animate_(position, True, False)

        self._delegate = WindowDelegate.alloc().init()
        self._delegate.__dict__['interface'] = self

        self._impl.setDelegate_(self._delegate)

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app

    @property
    def toolbar(self):
        return self._toolbar

    @toolbar.setter
    def toolbar(self, toolbar):
        self._toolbar = toolbar
        if self._toolbar:
            self._toolbar_items = dict((item.toolbar_identifier, item) for item in self._toolbar)
            self._toolbar_impl = NSToolbar.alloc().initWithIdentifier_('Toolbar-%s' % id(self))
            self._toolbar_impl.setDelegate_(self._delegate)
            self._impl.setToolbar_(self._toolbar_impl)

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

        self._impl.setContentView_(self._content._impl)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        if self._title:
            self._impl.setTitle_(self._title)
        else:
            self._impl.setTitle_('')

    def show(self):
        self._impl.makeKeyAndOrderFront_(None)
        # self._impl.visualizeConstraints_(self._impl.contentView.constraints())

    def on_close(self):
        pass