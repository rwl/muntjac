
from muntjac.ui import VerticalLayout, Window, Label, button, Button, Alignment


class SubwindowPositionedExample(VerticalLayout):

    def __init__(self):
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

        class CloseListener(button.IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                # close the window by removing it from the parent window
                self._c._subwindow.getParent().removeWindow(self._c._subwindow)

        close = Button('Close', CloseListener(self))

        # The components added to the window are actually added to the window's
        # layout; you can use either. Alignments are set using the layout
        layout.addComponent(close)
        layout.setComponentAlignment(close, Alignment.BOTTOM_RIGHT)

        # Add buttons for opening the subwindow
        class OpenListener50(button.IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                if self._c._subwindow.getParent() is None:
                    # Open the subwindow by adding it to the parent
                    # window
                    self.getWindow().addWindow(self._c._subwindow)
                # Set window position
                self._c._subwindow.setPositionX(50)
                self._c._subwindow.setPositionY(50)

        fifty = Button('Open window at position 50x50', OpenListener50(self))
        self.addComponent(fifty)

        class OpenListener150(button.IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                if self._c._subwindow.getParent() is None:
                    # Open the subwindow by adding it to the parent
                    # window
                    self.getWindow().addWindow(self._c._subwindow)
                # Set window position
                self._c._subwindow.setPositionX(150)
                self._c._subwindow.setPositionY(200)

        onefifty = Button('Open window at position 150x200',
                OpenListener150(self))
        self.addComponent(onefifty)

        class CenterListener(button.IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                if self._c._subwindow.getParent() is None:
                    # Open the subwindow by adding it to the parent
                    # window
                    self.getWindow().addWindow(self._c._subwindow)
                # Center the window
                self._c._subwindow.center()

        center = Button('Open centered window', CenterListener(self))
        self.addComponent(center)
