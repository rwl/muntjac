# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class WindowingExample(CustomComponent):
    """@author marc
     *
    """
    txt = '<p>There are two main types of windows: application-level windows, and ' + '\"sub windows\".</p><p>A sub window is rendered as a \"inline\" popup window' + ' within the (native) browser window to which it was added. You can create' + ' a sub window by creating a new Window and adding it to a application-level window, for instance' + ' your main window. </p><p> In contrast, you create a application-level window by' + ' creating a new Window and adding it to the Application. Application-level' + ' windows are not shown by default - you need to open a browser window for' + ' the url representing the window. You can think of the application-level' + ' windows as separate views into your application - and a way to create a' + ' \"native\" browser window.</p><p>Depending on your needs, it\'s also' + ' possible to create a new window instance (with it\'s own internal state)' + ' for each new (native) browser window, or you can share the same instance' + ' (and state) between several browser windows (the latter is most useful' + ' for read-only views).</p>'
    _windowUrl = None

    def __init__(self):
        main = VerticalLayout()
        main.setMargin(True)
        self.setCompositionRoot(main)
        l = Label(self.txt)
        # l.setContentMode(Label.CONTENT_XHTML);
        main.addComponent(l)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                w = Window('Subwindow')
                w.setWidth('50%')
                l = Label(WindowingExample_this.txt)
                # l.setContentMode(Label.CONTENT_XHTML);
                w.addComponent(l)
                self.getApplication().getMainWindow().addWindow(w)

        _0_ = _0_()
        b = Button('Create a new subwindow', _0_)
        b.setStyleName(BaseTheme.BUTTON_LINK)
        main.addComponent(b)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                w = Window('Modal window')
                w.setWidth('50%')
                w.setModal(True)
                l = Label(WindowingExample_this.txt)
                # l.setContentMode(Label.CONTENT_XHTML);
                w.addComponent(l)
                self.getApplication().getMainWindow().addWindow(w)

        _0_ = _0_()
        Button('Create a new modal window', _0_)
        b = _0_
        b.setStyleName(BaseTheme.BUTTON_LINK)
        main.addComponent(b)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                if WindowingExample_this._windowUrl is None:
                    w = Window('Subwindow')
                    l = Label(WindowingExample_this.txt)
                    # l.setContentMode(Label.CONTENT_XHTML);
                    w.addComponent(l)
                    self.getApplication().addWindow(w)
                    WindowingExample_this._windowUrl = w.getURL()
                self.getApplication().getMainWindow().open(ExternalResource(WindowingExample_this._windowUrl), '_new')

        _0_ = _0_()
        Button('Open a application-level window, with shared state', _0_)
        b = _0_
        b.setStyleName(BaseTheme.BUTTON_LINK)
        main.addComponent(b)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                w = Window('Subwindow')
                self.getApplication().addWindow(w)
                l = Label('Each opened window has its own' + ' name, and is accessed trough its own uri.')
                l.setCaption('Window ' + w.getName())
                w.addComponent(l)
                self.getApplication().getMainWindow().open(ExternalResource(w.getURL()), '_new')

        _0_ = _0_()
        Button('Create a new application-level window, with it\'s own state', _0_)
        b = _0_
        b.setStyleName(BaseTheme.BUTTON_LINK)
        main.addComponent(b)
