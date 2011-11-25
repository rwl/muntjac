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

from pyjamas import DOM
from pyjamas.ui import Event
from pyjamas.ui.HTML import HTML

from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.v_tooltip import VTooltip
from muntjac.terminal.gwt.client.paintable import Paintable
from muntjac.terminal.gwt.client.browser_info import BrowserInfo


class VLabel(HTML, Paintable):

    CLASSNAME = 'v-label'

    _CLASSNAME_UNDEFINED_WIDTH = 'v-label-undef-w'

    def __init__(self, text=None):

        self._client = None
        self._verticalPaddingBorder = 0
        self._horizontalPaddingBorder = 0

        super(VLabel, self).__init__(text)

        self.setStyleName(self.CLASSNAME)
        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)


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
        if (mode is None) or (mode == 'text'):
            self.setText(uidl.getChildString(0))
        elif mode == 'pre':
            preElement = DOM.createElement('pre')
            preElement.setInnerText(uidl.getChildUIDL(0).getChildString(0))
            # clear existing content
            self.setHTML('')
            # add preformatted text to dom
            self.getElement().appendChild(preElement)
        elif mode == 'uidl':
            self.setHTML(uidl.getChildrenAsXML())
        elif mode == 'xhtml':
            content = uidl.getChildUIDL(0).getChildUIDL(0)
            if content.getChildCount() > 0:
                self.setHTML(content.getChildString(0))
            else:
                self.setHTML('')
            sinkOnloads = True
        elif mode == 'xml':
            self.setHTML(uidl.getChildUIDL(0).getChildString(0))
        elif mode == 'raw':
            self.setHTML(uidl.getChildUIDL(0).getChildString(0))
            sinkOnloads = True
        else:
            self.setText('')
        if sinkOnloads:
            self.sinkOnloadsForContainedImgs()


    def sinkOnloadsForContainedImgs(self):
        images = self.getElement().getElementsByTagName('img')
        for img in images:
            DOM.sinkEvents(img, Event.ONLOAD)

    def setHeight(self, height):
        self._verticalPaddingBorder = \
            Util.setHeightExcludingPaddingAndBorder(self,
                    height, self._verticalPaddingBorder)


    def setWidth(self, width):
        self._horizontalPaddingBorder = \
            Util.setWidthExcludingPaddingAndBorder(self,
                    width, self._horizontalPaddingBorder)

        if (width is None) or (width == ''):
            self.setStyleName(self.getElement(),
                    self._CLASSNAME_UNDEFINED_WIDTH, True)
        else:
            self.setStyleName(self.getElement(),
                    self._CLASSNAME_UNDEFINED_WIDTH, False)


    def setText(self, text):
        if BrowserInfo.get().isIE() and BrowserInfo.get().getIEVersion() < 9:
            # #3983 - IE6-IE8 incorrectly replaces \n with <br> so we do the
            # escaping manually and set as HTML
            super(VLabel, self).setHTML(Util.escapeHTML(text))
        else:
            super(VLabel, self).setText(text)
