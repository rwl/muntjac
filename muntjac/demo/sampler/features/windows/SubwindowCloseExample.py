
from muntjac.api import VerticalLayout, CheckBox, Window, Label, Button
from muntjac.data.property import IValueChangeListener
from muntjac.ui.window import ICloseListener
from muntjac.ui.button import IClickListener


class SubwindowCloseExample(VerticalLayout):

    _openWindowText = 'Open a window'
    _closeWindowText = 'Close the window'


    def __init__(self):
        super(SubwindowCloseExample, self).__init__()

        self._closableWindow = CheckBox('Allow user to close the window', True)
        self._closableWindow.setImmediate(True)

        self._closableWindow.addListener(ClosableChangeListener(self),
                IValueChangeListener)

        # Create the window
        self._subwindow = Window('A subwindow w/ close-listener')

        self._subwindow.addListener(CloseListener(self), ICloseListener)

        # Configure the windws layout; by default a VerticalLayout
        layout = self._subwindow.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)

        # Add some content; a label and a close-button
        message = Label('This is a subwindow with a close-listener.')
        self._subwindow.addComponent(message)

        # Add a button for opening the subwindow
        self._openCloseButton = Button("Open window", ClickListener(self))

        self.setSpacing(True)
        self.addComponent(self._closableWindow)
        self.addComponent(self._openCloseButton)


class ClosableChangeListener(IValueChangeListener):

    def __init__(self, c):
        self._c = c

    def valueChange(self, event):
        self._c._subwindow.setClosable(self._c._closableWindow.booleanValue())


class CloseListener(ICloseListener):

    def __init__(self, c):
        self._c = c

    def windowClose(self, e):
        self._c.getWindow().showNotification("Window closed by user")
        self._c._openCloseButton.setCaption(self._c._openWindowText)


class ClickListener(IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        if (self._c._subwindow.getParent() is not None):
            # window is already showing
            self._c._subwindow.getParent().removeWindow(self._c._subwindow)

            self._c._openCloseButton.setCaption(self._c._openWindowText)
        else:
            # Open the subwindow by adding it to the parent window
            self._c.getWindow().addWindow(self._c._subwindow)
            self._c._openCloseButton.setCaption(self._c._closeWindowText)
