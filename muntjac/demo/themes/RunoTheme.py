# -*- coding: utf-8 -*-
# from com.vaadin.data.Item import (Item,)
# from com.vaadin.event.LayoutEvents.LayoutClickEvent import (LayoutClickEvent,)
# from com.vaadin.event.LayoutEvents.LayoutClickListener import (LayoutClickListener,)
# from com.vaadin.terminal.Sizeable import (Sizeable,)
# from com.vaadin.terminal.ThemeResource import (ThemeResource,)
# from com.vaadin.ui.AbsoluteLayout import (AbsoluteLayout,)
# from com.vaadin.ui.Accordion import (Accordion,)
# from com.vaadin.ui.ComponentContainer import (ComponentContainer,)
# from com.vaadin.ui.Embedded import (Embedded,)
# from com.vaadin.ui.FormLayout import (FormLayout,)
# from com.vaadin.ui.OptionGroup import (OptionGroup,)
# from com.vaadin.ui.Slider import (Slider,)
# from com.vaadin.ui.Slider.ValueOutOfBoundsException import (ValueOutOfBoundsException,)
# from com.vaadin.ui.Tree import (Tree,)
# from com.vaadin.ui.Window.Notification import (Notification,)
# from com.vaadin.ui.themes.Runo import (Runo,)


class RunoTheme(Application):
    _DATEFIELD_VALUE = Date(2010 - 1900, 7 - 1, 19, 14, 46, 0)
    _right = TabSheet()
    _styles = TabSheet()
    _samples = TabSheet()

    def init(self):
        self.setTheme(Runo.themeName())
        root = VerticalLayout()
        root.setMargin(True)
        root.setSizeFull()
        main = Window('Vaadin Runo Theme', root)
        self.setMainWindow(main)
        title = ALabel('Vaadin Runo Theme')
        title.addStyleName(Runo.LABEL_H1)
        title.setSizeUndefined()
        root.addComponent(title)
        root.setComponentAlignment(title, Alignment.TOP_CENTER)
        slogan = ALabel('Presenting a Stylish Alternative for the Traditional Desktop-Look')
        slogan.addStyleName(Runo.LABEL_SMALL)
        slogan.setSizeUndefined()
        root.addComponent(slogan)
        root.setComponentAlignment(slogan, Alignment.TOP_CENTER)
        spacer = ALabel('')
        spacer.setHeight('20px')
        root.addComponent(spacer)
        split = HorizontalSplitPanel()
        split.setStyleName(Runo.SPLITPANEL_REDUCED)
        split.setSplitPosition(1, Sizeable.UNITS_PIXELS)
        split.setLocked(True)
        root.addComponent(split)
        root.setExpandRatio(split, 1)
        left = Panel('Example Sidebar')
        left.setSizeFull()
        split.setFirstComponent(left)
        accordion = Accordion()
        accordion.setSizeFull()
        left.setContent(accordion)
        accordion.addTab(self.buildTree(), 'Pages', None)
        accordion.addTab(ALabel(''), 'Preferences', None)
        accordion.addTab(ALabel(''), 'Quick Search', None)
        self._right.setSizeFull()
        # right.addStyleName(Runo.TABSHEET_SMALL);
        split.setSecondComponent(self._right)
        split.setLocked(True)
        self._right.addTab(self.buildWelcomeScreen(), 'Welcome', None)
        self._right.addTab(self.buildSamples(), 'Sample Layouts', None)
        self._right.addTab(self.buildStyleReference(), 'Style Reference', None)

        class _0_(TabSheet.SelectedTabChangeListener):

            def selectedTabChange(self, event):
                if RunoTheme_this._right.getSelectedTab() == RunoTheme_this._samples:
                    self.split.setSplitPosition(25, Sizeable.UNITS_PERCENTAGE)
                    self.split.setLocked(False)
                else:
                    self.split.setSplitPosition(1, Sizeable.UNITS_PIXELS)
                    self.split.setLocked(True)

        _0_ = _0_()
        self._right.addListener(_0_)

    def buildTree(self):
        margin = CssLayout()
        margin.setWidth('100%')
        margin.setMargin(True, False, True, True)
        t = Tree()
        t.addItem('Archive')
        t.select('Archive')
        t.setItemIcon('Archive', ThemeResource('icons/16/calendar.png'))
        self.createTreeItem(t, 'January', 'Archive')
        self.createTreeItem(t, 'February', 'Archive')
        self.createTreeItem(t, 'March', 'Archive')
        self.createTreeItem(t, 'April', 'Archive')
        self.createTreeItem(t, 'May', 'Archive')
        self.createTreeItem(t, 'June', 'Archive')
        self.createTreeItem(t, 'July', 'Archive')
        self.createTreeItem(t, 'August', 'Archive')
        self.createTreeItem(t, 'September', 'Archive')
        self.createTreeItem(t, 'October', 'Archive')
        self.createTreeItem(t, 'November', 'Archive')
        self.createTreeItem(t, 'December', 'Archive')
        t.addItem('Personal Files')
        t.setItemIcon('Personal Files', ThemeResource('icons/16/document.png'))
        self.createTreeItem(t, 'Photos', 'Personal Files')
        self.createTreeItem(t, 'Videos', 'Personal Files')
        self.createTreeItem(t, 'Audio', 'Personal Files')
        self.createTreeItem(t, 'Documents', 'Personal Files')
        t.expandItem('Personal Files')
        t.addItem('Company Storage')
        t.setItemIcon('Company Storage', ThemeResource('icons/16/folder.png'))
        self.createTreeItem(t, 'Books', 'Company Storage')
        self.createTreeItem(t, 'Development', 'Company Storage')
        self.createTreeItem(t, 'Staff Peripherals', 'Company Storage')
        self.createTreeItem(t, 'Photo Enthusiasts', 'Company Storage')
        t.expandItem('Company Storage')
        t.setItemIcon('Photo Enthusiasts', ThemeResource('icons/16/users.png'))
        t.setChildrenAllowed('Photo Enthusiasts', False)
        margin.addComponent(t)
        # Spacing
        margin.addComponent(ALabel('&nbsp;', ALabel.CONTENT_XHTML))
        text = ALabel('The above tree and the example screens on the right don\'t actually do anything, they are here purely for show.')
        text.addStyleName(Runo.LABEL_SMALL)
        margin.addComponent(text)
        text.setWidth('90%')
        return margin

    def createTreeItem(self, tree, caption, parent):
        tree.addItem(caption)
        if parent is not None:
            tree.setChildrenAllowed(parent, True)
            tree.setParent(caption, parent)
            if parent == 'Archive':
                tree.setChildrenAllowed(caption, False)

    def buildWelcomeScreen(self):
        l = VerticalLayout()
        l.setSizeFull()
        l.setCaption('Welcome')
        welcome = Panel('Runo Theme')
        welcome.setSizeFull()
        welcome.addStyleName(Runo.PANEL_LIGHT)
        l.addComponent(welcome)
        l.setExpandRatio(welcome, 1)
        margin = CssLayout()
        margin.setMargin(True)
        margin.setWidth('100%')
        welcome.setContent(margin)
        title = ALabel('Runo Theme')
        title.addStyleName(Runo.LABEL_H1)
        # margin.addComponent(title);
        texts = HorizontalLayout()
        texts.setSpacing(True)
        texts.setWidth('100%')
        margin.addComponent(texts)
        text = ALabel('<h3>A Complete Theme</h3><p>The Runo theme is a complete, general purpose theme suitable for many types of applications.</p><p>The name Runo is a Finnish word, meaning \"a poem\" in English. It is also used to refer to a very particular kind of female reindeer.</p>', ALabel.CONTENT_XHTML)
        texts.addComponent(text)
        texts.setExpandRatio(text, 1)
        # Spacer
        text = ALabel('')
        text.setWidth('20px')
        texts.addComponent(text)
        text = ALabel('<h3>Everything You Need Is Here</h3><p>Everything you see inside this application, all the different styles, are provided by the Runo theme, out-of-the-box. That means you don\'t necessarily need to create any custom CSS for your application: you can build a cohesive result writing plain Java code.</p><p>A little creativity, good organization and careful typography carries a long way.</p>', ALabel.CONTENT_XHTML)
        texts.addComponent(text)
        texts.setExpandRatio(text, 1)
        # Spacer
        text = ALabel('')
        text.setWidth('20px')
        texts.addComponent(text)
        text = ALabel('<h3>The Names of The Styles</h3><p>Look for a class named <code>Runo</code> inside the Vaadin JAR (<code>com.vaadin.ui.themes.Runo</code>).</p><p>All the available style names are documented and available there as constants, prefixed by component names, e.g. <code>Runo.BUTTON_SMALL</code>.</p>', ALabel.CONTENT_XHTML)
        texts.addComponent(text)
        texts.setExpandRatio(text, 1)
        l.addComponent(ALabel('<hr />', ALabel.CONTENT_XHTML))
        texts = HorizontalLayout()
        texts.addStyleName(Runo.LAYOUT_DARKER)
        texts.setSpacing(True)
        texts.setWidth('100%')
        texts.setMargin(True)
        l.addComponent(texts)
        text = ALabel('<h4>About This Application</h4>In addition to this welcome screen, you\'ll find the style name reference and sample views within the two other main tabs.', ALabel.CONTENT_XHTML)
        text.addStyleName(Runo.LABEL_SMALL)
        texts.addComponent(text)
        texts.setExpandRatio(text, 1)
        # Spacer
        text = ALabel('')
        text.setWidth('20px')
        texts.addComponent(text)

        class _1_(Button.ClickListener):

            def buttonClick(self, event):
                RunoTheme_this._right.setSelectedTab(RunoTheme_this._samples)

        _1_ = _1_()
        next = Button('View Samples »', _1_)
        next.setWidth('100%')
        next.addStyleName(Runo.BUTTON_DEFAULT)
        next.addStyleName(Runo.BUTTON_BIG)
        texts.addComponent(next)
        texts.setComponentAlignment(next, Alignment.BOTTOM_LEFT)
        texts.setExpandRatio(next, 1)
        # Spacer
        text = ALabel('')
        text.setWidth('20px')
        texts.addComponent(text)

        class _1_(Button.ClickListener):

            def buttonClick(self, event):
                RunoTheme_this._right.setSelectedTab(RunoTheme_this._styles)

        _1_ = _1_()
        Button('Style Reference »', _1_)
        next = _1_
        next.setWidth('100%')
        next.addStyleName(Runo.BUTTON_DEFAULT)
        next.addStyleName(Runo.BUTTON_BIG)
        texts.addComponent(next)
        texts.setComponentAlignment(next, Alignment.BOTTOM_LEFT)
        texts.setExpandRatio(next, 1)
        return l

    def buildStyleReference(self):
        self._styles.addStyleName(Runo.TABSHEET_SMALL)
        self._styles.setSizeFull()
        self._styles.addTab(self.buildLabels())
        self._styles.addTab(self.buildButtons())
        self._styles.addTab(self.buildTextFields())
        self._styles.addTab(self.buildSelects())
        self._styles.addTab(self.buildDateFields())
        self._styles.addTab(self.buildSliders())
        self._styles.addTab(self.buildTabSheets())
        self._styles.addTab(self.buildAccordions())
        self._styles.addTab(self.buildPanels())
        self._styles.addTab(self.buildSplitPanels())
        self._styles.addTab(self.buildTables())
        self._styles.addTab(self.buildWindows())
        self._styles.addTab(self.buildNotifications())
        self._styles.addTab(self.buildLayouts())
        return self._styles

    def buildLabels(self):
        l = GridLayout(2, 1)
        l.setWidth('560px')
        l.setSpacing(True)
        l.setMargin(True)
        l.setCaption('Labels')
        l.addComponent(ALabel('Header Style (<code>Runo.LABEL_H1</code>)', ALabel.CONTENT_XHTML))
        label = ALabel('Lorem Ipsum')
        label.addStyleName(Runo.LABEL_H1)
        l.addComponent(label)
        l.addComponent(ALabel('Sub-header Style (<code>Runo.LABEL_H2</code>)', ALabel.CONTENT_XHTML))
        label = ALabel('Lorem Ipsum Dolor')
        label.addStyleName(Runo.LABEL_H2)
        l.addComponent(label)
        l.addComponent(ALabel('Normal Label', ALabel.CONTENT_XHTML))
        l.addComponent(ALabel('Lorem ipsum dolor sit amet, consectetur adipiscing elit.'))
        l.addComponent(ALabel('Small Style (<code>Runo.LABEL_SMALL</code>)', ALabel.CONTENT_XHTML))
        label = ALabel('Lorem ipsum dolor sit amet, consectetur adipiscing elit.')
        label.addStyleName(Runo.LABEL_SMALL)
        l.addComponent(label)
        return l

    def buildButtons(self):
        l = GridLayout(2, 1)
        l.setCaption('Buttons')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('500px')
        l.setColumnExpandRatio(0, 1)
        l.addComponent(ALabel('Normal Button', ALabel.CONTENT_XHTML))
        b = Button('Normal Button')
        l.addComponent(b)
        l.addComponent(ALabel('\"Default\" Style<br />(<code>Runo.BUTTON_DEFAULT</code>)', ALabel.CONTENT_XHTML))
        b = Button('Default Button')
        b.setStyleName(Runo.BUTTON_DEFAULT)
        l.addComponent(b)
        l.addComponent(ALabel('Big Style<br />(<code>Runo.BUTTON_BIG</code>)', ALabel.CONTENT_XHTML))
        b = Button('Big Button')
        b.setStyleName(Runo.BUTTON_BIG)
        l.addComponent(b)
        l.addComponent(ALabel('Big Default<br />(<code>Runo.BUTTON_BIG & Runo.BUTTON_DEFAULT</code>)', ALabel.CONTENT_XHTML))
        b = Button('Big Default')
        b.setStyleName(Runo.BUTTON_BIG)
        b.addStyleName(Runo.BUTTON_DEFAULT)
        l.addComponent(b)
        l.addComponent(ALabel('Small Style<br />(<code>Runo.BUTTON_SMALL</code>)', ALabel.CONTENT_XHTML))
        b = Button('Small Button')
        b.setStyleName(Runo.BUTTON_SMALL)
        l.addComponent(b)
        l.addComponent(ALabel('Small Default<br />(<code>Runo.BUTTON_SMALL & Runo.BUTTON_DEFAULT</code>)', ALabel.CONTENT_XHTML))
        b = Button('Small Default')
        b.setStyleName(Runo.BUTTON_SMALL)
        b.addStyleName(Runo.BUTTON_DEFAULT)
        l.addComponent(b)
        l.addComponent(ALabel('Disabled Button<br />(<code>Button.setEnabled(false)</code>)', ALabel.CONTENT_XHTML))
        b = Button('Disabled Button')
        b.setEnabled(False)
        l.addComponent(b)
        l.addComponent(ALabel('Link Style<br />(<code>Runo.BUTTON_LINK</code>)', ALabel.CONTENT_XHTML))
        b = Button('Link Button')
        b.setStyleName(Runo.BUTTON_LINK)
        l.addComponent(b)
        return l

    def buildTextFields(self):
        l = GridLayout(2, 1)
        l.setCaption('Text fields')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('400px')
        l.setColumnExpandRatio(0, 1)
        l.addComponent(ALabel('Normal TextField', ALabel.CONTENT_XHTML))
        tf = TextField()
        tf.setInputPrompt('Enter text')
        l.addComponent(tf)
        l.addComponent(ALabel('Small Style (<code>Runo.TEXTFIELD_SMALL</code>)', ALabel.CONTENT_XHTML))
        tf = TextField()
        tf.setStyleName(Runo.TEXTFIELD_SMALL)
        tf.setInputPrompt('Enter text')
        l.addComponent(tf)
        l.addComponent(ALabel('Normal TextArea', ALabel.CONTENT_XHTML))
        tf = TextField()
        tf.setHeight('5em')
        tf.setInputPrompt('Enter text')
        l.addComponent(tf)
        l.addComponent(ALabel('Small Style TextArea (<code>Runo.TEXTFIELD_SMALL</code>)', ALabel.CONTENT_XHTML))
        tf = TextField()
        tf.setHeight('5em')
        tf.setStyleName(Runo.TEXTFIELD_SMALL)
        tf.setInputPrompt('Enter text')
        l.addComponent(tf)
        return l

    def buildSelects(self):
        l = VerticalLayout()
        l.setCaption('Selects')
        l.setMargin(True)
        l.setSpacing(True)
        l.addComponent(ALabel('Selects don\'t currently have any additional style names.'))
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
            if not (i < 25):
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
        l.addComponent(ALabel('Date fields don\'t currently have any additional style names.'))
        hl = HorizontalLayout()
        hl.setSpacing(True)
        hl.setMargin(True, False, False, False)
        l.addComponent(hl)
        df = DateField()
        df.setValue(self._DATEFIELD_VALUE)
        df.setResolution(DateField.RESOLUTION_MIN)
        hl.addComponent(df)
        df = InlineDateField()
        df.setValue(self._DATEFIELD_VALUE)
        df.setResolution(DateField.RESOLUTION_DAY)
        hl.addComponent(df)
        df = InlineDateField()
        df.setValue(self._DATEFIELD_VALUE)
        df.setResolution(DateField.RESOLUTION_YEAR)
        hl.addComponent(df)
        return l

    def buildTabSheets(self):
        l = GridLayout(2, 1)
        l.setCaption('Tabs')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('700px')
        l.setColumnExpandRatio(0, 3)
        l.setColumnExpandRatio(1, 5)
        checks = HorizontalLayout()
        checks.setSpacing(True)
        closable = CheckBox('Closable tabs')
        closable.setImmediate(True)
        checks.addComponent(closable)
        l.addComponent(checks, 1, 0)
        l.setCursorX(0)
        l.setCursorY(1)
        l.addComponent(ALabel('Normal Tabs', ALabel.CONTENT_XHTML))
        ts = TabSheet()
        ts.setHeight('100px')
        l.addComponent(ts)
        l.addComponent(ALabel('Small Style (<code>Runo.TABSHEET_SMALL</code>)', ALabel.CONTENT_XHTML))
        ts2 = TabSheet()
        ts2.setStyleName(Runo.TABSHEET_SMALL)
        l.addComponent(ts2)
        _0 = True
        i = 1
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 10):
                break
            ts.addTab(ALabel(), 'Tab ' + i, None)
            ts2.addTab(ALabel(), 'Tab ' + i, None)

        class _1_(Button.ClickListener):

            def buttonClick(self, event):
                it = self.ts.getComponentIterator()
                it2 = self.ts2.getComponentIterator()
                _0 = True
                while True:
                    if _0 is True:
                        _0 = False
                    if not it.hasNext():
                        break
                    c = it.next()
                    self.ts.getTab(c).setClosable(event.getButton().booleanValue())
                _1 = True
                while True:
                    if _1 is True:
                        _1 = False
                    if not it2.hasNext():
                        break
                    c = it2.next()
                    self.ts2.getTab(c).setClosable(event.getButton().booleanValue())

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
        l.addComponent(ALabel('Normal Panel', ALabel.CONTENT_XHTML))
        p = Panel('Normal Panel')
        p.addComponent(ALabel('Panel content'))
        l.addComponent(p)
        l.addComponent(ALabel('Light Style (<code>Runo.PANEL_LIGHT</code>)', ALabel.CONTENT_XHTML))
        p2 = Panel('Light Style Panel')
        p2.setStyleName('light')
        p2.addComponent(ALabel('Panel content'))
        l.addComponent(p2)
        return l

    def buildTables(self):
        l = GridLayout(2, 1)
        l.setCaption('Tables')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('700px')
        l.setColumnExpandRatio(0, 3)
        l.setColumnExpandRatio(1, 5)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 4):
                break
            t = Table()
            t.setWidth('100%')
            t.setPageLength(3)
            t.setSelectable(True)
            t.setColumnCollapsingAllowed(True)
            t.setColumnReorderingAllowed(True)
            if i == 2:
                t.setStyleName(Runo.TABLE_SMALL)
                l.addComponent(ALabel('Small Style (<code>Runo.TABLE_SMALL</code>)', ALabel.CONTENT_XHTML))
            elif i == 1:
                t.setStyleName(Runo.TABLE_BORDERLESS)
                l.addComponent(ALabel('Borderless Style (<code>Runo.TABLE_BORDERLESS</code>)', ALabel.CONTENT_XHTML))
            elif i == 3:
                t.setStyleName(Runo.TABLE_BORDERLESS)
                t.addStyleName(Runo.TABLE_SMALL)
                l.addComponent(ALabel('Borderless & Small (<code>Runo.TABLE_BORDERLESS & Runo.TABLE_SMALL</code>)', ALabel.CONTENT_XHTML))
            else:
                l.addComponent(ALabel('Normal Table', ALabel.CONTENT_XHTML))
            t.addContainerProperty('First', str, None)
            t.addContainerProperty('Second', str, None)
            t.addContainerProperty('Third', str, None)
            _1 = True
            j = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    j += 1
                if not (j < 100):
                    break
                t.addItem(['Foo ' + j, 'Bar value ' + j, 'Last column value ' + j], j)
            l.addComponent(t)
        return l

    def buildWindows(self):
        l = CssLayout()
        l.setCaption('Windows')
        w = Window('Normal Window')
        w.setWidth('250px')
        w.setHeight('180px')
        w.setPositionX(120)
        w.setPositionY(200)
        w2 = Window('Dialog Window')
        w2.setWidth('250px')
        w2.setHeight('180px')
        w2.setStyleName('dialog')
        w2.setPositionX(400)
        w2.setPositionY(200)
        w2.addComponent(ALabel('<code>Runo.WINDOW_DIALOG</code>', ALabel.CONTENT_XHTML))
        w2.getContent().addStyleName(Runo.LAYOUT_DARKER)

        class reveal(TabSheet.SelectedTabChangeListener):

            def selectedTabChange(self, event):
                if (
                    RunoTheme_this._right.getSelectedTab() == RunoTheme_this._styles and RunoTheme_this._styles.getSelectedTab() == self.l
                ):
                    self.getMainWindow().addWindow(self.w)
                    self.getMainWindow().addWindow(self.w2)
                else:
                    self.getMainWindow().removeWindow(self.w)
                    self.getMainWindow().removeWindow(self.w2)

        self._styles.addListener(reveal)
        self._right.addListener(reveal)
        return l

    def buildSplitPanels(self):
        l = GridLayout(2, 1)
        l.setCaption('Split panels')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('400px')
        l.setColumnExpandRatio(0, 1)
        checks = HorizontalLayout()
        checks.setSpacing(True)
        locked = CheckBox('Locked')
        locked.setDescription('Prevent split dragging')
        locked.setImmediate(True)
        checks.addComponent(locked)
        l.addComponent(checks, 1, 0)
        l.setCursorX(0)
        l.setCursorY(1)
        l.addComponent(ALabel('Normal SplitPanel', ALabel.CONTENT_XHTML))
        sp = HorizontalSplitPanel()
        sp.setWidth('100px')
        sp.setHeight('120px')
        l.addComponent(sp)
        l.addComponent(ALabel('Reduced Style (<code>Runo.SPLITPANEL_REDUCED</code>)', ALabel.CONTENT_XHTML))
        sp2 = HorizontalSplitPanel()
        sp2.setStyleName(Runo.SPLITPANEL_REDUCED)
        sp2.setWidth('100px')
        sp2.setHeight('120px')
        l.addComponent(sp2)
        l.addComponent(ALabel('Small Style (<code>Runo.SPLITPANEL_SMALL</code>)', ALabel.CONTENT_XHTML))
        sp3 = HorizontalSplitPanel()
        sp3.setStyleName(Runo.SPLITPANEL_SMALL)
        sp3.setWidth('100px')
        sp3.setHeight('120px')
        l.addComponent(sp3)

        class _3_(Button.ClickListener):

            def buttonClick(self, event):
                self.sp.setLocked(event.getButton().booleanValue())
                self.sp2.setLocked(event.getButton().booleanValue())
                self.sp3.setLocked(event.getButton().booleanValue())

        _3_ = _3_()
        locked.addListener(_3_)
        return l

    def buildAccordions(self):
        l = GridLayout(2, 1)
        l.setCaption('Accordions')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('600px')
        l.setColumnExpandRatio(0, 1)
        l.setColumnExpandRatio(1, 2)
        l.addComponent(ALabel('Normal Accordion', ALabel.CONTENT_XHTML))
        a = Accordion()
        a.setWidth('100%')
        a.setHeight('170px')
        l.addComponent(a)
        l.addComponent(ALabel('Light Style<br />(<code>Runo.ACCORDION_LIGHT</code>)', ALabel.CONTENT_XHTML))
        a2 = Accordion()
        a2.setWidth('100%')
        a2.setHeight('170px')
        a2.addStyleName(Runo.ACCORDION_LIGHT)
        l.addComponent(a2)
        _0 = True
        i = 1
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 4):
                break
            a.addTab(ALabel(), 'Sheet ' + i, None)
            a2.addTab(ALabel(), 'Sheet ' + i, None)
        return l

    def buildSliders(self):
        l = GridLayout(2, 1)
        l.setCaption('Sliders')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('400px')
        l.setColumnExpandRatio(0, 1)
        l.addComponent(ALabel('Normal Slider', ALabel.CONTENT_XHTML))
        s = Slider()
        s.setWidth('200px')
        # TODO Auto-generated catch block
        try:
            s.setValue(50)
        except ValueOutOfBoundsException, e:
            e.printStackTrace()
        l.addComponent(s)
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
        l.addComponent(ALabel('<h3>Type</h3>', ALabel.CONTENT_XHTML))
        l.addComponent(ALabel('<h3>Preview</h3>', ALabel.CONTENT_XHTML))
        l.addComponent(ALabel('Humanized', ALabel.CONTENT_XHTML))

        class _4_(Button.ClickListener):

            def buttonClick(self, event):
                event.getButton().getWindow().showNotification(self.title.getValue(), self.message.getValue())

        _4_ = _4_()
        show = Button('Humanized Notification', _4_)
        l.addComponent(show)
        l.addComponent(ALabel('Warning', ALabel.CONTENT_XHTML))

        class _4_(Button.ClickListener):

            def buttonClick(self, event):
                event.getButton().getWindow().showNotification(self.title.getValue(), self.message.getValue(), Notification.TYPE_WARNING_MESSAGE)

        _4_ = _4_()
        Button('Warning Notification', _4_)
        show = _4_
        l.addComponent(show)
        l.addComponent(ALabel('Error', ALabel.CONTENT_XHTML))

        class _4_(Button.ClickListener):

            def buttonClick(self, event):
                event.getButton().getWindow().showNotification(self.title.getValue(), self.message.getValue(), Notification.TYPE_ERROR_MESSAGE)

        _4_ = _4_()
        Button('Error Notification', _4_)
        show = _4_
        l.addComponent(show)
        l.addComponent(ALabel('Tray', ALabel.CONTENT_XHTML))

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

    def buildLayouts(self):
        l = GridLayout(2, 1)
        l.setCaption('Layouts')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('550px')
        l.setColumnExpandRatio(0, 1)
        l.addComponent(ALabel('Box Shadow<br />(<code>Runo.CSSLAYOUT_SHADOW</code>)', ALabel.CONTENT_XHTML))
        layout = CssLayout()
        layout.addStyleName(Runo.CSSLAYOUT_SHADOW)
        text = ALabel('Content')
        text.setSizeUndefined()
        align = VerticalLayout()
        align.addStyleName(Runo.LAYOUT_DARKER)
        align.setWidth('100px')
        align.setHeight('100px')
        align.addComponent(text)
        align.setComponentAlignment(text, Alignment.MIDDLE_CENTER)
        layout.addComponent(align)
        l.addComponent(layout)
        l.addComponent(ALabel('Selectable<br />(<code>Runo.CSSLAYOUT_SELECTABLE</code> & <code>Runo.CSSLAYOUT_SELECTABLE_SELECTED</code>)', ALabel.CONTENT_XHTML))
        layout = CssLayout()
        layout.addStyleName(Runo.CSSLAYOUT_SELECTABLE)
        layout.addStyleName(Runo.CSSLAYOUT_SELECTABLE_SELECTED)

        class _4_(LayoutClickListener):

            def layoutClick(self, event):
                if (
                    event.getComponent().getStyleName().contains(Runo.CSSLAYOUT_SELECTABLE_SELECTED)
                ):
                    event.getComponent().removeStyleName(Runo.CSSLAYOUT_SELECTABLE_SELECTED)
                else:
                    event.getComponent().addStyleName(Runo.CSSLAYOUT_SELECTABLE_SELECTED)

        _4_ = _4_()
        layout.addListener(_4_)
        text = ALabel('Click here')
        text.setSizeUndefined()
        align = VerticalLayout()
        align.setWidth('100px')
        align.setHeight('100px')
        align.addComponent(text)
        align.setComponentAlignment(text, Alignment.MIDDLE_CENTER)
        layout.addComponent(align)
        l.addComponent(layout)
        return l

    def buildSamples(self):
        self._samples.addStyleName(Runo.TABSHEET_SMALL)
        self._samples.setSizeFull()
        self._samples.addTab(self.buildLibraryScreen())
        self._samples.addTab(self.buildBillingScreen())
        return self._samples

    def buildBillingScreen(self):
        root = AbsoluteLayout()
        root.setSizeFull()
        root.setCaption('Time Tracking')
        buttons = HorizontalLayout()
        buttons.setSpacing(True)

        class _5_(Button.ClickListener):

            def buttonClick(self, event):
                w = Window('Add Hours')
                w.addStyleName(Runo.WINDOW_DIALOG)
                w.setModal(True)
                w.setResizable(False)
                w.setCloseShortcut(KeyCode.ESCAPE, None)
                l = FormLayout()
                l.setSizeUndefined()
                w.setContent(l)
                l.setMargin(True)
                l.setSpacing(True)
                s = NativeSelect('Hour Type:')
                s.addItem('Billed')
                s.addItem('Not billed')
                s.setNullSelectionAllowed(False)
                s.select('Billed')
                l.addComponent(s)
                s.focus()
                l.addComponent(ComboBox('Description:'))
                l.addComponent(TextField('Notes:'))
                buttons = HorizontalLayout()
                buttons.setSpacing(True)
                b = Button('Add')
                b.addStyleName(Runo.BUTTON_DEFAULT)
                buttons.addComponent(b)
                buttons.addComponent(Button('Cancel'))
                l.addComponent(buttons)
                event.getButton().getWindow().addWindow(w)

        _5_ = _5_()
        b = Button('+ Add Hours', _5_)
        b.addStyleName(Runo.BUTTON_DEFAULT)
        buttons.addComponent(b)

        class _5_(Button.ClickListener):

            def buttonClick(self, event):
                w = Window('Generate Workhours Report')
                w.setPositionX(50)
                w.setPositionY(70)
                w.setResizable(False)
                w.setCloseShortcut(KeyCode.ESCAPE, None)
                root = GridLayout(2, 3)
                root.setMargin(True)
                root.setSpacing(True)
                w.setContent(root)
                format = CssLayout()
                opt = OptionGroup('1. Select output format')
                opt.addItem('Excel sheet')
                opt.addItem('CSV plain text')
                opt.select('CSV plain text')
                format.addComponent(opt)
                csv = ComboBox()
                csv.setWidth('170px')
                csv.addItem('Separate by comma (,)')
                csv.addItem('Separate by colon (:)')
                csv.addItem('Separate by semicolon (;)')
                csv.setNullSelectionAllowed(False)
                csv.select('Separate by comma (,)')
                margin = CssLayout()
                margin.setMargin(False, False, True, True)
                margin.addComponent(csv)
                format.addComponent(margin)
                root.addComponent(format)
                res = CssLayout()
                res.setCaption('Output resolution')
                slider = Slider()
                # Ignore
                try:
                    slider.setValue(30)
                except ValueOutOfBoundsException, e:
                    pass # astStmt: [Stmt([]), None]
                res.addComponent(slider)
                slider.setWidth('200px')
                labels = HorizontalLayout()
                labels.setWidth('200px')
                text = ALabel('Coarse info')
                text.setSizeUndefined()
                text.addStyleName(Runo.LABEL_SMALL)
                labels.addComponent(text)
                text = ALabel('Fine details')
                text.setSizeUndefined()
                text.addStyleName(Runo.LABEL_SMALL)
                labels.addComponent(text)
                labels.setComponentAlignment(text, Alignment.TOP_RIGHT)
                res.addComponent(labels)
                root.addComponent(res)
                rec = ComboBox('2. Select recepient')
                rec.addItem('john.doe@example.org')
                rec.addItem('harry.driver@example.org')
                rec.addItem('guybrush.threepwood@melee.mi')
                rec.setNewItemsAllowed(True)
                root.addComponent(rec)
                rec.setWidth('188px')
                buttons = HorizontalLayout()
                buttons.setSpacing(True)
                b = Button('Generate')
                b.addStyleName(Runo.BUTTON_DEFAULT)
                buttons.addComponent(b)
                b = Button('Cancel')
                buttons.addComponent(b)
                root.addComponent(buttons, 0, 2, 1, 2)
                root.setComponentAlignment(buttons, Alignment.TOP_RIGHT)
                event.getButton().getWindow().addWindow(w)

        _5_ = _5_()
        Button('Generate Report', _5_)
        b = _5_
        buttons.addComponent(b)
        root.addComponent(buttons, 'top: 11px; right: 18px; z-index:1;')
        content = VerticalLayout()
        content.setSizeFull()
        root.addComponent(content)
        top = Panel('Browse & Edit Workhours', VerticalLayout())
        top.setSizeFull()
        top.addStyleName(Runo.PANEL_LIGHT)
        top.getContent().setSizeFull()
        content.addComponent(top)
        content.setExpandRatio(top, 1)
        table = Table()
        table.setSizeFull()
        table.setSelectable(True)
        table.setColumnReorderingAllowed(True)
        table.addStyleName(Runo.TABLE_BORDERLESS)
        top.addComponent(table)
        table.addContainerProperty('info', Embedded, None)
        table.addContainerProperty('check', CheckBox, None)
        table.addContainerProperty('locked', Embedded, None)
        table.addContainerProperty('hours', str, '00:00:00')
        table.addContainerProperty('cost', str, '$0.00')
        table.addContainerProperty('start', str, '00/00/0000')
        table.addContainerProperty('end', str, '00/00/0000')
        table.addContainerProperty('note', Embedded, Embedded(None, ThemeResource('icons/16/note.png')))
        table.addContainerProperty('desc', str, None)
        table.setColumnHeaders(['', '', '', 'Hours', 'Cost', 'Start Date', 'End Date', 'Note', 'Description'])
        table.setColumnAlignment('info', Table.ALIGN_CENTER)
        table.setColumnAlignment('check', Table.ALIGN_CENTER)
        table.setColumnAlignment('note', Table.ALIGN_CENTER)
        _0 = True
        j = 1
        while True:
            if _0 is True:
                _0 = False
            else:
                j += 1
            if not (j < 6):
                break
            i = table.addItem(j)
            i.getItemProperty('info').setValue(self.create16pxIcon('icons/16/attention.png'))
            i.getItemProperty('check').setValue(CheckBox(None, True))
            i.getItemProperty('note').setValue(self.create16pxIcon('icons/16/note.png'))
        table.select(1)
        i = table.getItem(1)
        i.getItemProperty('hours').setValue('07:02:18')
        i.getItemProperty('cost').setValue('$703.83')
        i.getItemProperty('start').setValue('1/17/10')
        i.getItemProperty('end').setValue('1/17/10')
        i.getItemProperty('desc').setValue('More revisions')
        i = table.getItem(2)
        i.getItemProperty('hours').setValue('04:00:00')
        i.getItemProperty('cost').setValue('$360.00')
        i.getItemProperty('start').setValue('1/14/10')
        i.getItemProperty('end').setValue('1/14/10')
        i.getItemProperty('desc').setValue('Algorithm selection')
        i.getItemProperty('note').setValue(None)
        i = table.getItem(3)
        i.getItemProperty('hours').setValue('02:34:45')
        i.getItemProperty('cost').setValue('$160.00')
        i.getItemProperty('start').setValue('1/13/10')
        i.getItemProperty('end').setValue('1/13/10')
        i.getItemProperty('desc').setValue('New features implementation')
        i.getItemProperty('note').setValue(None)
        i = table.getItem(4)
        i.getItemProperty('hours').setValue('0:14:00')
        i.getItemProperty('cost').setValue('$60.00')
        i.getItemProperty('start').setValue('1/6/10')
        i.getItemProperty('end').setValue('1/6/10')
        i = table.getItem(5)
        i.getItemProperty('hours').setValue('03:07:23')
        i.getItemProperty('cost').setValue('$560.00')
        i.getItemProperty('start').setValue('1/5/10')
        i.getItemProperty('end').setValue('1/5/10')
        i.getItemProperty('desc').setValue('More revisions')
        i.getItemProperty('note').setValue(None)
        content.addComponent(ALabel('<hr />', ALabel.CONTENT_XHTML))
        bottom = VerticalLayout()
        bottom.setMargin(True)
        bottom.setSpacing(True)
        bottom.addStyleName(Runo.LAYOUT_DARKER)
        content.addComponent(bottom)

        class line(HorizontalLayout):

            def addComponent(self, c):
                super(_5_, self).addComponent(c)
                self.setComponentAlignment(c, Alignment.MIDDLE_LEFT)
                c.setSizeUndefined()

        line.setWidth('100%')
        line.setSpacing(True)
        first = ALabel('Item Type:')
        line.addComponent(first)
        first.setWidth('80px')
        select = NativeSelect()
        select.addItem('Timed')
        select.addItem('Not billable')
        select.setNullSelectionAllowed(False)
        select.select('Timed')
        line.addComponent(select)
        line.addComponent(ALabel('Customer Hourly Rate:'))
        tf = TextField()
        tf.setInputPrompt('$45.00')
        line.addComponent(tf)
        tf.setWidth('100%')
        line.setExpandRatio(tf, 1)
        line.addComponent(Button('Remove'))
        cb = CheckBox('Taxable')
        cb.setValue(True)
        line.addComponent(cb)
        bottom.addComponent(line)

        class _6_(HorizontalLayout):

            def addComponent(self, c):
                super(_6_, self).addComponent(c)
                self.setComponentAlignment(c, Alignment.MIDDLE_LEFT)
                c.setSizeUndefined()

        _6_ = _6_()
        line = _6_
        line.setWidth('100%')
        line.setSpacing(True)
        first = ALabel('Hours:')
        line.addComponent(first)
        first.setWidth('80px')
        first = ALabel('11:56:10 from 1 timing session.')
        line.addComponent(first)
        line.setExpandRatio(first, 1)
        line.addComponent(Button('Timing Sessions'))
        line.addComponent(Button('Quick Add'))
        line.addComponent(Button('Quick Modify'))
        cb = CheckBox('Included')
        cb.setValue(True)
        line.addComponent(cb)
        bottom.addComponent(line)

        class _7_(HorizontalLayout):

            def addComponent(self, c):
                super(_7_, self).addComponent(c)
                self.setComponentAlignment(c, Alignment.MIDDLE_RIGHT)

        _7_ = _7_()
        line = _7_
        line.setWidth('100%')
        line.setSpacing(True)
        first = ALabel('Description:')
        line.addComponent(first)
        first.setWidth('80px')
        combo = ComboBox()
        combo.setInputPrompt('Add a description')
        combo.setNewItemsAllowed(True)
        line.addComponent(combo)
        combo.setWidth('100%')
        line.setExpandRatio(combo, 1)
        bottom.addComponent(line)

        class _8_(HorizontalLayout):

            def addComponent(self, c):
                super(_8_, self).addComponent(c)
                self.setComponentAlignment(c, Alignment.TOP_RIGHT)

        _8_ = _8_()
        line = _8_
        line.setWidth('100%')
        line.setSpacing(True)
        first = ALabel('Notes:')
        line.addComponent(first)
        first.setWidth('80px')
        tf = TextField()
        line.addComponent(tf)
        tf.setWidth('100%')
        tf.setHeight('4em')
        line.setExpandRatio(tf, 1)
        bottom.addComponent(line)
        return root

    def create16pxIcon(self, iconid):
        em = Embedded(None, ThemeResource(iconid))
        em.setStyleName('icon-16')
        return em

    def buildLibraryScreen(self):
        root = AbsoluteLayout()
        root.setSizeFull()
        root.setCaption('Media Library')
        size = HorizontalLayout()
        size.setSpacing(True)
        size.addComponent(ALabel('-'))
        slider = Slider()
        # Ignore
        try:
            slider.setValue(70)
        except ValueOutOfBoundsException, e:
            pass # astStmt: [Stmt([]), None]
        slider.setWidth('200px')
        size.addComponent(slider)
        size.addComponent(ALabel('+'))
        root.addComponent(size, 'top: 16px; right: 18px; z-index:1;')
        content = VerticalLayout()
        content.setSizeFull()
        root.addComponent(content)
        grid = GridLayout(4, 1)
        top = Panel('My Book Collection', grid)
        top.setSizeFull()
        top.addStyleName(Runo.PANEL_LIGHT)
        grid.setWidth('100%')
        grid.setMargin(True)
        grid.addStyleName(Runo.LAYOUT_DARKER)
        content.addComponent(top)
        content.setExpandRatio(top, 1)

        class _9_(LayoutClickListener):

            def layoutClick(self, event):
                _0 = True
                it = self.grid.getComponentIterator()
                while True:
                    if _0 is True:
                        _0 = False
                    if not it.hasNext():
                        break
                    c = it.next()
                    c.removeStyleName(Runo.CSSLAYOUT_SELECTABLE_SELECTED)
                if event.getChildComponent() is not None:
                    event.getChildComponent().addStyleName(Runo.CSSLAYOUT_SELECTABLE_SELECTED)

        _9_ = _9_()
        grid.addListener(_9_)
        covers = ['designing-interfaces.png', 'comics.png', 'gdtnb.png', 'new-mind.png', 'simplicity.png', 'upod.png', 'designing-interactions.png', 'rogue-leaders.png', 'tcss.png', 'wfd.png', 'new-type.png']
        for cover in covers:
            select = CssLayout()
            select.addStyleName(Runo.CSSLAYOUT_SELECTABLE)
            book = CssLayout()
            book.addStyleName(Runo.CSSLAYOUT_SHADOW)
            book.addComponent(Embedded(None, ThemeResource('../demo/book-covers/' + cover)))
            select.addComponent(book)
            grid.addComponent(select)
            grid.setComponentAlignment(select, Alignment.MIDDLE_CENTER)
            if cover == 'gdtnb.png':
                select.addStyleName(Runo.CSSLAYOUT_SELECTABLE_SELECTED)
        text = ALabel('Note: the book cover images are not included in the Runo theme, they are provided extenally for this example. The shadow for the books is supplied by the theme.')
        text.addStyleName(Runo.LABEL_SMALL)
        text.setWidth('90%')
        grid.addComponent(text)
        grid.setComponentAlignment(text, Alignment.MIDDLE_CENTER)
        text = ALabel('')
        text.addStyleName('hr')
        content.addComponent(text)
        bottom = HorizontalLayout()
        bottom.setWidth('100%')
        content.addComponent(bottom)
        side = VerticalLayout()
        side.setMargin(True)
        side.setSpacing(True)
        side.setWidth('170px')
        bottom.addComponent(side)
        book = CssLayout()
        book.addStyleName(Runo.CSSLAYOUT_SHADOW)
        book.addComponent(Embedded(None, ThemeResource('../demo/book-covers/gdtnb.png')))
        side.addComponent(book)
        read = NativeSelect('Mark the book as:')
        read.setWidth('130px')
        read.addItem('Not Read')
        read.addItem('Read')
        read.setNullSelectionAllowed(False)
        read.select('Read')
        side.addComponent(read)
        read = NativeSelect()
        read.setWidth('130px')
        read.addItem('Mine')
        read.addItem('Loaned')
        read.setNullSelectionAllowed(False)
        read.select('Loaned')
        side.addComponent(read)
        details = CssLayout()
        details.setWidth('100%')
        details.setMargin(False, True, False, False)
        bottom.addComponent(details)
        bottom.setExpandRatio(details, 1)
        title = ALabel('<h3>Graphic Design &ndash; The New Basics</h3>', ALabel.CONTENT_XHTML)
        details.addComponent(title)
        title.setSizeUndefined()
        tabs = TabSheet()
        tabs.addStyleName(Runo.TABSHEET_SMALL)
        tabs.setWidth('100%')
        tabs.setHeight('180px')
        details.addComponent(tabs)
        l = FormLayout()
        tabs.addTab(l, 'Info', None)
        text = ALabel('248 pages')
        text.setCaption('Hardcover:')
        l.addComponent(text)
        text = ALabel('Princeton Architectural Press; 1 edition (May 1, 2008)')
        text.setCaption('Publisher:')
        l.addComponent(text)
        text = ALabel('English')
        text.setCaption('Language:')
        l.addComponent(text)
        text = ALabel('1568987706')
        text.setCaption('ISBN-10:')
        l.addComponent(text)
        text = ALabel('978-1568987705')
        text.setCaption('ISBN-13:')
        l.addComponent(text)
        text = ALabel('9.1 x 8.1 x 1.1 inches')
        text.setCaption('Product Dimensions:')
        l.addComponent(text)
        text = ALabel('2.2 pounds')
        text.setCaption('Shipping Weight:')
        l.addComponent(text)
        tabs.addTab(ALabel(), 'Reviews', None)
        tabs.addTab(ALabel(), 'Personal', None)
        return root
