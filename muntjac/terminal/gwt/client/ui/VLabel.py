# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from com.google.gwt.dom.client.PreElement import (PreElement,)


class VLabel(HTML, Paintable):
    CLASSNAME = 'v-label'
    _CLASSNAME_UNDEFINED_WIDTH = 'v-label-undef-w'
    _client = None
    _verticalPaddingBorder = 0
    _horizontalPaddingBorder = 0

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            super(VLabel, self)()
            self.setStyleName(self.CLASSNAME)
            self.sinkEvents(VTooltip.TOOLTIP_EVENTS)
        elif _1 == 1:
            text, = _0
            super(VLabel, self)(text)
            self.setStyleName(self.CLASSNAME)
            self.sinkEvents(VTooltip.TOOLTIP_EVENTS)
        else:
            raise ARGERROR(0, 1)

    def onBrowserEvent(self, event):
        super(VLabel, self).onBrowserEvent(event)
        if event.getTypeInt() == Event.ONLOAD:
            Util.notifyParentOfSizeChange(self, True)
            event.cancelBubble(True)
            return
        if self._client is not None:
            self._client.handleTooltipEvent(event, self)

    def updateFromUIDL(self, uidl, client):
        if client.updateComponent(self, uidl, True):
            return
        self._client = client
        sinkOnloads = False
        mode = uidl.getStringAttribute('mode')
        if (mode is None) or ('text' == mode):
            self.setText(uidl.getChildString(0))
        elif 'pre' == mode:
            preElement = Document.get().createPreElement()
            preElement.setInnerText(uidl.getChildUIDL(0).getChildString(0))
            # clear existing content
            self.setHTML('')
            # add preformatted text to dom
            self.getElement().appendChild(preElement)
        elif 'uidl' == mode:
            self.setHTML(uidl.getChildrenAsXML())
        elif 'xhtml' == mode:
            content = uidl.getChildUIDL(0).getChildUIDL(0)
            if content.getChildCount() > 0:
                self.setHTML(content.getChildString(0))
            else:
                self.setHTML('')
            sinkOnloads = True
        elif 'xml' == mode:
            self.setHTML(uidl.getChildUIDL(0).getChildString(0))
        elif 'raw' == mode:
            self.setHTML(uidl.getChildUIDL(0).getChildString(0))
            sinkOnloads = True
        else:
            self.setText('')
        if sinkOnloads:
            self.sinkOnloadsForContainedImgs()

    def sinkOnloadsForContainedImgs(self):
        images = self.getElement().getElementsByTagName('img')
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < images.getLength()):
                break
            img = images.getItem(i)
            DOM.sinkEvents(img, Event.ONLOAD)

    def setHeight(self, height):
        self._verticalPaddingBorder = Util.setHeightExcludingPaddingAndBorder(self, height, self._verticalPaddingBorder)

    def setWidth(self, width):
        self._horizontalPaddingBorder = Util.setWidthExcludingPaddingAndBorder(self, width, self._horizontalPaddingBorder)
        if (width is None) or (width == ''):
            self.setStyleName(self.getElement(), self._CLASSNAME_UNDEFINED_WIDTH, True)
        else:
            self.setStyleName(self.getElement(), self._CLASSNAME_UNDEFINED_WIDTH, False)

    def setText(self, text):
        if BrowserInfo.get().isIE() and BrowserInfo.get().getIEVersion() < 9:
            # #3983 - IE6-IE8 incorrectly replaces \n with <br> so we do the
            # escaping manually and set as HTML
            super(VLabel, self).setHTML(Util.escapeHTML(text))
        else:
            super(VLabel, self).setText(text)
