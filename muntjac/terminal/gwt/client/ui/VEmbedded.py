# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.ui.ClickEventHandler import (ClickEventHandler,)
from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.UIDL import (UIDL,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from com.google.gwt.dom.client.ObjectElement import (ObjectElement,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.Map import (Map,)


class VEmbedded(HTML, Paintable):
    CLICK_EVENT_IDENTIFIER = 'click'
    _CLASSNAME = 'v-embedded'
    _height = None
    _width = None
    _browserElement = None
    _type = None
    _client = None

    class clickEventHandler(ClickEventHandler):

        def registerHandler(self, handler, type):
            return self.addDomHandler(handler, type)

    def __init__(self):
        self.setStyleName(self._CLASSNAME)

    def updateFromUIDL(self, uidl, client):
        if client.updateComponent(self, uidl, True):
            return
        self._client = client
        clearBrowserElement = True
        self.clickEventHandler.handleEventHandlerRegistration(client)
        if uidl.hasAttribute('type'):
            self._type = uidl.getStringAttribute('type')
            if self._type == 'image':
                self.addStyleName(self._CLASSNAME + '-image')
                el = None
                created = False
                nodes = self.getElement().getChildNodes()
                if nodes is not None and nodes.getLength() == 1:
                    n = nodes.getItem(0)
                    if n.getNodeType() == Node.ELEMENT_NODE:
                        e = n
                        if e.getTagName() == 'IMG':
                            el = e
                if el is None:
                    self.setHTML('')
                    el = DOM.createImg()
                    created = True
                    client.addPngFix(el)
                    DOM.sinkEvents(el, Event.ONLOAD)
                # Set attributes
                style = el.getStyle()
                w = uidl.getStringAttribute('width')
                if w is not None:
                    style.setProperty('width', w)
                else:
                    style.setProperty('width', '')
                h = uidl.getStringAttribute('height')
                if h is not None:
                    style.setProperty('height', h)
                else:
                    style.setProperty('height', '')
                DOM.setElementProperty(el, 'src', self.getSrc(uidl, client))
                if created:
                    # insert in dom late
                    self.getElement().appendChild(el)
                # Sink tooltip events so tooltip is displayed when hovering the
                # image.

                self.sinkEvents(VTooltip.TOOLTIP_EVENTS)
            elif self._type == 'browser':
                self.addStyleName(self._CLASSNAME + '-browser')
                if self._browserElement is None:
                    self.setHTML('<iframe width=\"100%\" height=\"100%\" frameborder=\"0\"' + ' allowTransparency=\"true\" src=\"\"' + ' name=\"' + uidl.getId() + '\"></iframe>')
                    self._browserElement = DOM.getFirstChild(self.getElement())
                DOM.setElementAttribute(self._browserElement, 'src', self.getSrc(uidl, client))
                clearBrowserElement = False
            else:
                VConsole.log('Unknown Embedded type \'' + self._type + '\'')
        elif uidl.hasAttribute('mimetype'):
            mime = uidl.getStringAttribute('mimetype')
            if mime == 'application/x-shockwave-flash':
                # Handle embedding of Flash
                self.addStyleName(self._CLASSNAME + '-flash')
                self.setHTML(self.createFlashEmbed(uidl))
            elif mime == 'image/svg+xml':
                self.addStyleName(self._CLASSNAME + '-svg')
                parameters = self.getParameters(uidl)
                if parameters['data'] is None:
                    data = self.getSrc(uidl, client)
                else:
                    data = 'data:image/svg+xml,' + parameters['data']
                self.setHTML('')
                obj = Document.get().createObjectElement()
                obj.setType(mime)
                obj.setData(data)
                if self._width is not None:
                    obj.getStyle().setProperty('width', '100%')
                if self._height is not None:
                    obj.getStyle().setProperty('height', '100%')
                if uidl.hasAttribute('classid'):
                    obj.setAttribute('classid', uidl.getStringAttribute('classid'))
                if uidl.hasAttribute('codebase'):
                    obj.setAttribute('codebase', uidl.getStringAttribute('codebase'))
                if uidl.hasAttribute('codetype'):
                    obj.setAttribute('codetype', uidl.getStringAttribute('codetype'))
                if uidl.hasAttribute('archive'):
                    obj.setAttribute('archive', uidl.getStringAttribute('archive'))
                if uidl.hasAttribute('standby'):
                    obj.setAttribute('standby', uidl.getStringAttribute('standby'))
                self.getElement().appendChild(obj)
            else:
                VConsole.log('Unknown Embedded mimetype \'' + mime + '\'')
        else:
            VConsole.log('Unknown Embedded; no type or mimetype attribute')
        if clearBrowserElement:
            self._browserElement = None

    def createFlashEmbed(self, uidl):
        """Creates the Object and Embed tags for the Flash plugin so it works
        cross-browser

        @param uidl
                   The UIDL
        @return Tags concatenated into a string
        """
        # To ensure cross-browser compatibility we are using the twice-cooked
        # method to embed flash i.e. we add a OBJECT tag for IE ActiveX and
        # inside it a EMBED for all other browsers.

        html = self.StringBuilder()
        # Start the object tag
        html.append('<object ')
        # Add classid required for ActiveX to recognize the flash. This is a
        # predefined value which ActiveX recognizes and must be the given
        # value. More info can be found on
        # http://kb2.adobe.com/cps/415/tn_4150.html. Allow user to override
        # this by setting his own classid.

        if uidl.hasAttribute('classid'):
            html.append('classid=\"' + Util.escapeAttribute(uidl.getStringAttribute('classid')) + '\" ')
        else:
            html.append('classid=\"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000\" ')
        # Add codebase required for ActiveX and must be exactly this according
        # to http://kb2.adobe.com/cps/415/tn_4150.html to work with the above
        # given classid. Again, see more info on
        # http://kb2.adobe.com/cps/415/tn_4150.html. Limiting Flash version to
        # 6.0.0.0 and above. Allow user to override this by setting his own
        # codebase

        if uidl.hasAttribute('codebase'):
            html.append('codebase=\"' + Util.escapeAttribute(uidl.getStringAttribute('codebase')) + '\" ')
        else:
            html.append('codebase=\"http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,0,0\" ')
        # Add width and height
        html.append('width=\"' + Util.escapeAttribute(self._width) + '\" ')
        html.append('height=\"' + Util.escapeAttribute(self._height) + '\" ')
        html.append('type=\"application/x-shockwave-flash\" ')
        # Codetype
        if uidl.hasAttribute('codetype'):
            html.append('codetype=\"' + Util.escapeAttribute(uidl.getStringAttribute('codetype')) + '\" ')
        # Standby
        if uidl.hasAttribute('standby'):
            html.append('standby=\"' + Util.escapeAttribute(uidl.getStringAttribute('standby')) + '\" ')
        # Archive
        if uidl.hasAttribute('archive'):
            html.append('archive=\"' + Util.escapeAttribute(uidl.getStringAttribute('archive')) + '\" ')
        # End object tag
        html.append('>')
        # Ensure we have an movie parameter
        parameters = self.getParameters(uidl)
        if parameters['movie'] is None:
            parameters.put('movie', self.getSrc(uidl, self._client))
        # Add parameters to OBJECT
        for name in parameters.keys():
            html.append('<param ')
            html.append('name=\"' + Util.escapeAttribute(name) + '\" ')
            html.append('value=\"' + Util.escapeAttribute(parameters[name]) + '\" ')
            html.append('/>')
        # Build inner EMBED tag
        html.append('<embed ')
        html.append('src=\"' + Util.escapeAttribute(self.getSrc(uidl, self._client)) + '\" ')
        html.append('width=\"' + Util.escapeAttribute(self._width) + '\" ')
        html.append('height=\"' + Util.escapeAttribute(self._height) + '\" ')
        html.append('type=\"application/x-shockwave-flash\" ')
        # Add the parameters to the Embed
        for name in parameters.keys():
            html.append(Util.escapeAttribute(name))
            html.append('=')
            html.append('\"' + Util.escapeAttribute(parameters[name]) + '\"')
        # End embed tag
        html.append('></embed>')
        # End object tag
        html.append('</object>')
        return str(html)

    @classmethod
    def getParameters(cls, uidl):
        """Returns a map (name -> value) of all parameters in the UIDL.

        @param uidl
        @return
        """
        parameters = dict()
        childIterator = uidl.getChildIterator()
        while childIterator.hasNext():
            child = childIterator.next()
            if isinstance(child, UIDL):
                childUIDL = child
                if childUIDL.getTag() == 'embeddedparam':
                    name = childUIDL.getStringAttribute('name')
                    value = childUIDL.getStringAttribute('value')
                    parameters.put(name, value)
        return parameters

    def getSrc(self, uidl, client):
        """Helper to return translated src-attribute from embedded's UIDL

        @param uidl
        @param client
        @return
        """
        url = client.translateVaadinUri(uidl.getStringAttribute('src'))
        if url is None:
            return ''
        return url

    def setWidth(self, width):
        self._width = width
        if self.isDynamicHeight():
            oldHeight = self.getOffsetHeight()
            super(VEmbedded, self).setWidth(width)
            newHeight = self.getOffsetHeight()
            # Must notify parent if the height changes as a result of a width
            # change

            if oldHeight != newHeight:
                Util.notifyParentOfSizeChange(self, False)
        else:
            super(VEmbedded, self).setWidth(width)

    def isDynamicWidth(self):
        return (self._width is None) or (self._width == '')

    def isDynamicHeight(self):
        return (self._height is None) or (self._height == '')

    def setHeight(self, height):
        self._height = height
        super(VEmbedded, self).setHeight(height)

    def onDetach(self):
        if BrowserInfo.get().isIE():
            # Force browser to fire unload event when component is detached
            # from the view (IE doesn't do this automatically)
            if self._browserElement is not None:
                DOM.setElementAttribute(self._browserElement, 'src', 'javascript:false')
        super(VEmbedded, self).onDetach()

    def onBrowserEvent(self, event):
        super(VEmbedded, self).onBrowserEvent(event)
        if DOM.eventGetType(event) == Event.ONLOAD:
            if 'image' == self._type:
                self.updateElementDynamicSizeFromImage()
            Util.notifyParentOfSizeChange(self, True)
        self._client.handleTooltipEvent(event, self)

    def updateElementDynamicSizeFromImage(self):
        """Updates the size of the embedded component's element if size is
        undefined. Without this embeddeds containing images will remain the wrong
        size in certain cases (e.g. #6304).
        """
        if self.isDynamicWidth():
            self.getElement().getStyle().setWidth(self.getElement().getFirstChildElement().getOffsetWidth(), Unit.PX)
        if self.isDynamicHeight():
            self.getElement().getStyle().setHeight(self.getElement().getFirstChildElement().getOffsetHeight(), Unit.PX)
