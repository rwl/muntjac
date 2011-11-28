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

from __pyjamas__ import JS

from pyjamas import DOM

from pyjamas.ui import Event

from pyjamas.ui.HTML import HTML

from muntjac.terminal.gwt.client.v_console import VConsole
from muntjac.terminal.gwt.client.v_tooltip import VTooltip
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.application_connection import ApplicationConnection
from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.ui.icon import Icon


class VCaption(HTML):

    CLASSNAME = 'v-caption'

    ATTRIBUTE_ICON = 'icon'

    ATTRIBUTE_CAPTION = 'caption'

    ATTRIBUTE_DESCRIPTION = 'description'

    ATTRIBUTE_REQUIRED = 'required'

    ATTRIBUTE_ERROR = 'error'

    ATTRIBUTE_HIDEERRORS = 'hideErrors'

    _CLASSNAME_CLEAR = CLASSNAME + '-clearelem'

    def __init__(self, component, client):
        """@param component:
                   optional owner of caption. If not set, getOwner will
                   return null
        @param client:
        """
        self._owner = component

        self._errorIndicatorElement = None

        self._requiredFieldIndicator = None

        self._icon = None

        self._captionText = None

        self._clearElement = None

        self._client = client

        self._placedAfterComponent = False

        self._iconOnloadHandled = False

        self._maxWidth = -1

        super(VCaption, self).__init__()

        if client is not None and self._owner is not None:
            self.setOwnerPid(self.getElement(), client.getPid(self._owner))

        self.setStyleName(self.CLASSNAME)
        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)


    def updateCaption(self, uidl):
        """Updates the caption from UIDL.

        @return: true if the position where the caption should be placed has
                 changed
        """
        self.setVisible(not uidl.getBooleanAttribute('invisible'))

        wasPlacedAfterComponent = self._placedAfterComponent

        # Caption is placed after component unless there is some part which
        # moves it above.
        self._placedAfterComponent = True

        style = self.CLASSNAME
        if uidl.hasAttribute('style'):
            styles = uidl.getStringAttribute('style').split(' ')
            for i in range(len(styles)):
                style += ' ' + self.CLASSNAME + '-' + styles[i]

        if uidl.hasAttribute('disabled'):
            style += ' ' + ApplicationConnection.DISABLED_CLASSNAME

        self.setStyleName(style)

        hasIcon = uidl.hasAttribute(self.ATTRIBUTE_ICON)
        hasText = uidl.hasAttribute(self.ATTRIBUTE_CAPTION)
        hasDescription = uidl.hasAttribute(self.ATTRIBUTE_DESCRIPTION)
        showRequired = uidl.getBooleanAttribute(self.ATTRIBUTE_REQUIRED)
        showError = (uidl.hasAttribute(self.ATTRIBUTE_ERROR)
                and not uidl.getBooleanAttribute(self.ATTRIBUTE_HIDEERRORS))

        if hasIcon:
            if self._icon is None:
                self._icon = Icon(self._client)
                self._icon.setWidth('0')
                self._icon.setHeight('0')

                DOM.insertChild(self.getElement(), self._icon.getElement(),
                        self.getInsertPosition(self.ATTRIBUTE_ICON))

            # Icon forces the caption to be above the component
            self._placedAfterComponent = False

            self._iconOnloadHandled = False
            self._icon.setUri(uidl.getStringAttribute(self.ATTRIBUTE_ICON))

        elif self._icon is not None:
            # Remove existing
            DOM.removeChild(self.getElement(), self._icon.getElement())
            self._icon = None

        if hasText:
            # A caption text should be shown if the attribute is set
            # If the caption is null the ATTRIBUTE_CAPTION should not be set to
            # avoid ending up here.
            if self._captionText is None:
                self._captionText = DOM.createDiv()
                self._captionText.setClassName('v-captiontext')
                DOM.insertChild(self.getElement(), self._captionText,
                        self.getInsertPosition(self.ATTRIBUTE_CAPTION))

            # Update caption text
            c = uidl.getStringAttribute(self.ATTRIBUTE_CAPTION)

            # A text forces the caption to be above the component.
            self._placedAfterComponent = False
            if (c is None) or (c.trim() == ''):
                # Not sure if c even can be null. Should not.
                # This is required to ensure that the caption uses space in all
                # browsers when it is set to the empty string. If there is an
                # icon, error indicator or required indicator they will ensure
                # that space is reserved.
                if not hasIcon and not showRequired and not showError:
                    self._captionText.setInnerHTML('&nbsp;')
            else:
                DOM.setInnerText(self._captionText, c)
        elif self._captionText is not None:
            # Remove existing
            DOM.removeChild(self.getElement(), self._captionText)
            self._captionText = None

        if hasDescription:
            if self._captionText is not None:
                self.addStyleDependentName('hasdescription')
            else:
                self.removeStyleDependentName('hasdescription')

        if showRequired:
            if self._requiredFieldIndicator is None:
                self._requiredFieldIndicator = DOM.createDiv()
                self._requiredFieldIndicator.setClassName('v-required-field-indicator')
                DOM.setInnerText(self._requiredFieldIndicator, '*')
                DOM.insertChild(self.getElement(), self._requiredFieldIndicator, self.getInsertPosition(self.ATTRIBUTE_REQUIRED))
        elif self._requiredFieldIndicator is not None:
            # Remove existing
            DOM.removeChild(self.getElement(), self._requiredFieldIndicator)
            self._requiredFieldIndicator = None

        if showError:
            if self._errorIndicatorElement is None:
                self._errorIndicatorElement = DOM.createDiv()
                DOM.setInnerHTML(self._errorIndicatorElement, '&nbsp;')
                DOM.setElemAttribute(self._errorIndicatorElement, 'className',
                        'v-errorindicator')
                DOM.insertChild(self.getElement(), self._errorIndicatorElement,
                        self.getInsertPosition(self.ATTRIBUTE_ERROR))
        elif self._errorIndicatorElement is not None:
            # Remove existing
            self.getElement().removeChild(self._errorIndicatorElement)
            self._errorIndicatorElement = None

        if self._clearElement is None:
            self._clearElement = DOM.createDiv()
            self._clearElement.setClassName(self._CLASSNAME_CLEAR)
            self.getElement().appendChild(self._clearElement)

        return wasPlacedAfterComponent != self._placedAfterComponent


    def getInsertPosition(self, element):
        pos = 0
        if element == self.ATTRIBUTE_ICON:
            return pos

        if self._icon is not None:
            pos += 1

        if element == self.ATTRIBUTE_CAPTION:
            return pos

        if self._captionText is not None:
            pos += 1

        if element == self.ATTRIBUTE_REQUIRED:
            return pos

        if self._requiredFieldIndicator is not None:
            pos += 1

        # if element == self.ATTRIBUTE_ERROR:
        return pos


    def onBrowserEvent(self, event):
        super(VCaption, self).onBrowserEvent(event)
        target = DOM.eventGetTarget(event)
        if (self._client is not None and self._owner is not None
                and target != self.getElement()):
            self._client.handleTooltipEvent(event, self._owner)

        if (DOM.eventGetType(event) == Event.ONLOAD
                and self._icon.getElement() == target
                and not self._iconOnloadHandled):
            self._icon.setWidth('')
            self._icon.setHeight('')
            # IE6 pngFix causes two onload events to be fired and we want to
            # react only to the first one
            self._iconOnloadHandled = True

            # if max width defined, recalculate
            if self._maxWidth != -1:
                self.setMaxWidth(self._maxWidth)
            else:
                width = self.getElement().getStyle().getProperty('width')
                if width is not None and not (width == ''):
                    self.setWidth(self.getRequiredWidth() + 'px')

            # The size of the icon might affect the size of the component so we
            # must report the size change to the parent TODO consider moving
            # the responsibility of reacting to ONLOAD from VCaption to layouts
            if self._owner is not None:
                Util.notifyParentOfSizeChange(self._owner, True)
            else:
                VConsole.log('Warning: Icon load event was not propagated because VCaption owner is unknown.')


    @classmethod
    def isNeeded(cls, uidl):
        if uidl.getStringAttribute(cls.ATTRIBUTE_CAPTION) is not None:
            return True

        if uidl.hasAttribute(cls.ATTRIBUTE_ERROR):
            return True

        if uidl.hasAttribute(cls.ATTRIBUTE_ICON):
            return True

        if uidl.hasAttribute(cls.ATTRIBUTE_REQUIRED):
            return True

        return False


    def getOwner(self):
        """Returns Paintable for which this Caption belongs to.

        @return owner Widget
        """
        return self._owner


    def shouldBePlacedAfterComponent(self):
        return self._placedAfterComponent


    def getRenderedWidth(self):
        width = 0
        if self._icon is not None:
            width += Util.getRequiredWidth(self._icon.getElement())

        if self._captionText is not None:
            width += Util.getRequiredWidth(self._captionText)

        if self._requiredFieldIndicator is not None:
            width += Util.getRequiredWidth(self._requiredFieldIndicator)

        if self._errorIndicatorElement is not None:
            width += Util.getRequiredWidth(self._errorIndicatorElement)

        return width


    def getRequiredWidth(self):
        width = 0
        if self._icon is not None:
            width += Util.getRequiredWidth(self._icon.getElement())

        if self._captionText is not None:
            textWidth = self._captionText.getScrollWidth()
            if BrowserInfo.get().isFirefox():
                # In Firefox3 the caption might require more space than the
                # scrollWidth returns as scrollWidth is rounded down.

                requiredWidth = Util.getRequiredWidth(self._captionText)
                if requiredWidth > textWidth:
                    textWidth = requiredWidth
            width += textWidth

        if self._requiredFieldIndicator is not None:
            width += Util.getRequiredWidth(self._requiredFieldIndicator)

        if self._errorIndicatorElement is not None:
            width += Util.getRequiredWidth(self._errorIndicatorElement)

        return width


    def getHeight(self):
        height = 0
        if self._icon is not None:
            h = Util.getRequiredHeight(self._icon.getElement())
            if h > height:
                height = h

        if self._captionText is not None:
            h = Util.getRequiredHeight(self._captionText)
            if h > height:
                height = h

        if self._requiredFieldIndicator is not None:
            h = Util.getRequiredHeight(self._requiredFieldIndicator)
            if h > height:
                height = h

        if self._errorIndicatorElement is not None:
            h = Util.getRequiredHeight(self._errorIndicatorElement)
            if h > height:
                height = h

        return height


    def setAlignment(self, alignment):
        DOM.setStyleAttribute(self.getElement(), 'textAlign', alignment)


    def setMaxWidth(self, maxWidth):
        self._maxWidth = maxWidth
        DOM.setStyleAttribute(self.getElement(), 'width', maxWidth + 'px')

        if self._icon is not None:
            DOM.setStyleAttribute(self._icon.getElement(), 'width', '')

        if self._captionText is not None:
            DOM.setStyleAttribute(self._captionText, 'width', '')

        requiredWidth = self.getRequiredWidth()

        # ApplicationConnection.getConsole().log( "Caption maxWidth: " +
        # maxWidth + ", requiredWidth: " + requiredWidth);
        if requiredWidth > maxWidth:
            # Needs to truncate and clip
            availableWidth = maxWidth
            # DOM.setStyleAttribute(getElement(), "width", maxWidth + "px");
            if self._requiredFieldIndicator is not None:
                availableWidth -= Util.getRequiredWidth(self._requiredFieldIndicator)

            if self._errorIndicatorElement is not None:
                availableWidth -= Util.getRequiredWidth(self._errorIndicatorElement)

            if availableWidth < 0:
                availableWidth = 0

            if self._icon is not None:
                iconRequiredWidth = Util.getRequiredWidth(self._icon.getElement())
                if availableWidth > iconRequiredWidth:
                    availableWidth -= iconRequiredWidth
                else:
                    DOM.setStyleAttribute(self._icon.getElement(), 'width', availableWidth + 'px')
                    availableWidth = 0

            if self._captionText is not None:
                captionWidth = Util.getRequiredWidth(self._captionText)
                if availableWidth > captionWidth:
                    availableWidth -= captionWidth
                else:
                    DOM.setStyleAttribute(self._captionText, 'width', availableWidth + 'px')
                    availableWidth = 0


    def getTextElement(self):
        return self._captionText


    @classmethod
    def getCaptionOwnerPid(cls, e):
        return cls.getOwnerPid(e)


    @classmethod
    def setOwnerPid(cls, el, pid):
        JS("""
            @{{el}}.vOwnerPid = @{{pid}};
        """)
        pass


    @classmethod
    def getOwnerPid(cls, el):
        JS("""
            return @{{el}}.vOwnerPid;
        """)
        pass
