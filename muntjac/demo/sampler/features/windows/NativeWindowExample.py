
from datetime import datetime

from muntjac.demo.sampler.features.windows.NativeWindow import NativeWindow

from muntjac.ui import VerticalLayout
from muntjac.ui import Window, Label, button, Button, Link
from muntjac.ui.window import ICloseListener

from muntjac.terminal.external_resource import ExternalResource


class NativeWindowExample(VerticalLayout):

    def __init__(self):
        self.setSpacing(True)

        # Add a button for opening the window
        class OpenListener(button.IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                window = NativeWindow()
                # Add the window to the application
                self.getApplication().addWindow(window)
                # Get the URL for the window, and open that in a new
                # browser window, in this case in a small window.
                self._c.getWindow().open(ExternalResource(window.getURL()),
                        '_blank', 500, 200, Window.BORDER_NONE)

        opn = Button('Open native window', OpenListener(self))
        self.addComponent(opn)

        # Add a link for opening sampler in a new window; this will cause
        # Sampler's getWindow() to create a new Window.
        openSampler = Link('Open Sampler in a new window',
            ExternalResource('#'),
            '_blank', 700, 500, Link.TARGET_BORDER_NONE)
        self.addComponent(openSampler)

# We'll be instantiating the same window multiple times, so we'll make
# an inner class for separation. You could of course just create a new
# Window() and addCompoent to that instead.
class NativeWindow(Window):

    def __init__(self):
        # Configure the layout
        layout = self.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)

        # Add some content; a label and a close-button
        message = Label('This is a native window, created at '
                + datetime.today())
        self.addComponent(message)

        # It's a good idea to remove the window when it's closed (also
        # when the browser window 'x' is used), unless you explicitly
        # want the window to persist (if it's not removed from the
        # application, it can still be retrieved from it's URL.

        class WindowCloseListener(ICloseListener):

            def __init__(self, w):
                self._w = w

            def windowClose(self, e):
                # remove from application
                self._w.getApplication().removeWindow(self._w)

        self.addListener(WindowCloseListener(self))
