
from muntjac.api import Application

from muntjac.demo.sampler.CodeLabel import CodeLabel
from muntjac.demo.sampler.FeatureSet import FeatureSet
from muntjac.demo.sampler.FeatureView import FeatureView
from muntjac.demo.sampler.GoogleAnalytics import GoogleAnalytics
from muntjac.demo.sampler.Feature import Feature
from muntjac.demo.sampler.ActiveLink import ActiveLink, ILinkActivatedListener
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.data.util.object_property import ObjectProperty

from muntjac.api import \
    (UriFragmentUtility, VerticalLayout, HorizontalLayout, Table, Panel,
     Window, Alignment, HorizontalSplitPanel, CssLayout, ComboBox, PopupView,
     NativeButton, Tree, CustomComponent, Label, Embedded)

from muntjac.ui import window, button, table, tree as ui_tree
from muntjac.ui.themes import BaseTheme, Reindeer
from muntjac.data  import property as prop

from muntjac.event.item_click_event import IItemClickListener, ItemClickEvent
from muntjac.terminal.uri_handler import IUriHandler
from muntjac.terminal.sizeable import ISizeable
from muntjac.terminal.class_resource import ClassResource
from muntjac.terminal.external_resource import ExternalResource
from muntjac.ui.uri_fragment_utility import IFragmentChangedListener
from muntjac.ui.popup_view import IPopupVisibilityListener

from muntjac.ui.component import IComponent


class SamplerApplication(Application):

    # All features in one container
    _allFeatures = FeatureSet.FEATURES.getContainer(True)

    _sampleIconCache = dict()

    # init() inits
    _THEMES = ['reindeer', 'runo']
    _SAMPLER_THEME_NAME = 'sampler'

    # used when trying to guess theme location
    _APP_URL = ''


    def __init__(self):
        super(SamplerApplication, self).__init__()

        self._currentApplicationTheme = (self._SAMPLER_THEME_NAME +
                '-' + self._THEMES[0])


    def init(self):
        self.setMainWindow(SamplerWindow(self))
        url = self.getURL()
        self._APP_URL = str(self.getURL()) if url is not None else ''


    @classmethod
    def getThemeBase(cls):
        """Tries to guess theme location.
        """
        # Supports multiple browser windows
#        try:
        uri = (cls._APP_URL + '../VAADIN/themes/'
               + cls._SAMPLER_THEME_NAME + '/')
        return uri  # FIXME: normalize
#        except Exception, e:
#            print 'Theme location could not be resolved:' + str(e)
        return '/VAADIN/themes/' + cls._SAMPLER_THEME_NAME + '/'


    def getWindow(self, name):
        w = super(SamplerApplication, self).getWindow(name)
        if w is None:
            if name.startswith('src'):
                w = SourceWindow()
            else:
                w = SamplerWindow(self)
                w.setName(name)
            self.addWindow(w)
        return w

    @classmethod
    def getFullPathFor(cls, f):
        """Gets absolute path for given Feature

        @param f:
                   the Feature whose path to get, of null if not found
        @return: the path of the Feature
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
        """Gets the instance for the given Feature class,
        e.g DummyFeature.__class__.
        """
        for f in cls._allFeatures.getItemIds():
            if f.__class__ == clazz:
                return f
        return None


    def getSampleIcon(self, resId):
        res = self._sampleIconCache.get(resId)
        if res is None:
            res = ThemeResource('../sampler/icons/sampleicons/' + resId)
            self._sampleIconCache[resId] = res
        return res


    @classmethod
    def getAllFeatures(cls):
        return cls._allFeatures


    def close(self):
        self.removeWindow(self.getMainWindow())
        super(SamplerApplication, self).close()


_EMPTY_THEME_ICON = ThemeResource('../sampler/sampler/icon-empty.png')
_SELECTED_THEME_ICON = ThemeResource('../sampler/sampler/select-bullet.png')


class SamplerWindow(Window):
    """The main window for Sampler, contains the full application UI."""

    _TITLE = 'Muntjac Sampler'

    def __init__(self, app):
        super(SamplerWindow, self).__init__()

        self._app = app

        self._currentList = FeatureGrid(self._app)
        self._featureView = FeatureView()
        self._currentFeature = ObjectProperty(None, Feature)

        self._mainSplit = None
        self._navigationTree = None
#        self._webAnalytics = GoogleAnalytics('UA-658457-6', 'none')
        # "backbutton"
        self._uriFragmentUtility = UriFragmentUtility()

        # breadcrumbs
        self._breadcrumbs = BreadCrumbs(self)

        self._previousSample = None
        self._nextSample = None
        self._search = None
        self.theme = None

        # Main top/expanded-bottom layout
        mainExpand = VerticalLayout()
        self.setContent(mainExpand)
        self.setSizeFull()
        mainExpand.setSizeFull()
        self.setCaption(self._TITLE)
        self.setTheme(self._app._currentApplicationTheme)

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
#        nav.addComponent(self._webAnalytics)

        # "backbutton"
        nav.addComponent(self._uriFragmentUtility)

        self._uriFragmentUtility.addListener(UriListener(self),
                IFragmentChangedListener)

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

        self.addListener(WindowCloseListener(self, self._app),
                window.ICloseListener)
        self.updateFeatureList(self._currentList)


    def detach(self):
        super(SamplerWindow, self).detach()
        self._search.setContainerDataSource(None)
        self._navigationTree.setContainerDataSource(None)


    def removeSubwindows(self):
        wins = self.getChildWindows()
        if None is not wins:
            for w in wins:
                self.removeWindow(w)


    def setFeature(self, arg):
        """Displays a Feature(Set) or displays a Feature(Set) matching the
        given path, or the main view if no matching Feature(Set) is found.

        @param arg:
                   Either the Feature(Set) to show or the path of the
                   Feature(Set) to show
        """
        if isinstance(arg, basestring):
            path = arg
            f = FeatureSet.FEATURES.getFeature(path)
            self.setFeature(f)
        else:
            f = arg
            if f == FeatureSet.FEATURES:
                # "All" is no longer in the tree, use null instead
                f = None
            self._currentFeature.setValue(f)
            fragment = f.getFragmentName() if f is not None else ''

#            self._webAnalytics.trackPageview(fragment)
            self._uriFragmentUtility.setFragment(fragment, False)
            self._breadcrumbs.setPath( self._app.getFullPathFor(f) )

            self._previousSample.setEnabled(f is not None)
            self._nextSample.setEnabled(not self._app._allFeatures.isLastId(f))

            self.updateFeatureList(self._currentList)

            self.setCaption((f.getName() + ': ' if f is not None else '')
                    + self._TITLE)

    # SamplerWindow helpers

    def createSearch(self):
        self._search = ComboBox()
        self._search.setWidth('160px')
        self._search.setNewItemsAllowed(False)
        self._search.setFilteringMode(ComboBox.FILTERINGMODE_CONTAINS)
        self._search.setNullSelectionAllowed(True)
        self._search.setImmediate(True)
        self._search.setInputPrompt('Search samples...')
        self._search.setContainerDataSource( self._app._allFeatures )

        for idd in self._app._allFeatures.getItemIds():
            if isinstance(idd, FeatureSet):
                pass  # FIXME: 'SamplerApplication' has no attribute 'getResourceAsStream'
#                self._search.setItemIcon(idd,
#                        ClassResource('folder.gif', self._app))

        self._search.addListener(SearchListener(self),
                prop.IValueChangeListener)

        # TODO add icons for section/sample
        # PopupView pv = new PopupView("", search) { public void
        # changeVariables(Object source, Map variables) {
        # super.changeVariables(source, variables); if (isPopupVisible()) {
        # search.focus(); } } };

        pv = PopupView('<span></span>', self._search)

        pv.addListener(PopupListener(self),
                IPopupVisibilityListener)
        pv.setStyleName('quickjump')
        pv.setDescription('Quick jump')

        return pv


    def createThemeSelect(self):
        self.theme = ComboBox()
        self.theme.setWidth('32px')
        self.theme.setNewItemsAllowed(False)
        self.theme.setFilteringMode(ComboBox.FILTERINGMODE_CONTAINS)
        self.theme.setImmediate(True)
        self.theme.setNullSelectionAllowed(False)
        for themeName in self._app._THEMES:
            idd = self._app._SAMPLER_THEME_NAME + '-' + themeName
            self.theme.addItem(idd)
            self.theme.setItemCaption(idd,
                    themeName[:1].upper() + (themeName[1:]) + ' theme')
            self.theme.setItemIcon(idd, _EMPTY_THEME_ICON)
        currentWindowTheme = self.getTheme()
        self.theme.setValue(currentWindowTheme)
        self.theme.setItemIcon(currentWindowTheme, _SELECTED_THEME_ICON)

        self.theme.addListener(ThemeChangeListener(self, self._app),
                prop.IValueChangeListener)
        self.theme.setStyleName('theme-select')
        self.theme.setDescription('Select Theme')
        return self.theme


    def createLogo(self):
        logo = NativeButton('', LogoClickListener(self))
        logo.setDescription('Home')
        logo.setStyleName(BaseTheme.BUTTON_LINK)
        logo.addStyleName('logo')
        return logo


    def createNextButton(self):
        b = NativeButton('', NextClickListener(self, self._app))
        b.setStyleName('next')
        b.setDescription('Jump to the next sample')
        return b


    def createPrevButton(self):
        b = NativeButton('', PrevClickListener(self, self._app))
        b.setEnabled(False)
        b.setStyleName('previous')
        b.setDescription('Jump to the previous sample')
        return b


    def createTreeSwitch(self):
        b = NativeButton()
        b.setStyleName('tree-switch')
        b.addStyleName('down')
        b.setDescription('Toggle sample tree visibility')

        b.addListener(TreeClickListener(self),
                button.IClickListener)
        self._mainSplit.setSplitPosition(250, ISizeable.UNITS_PIXELS)
        return b


    def createMenuTree(self):
        tree = Tree()
        tree.setImmediate(True)
        tree.setStyleName('menu')
        tree.setContainerDataSource(self._app._allFeatures)

        self._currentFeature.addListener(FeatureChangeListener(self, tree),
                prop.IValueChangeListener)
        for f in FeatureSet.FEATURES.getFeatures():
            tree.expandItemsRecursively(f)
        tree.expandItemsRecursively(FeatureSet.FEATURES)

        tree.addListener(TreeChangeListener(self),
                prop.IValueChangeListener)

        tree.setItemStyleGenerator(TreeStyleGenerator())
        return tree


    def updateFeatureList(self, lst):
        self._currentList = lst
        val = self._currentFeature.getValue()
        if val is None:
            self._currentList.setFeatureContainer(self._app._allFeatures)
            self._mainSplit.setSecondComponent(self._currentList)
        elif isinstance(val, FeatureSet):
            self._currentList.setFeatureContainer(val.getContainer(True))
            self._mainSplit.setSecondComponent(self._currentList)
        else:
            self._mainSplit.setSecondComponent(self._featureView)
            self._featureView.setFeature(val)


class BreadCrumbs(CustomComponent, ILinkActivatedListener):

    def __init__(self, window):
        super(BreadCrumbs, self).__init__()

        self._window = window

        self._layout = HorizontalLayout()
        self._layout.setSpacing(True)
        self.setCompositionRoot(self._layout)
        self.setStyleName('breadcrumbs')
        self.setPath(None)


    def setPath(self, path):
        # could be optimized: always builds path from scratch home
        self._layout.removeAllComponents()
        link = ActiveLink('Home', ExternalResource('#'))
        link.addListener(self, ILinkActivatedListener)
        self._layout.addComponent(link)
        if path is not None and not ('' == path):
            parts = path.split('/')
            link = None
            for part in parts:
                separator = Label("&raquo;", Label.CONTENT_XHTML);
                separator.setSizeUndefined()
                self._layout.addComponent(separator)
                f = FeatureSet.FEATURES.getFeature(part)
                link = ActiveLink(f.getName(),
                        ExternalResource('#' + f.getFragmentName()))
                link.setData(f)
                link.addListener(self, ILinkActivatedListener)
                self._layout.addComponent(link)
            if link is not None:
                link.setStyleName('bold')


    def linkActivated(self, event):
        if not event.isLinkOpened():
            self._window.getWindow().setFeature(event.getActiveLink().getData())


class IFeatureList(IComponent):
    """Components capable of listing Features should implement this."""

    def setFeatureContainer(self, c):
        """Shows the given Features

        @param c
                   Container with Features to show.
        """
        pass


class FeatureTable(Table, IFeatureList):
    """Table -mode FeatureList. Displays the features in a Table."""

    def __init__(self, app):
        super(FeatureTable, self).__init__()

        self._app = app

        self.setStyleName('featuretable')
        self.alwaysRecalculateColumnWidths = True
        self.setSelectable(False)
        self.setSizeFull()
        self.setColumnHeaderMode(Table.COLUMN_HEADER_MODE_HIDDEN)

        self.addGeneratedColumn(Feature.PROPERTY_ICON,
                IconColumnGenerator(self._app))

        self.addGeneratedColumn('', TableColumnGenerator(self._app))

        self.addListener(FeatureTableClickListener(self._app),
                IItemClickListener)

        self.setCellStyleGenerator(FeatureCellStyleGenerator(self._app))


    def setFeatureContainer(self, c):
        self.setContainerDataSource(c)
        self.setVisibleColumns([Feature.PROPERTY_ICON,
                Feature.PROPERTY_NAME, ''])
        self.setColumnWidth(Feature.PROPERTY_ICON, 60)


class FeatureGrid(Panel, IFeatureList):

    def __init__(self, app):
        super(FeatureGrid, self).__init__()

        self._app = app

        self._grid = CssLayout()

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
        for f in features:
            if isinstance(f, FeatureSet):
                if c.isRoot(f):
                    if rootTitle is not None:
                        rootTitle.setValue(('<em>' + str(sampleCount)
                                + ' samples</em>' + rootTitle.getValue()))
                        sampleCount = 0
                    desc = f.getDescription()
                    try:
                        idx = desc.index(".")
                    except ValueError:
                        idx = -1
                    rootTitle = Label("<h2>"
                            + f.getName()
                            + "</h2><span>"
                            + desc[:idx + 1]
                            + "</span>", Label.CONTENT_XHTML)
                    rootTitle.setSizeUndefined()
                    if f.getRelatedFeatures() is not None:
                        rootTitle.setValue('<em>'
                                + len(f.getRelatedFeatures())
                                + ' samples</em>'
                                + rootTitle.getValue())
                    rootSet = CssLayout()
                    rootSet.setStyleName('root')
                    rootTitle.setStyleName('root-section')
                    self._grid.addComponent(rootTitle)
                    self._grid.addComponent(rootSet)
            else:
                sampleCount += 1
                resId = '75-' + f.getIconName()
                res = self._app.getSampleIcon(resId)
                if rootSet.getParent() is None:
                    # This sample is directly inside a non root feature
                    # set, we present these with higher priority
                    if rootTitle is None:
                        parent = self._app._allFeatures.getParent(f)
                        rootTitle = Label("<h2>" + parent.getName()
                                + "</h2>", Label.CONTENT_XHTML)
                        rootTitle.setStyleName('root-section highlights-title')
                        rootTitle.setSizeUndefined()
                        self._grid.addComponent(rootTitle)
                        if parent.getDescription() is not None:
                            desc = Label(parent.getDescription(),
                                    Label.CONTENT_XHTML)
                            desc.setStyleName('highlights-description')
                            desc.setSizeUndefined()
                            self._grid.addComponent(desc)
                    # Two samples per row
                    if sampleCount % 2 == 1:
                        highlightRow = CssLayout()
                        highlightRow.setStyleName('highlight-row')
                        self._grid.addComponent(highlightRow)
                    l = CssLayout()
                    l.setStyleName('highlight')
                    er = ExternalResource('#' + f.getFragmentName())
                    sample = ActiveLink(f.getName(), er)
                    sample.setIcon(res)
#                    if f.getSinceVersion().isNew():
#                        sample.addStyleName('new')
                    l.addComponent(sample)
                    if (f.getDescription() is not None
                            and f.getDescription() != ''):
                        d = f.getDescription()
                        desc = Label(d[:d.index(".") + 1], Label.CONTENT_XHTML)
                        desc.setSizeUndefined()
                        l.addComponent(desc)
                    highlightRow.addComponent(l)
                else:
                    sample = ActiveLink(f.getName(),
                            ExternalResource('#' + f.getFragmentName()))
                    sample.setStyleName(BaseTheme.BUTTON_LINK)
                    sample.addStyleName('screenshot')
                    if (f.getDescription() is not None
                            and f.getDescription() != ''):
                        desc = f.getDescription()
                        try:
                            idx = desc.index('.')
                        except ValueError:
                            idx = -1
                        sample.setDescription(desc[:idx + 1])
#                    if f.getSinceVersion().isNew():
#                        sample.addStyleName('new')
                    sample.setIcon(res)
                    rootSet.addComponent(sample)
        if rootTitle is not None:
            rootTitle.setValue('<em>' + str(sampleCount) + ' samples</em>'
                    + rootTitle.getValue())


class SourceWindow(Window):

    def __init__(self, app):
        super(SourceWindow, self).__init__()

        self.addURIHandler( SourceUriHandler() )

        self.addListener(SourceWindowCloseListener(app),
                window.ICloseListener)


class UriListener(IFragmentChangedListener):

    def __init__(self, window):
        self._window = window

    def fragmentChanged(self, source):
        frag = source.getUriFragmentUtility().getFragment()
        if (frag is not None) and ('/' in frag):
            parts = frag.split('/')
            frag = parts[len(parts) - 1]
        self._window.setFeature(frag)


class WindowCloseListener(window.ICloseListener):

    def __init__(self, window, app):
        self._window = window
        self._app = app

    def windowClose(self, e):
        if self._app.getMainWindow() != self._window:
            self._app.removeWindow(self._window)


class SearchListener(prop.IValueChangeListener):

    def __init__(self, window):
        self._window = window

    def valueChange(self, event):
        f = event.getProperty().getValue()
        if f is not None:
            self._window.setFeature(f)
            event.getProperty().setValue(None)


class PopupListener(IPopupVisibilityListener):

    def __init__(self, window):
        self._window = window

    def popupVisibilityChange(self, event):
        if event.isPopupVisible():
            self._window._search.focus()


class ThemeChangeListener(prop.IValueChangeListener):

    def __init__(self, window, app):
        self._window = window
        self._app = app

    def valueChange(self, event):
        newTheme = str(event.getProperty().getValue())
        self._window.setTheme(newTheme)
        for themeName in self._app._THEMES:
            idd = self._app._SAMPLER_THEME_NAME + '-' + themeName
            self._window.theme.setItemIcon(idd, _EMPTY_THEME_ICON)
        self._window.theme.setItemIcon(newTheme, _SELECTED_THEME_ICON)
        self._app._currentApplicationTheme = newTheme


class LogoClickListener(button.IClickListener):

    def __init__(self, window):
        self._window = window

    def buttonClick(self, event):
        self._window.setFeature(None)


class NextClickListener(button.IClickListener):

    def __init__(self, window, app):
        self._window = window
        self._app = app

    def buttonClick(self, event):
        curr = self._window._currentFeature.getValue()
        if curr is None:
            # Navigate from main view to first sample.
            nextt = self._app._allFeatures.firstItemId()
        else:
            # Navigate to next sample
            nextt = self._app._allFeatures.nextItemId(curr)

        while nextt is not None and isinstance(nextt, FeatureSet):
            nextt = self._app._allFeatures.nextItemId(nextt)

        if nextt is not None:
            self._window._currentFeature.setValue(nextt)
        else:
            # could potentially occur if there is an empty section
            self.showNotification('Last sample')


class PrevClickListener(button.IClickListener):

    def __init__(self, window, app):
        self._window = window
        self._app = app

    def buttonClick(self, event):
        curr = self._window._currentFeature.getValue()
        prev = self._app._allFeatures.prevItemId(curr)
        while prev is not None and isinstance(prev, FeatureSet):
            prev = self._app._allFeatures.prevItemId(prev)
        self._window._currentFeature.setValue(prev)


class TreeClickListener(button.IClickListener):

    def __init__(self, window):
        self._window = window

    def buttonClick(self, event):
        if self.b.getStyleName().contains('down'):
            self.b.removeStyleName('down')
            self._window._mainSplit.setSplitPosition(0)
            self._window._navigationTree.setVisible(False)
            self._window._mainSplit.setLocked(True)
        else:
            self.b.addStyleName('down')
            self._window._mainSplit.setSplitPosition(250,
                    ISizeable.UNITS_PIXELS)
            self._window._mainSplit.setLocked(False)
            self._window._navigationTree.setVisible(True)


class FeatureChangeListener(prop.IValueChangeListener):

    def __init__(self, window, tree):
        self._window = window
        self._tree = tree

    def valueChange(self, event):
        f = event.getProperty().getValue()
        v = self._tree.getValue()
        if ((f is not None and f != v)
                or (f is None and v is not None)):
            self._tree.setValue(f)
        self._window.removeSubwindows()


class TreeChangeListener(prop.IValueChangeListener):

    def __init__(self, window):
        self._window = window

    def valueChange(self, event):
        f = event.getProperty().getValue()
        self._window.setFeature(f)


class TreeStyleGenerator(ui_tree.IItemStyleGenerator):

    def getStyle(self, itemId):
        f = itemId
#        if f.getSinceVersion().isNew():
#            return 'new'
        return None


class IconColumnGenerator(table.IColumnGenerator):

    def __init__(self, app):
        self._app = app

    def generateCell(self, source, itemId, columnId):
        f = itemId
        if isinstance(f, FeatureSet):
            # no icon for sections
            return None
        resId = '75-' + f.getIconName()
        res = self._app.getSampleIcon(resId)
        emb = Embedded('', res)
        emb.setWidth('48px')
        emb.setHeight('48px')
        emb.setType(Embedded.TYPE_IMAGE)
        return emb


class TableColumnGenerator(table.IColumnGenerator):

    def __init__(self, app):
        self._app = app

    def generateCell(self, source, itemId, columnId):
        feature = itemId
        if isinstance(feature, FeatureSet):
            return None
        else:
            b = ActiveLink('View sample',
                    ExternalResource('#' + feature.getFragmentName()))

            b.addListener(LinkListener(self._app),
                    ILinkActivatedListener)

            b.setStyleName(BaseTheme.BUTTON_LINK)
            return b

class LinkListener(ILinkActivatedListener):

    def __init__(self, app):
        self._app = app

    def linkActivated(self, event):
        if not event.isLinkOpened():
            self._app.getWindow().setFeature(self.feature)


class FeatureTableClickListener(IItemClickListener):

    def __init__(self, app):
        self._app = app

    def itemClick(self, event):
        f = event.getItemId()
        if ((event.getButton() == ItemClickEvent.BUTTON_MIDDLE)
                or event.isCtrlKey() or event.isShiftKey()):
            er = ExternalResource(self.getURL()
                    + '#' + f.getFragmentName())
            self._app.getWindow().open(er, '_blank')
        else:
            self._app.getWindow().setFeature(f)


class FeatureCellStyleGenerator(table.ICellStyleGenerator):

    def __init__(self, app):
        self._app = app

    def getStyle(self, itemId, propertyId):
        if propertyId is None and isinstance(itemId, FeatureSet):
            if self._app._allFeatures.isRoot(itemId):
                return 'section'
            else:
                return 'subsection'
        return None


class SourceUriHandler(IUriHandler):

    def __init__(self, window):
        self._window = window

    def handleURI(self, context, relativeUri):
        f = FeatureSet.FEATURES.getFeature(relativeUri)
        if f is not None:
            self._window.addComponent(CodeLabel(f.getSource()))
        else:
            lbl = Label('Sorry, no source found for ' + relativeUri)
            self._window.addComponent(lbl)
        return None


class SourceWindowCloseListener(window.ICloseListener):

    def __init__(self, window, app):
        self._app = app
        self._window = window

    def windowClose(self, e):
        self._app.removeWindow(self._window)


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(SamplerApplication, nogui=True, forever=True, debug=True,
            widgetset='com.vaadin.demo.sampler.gwt.SamplerWidgetSet')
