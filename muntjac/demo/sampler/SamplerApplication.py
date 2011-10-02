# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
from com.vaadin.demo.sampler.CodeLabel import (CodeLabel,)
from com.vaadin.demo.sampler.FeatureView import (FeatureView,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.GoogleAnalytics import (GoogleAnalytics,)
from com.vaadin.demo.sampler.Feature import (Feature,)
from com.vaadin.demo.sampler.ActiveLink import (ActiveLink,)
# from com.vaadin.Application import (Application,)
# from com.vaadin.data.Property.ValueChangeEvent import (ValueChangeEvent,)
# from com.vaadin.data.util.ObjectProperty import (ObjectProperty,)
# from com.vaadin.event.ItemClickEvent import (ItemClickEvent,)
# from com.vaadin.event.ItemClickEvent.ItemClickListener import (ItemClickListener,)
# from com.vaadin.terminal.ClassResource import (ClassResource,)
# from com.vaadin.terminal.DownloadStream import (DownloadStream,)
# from com.vaadin.terminal.Sizeable import (Sizeable,)
# from com.vaadin.terminal.URIHandler import (URIHandler,)
# from com.vaadin.ui.Alignment import (Alignment,)
# from com.vaadin.ui.Button.ClickListener import (ClickListener,)
# from com.vaadin.ui.ComboBox import (ComboBox,)
# from com.vaadin.ui.CssLayout import (CssLayout,)
# from com.vaadin.ui.CustomComponent import (CustomComponent,)
# from com.vaadin.ui.Embedded import (Embedded,)
# from com.vaadin.ui.HorizontalSplitPanel import (HorizontalSplitPanel,)
# from com.vaadin.ui.PopupView import (PopupView,)
# from com.vaadin.ui.PopupView.PopupVisibilityEvent import (PopupVisibilityEvent,)
# from com.vaadin.ui.Table import (Table,)
# from com.vaadin.ui.Tree import (Tree,)
# from com.vaadin.ui.UriFragmentUtility import (UriFragmentUtility,)
# from com.vaadin.ui.UriFragmentUtility.FragmentChangedEvent import (FragmentChangedEvent,)
# from com.vaadin.ui.UriFragmentUtility.FragmentChangedListener import (FragmentChangedListener,)
# from java.net.URI import (URI,)
# from java.net.URL import (URL,)
# from java.util.Collection import (Collection,)
# from java.util.Iterator import (Iterator,)


class SamplerApplication(Application):
    # All features in one container
    _allFeatures = FeatureSet.FEATURES.getContainer(True)
    # init() inits
    _THEMES = ['reindeer', 'runo']
    _SAMPLER_THEME_NAME = 'sampler'
    # used when trying to guess theme location
    _APP_URL = None
    _currentApplicationTheme = _SAMPLER_THEME_NAME + '-' + _THEMES[0]

    def init(self):
        self.setMainWindow(self.SamplerWindow())
        url = self.getURL()
        self._APP_URL = str(self.getURL()) if url is not None else ''

    @classmethod
    def getThemeBase(cls):
        """Tries to guess theme location.

        @return
        """
        # Supports multiple browser windows
        try:
            uri = URI(cls._APP_URL + '../VAADIN/themes/' + cls._SAMPLER_THEME_NAME + '/')
            return str(uri.normalize())
        except Exception, e:
            print 'Theme location could not be resolved:' + e
        return '/VAADIN/themes/' + cls._SAMPLER_THEME_NAME + '/'

    def getWindow(self, name):
        w = super(SamplerApplication, self).getWindow(name)
        if w is None:
            if name.startswith('src'):
                w = self.SourceWindow()
            else:
                w = self.SamplerWindow()
                w.setName(name)
            self.addWindow(w)
        return w

    @classmethod
    def getFullPathFor(cls, f):
        """Gets absolute path for given Feature

        @param f
                   the Feature whose path to get, of null if not found
        @return the path of the Feature
        """
        if f is None:
            return ''
        if cls._allFeatures.containsId(f):
            path = f.getFragmentName()
            f = cls._allFeatures.getParent(f)
            while f is not None:
                path = f.getFragmentName() + '/' + path
                f = cls._allFeatures.getParent(f)
            return path
        return ''

    @classmethod
    def getFeatureFor(cls, clazz):
        """Gets the instance for the given Feature class, e.g DummyFeature.class.

        @param clazz
        @return
        """
        _0 = True
        it = cls._allFeatures.getItemIds()
        while True:
            if _0 is True:
                _0 = False
            if not it.hasNext():
                break
            f = it.next()
            if f.getClass() == clazz:
                return f
        return None

    def SamplerWindow(SamplerApplication_this, *args, **kwargs):

        class SamplerWindow(Window):
            """The main window for Sampler, contains the full application UI."""
            _TITLE = 'Vaadin Sampler'
            _EMPTY_THEME_ICON = ThemeResource('../sampler/sampler/icon-empty.png')
            _SELECTED_THEME_ICON = ThemeResource('../sampler/sampler/select-bullet.png')
            _currentList = SamplerApplication_this.FeatureGrid()
            _featureView = FeatureView()
            _currentFeature = ObjectProperty(None, Feature)
            _mainSplit = None
            _navigationTree = None
            # itmill: UA-658457-6
            _webAnalytics = GoogleAnalytics('UA-658457-6', 'none')
            # "backbutton"
            _uriFragmentUtility = UriFragmentUtility()
            # breadcrumbs
            _breadcrumbs = SamplerApplication_this.BreadCrumbs()
            _previousSample = None
            _nextSample = None
            _search = None
            _theme = None

            def detach(self):
                super(SamplerWindow, self).detach()
                self._search.setContainerDataSource(None)
                self._navigationTree.setContainerDataSource(None)

            def __init__(self):
                # Main top/expanded-bottom layout
                mainExpand = VerticalLayout()
                self.setContent(mainExpand)
                self.setSizeFull()
                mainExpand.setSizeFull()
                self.setCaption(self._TITLE)
                self.setTheme(SamplerApplication_this._currentApplicationTheme)
                # topbar (navigation)
                nav = HorizontalLayout()
                mainExpand.addComponent(nav)
                nav.setHeight('44px')
                nav.setWidth('100%')
                nav.setStyleName('topbar')
                nav.setSpacing(True)
                nav.setMargin(False, True, False, False)
                # Upper left logo
                logo = self.createLogo()
                nav.addComponent(logo)
                nav.setComponentAlignment(logo, Alignment.MIDDLE_LEFT)
                # Breadcrumbs
                nav.addComponent(self._breadcrumbs)
                nav.setExpandRatio(self._breadcrumbs, 1)
                nav.setComponentAlignment(self._breadcrumbs, Alignment.MIDDLE_LEFT)
                # invisible analytics -component
                nav.addComponent(self._webAnalytics)
                # "backbutton"
                nav.addComponent(self._uriFragmentUtility)

                class _1_(FragmentChangedListener):

                    def fragmentChanged(self, source):
                        frag = source.getUriFragmentUtility().getFragment()
                        if frag is not None and frag.contains('/'):
                            parts = frag.split('/')
                            frag = parts[len(parts) - 1]
                        SamplerWindow_this.setFeature(frag)

                _1_ = _1_()
                self._uriFragmentUtility.addListener(_1_)
                # Main left/right split; hidden menu tree
                self._mainSplit = HorizontalSplitPanel()
                self._mainSplit.setSizeFull()
                self._mainSplit.setStyleName('main-split')
                mainExpand.addComponent(self._mainSplit)
                mainExpand.setExpandRatio(self._mainSplit, 1)
                # Select theme
                themeSelect = self.createThemeSelect()
                nav.addComponent(themeSelect)
                nav.setComponentAlignment(themeSelect, Alignment.MIDDLE_LEFT)
                # Layouts for top area buttons
                quicknav = HorizontalLayout()
                arrows = HorizontalLayout()
                nav.addComponent(quicknav)
                nav.addComponent(arrows)
                nav.setComponentAlignment(quicknav, Alignment.MIDDLE_LEFT)
                nav.setComponentAlignment(arrows, Alignment.MIDDLE_LEFT)
                quicknav.setStyleName('segment')
                arrows.setStyleName('segment')
                # Previous sample
                self._previousSample = self.createPrevButton()
                arrows.addComponent(self._previousSample)
                # Next sample
                self._nextSample = self.createNextButton()
                arrows.addComponent(self._nextSample)
                # "Search" combobox
                searchComponent = self.createSearch()
                quicknav.addComponent(searchComponent)
                # Menu tree, initially shown
                menuLayout = CssLayout()
                allSamples = ActiveLink('All Samples', ExternalResource('#'))
                menuLayout.addComponent(allSamples)
                self._navigationTree = self.createMenuTree()
                menuLayout.addComponent(self._navigationTree)
                self._mainSplit.setFirstComponent(menuLayout)
                # Show / hide tree
                treeSwitch = self.createTreeSwitch()
                quicknav.addComponent(treeSwitch)
                SamplerWindow_this = self
                SamplerApplication_this = self

                class _2_(self.CloseListener):

                    def windowClose(self, e):
                        if self.getMainWindow() != SamplerWindow_this:
                            SamplerApplication_this.removeWindow(SamplerWindow_this)

                _2_ = _2_()
                self.addListener(_2_)
                self.updateFeatureList(self._currentList)

            def removeSubwindows(self):
                wins = self.getChildWindows()
                if None is not wins:
                    for w in wins:
                        self.removeWindow(w)

            def setFeature(self, *args):
                """Displays a Feature(Set)

                @param f
                           the Feature(Set) to show
                ---
                Displays a Feature(Set) matching the given path, or the main view if
                no matching Feature(Set) is found.

                @param path
                           the path of the Feature(Set) to show
                """
                _0 = args
                _1 = len(args)
                if _1 == 1:
                    if isinstance(_0[0], Feature):
                        f, = _0
                        if f == FeatureSet.FEATURES:
                            # "All" is no longer in the tree, use null instead
                            f = None
                        self._currentFeature.setValue(f)
                        fragment = f.getFragmentName() if f is not None else ''
                        self._webAnalytics.trackPageview(fragment)
                        self._uriFragmentUtility.setFragment(fragment, False)
                        self._breadcrumbs.setPath(SamplerApplication_this.getFullPathFor(f))
                        self._previousSample.setEnabled(f is not None)
                        self._nextSample.setEnabled(not SamplerApplication_this._allFeatures.isLastId(f))
                        self.updateFeatureList(self._currentList)
                        self.setCaption((f.getName() + ' }> ' if f is not None else '') + self._TITLE)
                    else:
                        path, = _0
                        f = FeatureSet.FEATURES.getFeature(path)
                        self.setFeature(f)
                else:
                    raise ARGERROR(1, 1)

            # SamplerWindow helpers

            def createSearch(self):
                self._search = ComboBox()
                self._search.setWidth('160px')
                self._search.setNewItemsAllowed(False)
                self._search.setFilteringMode(ComboBox.FILTERINGMODE_CONTAINS)
                self._search.setNullSelectionAllowed(True)
                self._search.setImmediate(True)
                self._search.setInputPrompt('Search samples...')
                self._search.setContainerDataSource(SamplerApplication_this._allFeatures)
                _0 = True
                it = SamplerApplication_this._allFeatures.getItemIds()
                while True:
                    if _0 is True:
                        _0 = False
                    if not it.hasNext():
                        break
                    id = it.next()
                    if isinstance(id, FeatureSet):
                        self._search.setItemIcon(id, ClassResource('folder.gif', SamplerApplication_this))
                SamplerWindow_this = self

                class _3_(ComboBox.ValueChangeListener):

                    def valueChange(self, event):
                        f = event.getProperty().getValue()
                        if f is not None:
                            SamplerWindow_this.setFeature(f)
                            event.getProperty().setValue(None)

                _3_ = _3_()
                self._search.addListener(_3_)
                # TODO add icons for section/sample
                # PopupView pv = new PopupView("", search) { public void
                # changeVariables(Object source, Map variables) {
                # super.changeVariables(source, variables); if (isPopupVisible()) {
                # search.focus(); } } };

                pv = PopupView('<span></span>', self._search)

                class _4_(PopupView.PopupVisibilityListener):

                    def popupVisibilityChange(self, event):
                        if event.isPopupVisible():
                            SamplerWindow_this._search.focus()

                _4_ = _4_()
                pv.addListener(_4_)
                pv.setStyleName('quickjump')
                pv.setDescription('Quick jump')
                return pv

            def createThemeSelect(self):
                self._theme = ComboBox()
                self._theme.setWidth('32px')
                self._theme.setNewItemsAllowed(False)
                self._theme.setFilteringMode(ComboBox.FILTERINGMODE_CONTAINS)
                self._theme.setImmediate(True)
                self._theme.setNullSelectionAllowed(False)
                for themeName in SamplerApplication_this._THEMES:
                    id = SamplerApplication_this._SAMPLER_THEME_NAME + '-' + themeName
                    self._theme.addItem(id)
                    self._theme.setItemCaption(id, themeName[:1].toUpperCase() + (themeName[1:]) + ' theme')
                    self._theme.setItemIcon(id, self._EMPTY_THEME_ICON)
                currentWindowTheme = self.getTheme()
                self._theme.setValue(currentWindowTheme)
                self._theme.setItemIcon(currentWindowTheme, self._SELECTED_THEME_ICON)

                class _5_(ComboBox.ValueChangeListener):

                    def valueChange(self, event):
                        newTheme = str(event.getProperty().getValue())
                        self.setTheme(newTheme)
                        for themeName in SamplerApplication_this._THEMES:
                            id = SamplerApplication_this._SAMPLER_THEME_NAME + '-' + themeName
                            SamplerWindow_this._theme.setItemIcon(id, SamplerWindow_this._EMPTY_THEME_ICON)
                        SamplerWindow_this._theme.setItemIcon(newTheme, SamplerWindow_this._SELECTED_THEME_ICON)
                        SamplerApplication_this._currentApplicationTheme = newTheme

                _5_ = _5_()
                self._theme.addListener(_5_)
                self._theme.setStyleName('theme-select')
                self._theme.setDescription('Select Theme')
                return self._theme

            def createLogo(self):

                class _6_(Button.ClickListener):

                    def buttonClick(self, event):
                        SamplerWindow_this.setFeature(None)

                _6_ = _6_()
                logo = NativeButton('', _6_)
                logo.setDescription('↶ Home')
                logo.setStyleName(BaseTheme.BUTTON_LINK)
                logo.addStyleName('logo')
                return logo

            def createNextButton(self):

                class _6_(ClickListener):

                    def buttonClick(self, event):
                        curr = SamplerWindow_this._currentFeature.getValue()
                        if curr is None:
                            # Navigate from main view to first sample.
                            next = SamplerApplication_this._allFeatures.firstItemId()
                        else:
                            # Navigate to next sample
                            next = SamplerApplication_this._allFeatures.nextItemId(curr)
                        while next is not None and isinstance(next, FeatureSet):
                            next = SamplerApplication_this._allFeatures.nextItemId(next)
                        if next is not None:
                            SamplerWindow_this._currentFeature.setValue(next)
                        else:
                            # could potentially occur if there is an empty section
                            self.showNotification('Last sample')

                _6_ = _6_()
                b = NativeButton('', _6_)
                b.setStyleName('next')
                b.setDescription('Jump to the next sample')
                return b

            def createPrevButton(self):

                class _6_(ClickListener):

                    def buttonClick(self, event):
                        curr = SamplerWindow_this._currentFeature.getValue()
                        prev = SamplerApplication_this._allFeatures.prevItemId(curr)
                        while prev is not None and isinstance(prev, FeatureSet):
                            prev = SamplerApplication_this._allFeatures.prevItemId(prev)
                        SamplerWindow_this._currentFeature.setValue(prev)

                _6_ = _6_()
                b = NativeButton('', _6_)
                b.setEnabled(False)
                b.setStyleName('previous')
                b.setDescription('Jump to the previous sample')
                return b

            def createTreeSwitch(self):
                b = NativeButton()
                b.setStyleName('tree-switch')
                b.addStyleName('down')
                b.setDescription('Toggle sample tree visibility')

                class _6_(Button.ClickListener):

                    def buttonClick(self, event):
                        if self.b.getStyleName().contains('down'):
                            self.b.removeStyleName('down')
                            SamplerWindow_this._mainSplit.setSplitPosition(0)
                            SamplerWindow_this._navigationTree.setVisible(False)
                            SamplerWindow_this._mainSplit.setLocked(True)
                        else:
                            self.b.addStyleName('down')
                            SamplerWindow_this._mainSplit.setSplitPosition(250, Sizeable.UNITS_PIXELS)
                            SamplerWindow_this._mainSplit.setLocked(False)
                            SamplerWindow_this._navigationTree.setVisible(True)

                _6_ = _6_()
                b.addListener(_6_)
                self._mainSplit.setSplitPosition(250, Sizeable.UNITS_PIXELS)
                return b

            def createMenuTree(self):
                tree = Tree()
                tree.setImmediate(True)
                tree.setStyleName('menu')
                tree.setContainerDataSource(SamplerApplication_this._allFeatures)

                class _7_(Property.ValueChangeListener):

                    def valueChange(self, event):
                        f = event.getProperty().getValue()
                        v = self.tree.getValue()
                        if (f is not None and not (f == v)) or (f is None and v is not None):
                            self.tree.setValue(f)
                        SamplerWindow_this.removeSubwindows()

                _7_ = _7_()
                self._currentFeature.addListener(_7_)
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < FeatureSet.FEATURES.getFeatures().length):
                        break
                    tree.expandItemsRecursively(FeatureSet.FEATURES.getFeatures()[i])
                tree.expandItemsRecursively(FeatureSet.FEATURES)

                class _8_(Tree.ValueChangeListener):

                    def valueChange(self, event):
                        f = event.getProperty().getValue()
                        SamplerWindow_this.setFeature(f)

                _8_ = _8_()
                tree.addListener(_8_)

                class _9_(Tree.ItemStyleGenerator):

                    def getStyle(self, itemId):
                        f = itemId
                        if f.getSinceVersion().isNew():
                            return 'new'
                        return None

                _9_ = _9_()
                tree.setItemStyleGenerator(_9_)
                return tree

            def updateFeatureList(self, list):
                self._currentList = list
                val = self._currentFeature.getValue()
                if val is None:
                    self._currentList.setFeatureContainer(SamplerApplication_this._allFeatures)
                    self._mainSplit.setSecondComponent(self._currentList)
                elif isinstance(val, FeatureSet):
                    self._currentList.setFeatureContainer(val.getContainer(True))
                    self._mainSplit.setSecondComponent(self._currentList)
                else:
                    self._mainSplit.setSecondComponent(self._featureView)
                    self._featureView.setFeature(val)

        return SamplerWindow(*args, **kwargs)

    def BreadCrumbs(SamplerApplication_this, *args, **kwargs):

        class BreadCrumbs(CustomComponent, ActiveLink.LinkActivatedListener):
            _layout = None

            def __init__(self):
                self._layout = HorizontalLayout()
                self._layout.setSpacing(True)
                self.setCompositionRoot(self._layout)
                self.setStyleName('breadcrumbs')
                self.setPath(None)

            def setPath(self, path):
                # could be optimized: always builds path from scratch
                # home
                self._layout.removeAllComponents()
                link = ActiveLink('Home', ExternalResource('#'))
                link.addListener(self)
                self._layout.addComponent(link)
                if path is not None and not ('' == path):
                    parts = path.split('/')
                    link = None
                    _0 = True
                    i = 0
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            i += 1
                        if not (i < len(parts)):
                            break
                        # Label separator = new Label("&raquo;", Label.CONTENT_XHTML);
                        self.separator.setSizeUndefined()
                        self._layout.addComponent(self.separator)
                        f = FeatureSet.FEATURES.getFeature(parts[i])
                        link = ActiveLink(f.getName(), ExternalResource('#' + f.getFragmentName()))
                        link.setData(f)
                        link.addListener(self)
                        self._layout.addComponent(link)
                    if link is not None:
                        link.setStyleName('bold')

            def linkActivated(self, event):
                if not event.isLinkOpened():
                    SamplerApplication_this.getWindow().setFeature(event.getActiveLink().getData())

        return BreadCrumbs(*args, **kwargs)

    class FeatureList(Component):
        """Components capable of listing Features should implement this."""

        def setFeatureContainer(self, c):
            """Shows the given Features

            @param c
                       Container with Features to show.
            """
            pass

    def FeatureTable(SamplerApplication_this, *args, **kwargs):

        class FeatureTable(Table, FeatureList):
            """Table -mode FeatureList. Displays the features in a Table."""

            def __init__(self):
                self.setStyleName('featuretable')
                self.alwaysRecalculateColumnWidths = True
                self.setSelectable(False)
                self.setSizeFull()
                self.setColumnHeaderMode(Table.COLUMN_HEADER_MODE_HIDDEN)

                class _11_(Table.ColumnGenerator):

                    def generateCell(self, source, itemId, columnId):
                        f = itemId
                        if isinstance(f, FeatureSet):
                            # no icon for sections
                            return None
                        resId = '75-' + f.getIconName()
                        res = SamplerApplication_this.getSampleIcon(resId)
                        emb = Embedded('', res)
                        emb.setWidth('48px')
                        emb.setHeight('48px')
                        emb.setType(Embedded.TYPE_IMAGE)
                        return emb

                _11_ = _11_()
                self.addGeneratedColumn(Feature.PROPERTY_ICON, _11_)

                class _12_(Table.ColumnGenerator):

                    def generateCell(self, source, itemId, columnId):
                        feature = itemId
                        if isinstance(feature, FeatureSet):
                            return None
                        else:
                            b = ActiveLink('View sample ‣', ExternalResource('#' + feature.getFragmentName()))

                            class _12_(ActiveLink.LinkActivatedListener):

                                def linkActivated(self, event):
                                    if not event.isLinkOpened():
                                        SamplerApplication_this.getWindow().setFeature(self.feature)

                            _12_ = _12_()
                            b.addListener(_12_)
                            b.setStyleName(BaseTheme.BUTTON_LINK)
                            return b

                _12_ = _12_()
                self.addGeneratedColumn('', _12_)

                class _14_(ItemClickListener):

                    def itemClick(self, event):
                        f = event.getItemId()
                        if (
                            ((event.getButton() == ItemClickEvent.BUTTON_MIDDLE) or event.isCtrlKey()) or event.isShiftKey()
                        ):
                            SamplerApplication_this.getWindow().open(ExternalResource(self.getURL() + '#' + f.getFragmentName()), '_blank')
                        else:
                            SamplerApplication_this.getWindow().setFeature(f)

                _14_ = _14_()
                self.addListener(_14_)

                class _15_(self.CellStyleGenerator):

                    def getStyle(self, itemId, propertyId):
                        if propertyId is None and isinstance(itemId, FeatureSet):
                            if SamplerApplication_this._allFeatures.isRoot(itemId):
                                return 'section'
                            else:
                                return 'subsection'
                        return None

                _15_ = _15_()
                self.setCellStyleGenerator(_15_)

            def setFeatureContainer(self, c):
                self.setContainerDataSource(c)
                self.setVisibleColumns([Feature.PROPERTY_ICON, Feature.PROPERTY_NAME, ''])
                self.setColumnWidth(Feature.PROPERTY_ICON, 60)

        return FeatureTable(*args, **kwargs)

    _sampleIconCache = dict()

    def getSampleIcon(self, resId):
        res = self._sampleIconCache[resId]
        if res is None:
            res = ThemeResource('../sampler/icons/sampleicons/' + resId)
            self._sampleIconCache.put(resId, res)
        return res

    def FeatureGrid(SamplerApplication_this, *args, **kwargs):

        class FeatureGrid(Panel, FeatureList):
            _grid = CssLayout()

            def __init__(self):
                self.setSizeFull()
                self.setScrollable(True)
                self.setContent(self._grid)
                self.setStyleName(Reindeer.PANEL_LIGHT)
                self._grid.setStyleName('grid')

            def setFeatureContainer(self, c):
                self._grid.removeAllComponents()
                features = c.getItemIds()
                rootSet = CssLayout()
                rootTitle = None
                highlightRow = CssLayout()
                highlightRow.setStyleName('highlight-row')
                sampleCount = 0
                _0 = True
                it = features
                while True:
                    if _0 is True:
                        _0 = False
                    if not it.hasNext():
                        break
                    f = it.next()
                    if isinstance(f, FeatureSet):
                        if c.isRoot(f):
                            if rootTitle is not None:
                                rootTitle.setValue('<em>' + sampleCount + ' samples</em>' + rootTitle.getValue())
                                sampleCount = 0
                            # rootTitle = new Label("<h2>"
                            # + f.getName()
                            # + "</h2><span>"
                            # + f.getDescription().substring(0,
                            # f.getDescription().indexOf(".") + 1)
                            # + "</span>", Label.CONTENT_XHTML);
                            rootTitle.setSizeUndefined()
                            if f.getRelatedFeatures() is not None:
                                rootTitle.setValue('<em>' + f.getRelatedFeatures().length + ' samples</em>' + rootTitle.getValue())
                            rootSet = CssLayout()
                            rootSet.setStyleName('root')
                            rootTitle.setStyleName('root-section')
                            self._grid.addComponent(rootTitle)
                            self._grid.addComponent(rootSet)
                    else:
                        sampleCount += 1
                        resId = '75-' + f.getIconName()
                        res = SamplerApplication_this.getSampleIcon(resId)
                        if rootSet.getParent() is None:
                            # This sample is directly inside a non root feature
                            # set, we present these with higher priority
                            if rootTitle is None:
                                parent = SamplerApplication_this._allFeatures.getParent(f)
                                # rootTitle = new Label("<h2>" + parent.getName()
                                # + "</h2>", Label.CONTENT_XHTML);
                                rootTitle.setStyleName('root-section highlights-title')
                                rootTitle.setSizeUndefined()
                                self._grid.addComponent(rootTitle)
                                if parent.getDescription() is not None:
                                    # Label desc = new Label(parent.getDescription(),
                                    # Label.CONTENT_XHTML);
                                    self.desc.setStyleName('highlights-description')
                                    self.desc.setSizeUndefined()
                                    self._grid.addComponent(self.desc)
                            # Two samples per row
                            if sampleCount % 2 == 1:
                                highlightRow = CssLayout()
                                highlightRow.setStyleName('highlight-row')
                                self._grid.addComponent(highlightRow)
                            l = CssLayout()
                            l.setStyleName('highlight')
                            sample = ActiveLink(f.getName(), ExternalResource('#' + f.getFragmentName()))
                            sample.setIcon(res)
                            if f.getSinceVersion().isNew():
                                sample.addStyleName('new')
                            l.addComponent(sample)
                            if f.getDescription() is not None and f.getDescription() != '':
                                # Label desc = new Label(
                                # f.getDescription()
                                # .substring(
                                # 0,
                                # f.getDescription().indexOf(
                                # ".") + 1),
                                # Label.CONTENT_XHTML);
                                self.desc.setSizeUndefined()
                                l.addComponent(self.desc)
                            highlightRow.addComponent(l)
                        else:
                            sample = ActiveLink(f.getName(), ExternalResource('#' + f.getFragmentName()))
                            sample.setStyleName(BaseTheme.BUTTON_LINK)
                            sample.addStyleName('screenshot')
                            if f.getDescription() is not None and f.getDescription() != '':
                                sample.setDescription(f.getDescription()[:f.getDescription().index('.') + 1])
                            if f.getSinceVersion().isNew():
                                sample.addStyleName('new')
                            sample.setIcon(res)
                            rootSet.addComponent(sample)
                if rootTitle is not None:
                    rootTitle.setValue('<em>' + sampleCount + ' samples</em>' + rootTitle.getValue())

        return FeatureGrid(*args, **kwargs)

    @classmethod
    def getAllFeatures(cls):
        return cls._allFeatures

    class SourceWindow(Window):

        def __init__(self):

            class _16_(URIHandler):

                def handleURI(self, context, relativeUri):
                    f = FeatureSet.FEATURES.getFeature(relativeUri)
                    if f is not None:
                        self.addComponent(CodeLabel(f.getSource()))
                    else:
                        self.addComponent(Label('Sorry, no source found for ' + relativeUri))
                    return None

            _16_ = _16_()
            self.addURIHandler(_16_)
            SamplerApplication_this = self
            SourceWindow_this = self

            class _17_(self.CloseListener):

                def windowClose(self, e):
                    SamplerApplication_this.removeWindow(SourceWindow_this)

            _17_ = _17_()
            self.addListener(_17_)

    def close(self):
        self.removeWindow(self.getMainWindow())
        super(SamplerApplication, self).close()
