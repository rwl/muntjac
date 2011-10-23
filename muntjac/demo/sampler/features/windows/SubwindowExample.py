
from muntjac.api import VerticalLayout, Window, Label, button, Button, Alignment


class SubwindowExample(VerticalLayout):

    def __init__(self):
        # Create the window
        self._subwindow = Window('A subwindow')

        # Configure the windows layout; by default a VerticalLayout
        layout = self._subwindow.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)

        # Add some content; a label and a close-button
        message = Label('This is a subwindow')
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
        layout.setComponentAlignment(close, Alignment.TOP_RIGHT)

        # Add a button for opening the subwindow
        class OpenListener(button.IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                if self._c._subwindow.getParent() is not None:
                    # window is already showing
                    self.getWindow().showNotification('Window is already open')
                else:
                    # Open the subwindow by adding it to the parent window
                    self.getWindow().addWindow(self._c._subwindow)

        opn = Button('Open subwindow', OpenListener(self))
        self.addComponent(opn)
