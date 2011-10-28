
from muntjac.api import VerticalLayout, Window, Label, Button, Alignment
from muntjac.ui.button import IClickListener


class SubwindowModalExample(VerticalLayout):

    def __init__(self):
        super(SubwindowModalExample, self).__init__()

        # Create the window...
        self._subwindow = Window('A modal subwindow')
        # ...and make it modal
        self._subwindow.setModal(True)

        # Configure the windws layout; by default a VerticalLayout
        layout = self._subwindow.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)

        # Add some content; a label and a close-button
        message = Label('This is a modal subwindow.')
        self._subwindow.addComponent(message)

        close = Button('Close', CloseListener(self))

        # The components added to the window are actually added to the window's
        # layout; you can use either. Alignments are set using the layout
        layout.addComponent(close)
        layout.setComponentAlignment(close, Alignment.TOP_RIGHT)

        # Add a button for opening the subwindow
        opn = Button('Open modal window', OpenListener(self))
        self.addComponent(opn)


class CloseListener(IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        # close the window by removing it from the parent window
        self._c._subwindow.getParent().removeWindow(self._c._subwindow)


class OpenListener(IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        if self._c._subwindow.getParent() is not None:
            # window is already showing
            self._c.getWindow().showNotification('Window is already open')
        else:
            # Open the subwindow by adding it to the parent
            # window
            self._c.getWindow().addWindow(self._c._subwindow)
