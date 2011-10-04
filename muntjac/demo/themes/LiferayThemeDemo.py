# -*- coding: utf-8 -*-
# from com.vaadin.event.Action import (Action,)
# from com.vaadin.terminal.Resource import (Resource,)
# from com.vaadin.ui.Button.ClickListener import (ClickListener,)
# from com.vaadin.ui.NativeButton import (NativeButton,)
# from com.vaadin.ui.PopupView import (PopupView,)
# from com.vaadin.ui.TabSheet.Tab import (Tab,)
# from com.vaadin.ui.VerticalSplitPanel import (VerticalSplitPanel,)
# from com.vaadin.ui.themes.LiferayTheme import (LiferayTheme,)
# from java.util.Locale import (Locale,)


class LiferayThemeDemo(Application):
    _DATE = Date(2009 - 1900, 6 - 1, 2)
    _ICON_GLOBE = ThemeResource('../runo/icons/16/globe.png')
    _ICON_OK = ThemeResource('../runo/icons/16/ok.png')
    _main = None
    _mainLayout = None
    _tabs = None

    class handler(Action.Handler):

        def handleAction(self, action, sender, target):
            # NOP
            pass

        def getActions(self, target, sender):
            return [Action('Open'), Action('Delete', ThemeResource('../runo/icons/16/trash.png'))]

    def init(self):
        self._main = Window('Vaadin Liferay Theme')
        self._mainLayout = self._main.getContent()
        self._mainLayout.setMargin(False)
        self.setMainWindow(self._main)
        # setTheme("liferay");
        self.buildMainView()

    def buildMainView(self):
        self._mainLayout.setWidth('100%')
        self._mainLayout.setHeight('400px')
        self._mainLayout.addComponent(self.getTopMenu())
        margin = CssLayout()
        margin.setMargin(False, True, True, True)
        margin.setSizeFull()
        self._tabs = TabSheet()
        self._tabs.setSizeFull()
        margin.addComponent(self._tabs)
        self._mainLayout.addComponent(margin)
        self._mainLayout.setExpandRatio(margin, 1)
        self._tabs.addComponent(self.buildLabels())
        self._tabs.addComponent(self.buildButtons())
        self._tabs.addComponent(self.buildTextFields())
        self._tabs.addComponent(self.buildSelects())
        self._tabs.addComponent(self.buildDateFields())
        self._tabs.addComponent(self.buildSliders())
        self._tabs.addComponent(self.buildTabSheets())
        self._tabs.addComponent(self.buildAccordions())
        self._tabs.addComponent(self.buildPanels())
        self._tabs.addComponent(self.buildTables())
        self._tabs.addComponent(self.buildTrees())
        self._tabs.addComponent(self.buildWindows())
        self._tabs.addComponent(self.buildSplitPanels())
        self._tabs.addComponent(self.buildNotifications())
        self._tabs.addComponent(self.buildPopupViews())

    def buildLabels(self):
        l = GridLayout(2, 1)
        l.setWidth('560px')
        l.setSpacing(True)
        l.setMargin(True)
        l.setCaption('Labels')
        l.addComponent(Label('Normal Label', Label.CONTENT_XHTML))
        l.addComponent(Label('Lorem ipsum dolor sit amet, consectetur adipiscing elit.'))
        return l

    def buildButtons(self):
        l = GridLayout(3, 1)
        l.setCaption('Buttons')
        l.setMargin(True)
        l.setSpacing(True)
        b = Button('Normal Button')
        b.setDescription('This is a tooltip!')
        l.addComponent(b)
        b = NativeButton('Native Button')
        b.setDescription('<h2><img src=\"/html/VAADIN/themes/runo/icons/16/globe.png\"/>A richtext tooltip</h2>' + '<ul>' + '<li>HTML formatting</li><li>Images<br/>' + '</li><li>etc...</li></ul>')
        l.addComponent(b)
        b = CheckBox('Checkbox')
        l.addComponent(b)
        b = Button('Disabled')
        b.setEnabled(False)
        l.addComponent(b)
        b = NativeButton('Disabled')
        b.setEnabled(False)
        l.addComponent(b)
        b = CheckBox('Disabled')
        b.setEnabled(False)
        l.addComponent(b)
        b = Button('OK')
        b.setIcon(self._ICON_OK)
        l.addComponent(b)
        b = NativeButton('OK')
        b.setIcon(self._ICON_OK)
        l.addComponent(b)
        b = CheckBox('OK')
        b.setIcon(self._ICON_OK)
        l.addComponent(b)
        b = Button('Link Button')
        b.setStyleName(LiferayTheme.BUTTON_LINK)
        l.addComponent(b)
        b = NativeButton('Link Button')
        b.setStyleName(LiferayTheme.BUTTON_LINK)
        l.addComponent(b)
        l.newLine()
        b = Button('Link Button')
        b.setIcon(self._ICON_OK)
        b.setStyleName(LiferayTheme.BUTTON_LINK)
        l.addComponent(b)
        b = NativeButton('Link Button')
        b.setIcon(self._ICON_OK)
        b.setStyleName(LiferayTheme.BUTTON_LINK)
        l.addComponent(b)
        return l

    def buildTextFields(self):
        l = GridLayout(2, 1)
        l.setCaption('Text fields')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('400px')
        l.setColumnExpandRatio(0, 1)
        l.addComponent(Label('Normal TextField', Label.CONTENT_XHTML))
        tf = TextField()
        tf.setInputPrompt('Enter text')
        l.addComponent(tf)
        l.addComponent(Label('Normal TextArea', Label.CONTENT_XHTML))
        tf = TextField()
        tf.setHeight('5em')
        tf.setInputPrompt('Enter text')
        l.addComponent(tf)
        return l

    def buildSelects(self):
        l = VerticalLayout()
        l.setCaption('Selects')
        l.setMargin(True)
        l.setSpacing(True)
        hl = HorizontalLayout()
        hl.setSpacing(True)
        hl.setMargin(True, False, False, False)
        l.addComponent(hl)
        cb = ComboBox()
        nat = NativeSelect()
        list = ListSelect()
        twincol = TwinColSelect()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 50):
                break
            cb.addItem('Item ' + i)
            nat.addItem('Item ' + i)
            list.addItem('Item ' + i)
            twincol.addItem('Item ' + i)
        hl.addComponent(cb)
        hl.addComponent(nat)
        hl.addComponent(list)
        hl.addComponent(twincol)
        return l

    def buildDateFields(self):
        l = VerticalLayout()
        l.setCaption('Date fields')
        l.setMargin(True)
        l.setSpacing(True)
        hl = HorizontalLayout()
        hl.setSpacing(True)
        hl.setMargin(True, False, False, False)
        l.addComponent(hl)
        df = DateField()
        df.setValue(self._DATE)
        df.setResolution(DateField.RESOLUTION_MIN)
        hl.addComponent(df)
        df = InlineDateField()
        df.setLocale(Locale('fi', 'FI'))
        df.setShowISOWeekNumbers(True)
        df.setValue(self._DATE)
        df.setResolution(DateField.RESOLUTION_DAY)
        hl.addComponent(df)
        df = InlineDateField()
        df.setValue(self._DATE)
        df.setResolution(DateField.RESOLUTION_YEAR)
        hl.addComponent(df)
        return l

    def buildTabSheets(self):
        l = VerticalLayout()
        l.setCaption('Tabs')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('400px')
        closable = CheckBox('Closable tabs')
        closable.setImmediate(True)
        l.addComponent(closable)
        ts = TabSheet()
        ts.setHeight('100px')
        l.addComponent(ts)
        _0 = True
        i = 1
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 10):
                break
            t = ts.addTab(Label(), 'Tab ' + i, None)
            if i % 2 == 0:
                t.setIcon(self._ICON_GLOBE)
            if i == 2:
                t.setEnabled(False)

        class _1_(Button.ClickListener):

            def buttonClick(self, event):
                it = self.ts.getComponentIterator()
                _0 = True
                while True:
                    if _0 is True:
                        _0 = False
                    if not it.hasNext():
                        break
                    c = it.next()
                    self.ts.getTab(c).setClosable(event.getButton().booleanValue())

        _1_ = _1_()
        closable.addListener(_1_)
        return l

    def buildPanels(self):
        l = GridLayout(2, 1)
        l.setCaption('Panels')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('700px')
        l.setColumnExpandRatio(0, 2)
        l.setColumnExpandRatio(1, 5)
        l.addComponent(Label('Normal Panel', Label.CONTENT_XHTML))
        p = Panel('Normal Panel')
        p.setHeight('100px')
        p.addComponent(Label('Panel content'))
        l.addComponent(p)
        l.addComponent(Label('Light Style (<code>LiferayTheme.PANEL_LIGHT</code>)', Label.CONTENT_XHTML))
        p2 = Panel('Light Style Panel')
        p2.setStyleName(LiferayTheme.PANEL_LIGHT)
        p2.addComponent(Label('Panel content'))
        l.addComponent(p2)
        return l

    def buildTables(self):
        l = GridLayout(1, 1)
        l.setCaption('Tables')
        l.setMargin(True)
        l.setSpacing(True)
        t = Table()
        t.setWidth('700px')
        t.setPageLength(4)
        t.setSelectable(True)
        t.setColumnCollapsingAllowed(True)
        t.setColumnReorderingAllowed(True)
        t.addActionHandler(self.handler)
        t.addContainerProperty('First', str, None, 'First', self._ICON_GLOBE, Table.ALIGN_RIGHT)
        t.addContainerProperty('Second', str, None)
        t.addContainerProperty('Third', str, None)
        t.addContainerProperty('Fourth', TextField, None)
        t.setColumnCollapsed('Fourth', True)
        sum = 0
        _0 = True
        j = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                j += 1
            if not (j < 100):
                break
            t.addItem([j, 'Bar value ' + j, 'Last column value ' + j, TextField()], j)
            sum += j
        t.setFooterVisible(True)
        t.setColumnFooter('First', '' + sum)
        l.addComponent(t)
        return l

    def buildWindows(self):
        l = CssLayout()
        l.setCaption('Windows')
        w = Window('Normal window')
        w.setWidth('280px')
        w.setHeight('180px')
        w.setPositionX(40)
        w.setPositionY(160)
        w2 = Window('Window, no resize')
        w2.setResizable(False)
        w2.setWidth('280px')
        w2.setHeight('180px')
        w2.setPositionX(350)
        w2.setPositionY(160)
        w2.addComponent(Label('<code>Window.setResizable(false)</code>', Label.CONTENT_XHTML))

        class _2_(TabSheet.SelectedTabChangeListener):

            def selectedTabChange(self, event):
                if event.getTabSheet().getSelectedTab() == self.l:
                    self.getMainWindow().addWindow(self.w)
                    self.getMainWindow().addWindow(self.w2)
                else:
                    self.getMainWindow().removeWindow(self.w)
                    self.getMainWindow().removeWindow(self.w2)

        _2_ = _2_()
        self._tabs.addListener(_2_)
        return l

    def buildSplitPanels(self):
        l = GridLayout(2, 1)
        l.setCaption('Split panels')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('700px')
        l.setHeight('100%')
        l.setColumnExpandRatio(1, 1)
        lockCheckBox = CheckBox('Lock SplitPanels')
        lockCheckBox.setImmediate(True)
        l.addComponent(lockCheckBox, 1, 0)
        l.newLine()
        label = Label('Normal SplitPanel', Label.CONTENT_XHTML)
        label.setWidth(None)
        l.addComponent(label)
        sp = HorizontalSplitPanel()
        sp.setWidth('100%')
        sp.setHeight('100px')
        sp2 = VerticalSplitPanel()
        sp2.setSizeFull()
        sp.setSecondComponent(sp2)
        l.addComponent(sp)
        label = Label('Small Style<br />(<code>LiferayTheme.SPLITPANEL_SMALL</code>)', Label.CONTENT_XHTML)
        label.setWidth(None)
        l.addComponent(label)
        sp3 = HorizontalSplitPanel()
        sp3.setStyleName(LiferayTheme.SPLITPANEL_SMALL)
        sp3.setWidth('100%')
        sp3.setHeight('100px')
        sp4 = VerticalSplitPanel()
        sp4.setStyleName(LiferayTheme.SPLITPANEL_SMALL)
        sp4.setSizeFull()
        sp3.setSecondComponent(sp4)
        l.addComponent(sp3)

        class _3_(ClickListener):

            def buttonClick(self, event):
                self.sp.setLocked(event.getButton().booleanValue())
                self.sp2.setLocked(event.getButton().booleanValue())
                self.sp3.setLocked(event.getButton().booleanValue())
                self.sp4.setLocked(event.getButton().booleanValue())

        _3_ = _3_()
        lockCheckBox.addListener(_3_)
        return l

    def buildAccordions(self):
        l = GridLayout(2, 1)
        l.setCaption('Accordions')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('700px')
        a = Accordion()
        a.setWidth('100%')
        a.setHeight('170px')
        l.addComponent(a)
        _0 = True
        i = 1
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 5):
                break
            t = a.addTab(Label(), 'Sheet ' + i, None)
            if i % 2 == 0:
                t.setIcon(self._ICON_GLOBE)
            if i == 2:
                t.setEnabled(False)
        return l

    def buildSliders(self):
        l = GridLayout(2, 1)
        l.setCaption('Sliders')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('400px')
        l.setColumnExpandRatio(0, 1)
        l.addComponent(Label('Horizontal Slider', Label.CONTENT_XHTML))
        s = Slider()
        s.setWidth('200px')
        # TODO Auto-generated catch block
        try:
            s.setValue(50)
        except ValueOutOfBoundsException, e:
            e.printStackTrace()
        l.addComponent(s)
        l.addComponent(Label('Vertical Slider', Label.CONTENT_XHTML))
        s = Slider()
        s.setOrientation(Slider.ORIENTATION_VERTICAL)
        s.setHeight('200px')
        # TODO Auto-generated catch block
        try:
            s.setValue(50)
        except ValueOutOfBoundsException, e:
            e.printStackTrace()
        l.addComponent(s)
        return l

    def buildTrees(self):
        l = GridLayout(1, 1)
        l.setMargin(True)
        l.setCaption('Trees')
        tree = Tree()
        l.addComponent(tree)
        tree.addItem('Item 1')
        tree.setItemIcon('Item 1', self._ICON_GLOBE)
        tree.addItem('Child 1')
        tree.setItemIcon('Child 1', self._ICON_GLOBE)
        tree.setParent('Child 1', 'Item 1')
        tree.addItem('Child 2')
        tree.setParent('Child 2', 'Item 1')
        tree.addItem('Child 3')
        tree.setChildrenAllowed('Child 3', False)
        tree.setItemIcon('Child 3', self._ICON_GLOBE)
        tree.setParent('Child 3', 'Item 1')
        tree.addItem('Child 4')
        tree.setChildrenAllowed('Child 4', False)
        tree.setParent('Child 4', 'Item 1')
        tree.addItem('Item 2')
        tree.addItem('Item 3')
        tree.setItemIcon('Item 3', self._ICON_GLOBE)
        tree.setChildrenAllowed('Item 3', False)
        tree.addItem('Item 4')
        tree.setChildrenAllowed('Item 4', False)
        tree.addActionHandler(self.handler)
        return l

    def buildNotifications(self):
        l = GridLayout(2, 1)
        l.setCaption('Notifications')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('400px')
        l.setColumnExpandRatio(0, 1)
        title = TextField('Notification caption')
        title.setValue('Brown Fox!')
        message = TextField('Notification description')
        message.setValue('Jumped over the lazy dog.')
        message.setWidth('15em')
        l.addComponent(Label('<h3>Type</h3>', Label.CONTENT_XHTML))
        l.addComponent(Label('<h3>Preview</h3>', Label.CONTENT_XHTML))
        l.addComponent(Label('Humanized', Label.CONTENT_XHTML))

        class _4_(Button.ClickListener):

            def buttonClick(self, event):
                event.getButton().getWindow().showNotification(self.title.getValue(), self.message.getValue())

        _4_ = _4_()
        show = Button('Humanized Notification', _4_)
        l.addComponent(show)
        l.addComponent(Label('Warning', Label.CONTENT_XHTML))

        class _4_(Button.ClickListener):

            def buttonClick(self, event):
                event.getButton().getWindow().showNotification(self.title.getValue(), self.message.getValue(), Notification.TYPE_WARNING_MESSAGE)

        _4_ = _4_()
        Button('Warning Notification', _4_)
        show = _4_
        l.addComponent(show)
        l.addComponent(Label('Error', Label.CONTENT_XHTML))

        class _4_(Button.ClickListener):

            def buttonClick(self, event):
                event.getButton().getWindow().showNotification(self.title.getValue(), self.message.getValue(), Notification.TYPE_ERROR_MESSAGE)

        _4_ = _4_()
        Button('Error Notification', _4_)
        show = _4_
        l.addComponent(show)
        l.addComponent(Label('Tray', Label.CONTENT_XHTML))

        class _4_(Button.ClickListener):

            def buttonClick(self, event):
                event.getButton().getWindow().showNotification(self.title.getValue(), self.message.getValue(), Notification.TYPE_TRAY_NOTIFICATION)

        _4_ = _4_()
        Button('Tray Notification', _4_)
        show = _4_
        l.addComponent(show)
        l.addComponent(title)
        l.addComponent(message)
        return l

    def buildPopupViews(self):
        l = GridLayout(1, 1)
        l.setCaption('PopupViews')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('400px')
        content = Label('Lorem ipsum dolor sit amet, consectetur adipiscing elit.')
        content.setWidth('200px')
        pw = PopupView('Click me!', content)
        l.addComponent(pw)
        return l

    def getTopMenu(self):
        menubar = MenuBar()
        menubar.setWidth('100%')
        file = menubar.addItem('File', None)
        newItem = file.addItem('New', None)
        file.addItem('Open file...', ThemeResource('../runo/icons/16/folder.png'), None)
        file.addSeparator()
        newItem.addItem('File', None)
        newItem.addItem('Folder', None)
        newItem.addItem('Project...', None)
        file.addItem('Close', None)
        file.addItem('Close All', None)
        file.addSeparator()
        file.addItem('Save', None)
        file.addItem('Save As...', None)
        file.addItem('Save All', None)
        edit = menubar.addItem('Edit', None)
        edit.addItem('Undo', None)
        edit.addItem('Redo', None).setEnabled(False)
        edit.addSeparator()
        edit.addItem('Cut', None)
        edit.addItem('Copy', None)
        edit.addItem('Paste', None)
        edit.addSeparator()
        find = edit.addItem('Find/Replace', None)

        class _4_(Command):

            def menuSelected(self, selectedItem):
                self.getMainWindow().open(ExternalResource('http://www.google.com'))

        _4_ = _4_()
        find.addItem('Google Search', _4_)
        find.addSeparator()
        find.addItem('Find/Replace...', None)
        find.addItem('Find Next', None)
        find.addItem('Find Previous', None)
        view = menubar.addItem('View', ThemeResource('../runo/icons/16/user.png'), None)
        statusBarItem = view.addItem('Show/Hide Status Bar', None)
        statusBarItem.setCheckable(True)
        statusBarItem.setChecked(True)
        view.addItem('Customize Toolbar...', None)
        view.addSeparator()
        view.addItem('Actual Size', None)
        view.addItem('Zoom In', None)
        view.addItem('Zoom Out', None)
        menubar.addItem('Help', None).setEnabled(False)
        return menubar
