
from datetime import datetime

from muntjac.demo.sampler.features.windows.NativeWindow import NativeWindow

from muntjac.api import VerticalLayout
from muntjac.api import Window, Label, Button, Link
from muntjac.ui.window import ICloseListener
from muntjac.ui import button

from muntjac.terminal.external_resource import ExternalResource


class NativeWindowExample(VerticalLayout):

    def __init__(self):
        super(NativeWindowExample, self).__init__()

        self.setSpacing(True)

        # Add a button for opening the window
        opn = Button('Open native window', OpenListener(self))
        self.addComponent(opn)

        # Add a link for opening sampler in a new window; this will cause
        # Sampler's getWindow() to create a new Window.
        openSampler = Link('Open Sampler in a new window',
            ExternalResource('#'),  # FIXME: sampler url
            '_blank', 700, 500, Link.TARGET_BORDER_NONE)
        self.addComponent(openSampler)


class OpenListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        window = NativeWindow()
        # Add the window to the application
        self._c.getApplication().addWindow(window)
        # Get the URL for the window, and open that in a new
        # browser window, in this case in a small window.
        self._c.getWindow().open(ExternalResource(window.getURL()),
                '_blank', 500, 200, Window.BORDER_NONE)


# We'll be instantiating the same window multiple times, so we'll make
# an inner class for separation. You could of course just create a new
# Window() and addCompoent to that instead.
class NativeWindow(Window):

    def __init__(self):
        super(NativeWindow, self).__init__()

        # Configure the layout
        layout = self.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)

        # Add some content; a label and a close-button
        message = Label('This is a native window, created at '
                + str(datetime.today()))
        self.addComponent(message)

        # It's a good idea to remove the window when it's closed (also
        # when the browser window 'x' is used), unless you explicitly
        # want the window to persist (if it's not removed from the
        # application, it can still be retrieved from it's URL.
        self.addListener(WindowCloseListener(self), ICloseListener)


class WindowCloseListener(ICloseListener):

    def __init__(self, w):
        self._w = w

    def windowClose(self, e):
        # remove from application
        self._w.getApplication().removeWindow(self._w)
