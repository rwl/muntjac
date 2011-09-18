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

from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.Container import (Container,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.RenderInformation import (RenderInformation,)
from com.vaadin.terminal.gwt.client.VErrorMessage import (VErrorMessage,)
from com.vaadin.terminal.gwt.client.ui.Icon import (Icon,)
from com.vaadin.terminal.gwt.client.ui.ShortcutActionHandler import (ShortcutActionHandler,)
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
        self.setElement(self.DOM.createDiv())
        self.DOM.appendChild(self.getElement(), self._fieldSet)
        self.setStyleName(self.CLASSNAME)
        self.DOM.appendChild(self._fieldSet, self._legend)
        self.DOM.appendChild(self._legend, self._caption)
        self.DOM.setElementProperty(self._errorIndicatorElement, 'className', 'v-errorindicator')
        self.DOM.setStyleAttribute(self._errorIndicatorElement, 'display', 'none')
        self.DOM.setInnerText(self._errorIndicatorElement, ' ')
        # needed for IE
        self.DOM.setElementProperty(self._desc, 'className', 'v-form-description')
        self.DOM.appendChild(self._fieldSet, self._desc)
        self.DOM.appendChild(self._fieldSet, self._fieldContainer)
        self._errorMessage.setVisible(False)
        self._errorMessage.setStyleName(self.CLASSNAME + '-errormessage')
        self.DOM.appendChild(self._fieldSet, self._errorMessage.getElement())
        self.DOM.appendChild(self._fieldSet, self._footerContainer)

    def updateFromUIDL(self, uidl, client):
        self._rendering = True
        self._client = client
        self.id = uidl.getId()
        if client.updateComponent(self, uidl, False):
            self._rendering = False
            return
        legendEmpty = True
        if uidl.hasAttribute('caption'):
            self.DOM.setInnerText(self._caption, uidl.getStringAttribute('caption'))
            legendEmpty = False
        else:
            self.DOM.setInnerText(self._caption, '')
        if uidl.hasAttribute('icon'):
            if self._icon is None:
                self._icon = Icon(client)
                self.DOM.insertChild(self._legend, self._icon.getElement(), 0)
            self._icon.setUri(uidl.getStringAttribute('icon'))
            legendEmpty = False
        elif self._icon is not None:
            self.DOM.removeChild(self._legend, self._icon.getElement())
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
            self.DOM.setInnerHTML(self._desc, uidl.getStringAttribute('description'))
        else:
            self.DOM.setInnerHTML(self._desc, '')
        self.updateSize()
        # TODO Check if this is needed
        client.runDescendentsLayout(self)
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
            self.updateSize()
        elif self._footer is not None:
            self.remove(self._footer)
            client.unregisterPaintable(self._footer)
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
        # We may have actions attached
        if uidl.getChildCount() > 1:
            childUidl = uidl.getChildByTagName('actions')
            if childUidl is not None:
                if self._shortcutHandler is None:
                    self._shortcutHandler = ShortcutActionHandler(self.id, client)
                    self._keyDownRegistration = self.addDomHandler(self, self.KeyDownEvent.getType())
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


#    /**
#     * @return pixels consumed by decoration, captions, descrioptiosn etc.. In
#     *         other words space, not used by the actual layout in form.
#     */
#    private int getSpaceConsumedVertically() {
#        int offsetHeight2 = fieldSet.getOffsetHeight();
#        int offsetHeight3 = fieldContainer.getOffsetHeight();
#        int borderPadding = offsetHeight2 - offsetHeight3;
#        return borderPadding;
#    }
#
#    @Override
#    public void setWidth(String width) {
#        if (borderPaddingHorizontal < 0) {
#            // measure excess size lazyly after stylename setting, but before
#            // setting width
#            int ow = getOffsetWidth();
#            int dow = desc.getOffsetWidth();
#            borderPaddingHorizontal = ow - dow;
#        }
#        if (Util.equals(this.width, width)) {
#            return;
#        }
#
#        this.width = width;
#        super.setWidth(width);
#
#        updateSize();
#
#        if (!rendering && height.equals("")) {
#            // Width might affect height
#            Util.updateRelativeChildrenAndSendSizeUpdateEvent(client, this);
#        }
#    }
#
#    public void onKeyDown(KeyDownEvent event) {
#        shortcutHandler.handleKeyboardEvent(Event.as(event.getNativeEvent()));
#    }
