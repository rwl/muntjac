# -*- coding: utf-8 -*-


class SubwindowPositionedExample(VerticalLayout):
    _subwindow = None

    def __init__(self):
        self.setSpacing(True)
        # Create the window
        self._subwindow = Window('A positioned subwindow')
        # let's give it a size (optional)
        self._subwindow.setWidth('300px')
        self._subwindow.setHeight('200px')
        # Configure the windws layout; by default a VerticalLayout
        layout = self._subwindow.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)
        # make it fill the whole window
        layout.setSizeFull()
        # Add some content; a label and a close-button
        message = Label('This is a positioned window')
        self._subwindow.addComponent(message)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                # close the window by removing it from the parent window
                SubwindowPositionedExample_this._subwindow.getParent().removeWindow(SubwindowPositionedExample_this._subwindow)

        _0_ = _0_()
        close = Button('Close', _0_)
        # The components added to the window are actually added to the window's
        # layout; you can use either. Alignments are set using the layout
        layout.addComponent(close)
        layout.setComponentAlignment(close, Alignment.BOTTOM_RIGHT)
        # Add buttons for opening the subwindow

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                if SubwindowPositionedExample_this._subwindow.getParent() is None:
                    # Open the subwindow by adding it to the parent
                    # window
                    self.getWindow().addWindow(SubwindowPositionedExample_this._subwindow)
                # Set window position
                SubwindowPositionedExample_this._subwindow.setPositionX(50)
                SubwindowPositionedExample_this._subwindow.setPositionY(50)

        _0_ = _0_()
        fifty = Button('Open window at position 50x50', _0_)
        self.addComponent(fifty)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                if SubwindowPositionedExample_this._subwindow.getParent() is None:
                    # Open the subwindow by adding it to the parent
                    # window
                    self.getWindow().addWindow(SubwindowPositionedExample_this._subwindow)
                # Set window position
                SubwindowPositionedExample_this._subwindow.setPositionX(150)
                SubwindowPositionedExample_this._subwindow.setPositionY(200)

        _0_ = _0_()
        onefifty = Button('Open window at position 150x200', _0_)
        self.addComponent(onefifty)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                if SubwindowPositionedExample_this._subwindow.getParent() is None:
                    # Open the subwindow by adding it to the parent
                    # window
                    self.getWindow().addWindow(SubwindowPositionedExample_this._subwindow)
                # Center the window
                SubwindowPositionedExample_this._subwindow.center()

        _0_ = _0_()
        center = Button('Open centered window', _0_)
        self.addComponent(center)
