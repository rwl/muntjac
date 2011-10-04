# -*- coding: utf-8 -*-
# from com.vaadin.ui.Window.CloseEvent import (CloseEvent,)


class SubwindowCloseExample(VerticalLayout):
    _openWindowText = 'Open a window'
    _closeWindowText = 'Close the window'
    _subwindow = None
    _openCloseButton = None
    _closableWindow = None

    def __init__(self):
        self._closableWindow = CheckBox('Allow user to close the window', True)
        self._closableWindow.setImmediate(True)

        class _0_(ValueChangeListener):

            def valueChange(self, event):
                SubwindowCloseExample_this._subwindow.setClosable(SubwindowCloseExample_this._closableWindow.booleanValue())

        _0_ = _0_()
        self._closableWindow.addListener(_0_)
        # Create the window
        self._subwindow = Window('A subwindow w/ close-listener')
        # subwindow.addListener(new Window.CloseListener() {
        # // inline close-listener
        # public void windowClose(CloseEvent e) {
        # getWindow().showNotification("Window closed by user");
        # openCloseButton.setCaption(openWindowText);
        # }
        # });
        # Configure the windws layout; by default a VerticalLayout
        layout = self._subwindow.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)
        # Add some content; a label and a close-button
        message = Label('This is a subwindow with a close-listener.')
        self._subwindow.addComponent(message)
        # Add a button for opening the subwindow
        # openCloseButton = new Button("Open window", new Button.ClickListener() {
        # // inline click-listener
        # public void buttonClick(ClickEvent event) {
        # if (subwindow.getParent() != null) {
        # // window is already showing
        # (subwindow.getParent()).removeWindow(subwindow);
        # openCloseButton.setCaption(openWindowText);
        # } else {
        # // Open the subwindow by adding it to the parent window
        # getWindow().addWindow(subwindow);
        # openCloseButton.setCaption(closeWindowText);
        # }
        # }
        # });
        self.setSpacing(True)
        self.addComponent(self._closableWindow)
        self.addComponent(self._openCloseButton)
