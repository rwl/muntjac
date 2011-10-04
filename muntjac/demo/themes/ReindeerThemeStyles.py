# -*- coding: utf-8 -*-
# from com.vaadin.Application import (Application,)
# from com.vaadin.data.Property.ValueChangeEvent import (ValueChangeEvent,)
# from com.vaadin.data.Property.ValueChangeListener import (ValueChangeListener,)
# from com.vaadin.event.ShortcutAction.KeyCode import (KeyCode,)
# from com.vaadin.terminal.ExternalResource import (ExternalResource,)
# from com.vaadin.ui.Label import (Label,)
# from com.vaadin.ui.AbstractSelect import (AbstractSelect,)
# from com.vaadin.ui.Alignment import (Alignment,)
# from com.vaadin.ui.Button import (Button,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)
# from com.vaadin.ui.CheckBox import (CheckBox,)
# from com.vaadin.ui.ComboBox import (ComboBox,)
# from com.vaadin.ui.Component import (Component,)
# from com.vaadin.ui.CssLayout import (CssLayout,)
# from com.vaadin.ui.DateField import (DateField,)
# from com.vaadin.ui.GridLayout import (GridLayout,)
# from com.vaadin.ui.HorizontalLayout import (HorizontalLayout,)
# from com.vaadin.ui.HorizontalSplitPanel import (HorizontalSplitPanel,)
# from com.vaadin.ui.InlineDateField import (InlineDateField,)
# from com.vaadin.ui.Layout import (Layout,)
# from com.vaadin.ui.ListSelect import (ListSelect,)
# from com.vaadin.ui.MenuBar import (MenuBar,)
# from com.vaadin.ui.MenuBar.Command import (Command,)
# from com.vaadin.ui.MenuBar.MenuItem import (MenuItem,)
# from com.vaadin.ui.NativeSelect import (NativeSelect,)
# from com.vaadin.ui.Panel import (Panel,)
# from com.vaadin.ui.TabSheet import (TabSheet,)
# from com.vaadin.ui.TabSheet.SelectedTabChangeEvent import (SelectedTabChangeEvent,)
# from com.vaadin.ui.Table import (Table,)
# from com.vaadin.ui.TextField import (TextField,)
# from com.vaadin.ui.TwinColSelect import (TwinColSelect,)
# from com.vaadin.ui.VerticalLayout import (VerticalLayout,)
# from com.vaadin.ui.Window import (Window,)
# from com.vaadin.ui.themes.Reindeer import (Reindeer,)
# from java.util.Date import (Date,)
# from java.util.Iterator import (Iterator,)


class ReindeerThemeStyles(Application):
    """This Vaadin application demonstrates all the available styles that the
    Reindeer theme includes.

    @author Jouni Koivuviita, IT Mill Ltd.
    """
    _DATE = Date(2009 - 1900, 6 - 1, 2)
    _main = None
    _mainLayout = None
    _tabs = None

    def init(self):
        self.setTheme('reindeer')
        self._main = Window('Vaadin Reindeer Theme')
        self._mainLayout = self._main.getContent()
        self._mainLayout.setMargin(False)
        self.setMainWindow(self._main)
        self.buildMainView()

    def buildMainView(self):
        self._mainLayout.setSizeFull()
        self._mainLayout.addComponent(self.getTopMenu())
        self._mainLayout.addComponent(self.getHeader())
        margin = CssLayout()
        margin.setMargin(False, True, True, True)
        margin.setSizeFull()
        self._tabs = TabSheet()
        self._tabs.setSizeFull()
        margin.addComponent(self._tabs)
        self._mainLayout.addComponent(margin)
        self._mainLayout.setExpandRatio(margin, 1)
        self._tabs.addComponent(self.buildWelcomeScreen())
        self._tabs.addComponent(self.buildLabels())
        self._tabs.addComponent(self.buildButtons())
        self._tabs.addComponent(self.buildTextFields())
        self._tabs.addComponent(self.buildSelects())
        self._tabs.addComponent(self.buildDateFields())
        self._tabs.addComponent(self.buildTabSheets())
        self._tabs.addComponent(self.buildPanels())
        self._tabs.addComponent(self.buildTables())
        self._tabs.addComponent(self.buildWindows())
        self._tabs.addComponent(self.buildSplitPanels())

    def buildLabels(self):
        l = GridLayout(2, 1)
        l.setWidth('560px')
        l.setSpacing(True)
        l.setMargin(True)
        l.setCaption('Labels')
        l.addStyleName(Reindeer.LAYOUT_WHITE)
        l.addComponent(Label('Header Style (<code>Reindeer.LABEL_H1</code>)', Label.CONTENT_XHTML))
        l.addComponent(self.H1('Lorem Ipsum'))
        l.addComponent(Label('Sub-header Style (<code>Reindeer.LABEL_H2</code>)', Label.CONTENT_XHTML))
        l.addComponent(self.H2('Lorem Ipsum Dolor'))
        l.addComponent(Label('Normal Label', Label.CONTENT_XHTML))
        l.addComponent(Label('Lorem ipsum dolor sit amet, consectetur adipiscing elit.'))
        l.addComponent(Label('Small Style (<code>Reindeer.LABEL_SMALL</code>)', Label.CONTENT_XHTML))
        l.addComponent(self.SmallText('Lorem ipsum dolor sit amet, consectetur adipiscing elit.'))
        return l

    def buildButtons(self):
        l = GridLayout(2, 1)
        l.setCaption('Buttons')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('370px')
        l.setColumnExpandRatio(0, 1)
        l.addComponent(Label('\"Default\" Style (<code>Reindeer.BUTTON_DEFAULT</code>)', Label.CONTENT_XHTML))
        b = Button('Default Button')
        b.setStyleName(Reindeer.BUTTON_DEFAULT)
        l.addComponent(b)
        l.addComponent(Label('Normal Button', Label.CONTENT_XHTML))
        b = Button('Normal Button')
        l.addComponent(b)
        l.addComponent(Label('Disabled Button (<code>Button.setEnabled(false)</code>)', Label.CONTENT_XHTML))
        b = Button('Disabled Button')
        b.setEnabled(False)
        l.addComponent(b)
        l.addComponent(Label('Small Style (<code>Reindeer.BUTTON_SMALL</code>)', Label.CONTENT_XHTML))
        b = Button('Small Button')
        b.setStyleName(Reindeer.BUTTON_SMALL)
        l.addComponent(b)
        l.addComponent(Label('Link Style (<code>Reindeer.BUTTON_LINK</code>)', Label.CONTENT_XHTML))
        b = Button('Link Button')
        b.setStyleName(Reindeer.BUTTON_LINK)
        l.addComponent(b)
        return l

    def buildTextFields(self):
        l = GridLayout(2, 1)
        l.setCaption('Text fields')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('400px')
        l.setColumnExpandRatio(0, 1)
        l.addStyleName(Reindeer.LAYOUT_WHITE)
        l.addComponent(Label('Normal TextField', Label.CONTENT_XHTML))
        tf = TextField()
        tf.setInputPrompt('Enter text')
        l.addComponent(tf)
        l.addComponent(Label('Small Style (<code>Reindeer.TEXTFIELD_SMALL</code>)', Label.CONTENT_XHTML))
        tf = TextField()
        tf.setStyleName('small')
        tf.setInputPrompt('Enter text')
        l.addComponent(tf)
        l.addComponent(Label('Normal TextArea', Label.CONTENT_XHTML))
        tf = TextField()
        tf.setHeight('5em')
        tf.setInputPrompt('Enter text')
        l.addComponent(tf)
        l.addComponent(Label('Small Style TextArea (<code>Reindeer.TEXTFIELD_SMALL</code>)', Label.CONTENT_XHTML))
        tf = TextField()
        tf.setHeight('5em')
        tf.setStyleName('small')
        tf.setInputPrompt('Enter text')
        l.addComponent(tf)
        return l

    def buildSelects(self):
        l = VerticalLayout()
        l.setCaption('Selects')
        l.setMargin(True)
        l.setSpacing(True)
        l.addComponent(Label('Selects don\'t currently have any additional style names, but here you can see how they behave with the different background colors.'))
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
        l.addComponent(Label('Date fields don\'t currently have any additional style names, but here you can see how they behave with the different background colors.'))
        hl = HorizontalLayout()
        hl.setSpacing(True)
        hl.setMargin(True, False, False, False)
        l.addComponent(hl)
        df = DateField()
        df.setValue(self._DATE)
        df.setResolution(DateField.RESOLUTION_MIN)
        hl.addComponent(df)
        df = InlineDateField()
        df.setValue(self._DATE)
        df.setResolution(DateField.RESOLUTION_DAY)
        hl.addComponent(df)
        df = InlineDateField()
        df.setValue(self._DATE)
        df.setResolution(DateField.RESOLUTION_YEAR)
        hl.addComponent(df)
        return l

    def buildTabSheets(self):
        l = GridLayout(2, 1)
        l.setCaption('Tabs')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('700px')
        l.setColumnExpandRatio(0, 7)
        l.setColumnExpandRatio(1, 4)
        l.addStyleName(Reindeer.LAYOUT_WHITE)
        checks = HorizontalLayout()
        checks.setSpacing(True)
        closable = CheckBox('Closable tabs')
        closable.setImmediate(True)
        checks.addComponent(closable)
        hoverOnly = CheckBox('Only on hover')
        hoverOnly.setImmediate(True)
        hoverOnly.setEnabled(False)
        hoverOnly.setDescription('Adds style <code>Reindeer.TABSHEET_HOVER_CLOSABLE</code> to all tabs')
        checks.addComponent(hoverOnly)
        selectedOnly = CheckBox('Selected only')
        selectedOnly.setImmediate(True)
        selectedOnly.setEnabled(False)
        selectedOnly.setDescription('Adds style <code>Reindeer.TABSHEET_SELECTED_CLOSABLE</code> to all tabs')
        checks.addComponent(selectedOnly)
        l.addComponent(checks, 1, 0)
        l.setCursorX(0)
        l.setCursorY(1)
        l.addComponent(Label('Normal Tabs', Label.CONTENT_XHTML))
        ts = TabSheet()
        ts.setHeight('100px')
        l.addComponent(ts)
        l.addComponent(Label('Borderless Style (<code>Reindeer.TABSHEET_BORDERLESS</code>)', Label.CONTENT_XHTML))
        ts2 = TabSheet()
        ts2.setStyleName(Reindeer.TABSHEET_BORDERLESS)
        ts2.setHeight('100px')
        l.addComponent(ts2)
        l.addComponent(Label('Small Style (<code>Reindeer.TABSHEET_SMALL</code>)', Label.CONTENT_XHTML))
        ts3 = TabSheet()
        ts3.setStyleName(Reindeer.TABSHEET_SMALL)
        l.addComponent(ts3)
        l.addComponent(Label('Minimal Style (<code>Reindeer.TABSHEET_MINIMAL</code>)', Label.CONTENT_XHTML))
        ts4 = TabSheet()
        ts4.setStyleName(Reindeer.TABSHEET_MINIMAL)
        l.addComponent(ts4)
        _0 = True
        i = 1
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 10):
                break
            ts.addTab(Label(), 'Tab ' + i, None)
            ts2.addTab(Label(), 'Tab ' + i, None)
            ts3.addTab(Label(), 'Tab ' + i, None)
            ts4.addTab(Label(), 'Tab ' + i, None)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                it = self.ts.getComponentIterator()
                it2 = self.ts2.getComponentIterator()
                it3 = self.ts3.getComponentIterator()
                it4 = self.ts4.getComponentIterator()
                _0 = True
                while True:
                    if _0 is True:
                        _0 = False
                    if not it.hasNext():
                        break
                    c = it.next()
                    self.ts.getTab(c).setClosable(event.getButton().booleanValue())
                    c = it2.next()
                    self.ts2.getTab(c).setClosable(event.getButton().booleanValue())
                    c = it3.next()
                    self.ts3.getTab(c).setClosable(event.getButton().booleanValue())
                    c = it4.next()
                    self.ts4.getTab(c).setClosable(event.getButton().booleanValue())
                self.hoverOnly.setEnabled(event.getButton().booleanValue())
                self.selectedOnly.setEnabled(event.getButton().booleanValue())

        _0_ = _0_()
        closable.addListener(_0_)

        class _1_(Button.ClickListener):

            def buttonClick(self, event):
                if event.getButton().booleanValue():
                    self.ts.addStyleName(Reindeer.TABSHEET_HOVER_CLOSABLE)
                    self.ts2.addStyleName(Reindeer.TABSHEET_HOVER_CLOSABLE)
                    self.ts3.addStyleName(Reindeer.TABSHEET_HOVER_CLOSABLE)
                    self.ts4.addStyleName(Reindeer.TABSHEET_HOVER_CLOSABLE)
                else:
                    self.ts.removeStyleName(Reindeer.TABSHEET_HOVER_CLOSABLE)
                    self.ts2.removeStyleName(Reindeer.TABSHEET_HOVER_CLOSABLE)
                    self.ts3.removeStyleName(Reindeer.TABSHEET_HOVER_CLOSABLE)
                    self.ts4.removeStyleName(Reindeer.TABSHEET_HOVER_CLOSABLE)

        _1_ = _1_()
        hoverOnly.addListener(_1_)

        class _2_(Button.ClickListener):

            def buttonClick(self, event):
                if event.getButton().booleanValue():
                    self.ts.addStyleName(Reindeer.TABSHEET_SELECTED_CLOSABLE)
                    self.ts2.addStyleName(Reindeer.TABSHEET_SELECTED_CLOSABLE)
                    self.ts3.addStyleName(Reindeer.TABSHEET_SELECTED_CLOSABLE)
                    self.ts4.addStyleName(Reindeer.TABSHEET_SELECTED_CLOSABLE)
                else:
                    self.ts.removeStyleName(Reindeer.TABSHEET_SELECTED_CLOSABLE)
                    self.ts2.removeStyleName(Reindeer.TABSHEET_SELECTED_CLOSABLE)
                    self.ts3.removeStyleName(Reindeer.TABSHEET_SELECTED_CLOSABLE)
                    self.ts4.removeStyleName(Reindeer.TABSHEET_SELECTED_CLOSABLE)

        _2_ = _2_()
        selectedOnly.addListener(_2_)
        return l

    def buildPanels(self):
        l = GridLayout(2, 1)
        l.setCaption('Panels')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('700px')
        l.setColumnExpandRatio(0, 2)
        l.setColumnExpandRatio(1, 5)
        l.addStyleName(Reindeer.LAYOUT_WHITE)
        l.addComponent(Label('Normal Panel', Label.CONTENT_XHTML))
        p = Panel('Normal Panel')
        p.setHeight('100px')
        p.addComponent(Label('Panel content'))
        l.addComponent(p)
        l.addComponent(Label('Light Style (<code>Reindeer.PANEL_LIGHT</code>)', Label.CONTENT_XHTML))
        p2 = Panel('Light Style Panel')
        p2.setStyleName('light')
        p2.addComponent(Label('Panel content'))
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
        l.addStyleName(Reindeer.LAYOUT_WHITE)
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
            t.setPageLength(4)
            t.setSelectable(True)
            t.setColumnCollapsingAllowed(True)
            t.setColumnReorderingAllowed(True)
            if i == 1:
                t.setStyleName('strong')
                l.addComponent(Label('Strong Style (<code>Reindeer.TABLE_STRONG</code>)', Label.CONTENT_XHTML))
            elif i == 2:
                t.setStyleName('borderless')
                l.addComponent(Label('Borderless Style (<code>Reindeer.TABLE_BORDERLESS</code>)', Label.CONTENT_XHTML))
            elif i == 3:
                t.setStyleName('borderless strong')
                l.addComponent(Label('Borderless & Strong Combined', Label.CONTENT_XHTML))
            else:
                l.addComponent(Label('Normal Table', Label.CONTENT_XHTML))
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
        w3 = Window('Light window')
        w3.setWidth('280px')
        w3.setHeight('230px')
        w3.setStyleName('light')
        w3.setPositionX(40)
        w3.setPositionY(370)
        w3.addComponent(Label('<code>Reindeer.WINDOW_LIGHT</code>', Label.CONTENT_XHTML))
        w4 = Window('Black window')
        w4.setWidth('280px')
        w4.setHeight('230px')
        w4.setStyleName('black')
        w4.setPositionX(350)
        w4.setPositionY(370)
        w4.addComponent(Label('<code>Reindeer.WINDOW_BLACK</code>', Label.CONTENT_XHTML))

        class _3_(TabSheet.SelectedTabChangeListener):

            def selectedTabChange(self, event):
                mainWindow = self.getMainWindow()
                if event.getTabSheet().getSelectedTab() == self.l:
                    mainWindow.addWindow(self.w)
                    mainWindow.addWindow(self.w2)
                    mainWindow.addWindow(self.w3)
                    mainWindow.addWindow(self.w4)
                else:
                    if self.w.getParent() == mainWindow:
                        mainWindow.removeWindow(self.w)
                    if self.w2.getParent() == mainWindow:
                        mainWindow.removeWindow(self.w2)
                    if self.w3.getParent() == mainWindow:
                        mainWindow.removeWindow(self.w3)
                    if self.w4.getParent() == mainWindow:
                        mainWindow.removeWindow(self.w4)

        _3_ = _3_()
        self._tabs.addListener(_3_)
        return l

    def buildSplitPanels(self):
        l = GridLayout(2, 1)
        l.setCaption('Split panels')
        l.setMargin(True)
        l.setSpacing(True)
        l.setWidth('400px')
        l.addStyleName(Reindeer.LAYOUT_WHITE)
        l.setColumnExpandRatio(0, 1)
        l.addComponent(Label('Normal SplitPanel', Label.CONTENT_XHTML))
        sp = HorizontalSplitPanel()
        sp.setWidth('100px')
        sp.setHeight('200px')
        l.addComponent(sp)
        l.addComponent(Label('Small Style (<code>Reindeer.SPLITPANEL_SMALL</code>)', Label.CONTENT_XHTML))
        sp2 = HorizontalSplitPanel()
        sp2.setStyleName('small')
        sp2.setWidth('100px')
        sp2.setHeight('200px')
        l.addComponent(sp2)
        return l

    def buildWelcomeScreen(self):
        l = VerticalLayout()
        l.setMargin(True)
        l.setSpacing(True)
        l.setCaption('Welcome')
        l.setStyleName(Reindeer.LAYOUT_WHITE)
        margin = CssLayout()
        margin.setMargin(True)
        margin.setWidth('100%')
        l.addComponent(margin)
        title = self.H1('Guide to the Reindeer Theme')
        margin.addComponent(title)
        margin.addComponent(self.Ruler())
        texts = HorizontalLayout()
        texts.setSpacing(True)
        texts.setWidth('100%')
        texts.setMargin(False, False, True, False)
        margin.addComponent(texts)
        text = Label('<h4>A Complete Theme</h4><p>The Reindeer theme is a complete, general purpose theme suitable for almost all types of applications.<p>While a general purpose theme should not try to cater for every possible need, the Reindeer theme provides a set of useful styles that you can use to make the interface a bit more lively and interesing, emphasizing different parts of the application.</p>', Label.CONTENT_XHTML)
        texts.addComponent(text)
        texts.setExpandRatio(text, 1)
        # Spacer
        text = Label('')
        text.setWidth('20px')
        texts.addComponent(text)
        text = Label('<h4>Everything You Need Is Here</h4><p>Everything you see inside this application, all the different styles, are provided by the Reindeer theme, out-of-the-box. That means you don\'t necessarily need to create any custom CSS for your application: you can build a cohesive result writing plain Java code.</p><p>A little creativity, good organization and careful typography carries a long way.', Label.CONTENT_XHTML)
        texts.addComponent(text)
        texts.setExpandRatio(text, 1)
        # Spacer
        text = Label('')
        text.setWidth('20px')
        texts.addComponent(text)
        text = Label('<h4>The Names of The Styles</h4><p>Look for a class named <code>Reindeer</code> inside the Vaadin JAR (<code>com.vaadin.ui.themes.Reindeer</code>). All the available style names are documented and available there as constants, prefixed by component names, e.g. <code>Reindeer.BUTTON_SMALL</code>.', Label.CONTENT_XHTML)
        texts.addComponent(text)
        texts.setExpandRatio(text, 1)
        text = self.H2('One Theme &ndash; Three Styles')
        text.setContentMode(Label.CONTENT_XHTML)
        margin.addComponent(text)
        margin.addComponent(self.Ruler())
        text = Label('<p>You can easily change the feel of some parts of your application by using the three layout styles provided by Reindeer: white, blue and black. The colored area contains the margins of the layout. All contained components will switch their style if an alternative style is available for that color.</p>', Label.CONTENT_XHTML)
        margin.addComponent(text)
        colors = HorizontalLayout()
        colors.setWidth('100%')
        colors.setHeight('250px')
        margin.addComponent(colors)
        color = CssLayout()
        color.setSizeFull()
        color.setStyleName(Reindeer.LAYOUT_WHITE)
        color.setMargin(True)
        color.addComponent(self.H1('White'))
        color.addComponent(Label('<p><strong><code>Reindeer.LAYOUT_WHITE</code></strong></p><p>Changes the background to white. Has no other effect on contained components, they all behave like on the default gray background.', Label.CONTENT_XHTML))
        colors.addComponent(color)
        color = CssLayout()
        color.setSizeFull()
        color.setStyleName(Reindeer.LAYOUT_BLUE)
        color.setMargin(True)
        color.addComponent(self.H1('Blue'))
        color.addComponent(Label('<p><strong><code>Reindeer.LAYOUT_BLUE</code></strong></p><p>Changes the background to a shade of blue. A very few components have any difference here compared to the white style.', Label.CONTENT_XHTML))
        colors.addComponent(color)
        color = CssLayout()
        color.setSizeFull()
        color.setStyleName(Reindeer.LAYOUT_BLACK)
        color.setMargin(True)
        color.addComponent(self.H1('Black'))
        color.addComponent(Label('<p><strong><code>Reindeer.LAYOUT_BLACK</code></strong></p><p>Reserved for small parts of the application. Or alternatively, use for the whole application.</p><p><strong>This style is non-overridable</strong>, meaning that everything you place inside it will transform to their corresponding black styles when available, excluding Labels.</p>', Label.CONTENT_XHTML))
        colors.addComponent(color)
        text = Label('<p>Note, that you cannot nest the layout styles infinitely inside each other. After a couple levels, the result will be undefined, due to limitations in CSS (which are in fact caused by Internet Explorer 6).</p>', Label.CONTENT_XHTML)
        margin.addComponent(text)
        return l

    def getTopMenu(self):
        menubar = MenuBar()
        menubar.setWidth('100%')
        file = menubar.addItem('File', None)
        newItem = file.addItem('New', None)
        file.addItem('Open file...', None)
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
        view = menubar.addItem('View', None)
        statusBarItem = view.addItem('Show/Hide Status Bar', None)
        statusBarItem.setCheckable(True)
        statusBarItem.setChecked(True)
        view.addItem('Customize Toolbar...', None)
        view.addSeparator()
        view.addItem('Actual Size', None)
        view.addItem('Zoom In', None)
        view.addItem('Zoom Out', None)
        return menubar

    def getHeader(self):
        header = HorizontalLayout()
        header.setWidth('100%')
        header.setMargin(True)
        header.setSpacing(True)
        # header.setStyleName(Reindeer.LAYOUT_BLACK);
        titleLayout = CssLayout()
        title = self.H2('Vaadin Reindeer Theme')
        titleLayout.addComponent(title)
        description = self.SmallText('Documentation and Examples of Available Styles')
        description.setSizeUndefined()
        titleLayout.addComponent(description)
        header.addComponent(titleLayout)
        toggles = HorizontalLayout()
        toggles.setSpacing(True)
        bgColor = Label('Background color')
        bgColor.setDescription('Set the style name for the main layout of this window:<ul><li>Default - no style</li><li>White - Reindeer.LAYOUT_WHITE</li><li>Blue - Reindeer.LAYOUT_BLUE</li><li>Black - Reindeer.LAYOUT_BLACK</li></ul>')
        toggles.addComponent(bgColor)
        colors = NativeSelect()
        colors.setNullSelectionAllowed(False)
        colors.setDescription('Set the style name for the main layout of this window:<ul><li>Default - no style</li><li>White - Reindeer.LAYOUT_WHITE</li><li>Blue - Reindeer.LAYOUT_BLUE</li><li>Black - Reindeer.LAYOUT_BLACK</li></ul>')
        colors.addItem('Default')
        colors.addItem('White')
        colors.addItem('Blue')
        colors.addItem('Black')
        colors.setImmediate(True)

        class _5_(ValueChangeListener):

            def valueChange(self, event):
                ReindeerThemeStyles_this._mainLayout.setStyleName(str(event.getProperty().getValue()).toLowerCase())

        _5_ = _5_()
        colors.addListener(_5_)
        colors.setValue('Blue')
        toggles.addComponent(colors)

        class _6_(Button.ClickListener):

            def buttonClick(self, event):
                if event.getButton().booleanValue():
                    ReindeerThemeStyles_this._tabs.setStyleName(Reindeer.TABSHEET_MINIMAL)
                else:
                    ReindeerThemeStyles_this._tabs.removeStyleName(Reindeer.TABSHEET_MINIMAL)
                _0 = True
                it = ReindeerThemeStyles_this._tabs.getComponentIterator()
                while True:
                    if _0 is True:
                        _0 = False
                    if not it.hasNext():
                        break
                    c = it.next()
                    if event.getButton().booleanValue():
                        c.removeStyleName(Reindeer.LAYOUT_WHITE)
                    else:
                        c.addStyleName(Reindeer.LAYOUT_WHITE)
                # Force refresh
                self.getMainWindow().open(ExternalResource(self.getURL()))

        _6_ = _6_()
        transparent = CheckBox('Transparent tabs', _6_)
        transparent.setImmediate(True)
        transparent.setDescription('Set style Reindeer.TABSHEET_MINIMAL to the main tab sheet (preview components on different background colors).')
        toggles.addComponent(transparent)
        header.addComponent(toggles)
        header.setComponentAlignment(toggles, Alignment.MIDDLE_LEFT)
        titleLayout = CssLayout()
        user = Label('Welcome, Guest')
        user.setSizeUndefined()
        titleLayout.addComponent(user)
        buttons = HorizontalLayout()
        buttons.setSpacing(True)

        class _6_(Button.ClickListener):

            def buttonClick(self, event):
                ReindeerThemeStyles_this.openHelpWindow()

        _6_ = _6_()
        help = Button('Help', _6_)
        help.setStyleName(Reindeer.BUTTON_SMALL)
        buttons.addComponent(help)
        buttons.setComponentAlignment(help, Alignment.MIDDLE_LEFT)

        class _6_(Button.ClickListener):

            def buttonClick(self, event):
                ReindeerThemeStyles_this.openLogoutWindow()

        _6_ = _6_()
        logout = Button('Logout', _6_)
        logout.setStyleName(Reindeer.BUTTON_SMALL)
        buttons.addComponent(logout)
        titleLayout.addComponent(buttons)
        header.addComponent(titleLayout)
        header.setComponentAlignment(titleLayout, Alignment.TOP_RIGHT)
        return header

    _help = Window('Help')

    def openHelpWindow(self):
        if not ('initialized' == self._help.getData()):
            self._help.setData('initialized')
            self._help.setCloseShortcut(KeyCode.ESCAPE, None)
            self._help.center()
            # help.setStyleName(Reindeer.WINDOW_LIGHT);
            self._help.setWidth('400px')
            self._help.setResizable(False)
            helpText = Label('<strong>How To Use This Application</strong><p>Click around, explore. The purpose of this app is to show you what is possible to achieve with the Reindeer theme and its different styles.</p><p>Most of the UI controls that are visible in this application don\'t actually do anything. They are purely for show, like the menu items and the components that demostrate the different style names assosiated with the components.</p><strong>So, What Then?</strong><p>Go and use the styles you see here in your own application and make them beautiful!', Label.CONTENT_XHTML)
            self._help.addComponent(helpText)
        if not self.getMainWindow().getChildWindows().contains(self._help):
            self.getMainWindow().addWindow(self._help)

    def openLogoutWindow(self):
        logout = Window('Logout')
        logout.setModal(True)
        logout.setStyleName(Reindeer.WINDOW_BLACK)
        logout.setWidth('260px')
        logout.setResizable(False)
        logout.setClosable(False)
        logout.setDraggable(False)
        logout.setCloseShortcut(KeyCode.ESCAPE, None)
        helpText = Label('Are you sure you want to log out? You will be redirected to vaadin.com.', Label.CONTENT_XHTML)
        logout.addComponent(helpText)
        buttons = HorizontalLayout()
        buttons.setSpacing(True)

        class _6_(Button.ClickListener):

            def buttonClick(self, event):
                self.getMainWindow().open(ExternalResource('http://vaadin.com'))

        _6_ = _6_()
        yes = Button('Logout', _6_)
        yes.setStyleName(Reindeer.BUTTON_DEFAULT)
        yes.focus()
        buttons.addComponent(yes)

        class _6_(Button.ClickListener):

            def buttonClick(self, event):
                self.getMainWindow().removeWindow(event.getButton().getWindow())

        _6_ = _6_()
        no = Button('Cancel', _6_)
        buttons.addComponent(no)
        logout.addComponent(buttons)
        logout.getContent().setComponentAlignment(buttons, Alignment.TOP_CENTER)
        logout.getContent().setSpacing(True)
        self.getMainWindow().addWindow(logout)

    class H1(Label):

        def __init__(self, caption):
            super(H1, self)(caption)
            self.setSizeUndefined()
            self.setStyleName(Reindeer.LABEL_H1)

    class H2(Label):

        def __init__(self, caption):
            super(H2, self)(caption)
            self.setSizeUndefined()
            self.setStyleName(Reindeer.LABEL_H2)

    class SmallText(Label):

        def __init__(self, caption):
            super(SmallText, self)(caption)
            self.setStyleName(Reindeer.LABEL_SMALL)

    class Ruler(Label):

        def __init__(self):
            super(Ruler, self)('<hr />', Label.CONTENT_XHTML)
