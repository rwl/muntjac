# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.windows.NativeWindow import (NativeWindow,)
# from java.util.Date import (Date,)


class NativeWindowExample(VerticalLayout):

    def __init__(self):
        # We'll be instantiating the same window multiple times, so we'll make an
        # inner class for separation. You could of course just create a new
        # Window() and addCompoent to that instead.

        self.setSpacing(True)
        # Add a button for opening the window

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                window = NativeWindowExample_this.NativeWindow()
                # Add the window to the application
                self.getApplication().addWindow(window)
                # Get the URL for the window, and open that in a new
                # browser window, in this case in a small window.
                self.getWindow().open(ExternalResource(window.getURL()), '_blank', 500, 200, Window.BORDER_NONE)
                # URL
                # window name
                # width
                # weight

        _0_ = _0_()
        open = Button('Open native window', _0_)
        self.addComponent(open)
        # Add a link for opening sampler in a new window; this will cause
        # Sampler's getWindow() to create a new Window.
        openSampler = Link('Open Sampler in a new window', ExternalResource('#'), '_blank', 700, 500, Link.TARGET_BORDER_NONE)
        self.addComponent(openSampler)

    class NativeWindow(Window):

        def __init__(self):
            # Configure the layout
            layout = self.getContent()
            layout.setMargin(True)
            layout.setSpacing(True)
            # Add some content; a label and a close-button
            message = ALabel('This is a native window, created at ' + Date())
            self.addComponent(message)
            # It's a good idea to remove the window when it's closed (also
            # when the browser window 'x' is used), unless you explicitly
            # want the window to persist (if it's not removed from the
            # application, it can still be retrieved from it's URL.
            NativeWindow_this = self

            class _0_(self.CloseListener):

                def windowClose(self, e):
                    # remove from application
                    self.getApplication().removeWindow(NativeWindow_this)

            _0_ = _0_()
            self.addListener(_0_)
