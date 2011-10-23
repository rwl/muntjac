
from muntjac.api import VerticalLayout, CheckBox, Window, Label, Button
from muntjac.data.property import IValueChangeListener
from muntjac.ui.window import ICloseListener
from muntjac.ui.button import IClickListener


class SubwindowCloseExample(VerticalLayout):

    _openWindowText = 'Open a window'
    _closeWindowText = 'Close the window'


    def __init__(self):
        self._closableWindow = CheckBox('Allow user to close the window', True)
        self._closableWindow.setImmediate(True)

        class ClosableChangeListener(IValueChangeListener):

            def __init__(self, c):
                self._c = c

            def valueChange(self, event):
                self._c._subwindow.setClosable(bool(self._c._closableWindow))

        self._closableWindow.addListener(ClosableChangeListener(self))

        # Create the window
        self._subwindow = Window('A subwindow w/ close-listener')

        class CloseListener(ICloseListener):

            def __init__(self, c):
                self._c = c

            def windowClose(self, e):
                self._c.getWindow().showNotification("Window closed by user")
                self._c._openCloseButton.setCaption(self._c._openWindowText)

        self._subwindow.addListener(CloseListener(self))

        # Configure the windws layout; by default a VerticalLayout
        layout = self._subwindow.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)

        # Add some content; a label and a close-button
        message = Label('This is a subwindow with a close-listener.')
        self._subwindow.addComponent(message)

        # Add a button for opening the subwindow
        class ClickListener(IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                if (self._c._subwindow.getParent() is not None):
                    # window is already showing
                    self._c._subwindow.getParent().removeWindow(self._c._subwindow)

                    self._c._openCloseButton.setCaption(self._copenWindowText)
                else:
                    # Open the subwindow by adding it to the parent window
                    self._c.getWindow().addWindow(self._c._subwindow)
                    self._c._openCloseButton.setCaption(self._ccloseWindowText)

        self._c.openCloseButton = Button("Open window", ClickListener(self))

        self.setSpacing(True)
        self.addComponent(self._closableWindow)
        self.addComponent(self._openCloseButton)
