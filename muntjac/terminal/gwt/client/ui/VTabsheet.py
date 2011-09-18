# Copyright (C) 2011 Vaadin Ltd
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __pyjamas__ import (PREDEC,)
from com.vaadin.terminal.gwt.client.VCaption import (VCaption,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.RenderInformation import (RenderInformation,)
from com.vaadin.terminal.gwt.client.ui.VTabsheetBase import (VTabsheetBase,)
from com.vaadin.terminal.gwt.client.ui.VTabsheetPanel import (VTabsheetPanel,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.TooltipInfo import (TooltipInfo,)
from com.vaadin.terminal.gwt.client.ui.VLabel import (VLabel,)
# from com.google.gwt.dom.client.TableElement import (TableElement,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.Set import (Set,)


class VTabsheet(VTabsheetBase):

    class TabSheetCaption(VCaption):
        _hidden = False
        _closable = False
        _closeButton = None

        def __init__(self):
            super(TabSheetCaption, self)(None, self.client)

        def updateCaption(self, uidl):
            if (
                uidl.hasAttribute(self.ATTRIBUTE_DESCRIPTION) or uidl.hasAttribute(self.ATTRIBUTE_ERROR)
            ):
                tooltipInfo = TooltipInfo()
                tooltipInfo.setTitle(uidl.getStringAttribute(self.ATTRIBUTE_DESCRIPTION))
                if uidl.hasAttribute(self.ATTRIBUTE_ERROR):
                    tooltipInfo.setErrorUidl(uidl.getErrors())
                self.client.registerTooltip(_VTabsheet_this, self.getElement(), tooltipInfo)
            else:
                self.client.registerTooltip(_VTabsheet_this, self.getElement(), None)
            ret = super(TabSheetCaption, self).updateCaption(uidl)
            self.setClosable(uidl.hasAttribute('closable'))
            return ret

        def onBrowserEvent(self, event):
            if (
                self._closable and event.getTypeInt() == self.Event.ONCLICK and event.getEventTarget() == self._closeButton
            ):
                tabKey = str(self.tabKeys.get(self.tb.getTabIndex(self)))
                if not self.disabledTabKeys.contains(tabKey):
                    self.client.updateVariable(self.id, 'close', tabKey, True)
                    event.stopPropagation()
                    event.preventDefault()
                    return
            super(TabSheetCaption, self).onBrowserEvent(event)
            if event.getTypeInt() == self.Event.ONLOAD:
                # icon onloads may change total width of tabsheet
                if self.isDynamicWidth():
                    self.updateDynamicWidth()
                self.updateTabScroller()
            self.client.handleTooltipEvent(event, _VTabsheet_this, self.getElement())

        def setWidth(self, width):
            super(TabSheetCaption, self).setWidth(width)
            if BrowserInfo.get().isIE7():
                # IE7 apparently has problems with calculating width for
                # floated elements inside a DIV with padding. Set the width
                # explicitly for the caption.

                self.fixTextWidth()

        def fixTextWidth(self):
            captionText = self.getTextElement()
            if captionText is None:
                return
            captionWidth = Util.getRequiredWidth(captionText)
            scrollWidth = captionText.getScrollWidth()
            if scrollWidth > captionWidth:
                captionWidth = scrollWidth
            captionText.getStyle().setPropertyPx('width', captionWidth)

        def isHidden(self):
            return self._hidden

        def setHidden(self, hidden):
            self._hidden = hidden

        def setClosable(self, closable):
            self._closable = closable
            if closable and self._closeButton is None:
                self._closeButton = self.DOM.createSpan()
                self._closeButton.setInnerHTML('&times;')
                self._closeButton.setClassName(VTabsheet.CLASSNAME + '-caption-close')
                self.getElement().insertBefore(self._closeButton, self.getElement().getLastChild())
            elif not closable and self._closeButton is not None:
                self.getElement().removeChild(self._closeButton)
                self._closeButton = None
            if closable:
                self.addStyleDependentName('closable')
            else:
                self.removeStyleDependentName('closable')

        def getRequiredWidth(self):
            width = super(TabSheetCaption, self).getRequiredWidth()
            if self._closeButton is not None:
                width += Util.getRequiredWidth(self._closeButton)
            return width

    class TabBar(ComplexPanel, ClickHandler):
        _tr = DOM.createTR()
        _spacerTd = DOM.createTD()

        def __init__(self):
            el = self.DOM.createTable()
            tbody = self.DOM.createTBody()
            self.DOM.appendChild(el, tbody)
            self.DOM.appendChild(tbody, self._tr)
            self.setStyleName(self._spacerTd, self.CLASSNAME + '-spacertd')
            self.DOM.appendChild(self._tr, self._spacerTd)
            self.DOM.appendChild(self._spacerTd, self.DOM.createDiv())
            self.setElement(el)

        def getContainerElement(self):
            return self._tr

        _oldSelected = None

        def getTabCount(self):
            return self.getWidgetCount()

        def addTab(self, c):
            td = self.DOM.createTD()
            self.setStyleName(td, self.CLASSNAME + '-tabitemcell')
            if self.getWidgetCount() == 0:
                self.setStyleName(td, self.CLASSNAME + '-tabitemcell-first', True)
            div = self.DOM.createDiv()
            self.setStyleName(div, self.CLASSNAME + '-tabitem')
            self.DOM.appendChild(td, div)
            self.DOM.insertBefore(self._tr, td, self._spacerTd)
            c.addClickHandler(self)
            self.add(c, div)

        def onClick(self, event):
            index = self.getWidgetIndex(event.getSource())
            self.onTabSelected(index)

        def selectTab(self, index):
            classname = self.CLASSNAME + '-tabitem-selected'
            classname2 = self.CLASSNAME + '-tabitemcell-selected' + ('-first' if index == 0 else '')
            newSelected = self.getWidget(index)
            div = newSelected.getElement().getParentElement()
            self.Widget.setStyleName(div, classname, True)
            self.Widget.setStyleName(div.getParentElement(), classname2, True)
            if self._oldSelected is not None and self._oldSelected != newSelected:
                classname2 = self.CLASSNAME + '-tabitemcell-selected' + ('-first' if self.getWidgetIndex(self._oldSelected) == 0 else '')
                divOld = self._oldSelected.getElement().getParentElement()
                self.Widget.setStyleName(divOld, classname, False)
                self.Widget.setStyleName(divOld.getParentElement(), classname2, False)
            self._oldSelected = newSelected
            # The selected tab might need more (or less) space
            self.updateCaptionSize(index)
            self.updateCaptionSize(self.activeTabIndex)

        def removeTab(self, i):
            w = self.getWidget(i)
            if w is None:
                return
            caption = w.getElement()
            div = self.DOM.getParent(caption)
            td = self.DOM.getParent(div)
            tr = self.DOM.getParent(td)
            self.remove(w)
            # Widget is the Caption but we want to remove everything up to and
            # including the parent TD

            self.DOM.removeChild(tr, td)
            # If this widget was selected we need to unmark it as the last
            # selected

            if w == self._oldSelected:
                self._oldSelected = None

        def getTab(self, index):
            if index >= self.getWidgetCount():
                return None
            return self.getWidget(index)

        def getTabIndex(self, tab):
            return self.getChildren().index(tab)

        def setVisible(self, index, visible):
            e = self.getTab(index).getElement().getParentElement().getParentElement()
            if visible:
                e.getStyle().setProperty('display', '')
            else:
                e.getStyle().setProperty('display', 'none')

        def updateCaptionSize(self, index):
            c = self.getTab(index)
            c.setWidth(c.getRequiredWidth() + 'px')

    CLASSNAME = 'v-tabsheet'
    TABS_CLASSNAME = 'v-tabsheet-tabcontainer'
    SCROLLER_CLASSNAME = 'v-tabsheet-scroller'
    _tabs = None
    # tabbar and 'scroller' container
    _scroller = None
    # tab-scroller element
    _scrollerNext = None
    # tab-scroller next button element
    _scrollerPrev = None
    # tab-scroller prev button element
    # The index of the first visible tab (when scrolled)
    _scrollerIndex = 0
    _tb = TabBar()
    _tp = VTabsheetPanel()
    _contentNode = None
    _deco = None
    _captions = dict()
    _height = None
    _width = None
    _waitingForResponse = None
    _renderInformation = RenderInformation()
    # Previous visible widget is set invisible with CSS (not display: none, but
    # visibility: hidden), to avoid flickering during render process. Normal
    # visibility must be returned later when new widget is rendered.

    _previousVisibleWidget = None
    _rendering = False
    _currentStyle = None

    def onTabSelected(self, tabIndex):
        if self.disabled or self._waitingForResponse:
            return
        tabKey = self.tabKeys.get(tabIndex)
        if self.disabledTabKeys.contains(tabKey):
            return
        if self.client is not None and self.activeTabIndex != tabIndex:
            self._tb.selectTab(tabIndex)
            self.addStyleDependentName('loading')
            # run updating variables in deferred command to bypass some FF
            # optimization issues

            class _0_(Command):

                def execute(self):
                    self.previousVisibleWidget = self.tp.getWidget(self.tp.getVisibleWidget())
                    self.DOM.setStyleAttribute(self.DOM.getParent(self.previousVisibleWidget.getElement()), 'visibility', 'hidden')
                    self.client.updateVariable(self.id, 'selected', str(self.tabKeys.get(self.tabIndex)), True)

            _0_ = self._0_()
            self.Scheduler.get().scheduleDeferred(_0_)
            self._waitingForResponse = True

    def isDynamicWidth(self):
        return (self._width is None) or (self._width == '')

    def isDynamicHeight(self):
        return (self._height is None) or (self._height == '')

    def __init__(self):
        super(VTabsheet, self)(self.CLASSNAME)
        # Tab scrolling
        self.DOM.setStyleAttribute(self.getElement(), 'overflow', 'hidden')
        self._tabs = self.DOM.createDiv()
        self.DOM.setElementProperty(self._tabs, 'className', self.TABS_CLASSNAME)
        self._scroller = self.DOM.createDiv()
        self.DOM.setElementProperty(self._scroller, 'className', self.SCROLLER_CLASSNAME)
        self._scrollerPrev = self.DOM.createButton()
        self.DOM.setElementProperty(self._scrollerPrev, 'className', self.SCROLLER_CLASSNAME + 'Prev')
        self.DOM.sinkEvents(self._scrollerPrev, self.Event.ONCLICK)
        self._scrollerNext = self.DOM.createButton()
        self.DOM.setElementProperty(self._scrollerNext, 'className', self.SCROLLER_CLASSNAME + 'Next')
        self.DOM.sinkEvents(self._scrollerNext, self.Event.ONCLICK)
        self.DOM.appendChild(self.getElement(), self._tabs)
        # Tabs
        self._tp.setStyleName(self.CLASSNAME + '-tabsheetpanel')
        self._contentNode = self.DOM.createDiv()
        self._deco = self.DOM.createDiv()
        self.addStyleDependentName('loading')
        # Indicate initial progress
        self._tb.setStyleName(self.CLASSNAME + '-tabs')
        self.DOM.setElementProperty(self._contentNode, 'className', self.CLASSNAME + '-content')
        self.DOM.setElementProperty(self._deco, 'className', self.CLASSNAME + '-deco')
        self.add(self._tb, self._tabs)
        self.DOM.appendChild(self._scroller, self._scrollerPrev)
        self.DOM.appendChild(self._scroller, self._scrollerNext)
        self.DOM.appendChild(self.getElement(), self._contentNode)
        self.add(self._tp, self._contentNode)
        self.DOM.appendChild(self.getElement(), self._deco)
        self.DOM.appendChild(self._tabs, self._scroller)
        # TODO Use for Safari only. Fix annoying 1px first cell in TabBar.
        # DOM.setStyleAttribute(DOM.getFirstChild(DOM.getFirstChild(DOM
        # .getFirstChild(tb.getElement()))), "display", "none");

    def onBrowserEvent(self, event):
        # Tab scrolling
        if (
            self.isScrolledTabs() and self.DOM.eventGetTarget(event) == self._scrollerPrev
        ):
            prevVisible = self.getPreviousVisibleTab(self._scrollerIndex)
            if prevVisible != -1:
                self._tb.setVisible(prevVisible, True)
                self._tb.updateCaptionSize(prevVisible)
                self._scrollerIndex = prevVisible
                self.updateTabScroller()
        elif (
            self.isClippedTabs() and self.DOM.eventGetTarget(event) == self._scrollerNext
        ):
            firstVisible = self._scrollerIndex
            nextVisible = self.getNextVisibleTab(firstVisible)
            if nextVisible != -1:
                self._tb.setVisible(firstVisible, False)
                self._tb.updateCaptionSize(firstVisible)
                self._scrollerIndex = nextVisible
                self.updateTabScroller()
        else:
            super(VTabsheet, self).onBrowserEvent(event)

    def getNextVisibleTab(self, i):
        """Find the next visible tab. Returns -1 if none is found.

        @param i
        @return
        """
        tabs = self._tb.getTabCount()
        while _0 or (i < tabs and self._tb.getTab(i).isHidden()):
            _0 = False
            i += 1
        if i == tabs:
            return -1
        else:
            return i

    def getPreviousVisibleTab(self, i):
        """Find the previous visible tab. Returns -1 if none is found.

        @param i
        @return
        """
        while _0 or (i >= 0 and self._tb.getTab(i).isHidden()):
            _0 = False
            i -= 1
        return i

    def scrolledOutOfView(self, index):
        """Checks if the tab with the selected index has been scrolled out of the
        view (on the left side).

        @param index
        @return
        """
        return self._scrollerIndex > index

    def updateFromUIDL(self, uidl, client):
        self._rendering = True
        if not uidl.getBooleanAttribute('cached'):
            # Handle stylename changes before generics (might affect size
            # calculations)
            self.handleStyleNames(uidl)
        super(VTabsheet, self).updateFromUIDL(uidl, client)
        if self.cachedUpdate:
            self._rendering = False
            return
        # tabs; push or not
        if not self.isDynamicWidth():
            # FIXME: This makes tab sheet tabs go to 1px width on every update
            # and then back to original width
            # update width later, in updateTabScroller();
            self.DOM.setStyleAttribute(self._tabs, 'width', '1px')
            self.DOM.setStyleAttribute(self._tabs, 'overflow', 'hidden')
        else:
            self.showAllTabs()
            self.DOM.setStyleAttribute(self._tabs, 'width', '')
            self.DOM.setStyleAttribute(self._tabs, 'overflow', 'visible')
            self.updateDynamicWidth()
        if not self.isDynamicHeight():
            # Must update height after the styles have been set
            self.updateContentNodeHeight()
            self.updateOpenTabSize()
        self.iLayout()
        # Re run relative size update to ensure optimal scrollbars
        # TODO isolate to situation that visible tab has undefined height
        # Ignore, most likely empty tabsheet
        try:
            client.handleComponentRelativeSize(self._tp.getWidget(self._tp.getVisibleWidget()))
        except Exception, e:
            pass # astStmt: [Stmt([]), None]
        self._renderInformation.updateSize(self.getElement())
        self._waitingForResponse = False
        self._rendering = False

    def handleStyleNames(self, uidl):
        # Add proper stylenames for all elements (easier to prevent unwanted
        # style inheritance)
        if uidl.hasAttribute('style'):
            style = uidl.getStringAttribute('style')
            if self._currentStyle != style:
                self._currentStyle = style
                styles = style.split(' ')
                tabsBaseClass = self.TABS_CLASSNAME
                tabsClass = tabsBaseClass
                contentBaseClass = self.CLASSNAME + '-content'
                contentClass = contentBaseClass
                decoBaseClass = self.CLASSNAME + '-deco'
                decoClass = decoBaseClass
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(styles)):
                        break
                    self._tb.addStyleDependentName(styles[i])
                    tabsClass += ' ' + tabsBaseClass + '-' + styles[i]
                    contentClass += ' ' + contentBaseClass + '-' + styles[i]
                    decoClass += ' ' + decoBaseClass + '-' + styles[i]
                self.DOM.setElementProperty(self._tabs, 'className', tabsClass)
                self.DOM.setElementProperty(self._contentNode, 'className', contentClass)
                self.DOM.setElementProperty(self._deco, 'className', decoClass)
                self._borderW = -1
        else:
            self._tb.setStyleName(self.CLASSNAME + '-tabs')
            self.DOM.setElementProperty(self._tabs, 'className', self.TABS_CLASSNAME)
            self.DOM.setElementProperty(self._contentNode, 'className', self.CLASSNAME + '-content')
            self.DOM.setElementProperty(self._deco, 'className', self.CLASSNAME + '-deco')
        if uidl.hasAttribute('hidetabs'):
            self._tb.setVisible(False)
            self.addStyleName(self.CLASSNAME + '-hidetabs')
        else:
            self._tb.setVisible(True)
            self.removeStyleName(self.CLASSNAME + '-hidetabs')

    def updateDynamicWidth(self):
        # Find width consumed by tabs
        spacerCell = self._tb.getElement().getRows().getItem(0).getCells().getItem(self._tb.getTabCount())
        spacerWidth = spacerCell.getOffsetWidth()
        div = spacerCell.getFirstChildElement()
        spacerMinWidth = spacerCell.getOffsetWidth() - div.getOffsetWidth()
        tabsWidth = (self._tb.getOffsetWidth() - spacerWidth) + spacerMinWidth
        # Find content width
        style = self._tp.getElement().getStyle()
        overflow = style.getProperty('overflow')
        style.setProperty('overflow', 'hidden')
        style.setPropertyPx('width', tabsWidth)
        hasTabs = self._tp.getWidgetCount() > 0
        wrapperstyle = None
        if hasTabs:
            wrapperstyle = self._tp.getWidget(self._tp.getVisibleWidget()).getElement().getParentElement().getStyle()
            wrapperstyle.setPropertyPx('width', tabsWidth)
        # Get content width from actual widget
        contentWidth = 0
        if hasTabs:
            contentWidth = self._tp.getWidget(self._tp.getVisibleWidget()).getOffsetWidth()
        style.setProperty('overflow', overflow)
        # Set widths to max(tabs,content)
        if tabsWidth < contentWidth:
            tabsWidth = contentWidth
        outerWidth = tabsWidth + self.getContentAreaBorderWidth()
        self._tabs.getStyle().setPropertyPx('width', outerWidth)
        style.setPropertyPx('width', tabsWidth)
        if hasTabs:
            wrapperstyle.setPropertyPx('width', tabsWidth)
        self._contentNode.getStyle().setPropertyPx('width', tabsWidth)
        super(VTabsheet, self).setWidth(outerWidth + 'px')
        self.updateOpenTabSize()

    def renderTab(self, tabUidl, index, selected, hidden):
        c = self._tb.getTab(index)
        if c is None:
            c = self.TabSheetCaption()
            self._tb.addTab(c)
        c.updateCaption(tabUidl)
        c.setHidden(hidden)
        if self.scrolledOutOfView(index):
            # Should not set tabs visible if they are scrolled out of view
            hidden = True
        # Set the current visibility of the tab (in the browser)
        self._tb.setVisible(index, not hidden)
        # Force the width of the caption container so the content will not wrap
        # and tabs won't be too narrow in certain browsers

        c.setWidth(c.getRequiredWidth() + 'px')
        self._captions.put('' + index, c)
        tabContentUIDL = None
        tabContent = None
        if tabUidl.getChildCount() > 0:
            tabContentUIDL = tabUidl.getChildUIDL(0)
            tabContent = self.client.getPaintable(tabContentUIDL)
        if tabContent is not None:
            # This is a tab with content information
            oldIndex = self._tp.getWidgetIndex(tabContent)
            if oldIndex != -1 and oldIndex != index:
                # The tab has previously been rendered in another position so
                # we must move the cached content to correct position

                self._tp.insert(tabContent, index)
        elif index < self._tp.getWidgetCount():
            oldWidget = self._tp.getWidget(index)
            if not isinstance(oldWidget, PlaceHolder):
                self._tp.insert(self.PlaceHolder(), index)
        # A tab whose content has not yet been loaded
        # Make sure there is a corresponding empty tab in tp. The same
        # operation as the moving above but for not-loaded tabs.

        if selected:
            self.renderContent(tabContentUIDL)
            self._tb.selectTab(index)
        elif tabContentUIDL is not None:
            # updating a drawn child on hidden tab
            if self._tp.getWidgetIndex(tabContent) < 0:
                self._tp.insert(tabContent, index)
            tabContent.updateFromUIDL(tabContentUIDL, self.client)
        elif self._tp.getWidgetCount() <= index:
            self._tp.add(self.PlaceHolder())

    class PlaceHolder(VLabel):

        def __init__(self):
            super(PlaceHolder, self)('')

    def selectTab(self, index, contentUidl):
        if index != self.activeTabIndex:
            self.activeTabIndex = index
            self._tb.selectTab(self.activeTabIndex)
        self.renderContent(contentUidl)

    def renderContent(self, contentUIDL):
        content = self.client.getPaintable(contentUIDL)
        if self._tp.getWidgetCount() > self.activeTabIndex:
            old = self._tp.getWidget(self.activeTabIndex)
            if old != content:
                self._tp.remove(self.activeTabIndex)
                if isinstance(old, Paintable):
                    self.client.unregisterPaintable(old)
                self._tp.insert(content, self.activeTabIndex)
        else:
            self._tp.add(content)
        self._tp.showWidget(self.activeTabIndex)
        _VTabsheet_this.iLayout()
        content.updateFromUIDL(contentUIDL, self.client)
        # The size of a cached, relative sized component must be updated to
        # report correct size to updateOpenTabSize().

        if contentUIDL.getBooleanAttribute('cached'):
            self.client.handleComponentRelativeSize(content)
        self.updateOpenTabSize()
        _VTabsheet_this.removeStyleDependentName('loading')
        if self._previousVisibleWidget is not None:
            self.DOM.setStyleAttribute(self.DOM.getParent(self._previousVisibleWidget.getElement()), 'visibility', '')
            self._previousVisibleWidget = None

    def setHeight(self, height):
        super(VTabsheet, self).setHeight(height)
        self._height = height
        self.updateContentNodeHeight()
        if not self._rendering:
            self.updateOpenTabSize()
            self.iLayout()
            # TODO Check if this is needed
            self.client.runDescendentsLayout(self)

    def updateContentNodeHeight(self):
        if self._height is not None and not ('' == self._height):
            contentHeight = self.getOffsetHeight()
            contentHeight -= self.DOM.getElementPropertyInt(self._deco, 'offsetHeight')
            contentHeight -= self._tb.getOffsetHeight()
            if contentHeight < 0:
                contentHeight = 0
            # Set proper values for content element
            self.DOM.setStyleAttribute(self._contentNode, 'height', contentHeight + 'px')
            self._renderSpace.setHeight(contentHeight)
        else:
            self.DOM.setStyleAttribute(self._contentNode, 'height', '')
            self._renderSpace.setHeight(0)

    def setWidth(self, width):
        if (
            (self._width is None and width == '') or (self._width is not None and self._width == width)
        ):
            return
        super(VTabsheet, self).setWidth(width)
        if width == '':
            width = None
        self._width = width
        if width is None:
            self._renderSpace.setWidth(0)
            self._contentNode.getStyle().setProperty('width', '')
        else:
            contentWidth = self.getOffsetWidth() - self.getContentAreaBorderWidth()
            if contentWidth < 0:
                contentWidth = 0
            self._contentNode.getStyle().setProperty('width', contentWidth + 'px')
            self._renderSpace.setWidth(contentWidth)
        if not self._rendering:
            if self.isDynamicHeight():
                Util.updateRelativeChildrenAndSendSizeUpdateEvent(self.client, self._tp, self)
            self.updateOpenTabSize()
            self.iLayout()
            # TODO Check if this is needed
            self.client.runDescendentsLayout(self)

    def iLayout(self):
        self.updateTabScroller()
        self._tp.runWebkitOverflowAutoFix()

    def updateOpenTabSize(self):
        """Sets the size of the visible tab (component). As the tab is set to
        position: absolute (to work around a firefox flickering bug) we must keep
        this up-to-date by hand.
        """
        # The overflow=auto element must have a height specified, otherwise it
        # will be just as high as the contents and no scrollbars will appear

        height = -1
        width = -1
        minWidth = 0
        if not self.isDynamicHeight():
            height = self._renderSpace.getHeight()
        if not self.isDynamicWidth():
            width = self._renderSpace.getWidth()
        else:
            # If the tabbar is wider than the content we need to use the tabbar
            # width as minimum width so scrollbars get placed correctly (at the
            # right edge).

            minWidth = self._tb.getOffsetWidth() - self.getContentAreaBorderWidth()
        self._tp.fixVisibleTabSize(width, height, minWidth)

    def updateTabScroller(self):
        """Layouts the tab-scroller elements, and applies styles."""
        if self._width is not None:
            self.DOM.setStyleAttribute(self._tabs, 'width', self._width)
        # Make sure scrollerIndex is valid
        if (self._scrollerIndex < 0) or (self._scrollerIndex > self._tb.getTabCount()):
            self._scrollerIndex = self.getNextVisibleTab(-1)
        elif (
            self._tb.getTabCount() > 0 and self._tb.getTab(self._scrollerIndex).isHidden()
        ):
            self._scrollerIndex = self.getNextVisibleTab(self._scrollerIndex)
        scrolled = self.isScrolledTabs()
        clipped = self.isClippedTabs()
        if self._tb.getTabCount() > 0 and self._tb.isVisible() and scrolled or clipped:
            self.DOM.setStyleAttribute(self._scroller, 'display', '')
            self.DOM.setElementProperty(self._scrollerPrev, 'className', self.SCROLLER_CLASSNAME + ('Prev' if scrolled else 'Prev-disabled'))
            self.DOM.setElementProperty(self._scrollerNext, 'className', self.SCROLLER_CLASSNAME + ('Next' if clipped else 'Next-disabled'))
        else:
            self.DOM.setStyleAttribute(self._scroller, 'display', 'none')
        if BrowserInfo.get().isSafari():
            # fix tab height for safari, bugs sometimes if tabs contain icons
            property = self._tabs.getStyle().getProperty('height')
            if (property is None) or (property == ''):
                self._tabs.getStyle().setPropertyPx('height', self._tb.getOffsetHeight())
            # another hack for webkits. tabscroller sometimes drops without
            # "shaking it" reproducable in
            # com.vaadin.tests.components.tabsheet.TabSheetIcons

            style = self._scroller.getStyle()
            style.setProperty('whiteSpace', 'normal')

            class _1_(Command):

                def execute(self):
                    self.style.setProperty('whiteSpace', '')

            _1_ = self._1_()
            self.Scheduler.get().scheduleDeferred(_1_)

    def showAllTabs(self):
        self._scrollerIndex = self.getNextVisibleTab(-1)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < self._tb.getTabCount()):
                break
            if not self._tb.getTab(i).isHidden():
                self._tb.setVisible(i, True)

    def isScrolledTabs(self):
        return self._scrollerIndex > self.getNextVisibleTab(-1)

    def isClippedTabs(self):
        return self._tb.getOffsetWidth() - self.DOM.getElementPropertyInt(self._tb.getContainerElement().getLastChild(), 'offsetWidth') > self.getOffsetWidth() - (self._scroller.getOffsetWidth() if self.isScrolledTabs() else 0)

    def clearPaintables(self):
        i = self._tb.getTabCount()
        while i > 0:
            self._tb.removeTab(PREDEC(globals(), locals(), 'i'))
        self._tp.clear()

    def getPaintableIterator(self):
        return self._tp

    def hasChildComponent(self, component):
        if self._tp.getWidgetIndex(component) < 0:
            return False
        else:
            return True

    def replaceChildComponent(self, oldComponent, newComponent):
        self._tp.replaceComponent(oldComponent, newComponent)

    def updateCaption(self, component, uidl):
        # Tabsheet does not render its children's captions
        pass

    def requestLayout(self, child):
        if not self.isDynamicHeight() and not self.isDynamicWidth():
            # If the height and width has been specified for this container the
            # child components cannot make the size of the layout change

            # layout size change may affect its available space (scrollbars)
            for paintable in child:
                self.client.handleComponentRelativeSize(paintable)
            return True
        self.updateOpenTabSize()
        if self._renderInformation.updateSize(self.getElement()):
            # Size has changed so we let the child components know about the
            # new size.

            self.iLayout()
            self.client.runDescendentsLayout(self)
            return False
        else:
            # Size has not changed so we do not need to propagate the event
            # further

            return True

    _borderW = -1

    def getContentAreaBorderWidth(self):
        if self._borderW < 0:
            self._borderW = Util.measureHorizontalBorder(self._contentNode)
        return self._borderW

    _renderSpace = RenderSpace(0, 0, True)

    def getAllocatedSpace(self, child):
        # All tabs have equal amount of space allocated
        return self._renderSpace

    def getTabCount(self):
        return self._tb.getWidgetCount()

    def getTab(self, index):
        if self._tp.getWidgetCount() > index:
            return self._tp.getWidget(index)
        return None

    def removeTab(self, index):
        self._tb.removeTab(index)
        # This must be checked because renderTab automatically removes the
        # active tab content when it changes

        if self._tp.getWidgetCount() > index:
            self._tp.remove(index)
