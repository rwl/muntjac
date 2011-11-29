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
from com.vaadin.terminal.gwt.client.ui.ShortcutActionHandler import (ShortcutActionHandler,)
from com.vaadin.terminal.gwt.client.Container import (Container,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.RenderInformation import (RenderInformation,)
from com.vaadin.terminal.gwt.client.VErrorMessage import (VErrorMessage,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.Icon import (Icon,)
# from java.util.Set import (Set,)


class VForm(ComplexPanel, Container, KeyDownHandler):
    id = None
    _height = ''
    _width = ''
    CLASSNAME = 'v-form'
    _lo = None
    _legend = DOM.createLegend()
    _caption = DOM.createSpan()
    _errorIndicatorElement = DOM.createDiv()
    _desc = DOM.createDiv()
    _icon = None
    _errorMessage = VErrorMessage()
    _fieldContainer = DOM.createDiv()
    _footerContainer = DOM.createDiv()
    _fieldSet = DOM.createFieldSet()
    _footer = None
    _client = None
    _renderInformation = RenderInformation()
    _borderPaddingHorizontal = -1
    _rendering = False
    _shortcutHandler = None
    _keyDownRegistration = None

    def __init__(self):
        self.setElement(DOM.createDiv())
        self.getElement().appendChild(self._fieldSet)
        self.setStyleName(self.CLASSNAME)
        self._fieldSet.appendChild(self._legend)
        self._legend.appendChild(self._caption)
        self._errorIndicatorElement.setClassName('v-errorindicator')
        self._errorIndicatorElement.getStyle().setDisplay(Display.NONE)
        self._errorIndicatorElement.setInnerText(' ')
        # needed for IE
        self._desc.setClassName('v-form-description')
        self._fieldSet.appendChild(self._desc)
        # Adding description for initial padding
        # measurements, removed later if no
        # description is set
        self._fieldSet.appendChild(self._fieldContainer)
        self._errorMessage.setVisible(False)
        self._errorMessage.setStyleName(self.CLASSNAME + '-errormessage')
        self._fieldSet.appendChild(self._errorMessage.getElement())
        self._fieldSet.appendChild(self._footerContainer)

    def updateFromUIDL(self, uidl, client):
        self._rendering = True
        self._client = client
        self.id = uidl.getId()
        if client.updateComponent(self, uidl, False):
            self._rendering = False
            return
        legendEmpty = True
        if uidl.hasAttribute('caption'):
            self._caption.setInnerText(uidl.getStringAttribute('caption'))
            legendEmpty = False
        else:
            self._caption.setInnerText('')
        if uidl.hasAttribute('icon'):
            if self._icon is None:
                self._icon = Icon(client)
                self._legend.insertFirst(self._icon.getElement())
            self._icon.setUri(uidl.getStringAttribute('icon'))
            legendEmpty = False
        elif self._icon is not None:
            self._legend.removeChild(self._icon.getElement())
        if legendEmpty:
            self.addStyleDependentName('nocaption')
        else:
            self.removeStyleDependentName('nocaption')
        if uidl.hasAttribute('error'):
            errorUidl = uidl.getErrors()
            self._errorMessage.updateFromUIDL(errorUidl)
            self._errorMessage.setVisible(True)
        else:
            self._errorMessage.setVisible(False)
        if uidl.hasAttribute('description'):
            self._desc.setInnerHTML(uidl.getStringAttribute('description'))
            if self._desc.getParentElement() is None:
                self._fieldSet.insertAfter(self._desc, self._legend)
        else:
            self._desc.setInnerHTML('')
            if self._desc.getParentElement() is not None:
                self._fieldSet.removeChild(self._desc)
        self.updateSize()
        # first render footer so it will be easier to handle relative height of
        # main layout
        if (
            uidl.getChildCount() > 1 and not (uidl.getChildUIDL(1).getTag() == 'actions')
        ):
            # render footer
            newFooter = client.getPaintable(uidl.getChildUIDL(1))
            if self._footer is None:
                self.add(newFooter, self._footerContainer)
                self._footer = newFooter
            elif newFooter != self._footer:
                self.remove(self._footer)
                client.unregisterPaintable(self._footer)
                self.add(newFooter, self._footerContainer)
            self._footer = newFooter
            self._footer.updateFromUIDL(uidl.getChildUIDL(1), client)
            # needed for the main layout to know the space it has available
            self.updateSize()
        elif self._footer is not None:
            self.remove(self._footer)
            client.unregisterPaintable(self._footer)
            # needed for the main layout to know the space it has available
            self.updateSize()
        layoutUidl = uidl.getChildUIDL(0)
        newLo = client.getPaintable(layoutUidl)
        if self._lo is None:
            self._lo = newLo
            self.add(self._lo, self._fieldContainer)
        elif self._lo != newLo:
            client.unregisterPaintable(self._lo)
            self.remove(self._lo)
            self._lo = newLo
            self.add(self._lo, self._fieldContainer)
        self._lo.updateFromUIDL(layoutUidl, client)
        # also recalculates size of the footer if undefined size form - see
        # #3710
        self.updateSize()
        client.runDescendentsLayout(self)
        # We may have actions attached
        if uidl.getChildCount() > 1:
            childUidl = uidl.getChildByTagName('actions')
            if childUidl is not None:
                if self._shortcutHandler is None:
                    self._shortcutHandler = ShortcutActionHandler(self.id, client)
                    self._keyDownRegistration = self.addDomHandler(self, KeyDownEvent.getType())
                self._shortcutHandler.updateActionMap(childUidl)
        elif self._shortcutHandler is not None:
            self._keyDownRegistration.removeHandler()
            self._shortcutHandler = None
            self._keyDownRegistration = None
        self._rendering = False

    def updateSize(self):
        self._renderInformation.updateSize(self.getElement())
        self._renderInformation.setContentAreaHeight(self._renderInformation.getRenderedSize().getHeight() - self.getSpaceConsumedVertically())
        if BrowserInfo.get().isIE6():
            self.getElement().getStyle().setProperty('overflow', 'hidden')
        self._renderInformation.setContentAreaWidth(self._renderInformation.getRenderedSize().getWidth() - self._borderPaddingHorizontal)

    def getAllocatedSpace(self, child):
        if child == self._lo:
            return self._renderInformation.getContentAreaSize()
        elif child == self._footer:
            return RenderSpace(self._renderInformation.getContentAreaSize().getWidth(), 0)
        else:
            VConsole.error('Invalid child requested RenderSpace information')
            return None

    def hasChildComponent(self, component):
        return component is not None and (component == self._lo) or (component == self._footer)

    def replaceChildComponent(self, oldComponent, newComponent):
        if not self.hasChildComponent(oldComponent):
            raise self.IllegalArgumentException('Old component is not inside this Container')
        self.remove(oldComponent)
        if oldComponent == self._lo:
            self._lo = newComponent
            self.add(self._lo, self._fieldContainer)
        else:
            self._footer = newComponent
            self.add(self._footer, self._footerContainer)

    def requestLayout(self, child):
        if (
            self._height is not None and not ('' == self._height) and self._width is not None and not ('' == self._width)
        ):
            # If the height and width has been specified the child components
            # cannot make the size of the layout change

            return True
        if self._renderInformation.updateSize(self.getElement()):
            return False
        else:
            return True

    def updateCaption(self, component, uidl):
        # NOP form don't render caption for neither field layout nor footer
        # layout
        pass

    def setHeight(self, height):
        if self._height == height:
            return
        self._height = height
        super(VForm, self).setHeight(height)
        self.updateSize()

    def getSpaceConsumedVertically(self):
        """@return pixels consumed by decoration, captions, descrioptiosn etc.. In
                other words space, not used by the actual layout in form.
        """
        offsetHeight2 = self._fieldSet.getOffsetHeight()
        offsetHeight3 = self._fieldContainer.getOffsetHeight()
        borderPadding = offsetHeight2 - offsetHeight3
        return borderPadding

    def setWidth(self, width):
        if self._borderPaddingHorizontal < 0:
            # measure excess size lazily after stylename setting, but before
            # setting width
            ow = self.getOffsetWidth()
            dow = self._desc.getOffsetWidth()
            self._borderPaddingHorizontal = ow - dow
        # if (Util.equals(this.width, width)) {
        # return;
        # }
        self._width = width
        super(VForm, self).setWidth(width)
        self.updateSize()
        if not self._rendering and self._height == '':
            # Width might affect height
            Util.updateRelativeChildrenAndSendSizeUpdateEvent(self._client, self)

    def onKeyDown(self, event):
        self._shortcutHandler.handleKeyboardEvent(Event.as_(event.getNativeEvent()))
