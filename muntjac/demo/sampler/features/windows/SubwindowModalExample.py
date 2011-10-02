# -*- coding: utf-8 -*-


class SubwindowModalExample(VerticalLayout):
    _subwindow = None

    def __init__(self):
        # Create the window...
        self._subwindow = Window('A modal subwindow')
        # ...and make it modal
        self._subwindow.setModal(True)
        # Configure the windws layout; by default a VerticalLayout
        layout = self._subwindow.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)
        # Add some content; a label and a close-button
        message = ALabel('This is a modal subwindow.')
        self._subwindow.addComponent(message)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                # close the window by removing it from the parent window
                SubwindowModalExample_this._subwindow.getParent().removeWindow(SubwindowModalExample_this._subwindow)

        _0_ = _0_()
        close = Button('Close', _0_)
        # The components added to the window are actually added to the window's
        # layout; you can use either. Alignments are set using the layout
        layout.addComponent(close)
        layout.setComponentAlignment(close, Alignment.TOP_RIGHT)
        # Add a button for opening the subwindow

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                if SubwindowModalExample_this._subwindow.getParent() is not None:
                    # window is already showing
                    self.getWindow().showNotification('Window is already open')
                else:
                    # Open the subwindow by adding it to the parent
                    # window
                    self.getWindow().addWindow(SubwindowModalExample_this._subwindow)

        _0_ = _0_()
        open = Button('Open modal window', _0_)
        self.addComponent(open)
