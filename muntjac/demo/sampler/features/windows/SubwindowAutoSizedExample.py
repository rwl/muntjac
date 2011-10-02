# -*- coding: utf-8 -*-


class SubwindowAutoSizedExample(VerticalLayout):
    _subwindow = None

    def __init__(self):
        # Create the window
        self._subwindow = Window('Automatically sized subwindow')
        # Configure the windws layout; by default a VerticalLayout
        layout = self._subwindow.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)
        # make it undefined for auto-sizing window
        layout.setSizeUndefined()
        # Add some content;
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 7):
                break
            tf = TextField()
            tf.setWidth('400px')
            self._subwindow.addComponent(tf)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                # close the window by removing it from the parent window
                SubwindowAutoSizedExample_this._subwindow.getParent().removeWindow(SubwindowAutoSizedExample_this._subwindow)

        _0_ = _0_()
        close = Button('Close', _0_)
        # The components added to the window are actually added to the window's
        # layout; you can use either. Alignments are set using the layout
        layout.addComponent(close)
        layout.setComponentAlignment(close, Alignment.BOTTOM_RIGHT)
        # Add a button for opening the subwindow

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                if SubwindowAutoSizedExample_this._subwindow.getParent() is not None:
                    # window is already showing
                    self.getWindow().showNotification('Window is already open')
                else:
                    # Open the subwindow by adding it to the parent
                    # window
                    self.getWindow().addWindow(SubwindowAutoSizedExample_this._subwindow)

        _0_ = _0_()
        open = Button('Open sized window', _0_)
        self.addComponent(open)
