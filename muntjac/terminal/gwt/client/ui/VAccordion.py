# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.ContainerResizedListener import (ContainerResizedListener,)
from com.vaadin.terminal.gwt.client.ui.VTabsheetBase import (VTabsheetBase,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.RenderInformation import (RenderInformation,)
from com.vaadin.terminal.gwt.client.VCaption import (VCaption,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from java.util.HashMap import (HashMap,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.Set import (Set,)


class VAccordion(VTabsheetBase, ContainerResizedListener):
    CLASSNAME = 'v-accordion'
    _paintables = set()
    _height = None
    _width = ''
    _lazyUpdateMap = dict()
    _renderSpace = RenderSpace(0, 0, True)
    _openTab = None
    _rendering = False
    _selectedUIDLItemIndex = -1
    _renderInformation = RenderInformation()

    def __init__(self):
        super(VAccordion, self)(self.CLASSNAME)
        # IE6 needs this to calculate offsetHeight correctly
        if BrowserInfo.get().isIE6():
            DOM.setStyleAttribute(self.getElement(), 'zoom', '1')

    def updateFromUIDL(self, uidl, client):
        self._rendering = True
        self._selectedUIDLItemIndex = -1
        super(VAccordion, self).updateFromUIDL(uidl, client)
        # Render content after all tabs have been created and we know how large
        # the content area is

        if self._selectedUIDLItemIndex >= 0:
            selectedItem = self.getStackItem(self._selectedUIDLItemIndex)
            selectedTabUIDL = self._lazyUpdateMap.remove(selectedItem)
            self.open(self._selectedUIDLItemIndex)
            selectedItem.setContent(selectedTabUIDL)
        elif not uidl.getBooleanAttribute('cached') and self._openTab is not None:
            self.close(self._openTab)
        self.iLayout()
        # finally render possible hidden tabs
        if len(self._lazyUpdateMap) > 0:
            _0 = True
            iterator = self._lazyUpdateMap.keys()
            while True:
                if _0 is True:
                    _0 = False
                if not iterator.hasNext():
                    break
                item = iterator.next()
                item.setContent(self._lazyUpdateMap[item])
            self._lazyUpdateMap.clear()
        self._renderInformation.updateSize(self.getElement())
        self._rendering = False

    def renderTab(self, tabUidl, index, selected, hidden):
        if self.getWidgetCount() <= index:
            # Create stackItem and render caption
            item = self.StackItem(tabUidl)
            if self.getWidgetCount() == 0:
                item.addStyleDependentName('first')
            itemIndex = self.getWidgetCount()
            self.add(item, self.getElement())
        else:
            item = self.getStackItem(index)
            item = self.moveStackItemIfNeeded(item, index, tabUidl)
            itemIndex = index
        item.updateCaption(tabUidl)
        item.setVisible(not hidden)
        if selected:
            self._selectedUIDLItemIndex = itemIndex
        if tabUidl.getChildCount() > 0:
            self._lazyUpdateMap.put(item, tabUidl.getChildUIDL(0))

    def moveStackItemIfNeeded(self, item, newIndex, tabUidl):
        """This method tries to find out if a tab has been rendered with a different
        index previously. If this is the case it re-orders the children so the
        same StackItem is used for rendering this time. E.g. if the first tab has
        been removed all tabs which contain cached content must be moved 1 step
        up to preserve the cached content.

        @param item
        @param newIndex
        @param tabUidl
        @return
        """
        tabContentUIDL = None
        tabContent = None
        if tabUidl.getChildCount() > 0:
            tabContentUIDL = tabUidl.getChildUIDL(0)
            tabContent = self.client.getPaintable(tabContentUIDL)
        itemWidget = item.getComponent()
        if tabContent is not None:
            if tabContent != itemWidget:
                # This is not the same widget as before, find out if it has
                # been moved

                oldIndex = -1
                oldItem = None
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < self.getWidgetCount()):
                        break
                    w = self.getWidget(i)
                    oldItem = w
                    if tabContent == oldItem.getComponent():
                        oldIndex = i
                        break
                if oldIndex != -1 and oldIndex > newIndex:
                    # The tab has previously been rendered in another position
                    # so we must move the cached content to correct position.
                    # We move only items with oldIndex > newIndex to prevent
                    # moving items already rendered in this update. If for
                    # instance tabs 1,2,3 are removed and added as 3,2,1 we
                    # cannot re-use "1" when we get to the third tab.

                    self.insert(oldItem, self.getElement(), newIndex, True)
                    return oldItem
        else:
            # Tab which has never been loaded. Must assure we use an empty
            # StackItem
            oldWidget = item.getComponent()
            if oldWidget is not None:
                item = self.StackItem(tabUidl)
                self.insert(item, self.getElement(), newIndex, True)
        return item

    def open(self, itemIndex):
        item = self.getWidget(itemIndex)
        alreadyOpen = False
        if self._openTab is not None:
            if self._openTab.isOpen():
                if self._openTab == item:
                    alreadyOpen = True
                else:
                    self._openTab.close()
        if not alreadyOpen:
            item.open()
            self.activeTabIndex = itemIndex
            self._openTab = item
        # Update the size for the open tab
        self.updateOpenTabSize()

    def close(self, item):
        if not item.isOpen():
            return
        item.close()
        self.activeTabIndex = -1
        self._openTab = None

    def selectTab(self, index, contentUidl):
        item = self.getStackItem(index)
        if index != self.activeTabIndex:
            self.open(index)
            self.iLayout()
            # TODO Check if this is needed
            self.client.runDescendentsLayout(self)
        item.setContent(contentUidl)

    def onSelectTab(self, item):
        index = self.getWidgetIndex(item)
        if (
            index != self.activeTabIndex and not self.disabled and not self.readonly and not self.disabledTabKeys.contains(self.tabKeys.get(index))
        ):
            self.addStyleDependentName('loading')
            self.client.updateVariable(self.id, 'selected', '' + self.tabKeys.get(index), True)

    def setWidth(self, width):
        if self._width == width:
            return
        Util.setWidthExcludingPaddingAndBorder(self, width, 2)
        self._width = width
        if not self._rendering:
            self.updateOpenTabSize()
            if self.isDynamicHeight():
                Util.updateRelativeChildrenAndSendSizeUpdateEvent(self.client, self._openTab, self)
                self.updateOpenTabSize()
            if self.isDynamicHeight():
                self._openTab.setHeightFromWidget()
            self.iLayout()

    def setHeight(self, height):
        Util.setHeightExcludingPaddingAndBorder(self, height, 2)
        self._height = height
        if not self._rendering:
            self.updateOpenTabSize()

    def updateOpenTabSize(self):
        """Sets the size of the open tab"""
        if self._openTab is None:
            self._renderSpace.setHeight(0)
            self._renderSpace.setWidth(0)
            return
        # WIDTH
        if not self.isDynamicWidth():
            w = self.getOffsetWidth()
            self._openTab.setWidth(w)
            self._renderSpace.setWidth(w)
        else:
            self._renderSpace.setWidth(0)
        # HEIGHT
        if not self.isDynamicHeight():
            usedPixels = 0
            for w in self.getChildren():
                item = w
                if item == self._openTab:
                    usedPixels += item.getCaptionHeight()
                else:
                    # This includes the captionNode borders
                    usedPixels += item.getHeight()
            offsetHeight = self.getOffsetHeight()
            spaceForOpenItem = offsetHeight - usedPixels
            if spaceForOpenItem < 0:
                spaceForOpenItem = 0
            self._renderSpace.setHeight(spaceForOpenItem)
            self._openTab.setHeight(spaceForOpenItem)
        else:
            self._renderSpace.setHeight(0)
            self._openTab.setHeightFromWidget()

    def iLayout(self):
        if self._openTab is None:
            return
        if self.isDynamicWidth():
            maxWidth = 40
            for w in self.getChildren():
                si = w
                captionWidth = si.getCaptionWidth()
                if captionWidth > maxWidth:
                    maxWidth = captionWidth
            widgetWidth = self._openTab.getWidgetWidth()
            if widgetWidth > maxWidth:
                maxWidth = widgetWidth
            super(VAccordion, self).setWidth(maxWidth + 'px')
            self._openTab.setWidth(maxWidth)
        Util.runWebkitOverflowAutoFix(self._openTab.getContainerElement())

    def StackItem(VAccordion_this, *args, **kwargs):

        class StackItem(ComplexPanel, ClickHandler):

            def setHeight(self, height):
                if height == -1:
                    super(StackItem, self).setHeight('')
                    DOM.setStyleAttribute(self._content, 'height', '0px')
                else:
                    super(StackItem, self).setHeight(height + self.getCaptionHeight() + 'px')
                    DOM.setStyleAttribute(self._content, 'height', height + 'px')
                    DOM.setStyleAttribute(self._content, 'top', self.getCaptionHeight() + 'px')

            def getComponent(self):
                if self.getWidgetCount() < 2:
                    return None
                return self.getWidget(1)

            def setVisible(self, visible):
                super(StackItem, self).setVisible(visible)

            def setHeightFromWidget(self):
                paintable = self.getPaintable()
                if paintable is None:
                    return
                paintableHeight = paintable.getElement().getOffsetHeight()
                self.setHeight(paintableHeight)

            def getCaptionWidth(self):
                """Returns caption width including padding

                @return
                """
                if self._caption is None:
                    return 0
                captionWidth = self._caption.getRequiredWidth()
                padding = Util.measureHorizontalPaddingAndBorder(self._caption.getElement(), 18)
                return captionWidth + padding

            def setWidth(self, width):
                if width == -1:
                    super(StackItem, self).setWidth('')
                else:
                    super(StackItem, self).setWidth(width + 'px')

            def getHeight(self):
                return self.getOffsetHeight()

            def getCaptionHeight(self):
                return self._captionNode.getOffsetHeight()

            _caption = None
            _open = False
            _content = DOM.createDiv()
            _captionNode = DOM.createDiv()

            def __init__(self, tabUidl):
                self.setElement(DOM.createDiv())
                self._caption = VCaption(None, self.client)
                self._caption.addClickHandler(self)
                if BrowserInfo.get().isIE6():
                    DOM.setEventListener(self._captionNode, self)
                    DOM.sinkEvents(self._captionNode, Event.BUTTON_LEFT)
                super(StackItem, self).add(self._caption, self._captionNode)
                DOM.appendChild(self._captionNode, self._caption.getElement())
                DOM.appendChild(self.getElement(), self._captionNode)
                DOM.appendChild(self.getElement(), self._content)
                self.setStyleName(VAccordion_this.CLASSNAME + '-item')
                DOM.setElementProperty(self._content, 'className', VAccordion_this.CLASSNAME + '-item-content')
                DOM.setElementProperty(self._captionNode, 'className', VAccordion_this.CLASSNAME + '-item-caption')
                self.close()

            def onBrowserEvent(self, event):
                VAccordion_this.onSelectTab(self)

            def getContainerElement(self):
                return self._content

            def getPaintable(self):
                if self.getWidgetCount() > 1:
                    return self.getWidget(1)
                else:
                    return None

            def replacePaintable(self, newPntbl):
                if self.getWidgetCount() > 1:
                    self.client.unregisterPaintable(self.getWidget(1))
                    VAccordion_this._paintables.remove(self.getWidget(1))
                    self.remove(1)
                self.add(newPntbl, self._content)
                VAccordion_this._paintables.add(newPntbl)

            def open(self):
                self._open = True
                DOM.setStyleAttribute(self._content, 'top', self.getCaptionHeight() + 'px')
                DOM.setStyleAttribute(self._content, 'left', '0px')
                DOM.setStyleAttribute(self._content, 'visibility', '')
                self.addStyleDependentName('open')

            def hide(self):
                DOM.setStyleAttribute(self._content, 'visibility', 'hidden')

            def close(self):
                DOM.setStyleAttribute(self._content, 'visibility', 'hidden')
                DOM.setStyleAttribute(self._content, 'top', '-100000px')
                DOM.setStyleAttribute(self._content, 'left', '-100000px')
                self.removeStyleDependentName('open')
                self.setHeight(-1)
                self.setWidth('')
                if BrowserInfo.get().isIE6():
                    # Work around for IE6 layouting problem #3359
                    self.getElement().getStyle().setProperty('zoom', '1')
                self._open = False

            def isOpen(self):
                return self._open

            def setContent(self, contentUidl):
                newPntbl = self.client.getPaintable(contentUidl)
                if self.getPaintable() is None:
                    self.add(newPntbl, self._content)
                    VAccordion_this._paintables.add(newPntbl)
                elif self.getPaintable() != newPntbl:
                    self.replacePaintable(newPntbl)
                newPntbl.updateFromUIDL(contentUidl, self.client)
                if contentUidl.getBooleanAttribute('cached'):
                    # The size of a cached, relative sized component must be
                    # updated to report correct size.

                    self.client.handleComponentRelativeSize(newPntbl)
                if self.isOpen() and VAccordion_this.isDynamicHeight():
                    self.setHeightFromWidget()

            def onClick(self, event):
                VAccordion_this.onSelectTab(self)

            def updateCaption(self, uidl):
                self._caption.updateCaption(uidl)

            def getWidgetWidth(self):
                return DOM.getFirstChild(self._content).getOffsetWidth()

            def contains(self, p):
                return self.getPaintable() == p

            def isCaptionVisible(self):
                return self._caption.isVisible()

        return StackItem(*args, **kwargs)

    def clearPaintables(self):
        self.clear()

    def isDynamicHeight(self):
        return (self._height is None) or (self._height == '')

    def isDynamicWidth(self):
        return (self._width is None) or (self._width == '')

    def getPaintableIterator(self):
        return self._paintables

    def hasChildComponent(self, component):
        if component in self._paintables:
            return True
        else:
            return False

    def replaceChildComponent(self, oldComponent, newComponent):
        for w in self.getChildren():
            item = w
            if item.getPaintable() == oldComponent:
                item.replacePaintable(newComponent)
                return

    def updateCaption(self, component, uidl):
        # Accordion does not render its children's captions
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
            # TODO Check if this is needed
            self.client.runDescendentsLayout(self)
            return False
        else:
            # Size has not changed so we do not need to propagate the event
            # further

            return True

    def getAllocatedSpace(self, child):
        return self._renderSpace

    def getTabCount(self):
        return self.getWidgetCount()

    def removeTab(self, index):
        item = self.getStackItem(index)
        self.remove(item)

    def getTab(self, index):
        if index < self.getWidgetCount():
            return self.getStackItem(index).getPaintable()
        return None

    def getStackItem(self, index):
        return self.getWidget(index)
