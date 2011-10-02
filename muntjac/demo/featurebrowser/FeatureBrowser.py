# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (POSTINC,)
from com.vaadin.demo.featurebrowser.ValueInputExample import (ValueInputExample,)
from com.vaadin.demo.featurebrowser.LayoutExample import (LayoutExample,)
from com.vaadin.demo.featurebrowser.SelectExample import (SelectExample,)
from com.vaadin.demo.featurebrowser.ButtonExample import (ButtonExample,)
from com.vaadin.demo.featurebrowser.EmbeddedBrowserExample import (EmbeddedBrowserExample,)
from com.vaadin.demo.featurebrowser.AccordionExample import (AccordionExample,)
from com.vaadin.demo.featurebrowser.WindowingExample import (WindowingExample,)
from com.vaadin.demo.featurebrowser.TreeExample import (TreeExample,)
from com.vaadin.demo.featurebrowser.LabelExample import (LabelExample,)
from com.vaadin.demo.featurebrowser.ClientCachingExample import (ClientCachingExample,)
from com.vaadin.demo.featurebrowser.NotificationExample import (NotificationExample,)
from com.vaadin.demo.featurebrowser.RichTextExample import (RichTextExample,)
from com.vaadin.demo.featurebrowser.FormExample import (FormExample,)
from com.vaadin.demo.featurebrowser.TableExample import (TableExample,)
from com.vaadin.demo.featurebrowser.JavaScriptAPIExample import (JavaScriptAPIExample,)
from com.vaadin.demo.featurebrowser.ComboBoxExample import (ComboBoxExample,)
# from com.vaadin.data.util.HierarchicalContainer import (HierarchicalContainer,)
# from com.vaadin.data.util.IndexedContainer import (IndexedContainer,)
# from com.vaadin.terminal.Sizeable import (Sizeable,)
# from com.vaadin.terminal.ThemeResource import (ThemeResource,)
# from com.vaadin.ui.AbstractSelect import (AbstractSelect,)
# from com.vaadin.ui.HorizontalSplitPanel import (HorizontalSplitPanel,)
# from com.vaadin.ui.Tree import (Tree,)
# from com.vaadin.ui.VerticalSplitPanel import (VerticalSplitPanel,)
# from com.vaadin.ui.Window import (Window,)
# from java.util.HashMap import (HashMap,)
import com.vaadin.Application


class FeatureBrowser(com.vaadin.Application.Application, Select.ValueChangeListener):
    """@author IT Mill Ltd.
    @see com.vaadin.ui.Window
    """
    # Property IDs
    _PROPERTY_ID_CATEGORY = 'Category'
    _PROPERTY_ID_NAME = 'Name'
    _PROPERTY_ID_DESC = 'Description'
    _PROPERTY_ID_CLASS = 'Class'
    _PROPERTY_ID_VIEWED = 'Viewed'
    # Global components
    _tree = None
    _table = None
    _ts = None
    # Example "cache"
    _exampleInstances = dict()
    _section = None
    # List of examples
    _demos = ['Getting started', 'Labels', 'Some variations of Labels', LabelExample, 'Getting started', 'Buttons and links', 'Various Buttons and Links', ButtonExample, 'Getting started', 'Basic value input', 'TextFields, DateFields, and such', ValueInputExample, 'Getting started', 'RichText', 'Rich text editing', RichTextExample, 'Getting started', 'Choices, choices', 'Some variations of simple selects', SelectExample, 'Layouts', 'Basic layouts', 'Laying out components', LayoutExample, 'Layouts', 'Accordion', 'Play the Accordion!', AccordionExample, 'Wrangling data', 'ComboBox', 'ComboBox - the swiss army select', ComboBoxExample, 'Wrangling data', 'Table (\"grid\")', 'Table with bells, whistles, editmode and actions (contextmenu)', TableExample, 'Wrangling data', 'Form', 'Every application needs forms', FormExample, 'Wrangling data', 'Tree', 'A hierarchy of things', TreeExample, 'Misc', 'Notifications', 'Notifications can improve usability', NotificationExample, 'Misc', 'Client caching', 'Demonstrating of client-side caching', ClientCachingExample, 'Misc', 'Embedding', 'Embedding resources - another site in this case', EmbeddedBrowserExample, 'Misc', 'Windowing', 'About windowing', WindowingExample, 'Misc', 'JavaScript API', 'JavaScript to Vaadin communication', JavaScriptAPIExample]

    def init(self):
        # Need to set a theme for ThemeResources to work
        self.setTheme('example')
        # Create new window for the application and give the window a visible.
        main = Window('Vaadin 6')
        # set as main window
        self.setMainWindow(main)
        split = HorizontalSplitPanel()
        split.setSplitPosition(200, Sizeable.UNITS_PIXELS)
        main.setContent(split)
        sectionIds = dict()
        container = self.createContainer()
        rootId = container.addItem()
        item = container.getItem(rootId)
        p = item.getItemProperty(self._PROPERTY_ID_NAME)
        p.setValue('All examples')
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._demos)):
                break
            demo = self._demos[i]
            section = demo[0]
            if section in sectionIds:
                sectionId = sectionIds[section]
            else:
                sectionId = container.addItem()
                sectionIds.put(section, sectionId)
                container.setParent(sectionId, rootId)
                item = container.getItem(sectionId)
                p = item.getItemProperty(self._PROPERTY_ID_NAME)
                p.setValue(section)
            id = container.addItem()
            container.setParent(id, sectionId)
            self.initItem(container.getItem(id), demo)
        self._tree = Tree()
        self._tree.setDebugId('FeatureBrowser: Main Tree')
        self._tree.setSelectable(True)
        self._tree.setMultiSelect(False)
        self._tree.setNullSelectionAllowed(False)
        self._tree.setContainerDataSource(container)
        self._tree.setItemCaptionMode(AbstractSelect.ITEM_CAPTION_MODE_PROPERTY)
        self._tree.setItemCaptionPropertyId(self._PROPERTY_ID_NAME)
        self._tree.addListener(self)
        self._tree.setImmediate(True)
        self._tree.expandItemsRecursively(rootId)
        _1 = True
        i = container.getItemIds()
        while True:
            if _1 is True:
                _1 = False
            if not i.hasNext():
                break
            id = i.next()
            if container.getChildren(id) is None:
                self._tree.setChildrenAllowed(id, False)
        split.addComponent(self._tree)
        split2 = VerticalSplitPanel()
        split2.setSplitPosition(200, Sizeable.UNITS_PIXELS)
        split.addComponent(split2)
        self._table = Table()
        self._table.setDebugId('FeatureBrowser: Main Table')
        self._table.setSizeFull()
        self._table.setColumnReorderingAllowed(True)
        self._table.setColumnCollapsingAllowed(True)
        self._table.setSelectable(True)
        self._table.setMultiSelect(False)
        self._table.setNullSelectionAllowed(False)
        # Hide some columns
        try:
            self._table.setContainerDataSource(container.clone())
        except Exception, e:
            e.printStackTrace(System.err)
        self._table.setVisibleColumns([self._PROPERTY_ID_CATEGORY, self._PROPERTY_ID_NAME, self._PROPERTY_ID_DESC, self._PROPERTY_ID_VIEWED])
        self._table.addListener(self)
        self._table.setImmediate(True)
        split2.addComponent(self._table)
        exp = VerticalLayout()
        exp.setSizeFull()
        exp.setMargin(True)
        split2.addComponent(exp)
        wbLayout = HorizontalLayout()

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                component = FeatureBrowser_this._ts.getComponentIterator().next()
                caption = FeatureBrowser_this._ts.getTab(component).getCaption()
                # Could not create
                try:
                    component = component.getClass()()
                except Exception, e:
                    return
                w = Window(caption)
                w.setWidth('640px')
                if Layout.isAssignableFrom(component.getClass()):
                    w.setContent(component)
                else:
                    # w.getLayout().getSize().setSizeFull();
                    w.addComponent(component)
                self.getMainWindow().addWindow(w)

        _0_ = _0_()
        b = Button('Open in sub-window', _0_)
        b.setStyleName(BaseTheme.BUTTON_LINK)
        wbLayout.addComponent(b)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                component = FeatureBrowser_this._ts.getComponentIterator().next()
                caption = FeatureBrowser_this._ts.getTab(component).getCaption()
                w = self.getWindow(caption)
                if w is None:
                    # Could not create
                    try:
                        component = component.getClass()()
                    except Exception, e:
                        return
                    w = Window(caption)
                    w.setName(caption)
                    if Layout.isAssignableFrom(component.getClass()):
                        w.setContent(component)
                    else:
                        # w.getLayout().getSize().setSizeFull();
                        w.addComponent(component)
                    self.addWindow(w)
                self.getMainWindow().open(ExternalResource(w.getURL()), caption)

        _0_ = _0_()
        Button('Open in native window', _0_)
        b = _0_
        b.setStyleName(BaseTheme.BUTTON_LINK)
        wbLayout.addComponent(b)
        exp.addComponent(wbLayout)
        exp.setComponentAlignment(wbLayout, Alignment.TOP_RIGHT)
        self._ts = TabSheet()
        self._ts.setSizeFull()
        self._ts.addTab(Label(''), 'Choose example', None)
        exp.addComponent(self._ts)
        exp.setExpandRatio(self._ts, 1)
        status = Label('<a href=\"http://www.vaadin.com/learn\">30 Seconds to Vaadin</a>' + ' | <a href=\"http://www.vaadin.com/book\">Book of Vaadin</a>')
        # status.setContentMode(Label.CONTENT_XHTML);
        exp.addComponent(status)
        exp.setComponentAlignment(status, Alignment.MIDDLE_RIGHT)
        # select initial section ("All")
        self._tree.setValue(rootId)
        self.getMainWindow().showNotification('Welcome', 'Choose an example to begin.<br/><br/>And remember to experiment!', Window.Notification.TYPE_TRAY_NOTIFICATION)

    def initItem(self, item, data):
        p = 0
        prop = item.getItemProperty(self._PROPERTY_ID_CATEGORY)
        prop.setValue(data[POSTINC(globals(), locals(), 'p')])
        prop = item.getItemProperty(self._PROPERTY_ID_NAME)
        prop.setValue(data[POSTINC(globals(), locals(), 'p')])
        prop = item.getItemProperty(self._PROPERTY_ID_DESC)
        prop.setValue(data[POSTINC(globals(), locals(), 'p')])
        prop = item.getItemProperty(self._PROPERTY_ID_CLASS)
        prop.setValue(data[POSTINC(globals(), locals(), 'p')])

    def createContainer(self):
        c = HierarchicalContainer()
        c.addContainerProperty(self._PROPERTY_ID_CATEGORY, str, None)
        c.addContainerProperty(self._PROPERTY_ID_NAME, str, '')
        c.addContainerProperty(self._PROPERTY_ID_DESC, str, '')
        c.addContainerProperty(self._PROPERTY_ID_CLASS, self.Class, None)
        c.addContainerProperty(self._PROPERTY_ID_VIEWED, Embedded, None)
        return c

    def valueChange(self, event):
        if event.getProperty() == self._tree:
            id = self._tree.getValue()
            if id is None:
                return
            item = self._tree.getItem(id)
            if self._tree.isRoot(id):
                newSection = ''
                # show all sections
            elif self._tree.hasChildren(id):
                newSection = item.getItemProperty(self._PROPERTY_ID_NAME).getValue()
            else:
                newSection = item.getItemProperty(self._PROPERTY_ID_CATEGORY).getValue()
            self._table.setValue(None)
            c = self._table.getContainerDataSource()
            if newSection is not None and not (newSection == self._section):
                c.removeAllContainerFilters()
                c.addContainerFilter(self._PROPERTY_ID_CATEGORY, newSection, False, True)
            self._section = newSection
            if not self._tree.hasChildren(id):
                # Example, not section
                # update table selection
                self._table.setValue(id)
        elif event.getProperty() == self._table:
            if self._table.getValue() is not None:
                self._table.removeListener(self)
                self._tree.setValue(self._table.getValue())
                self._table.addListener(self)
                item = self._table.getItem(self._table.getValue())
                c = item.getItemProperty(self._PROPERTY_ID_CLASS).getValue()
                component = self.getComponent(c)
                if component is not None:
                    caption = item.getItemProperty(self._PROPERTY_ID_NAME).getValue()
                    self._ts.removeAllComponents()
                    self._ts.addTab(component, caption, None)
                # update "viewed" state
                p = item.getItemProperty(self._PROPERTY_ID_VIEWED)
                if p.getValue() is None:
                    p.setValue(Embedded('', ThemeResource('icons/ok.png')))
                self._table.requestRepaint()

    def getComponent(self, componentClass):
        if not (componentClass in self._exampleInstances):
            try:
                c = componentClass()
                self._exampleInstances.put(componentClass, c)
            except Exception, e:
                return None
        return self._exampleInstances[componentClass]
