
from muntjac.api import VerticalLayout, Window, Label, Button, Alignment
from muntjac.ui import button

class SubwindowPositionedExample(VerticalLayout):

    def __init__(self):
        super(SubwindowPositionedExample, self).__init__()

        self.setSpacing(True)
        # Create the window
        self._subwindow = Window('A positioned subwindow')

        # let's give it a size (optional)
        self._subwindow.setWidth('300px')
        self._subwindow.setHeight('200px')

        # Configure the windows layout; by default a VerticalLayout
        layout = self._subwindow.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)

        # make it fill the whole window
        layout.setSizeFull()

        # Add some content; a label and a close-button
        message = Label('This is a positioned window')
        self._subwindow.addComponent(message)

        close = Button('Close', CloseListener(self))

        # The components added to the window are actually added to the window's
        # layout; you can use either. Alignments are set using the layout
        layout.addComponent(close)
        layout.setComponentAlignment(close, Alignment.BOTTOM_RIGHT)

        # Add buttons for opening the subwindow
        fifty = Button('Open window at position 50x50', OpenListener50(self))
        self.addComponent(fifty)

        onefifty = Button('Open window at position 150x200',
                OpenListener150(self))
        self.addComponent(onefifty)

        center = Button('Open centered window', CenterListener(self))
        self.addComponent(center)


class CloseListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        # close the window by removing it from the parent window
        self._c._subwindow.getParent().removeWindow(self._c._subwindow)


class OpenListener50(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        if self._c._subwindow.getParent() is None:
            # Open the subwindow by adding it to the parent
            # window
            self._c.getWindow().addWindow(self._c._subwindow)
        # Set window position
        self._c._subwindow.setPositionX(50)
        self._c._subwindow.setPositionY(50)


class OpenListener150(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        if self._c._subwindow.getParent() is None:
            # Open the subwindow by adding it to the parent
            # window
            self._c.getWindow().addWindow(self._c._subwindow)
        # Set window position
        self._c._subwindow.setPositionX(150)
        self._c._subwindow.setPositionY(200)


class CenterListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        if self._c._subwindow.getParent() is None:
            # Open the subwindow by adding it to the parent
            # window
            self._c.getWindow().addWindow(self._c._subwindow)
        # Center the window
        self._c._subwindow.center()
