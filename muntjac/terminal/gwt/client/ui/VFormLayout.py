# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.Container import (Container,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.ui.VMarginInfo import (VMarginInfo,)
from com.vaadin.terminal.gwt.client.StyleConstants import (StyleConstants,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ApplicationConnection import (ApplicationConnection,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.Icon import (Icon,)
from com.vaadin.terminal.gwt.client.Focusable import (Focusable,)
# from com.google.gwt.user.client.ui.FlexTable import (FlexTable,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.List import (List,)
# from java.util.Set import (Set,)


class VFormLayout(SimplePanel, Container):
    """Two col Layout that places caption on left col and field on right col"""
    _CLASSNAME = 'v-formlayout'
    _client = None
    _table = None
    _width = ''
    _height = ''
    _rendering = False

    def __init__(self):
        super(VFormLayout, self)()
        self.setStyleName(self._CLASSNAME)
        self._table = self.VFormLayoutTable()
        self.setWidget(self._table)

    def getStylesFromUIDL(self, uidl):
        """Parses the stylenames from an uidl

        @param uidl
                   The uidl to get the stylenames from
        @return An array of stylenames
        """
        styles = list()
        if uidl.hasAttribute('style'):
            stylesnames = uidl.getStringAttribute('style').split(' ')
            for name in stylesnames:
                styles.add(name)
        if uidl.hasAttribute('disabled'):
            styles.add(ApplicationConnection.DISABLED_CLASSNAME)
        return list([None] * len(styles))

    def VFormLayoutTable(VFormLayout_this, *args, **kwargs):

        class VFormLayoutTable(FlexTable, ClickHandler):
            _COLUMN_CAPTION = 0
            _COLUMN_ERRORFLAG = 1
            _COLUMN_WIDGET = 2
            _componentToCaption = dict()
            _componentToError = dict()

            def __init__(self):
                DOM.setElementProperty(self.getElement(), 'cellPadding', '0')
                DOM.setElementProperty(self.getElement(), 'cellSpacing', '0')

            def updateFromUIDL(self, uidl, client):
                margins = VMarginInfo(uidl.getIntAttribute('margins'))
                margin = self.getElement()
                self.setStyleName(margin, VFormLayout_this._CLASSNAME + '-' + StyleConstants.MARGIN_TOP, margins.hasTop())
                self.setStyleName(margin, VFormLayout_this._CLASSNAME + '-' + StyleConstants.MARGIN_RIGHT, margins.hasRight())
                self.setStyleName(margin, VFormLayout_this._CLASSNAME + '-' + StyleConstants.MARGIN_BOTTOM, margins.hasBottom())
                self.setStyleName(margin, VFormLayout_this._CLASSNAME + '-' + StyleConstants.MARGIN_LEFT, margins.hasLeft())
                self.setStyleName(margin, VFormLayout_this._CLASSNAME + '-' + 'spacing', uidl.hasAttribute('spacing'))
                i = 0
                _0 = True
                it = uidl.getChildIterator()
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not it.hasNext():
                        break
                    self.prepareCell(i, 1)
                    childUidl = it.next()
                    p = client.getPaintable(childUidl)
                    caption = self._componentToCaption[p]
                    if caption is None:
                        caption = VFormLayout_this.Caption(p, client, VFormLayout_this.getStylesFromUIDL(childUidl))
                        caption.addClickHandler(self)
                        self._componentToCaption.put(p, caption)
                    error = self._componentToError[p]
                    if error is None:
                        error = VFormLayout_this.ErrorFlag()
                        self._componentToError.put(p, error)
                    self.prepareCell(i, self._COLUMN_WIDGET)
                    oldComponent = self.getWidget(i, self._COLUMN_WIDGET)
                    if oldComponent is None:
                        self.setWidget(i, self._COLUMN_WIDGET, p)
                    elif oldComponent != p:
                        client.unregisterPaintable(oldComponent)
                        self.setWidget(i, self._COLUMN_WIDGET, p)
                    self.getCellFormatter().setStyleName(i, self._COLUMN_WIDGET, VFormLayout_this._CLASSNAME + '-contentcell')
                    self.getCellFormatter().setStyleName(i, self._COLUMN_CAPTION, VFormLayout_this._CLASSNAME + '-captioncell')
                    self.setWidget(i, self._COLUMN_CAPTION, caption)
                    self.setContentWidth(i)
                    self.getCellFormatter().setStyleName(i, self._COLUMN_ERRORFLAG, VFormLayout_this._CLASSNAME + '-errorcell')
                    self.setWidget(i, self._COLUMN_ERRORFLAG, error)
                    p.updateFromUIDL(childUidl, client)
                    rowstyles = VFormLayout_this._CLASSNAME + '-row'
                    if i == 0:
                        rowstyles += ' ' + VFormLayout_this._CLASSNAME + '-firstrow'
                    if not it.hasNext():
                        rowstyles += ' ' + VFormLayout_this._CLASSNAME + '-lastrow'
                    self.getRowFormatter().setStyleName(i, rowstyles)
                while self.getRowCount() > i:
                    p = self.getWidget(i, self._COLUMN_WIDGET)
                    client.unregisterPaintable(p)
                    self._componentToCaption.remove(p)
                    self.removeRow(i)
                # Must update relative sized fields last when it is clear how much
                # space they are allowed to use

                for p in self._componentToCaption.keys():
                    client.handleComponentRelativeSize(p)

            def setContentWidths(self):
                _0 = True
                row = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        row += 1
                    if not (row < self.getRowCount()):
                        break
                    self.setContentWidth(row)

            def setContentWidth(self, row):
                width = ''
                if not VFormLayout_this.isDynamicWidth():
                    width = '100%'
                self.getCellFormatter().setWidth(row, self._COLUMN_WIDGET, width)

            def replaceChildComponent(self, oldComponent, newComponent):
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < self.getRowCount()):
                        break
                    candidate = self.getWidget(i, self._COLUMN_WIDGET)
                    if oldComponent == candidate:
                        oldCap = self._componentToCaption[oldComponent]
                        newCap = VFormLayout_this.Caption(newComponent, VFormLayout_this._client, None)
                        newCap.addClickHandler(self)
                        newCap.setStyleName(oldCap.getStyleName())
                        self._componentToCaption.put(newComponent, newCap)
                        error = self._componentToError[newComponent]
                        if error is None:
                            error = VFormLayout_this.ErrorFlag()
                            self._componentToError.put(newComponent, error)
                        self.setWidget(i, self._COLUMN_CAPTION, newCap)
                        self.setWidget(i, self._COLUMN_ERRORFLAG, error)
                        self.setWidget(i, self._COLUMN_WIDGET, newComponent)
                        break

            def hasChildComponent(self, component):
                return component in self._componentToCaption

            def updateCaption(self, component, uidl):
                c = self._componentToCaption[component]
                if c is not None:
                    c.updateCaption(uidl)
                e = self._componentToError[component]
                if e is not None:
                    e.updateFromUIDL(uidl, component)

            def getAllocatedWidth(self, child, availableWidth):
                # (non-Javadoc)
                # 
                # @see
                # com.google.gwt.event.dom.client.ClickHandler#onClick(com.google.gwt
                # .event.dom.client.ClickEvent)

                caption = self._componentToCaption[child]
                error = self._componentToError[child]
                width = availableWidth
                if caption is not None:
                    width -= DOM.getParent(caption.getElement()).getOffsetWidth()
                if error is not None:
                    width -= DOM.getParent(error.getElement()).getOffsetWidth()
                return width

            def onClick(self, event):
                caption = event.getSource()
                if caption.getOwner() is not None:
                    if isinstance(caption.getOwner(), Focusable):
                        caption.getOwner().focus()
                    elif (
                        isinstance(caption.getOwner(), self.com.google.gwt.user.client.ui.Focusable)
                    ):
                        caption.getOwner().setFocus(True)

        return VFormLayoutTable(*args, **kwargs)

    def updateFromUIDL(self, uidl, client):
        self._rendering = True
        self._client = client
        if client.updateComponent(self, uidl, True):
            self._rendering = False
            return
        self._table.updateFromUIDL(uidl, client)
        self._rendering = False

    def isDynamicWidth(self):
        return self._width == ''

    def hasChildComponent(self, component):
        return self._table.hasChildComponent(component)

    def replaceChildComponent(self, oldComponent, newComponent):
        self._table.replaceChildComponent(oldComponent, newComponent)

    def updateCaption(self, component, uidl):
        self._table.updateCaption(component, uidl)

    def Caption(VFormLayout_this, *args, **kwargs):

        class Caption(HTML):
            CLASSNAME = 'v-caption'
            _owner = None
            _requiredFieldIndicator = None
            _icon = None
            _captionText = None
            _client = None

            def __init__(self, component, client, styles):
                """@param component
                           optional owner of caption. If not set, getOwner will
                           return null
                @param client
                """
                super(Caption, self)()
                self._client = client
                self._owner = component
                style = self.CLASSNAME
                if styles is not None:
                    _0 = True
                    i = 0
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            i += 1
                        if not (i < len(styles)):
                            break
                        style += ' ' + self.CLASSNAME + '-' + styles[i]
                self.setStyleName(style)
                self.sinkEvents(VTooltip.TOOLTIP_EVENTS)

            def updateCaption(self, uidl):
                self.setVisible(not uidl.getBooleanAttribute('invisible'))
                self.setStyleName(self.getElement(), ApplicationConnection.DISABLED_CLASSNAME, uidl.hasAttribute('disabled'))
                isEmpty = True
                if uidl.hasAttribute('icon'):
                    if self._icon is None:
                        self._icon = Icon(self._client)
                        DOM.insertChild(self.getElement(), self._icon.getElement(), 0)
                    self._icon.setUri(uidl.getStringAttribute('icon'))
                    isEmpty = False
                elif self._icon is not None:
                    DOM.removeChild(self.getElement(), self._icon.getElement())
                    self._icon = None
                if uidl.hasAttribute('caption'):
                    if self._captionText is None:
                        self._captionText = DOM.createSpan()
                        DOM.insertChild(self.getElement(), self._captionText, 0 if self._icon is None else 1)
                    c = uidl.getStringAttribute('caption')
                    if c is None:
                        c = ''
                    else:
                        isEmpty = False
                    DOM.setInnerText(self._captionText, c)
                else:
                    # TODO should span also be removed
                    pass
                if uidl.hasAttribute('description'):
                    if self._captionText is not None:
                        self.addStyleDependentName('hasdescription')
                    else:
                        self.removeStyleDependentName('hasdescription')
                if uidl.getBooleanAttribute('required'):
                    if self._requiredFieldIndicator is None:
                        self._requiredFieldIndicator = DOM.createSpan()
                        DOM.setInnerText(self._requiredFieldIndicator, '*')
                        DOM.setElementProperty(self._requiredFieldIndicator, 'className', 'v-required-field-indicator')
                        DOM.appendChild(self.getElement(), self._requiredFieldIndicator)
                elif self._requiredFieldIndicator is not None:
                    DOM.removeChild(self.getElement(), self._requiredFieldIndicator)
                    self._requiredFieldIndicator = None
                # Workaround for IE weirdness, sometimes returns bad height in some
                # circumstances when Caption is empty. See #1444
                # IE7 bugs more often. I wonder what happens when IE8 arrives...
                if BrowserInfo.get().isIE():
                    if isEmpty:
                        VFormLayout_this.setHeight('0px')
                        DOM.setStyleAttribute(self.getElement(), 'overflow', 'hidden')
                    else:
                        VFormLayout_this.setHeight('')
                        DOM.setStyleAttribute(self.getElement(), 'overflow', '')

            def getOwner(self):
                """Returns Paintable for which this Caption belongs to.

                @return owner Widget
                """
                return self._owner

            def onBrowserEvent(self, event):
                super(Caption, self).onBrowserEvent(event)
                if self._client is not None:
                    self._client.handleTooltipEvent(event, self._owner)

        return Caption(*args, **kwargs)

    def ErrorFlag(VFormLayout_this, *args, **kwargs):

        class ErrorFlag(HTML):
            _CLASSNAME = VFormLayout.CLASSNAME + '-error-indicator'
            _errorIndicatorElement = None
            _owner = None

            def __init__(self):
                self.setStyleName(self._CLASSNAME)
                self.sinkEvents(VTooltip.TOOLTIP_EVENTS)

            def updateFromUIDL(self, uidl, component):
                self._owner = component
                if uidl.hasAttribute('error') and not uidl.getBooleanAttribute('hideErrors'):
                    if self._errorIndicatorElement is None:
                        self._errorIndicatorElement = DOM.createDiv()
                        DOM.setInnerHTML(self._errorIndicatorElement, '&nbsp;')
                        DOM.setElementProperty(self._errorIndicatorElement, 'className', 'v-errorindicator')
                        DOM.appendChild(self.getElement(), self._errorIndicatorElement)
                elif self._errorIndicatorElement is not None:
                    DOM.removeChild(self.getElement(), self._errorIndicatorElement)
                    self._errorIndicatorElement = None

            def onBrowserEvent(self, event):
                super(ErrorFlag, self).onBrowserEvent(event)
                if self._owner is not None:
                    VFormLayout_this._client.handleTooltipEvent(event, self._owner)

        return ErrorFlag(*args, **kwargs)

    def requestLayout(self, child):
        if (self._height == '') or (self._width == ''):
            # A dynamic size might change due to children changes
            return False
        return True

    def getAllocatedSpace(self, child):
        width = 0
        height = 0
        if not (self._width == ''):
            availableWidth = self.getOffsetWidth()
            width = self._table.getAllocatedWidth(child, availableWidth)
        return RenderSpace(width, height, False)

    def setHeight(self, height):
        if self._height == height:
            return
        self._height = height
        super(VFormLayout, self).setHeight(height)

    def setWidth(self, width):
        if self._width == width:
            return
        self._width = width
        super(VFormLayout, self).setWidth(width)
        if not self._rendering:
            self._table.setContentWidths()
            if self._height == '':
                # Width might affect height
                Util.updateRelativeChildrenAndSendSizeUpdateEvent(self._client, self)
