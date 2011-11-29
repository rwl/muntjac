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

from com.vaadin.terminal.gwt.client.Container import (Container,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.richtextarea.VRichTextArea import (VRichTextArea,)
from com.vaadin.terminal.gwt.client.VCaption import (VCaption,)
from com.vaadin.terminal.gwt.client.VCaptionWrapper import (VCaptionWrapper,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.NoSuchElementException import (NoSuchElementException,)
# from java.util.Set import (Set,)
Size = RenderInformation.Size


class VPopupView(HTML, Container, object):
    # class VPopupView
    CLASSNAME = 'v-popupview'
    # For server-client communication
    _uidlId = None
    _client = None
    # This variable helps to communicate popup visibility to the server
    _hostPopupVisible = None
    _popup = None
    _loading = Label()

    def __init__(self):
        """loading constructor"""
        super(VPopupView, self)()
        self._popup = self.CustomPopup()
        self.setStyleName(self.CLASSNAME)
        self._popup.setStyleName(self.CLASSNAME + '-popup')
        self._loading.setStyleName(self.CLASSNAME + '-loading')
        self.setHTML('')
        self._popup.setWidget(self._loading)
        # When we click to open the popup...

        class _0_(ClickHandler):

            def onClick(self, event):
                VPopupView_this.updateState(True)

        _0_ = _0_()
        self.addClickHandler(_0_)
        # ..and when we close it

        class _1_(CloseHandler):

            def onClose(self, event):
                VPopupView_this.updateState(False)

        _1_ = _1_()
        self._popup.addCloseHandler(_1_)
        self._popup.setAnimationEnabled(True)
        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)

    def updateFromUIDL(self, uidl, client):
        """@see com.vaadin.terminal.gwt.client.Paintable#updateFromUIDL(com.vaadin.terminal.gwt.client.UIDL,
             com.vaadin.terminal.gwt.client.ApplicationConnection)
        """
        # This call should be made first. Ensure correct implementation,
        # and don't let the containing layout manage caption.
        # updateFromUIDL
        if client.updateComponent(self, uidl, False):
            return
        # These are for future server connections
        self._client = client
        self._uidlId = uidl.getId()
        self._hostPopupVisible = uidl.getBooleanVariable('popupVisibility')
        self.setHTML(uidl.getStringAttribute('html'))
        if uidl.hasAttribute('hideOnMouseOut'):
            self._popup.setHideOnMouseOut(uidl.getBooleanAttribute('hideOnMouseOut'))
        # Render the popup if visible and show it.
        if self._hostPopupVisible:
            popupUIDL = uidl.getChildUIDL(0)
            # showPopupOnTop(popup, hostReference);
            self.preparePopup(self._popup)
            self._popup.updateFromUIDL(popupUIDL, client)
            if uidl.hasAttribute('style'):
                styles = uidl.getStringAttribute('style').split(' ')
                styleBuf = str()
                primaryName = self._popup.getStylePrimaryName()
                styleBuf.__add__(primaryName)
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(styles)):
                        break
                    styleBuf.__add__(' ')
                    styleBuf.__add__(primaryName)
                    styleBuf.__add__('-')
                    styleBuf.__add__(styles[i])
                self._popup.setStyleName(str(styleBuf))
            else:
                self._popup.setStyleName(self._popup.getStylePrimaryName())
            self.showPopup(self._popup)
            # The popup shouldn't be visible, try to hide it.
        else:
            self._popup.hide()

    def updateState(self, visible):
        """Update popup visibility to server

        @param visibility
        """
        # If we know the server connection
        # then update the current situation
        if self._uidlId is not None and self._client is not None and self.isAttached():
            self._client.updateVariable(self._uidlId, 'popupVisibility', visible, True)

    def preparePopup(self, popup):
        popup.setVisible(False)
        popup.show()

    def showPopup(self, popup):
        """Determines the correct position for a popup and displays the popup at
        that position.

        By default, the popup is shown centered relative to its host component,
        ensuring it is visible on the screen if possible.

        Can be overridden to customize the popup position.

        @param popup
        """
        windowTop = RootPanel.get().getAbsoluteTop()
        windowLeft = RootPanel.get().getAbsoluteLeft()
        windowRight = windowLeft + RootPanel.get().getOffsetWidth()
        windowBottom = windowTop + RootPanel.get().getOffsetHeight()
        offsetWidth = popup.getOffsetWidth()
        offsetHeight = popup.getOffsetHeight()
        hostHorizontalCenter = VPopupView_this.getAbsoluteLeft() + (VPopupView_this.getOffsetWidth() / 2)
        hostVerticalCenter = VPopupView_this.getAbsoluteTop() + (VPopupView_this.getOffsetHeight() / 2)
        left = hostHorizontalCenter - (offsetWidth / 2)
        top = hostVerticalCenter - (offsetHeight / 2)
        # Don't show the popup outside the screen.
        if left + offsetWidth > windowRight:
            left -= (left + offsetWidth) - windowRight
        if top + offsetHeight > windowBottom:
            top -= (top + offsetHeight) - windowBottom
        if left < 0:
            left = 0
        if top < 0:
            top = 0
        popup.setPopupPosition(left, top)
        popup.setVisible(True)

    def onDetach(self):
        """Make sure that we remove the popup when the main widget is removed.

        @see com.google.gwt.user.client.ui.Widget#onUnload()
        """
        self._popup.hide()
        super(VPopupView, self).onDetach()

    @classmethod
    def nativeBlur(cls, e):
        JS("""
        if(@{{e}} && @{{e}}.blur) {
            @{{e}}.blur();
        }
    """)
        pass

    def CustomPopup(VPopupView_this, *args, **kwargs):

        class CustomPopup(VOverlay):
            """This class is only protected to enable overriding showPopup, and is
            currently not intended to be extended or otherwise used directly. Its API
            (other than it being a VOverlay) is to be considered private and
            potentially subject to change.
            """
            _popupComponentPaintable = None
            _popupComponentWidget = None
            _captionWrapper = None
            _hasHadMouseOver = False
            _hideOnMouseOut = True
            _activeChildren = set()
            _hiding = False

            def __init__(self):
                # For some reason ONMOUSEOUT events are not always received, so we have
                # to use ONMOUSEMOVE that doesn't target the popup
                super(CustomPopup, self)(True, False, True)
                # autoHide, not modal, dropshadow

            def onEventPreview(self, event):
                target = DOM.eventGetTarget(event)
                eventTargetsPopup = DOM.isOrHasChild(self.getElement(), target)
                type = DOM.eventGetType(event)
                # Catch children that use keyboard, so we can unfocus them when
                # hiding
                if eventTargetsPopup and type == Event.ONKEYPRESS:
                    self._activeChildren.add(target)
                if eventTargetsPopup and type == Event.ONMOUSEMOVE:
                    self._hasHadMouseOver = True
                if not eventTargetsPopup and type == Event.ONMOUSEMOVE:
                    if self._hasHadMouseOver and self._hideOnMouseOut:
                        self.hide()
                        return True
                # Was the TAB key released outside of our popup?
                if (
                    not eventTargetsPopup and type == Event.ONKEYUP and event.getKeyCode() == KeyCodes.KEY_TAB
                ):
                    # Should we hide on focus out (mouse out)?
                    if self._hideOnMouseOut:
                        self.hide()
                        return True
                return super(CustomPopup, self).onEventPreview(event)

            def hide(self, autoClosed):
                self._hiding = True
                self.syncChildren()
                self.unregisterPaintables()
                if (
                    self._popupComponentWidget is not None and self._popupComponentWidget != VPopupView_this._loading
                ):
                    self.remove(self._popupComponentWidget)
                self._hasHadMouseOver = False
                super(CustomPopup, self).hide(autoClosed)

            def show(self):
                self._hiding = False
                super(CustomPopup, self).show()

            def syncChildren(self):
                """Try to sync all known active child widgets to server"""
                # Notify children with focus
                if isinstance(self._popupComponentWidget, Focusable):
                    self._popupComponentWidget.setFocus(False)
                else:
                    self.checkForRTE(self._popupComponentWidget)
                # Notify children that have used the keyboard
                for e in self._activeChildren:
                    try:
                        VPopupView_this.nativeBlur(e)
                    except Exception, ignored:
                        pass # astStmt: [Stmt([]), None]
                self._activeChildren.clear()

            def checkForRTE(self, popupComponentWidget2):
                if isinstance(popupComponentWidget2, VRichTextArea):
                    popupComponentWidget2.synchronizeContentToServer()
                elif isinstance(popupComponentWidget2, HasWidgets):
                    hw = popupComponentWidget2
                    iterator = hw
                    while iterator.hasNext():
                        self.checkForRTE(iterator.next())

            def remove(self, w):
                self._popupComponentPaintable = None
                self._popupComponentWidget = None
                self._captionWrapper = None
                return super(CustomPopup, self).remove(w)

            def updateFromUIDL(self, uidl, client):
                newPopupComponent = client.getPaintable(uidl.getChildUIDL(0))
                if newPopupComponent != self._popupComponentPaintable:
                    self.setWidget(newPopupComponent)
                    self._popupComponentWidget = newPopupComponent
                    self._popupComponentPaintable = newPopupComponent
                self._popupComponentPaintable.updateFromUIDL(uidl.getChildUIDL(0), client)

            def unregisterPaintables(self):
                if self._popupComponentPaintable is not None:
                    VPopupView_this._client.unregisterPaintable(self._popupComponentPaintable)

            def setHideOnMouseOut(self, hideOnMouseOut):
                # We need a hack make popup act as a child of VPopupView in Vaadin's
                # component tree, but work in default GWT manner when closing or
                # opening.
                # 
                # (non-Javadoc)
                # 
                # @see com.google.gwt.user.client.ui.Widget#getParent()

                self._hideOnMouseOut = hideOnMouseOut

            def getParent(self):
                if (not self.isAttached()) or self._hiding:
                    return super(CustomPopup, self).getParent()
                else:
                    return VPopupView_this

            def onDetach(self):
                super(CustomPopup, self).onDetach()
                self._hiding = False

            def getContainerElement(self):
                return super(CustomPopup, self).getContainerElement()

        return CustomPopup(*args, **kwargs)

    # class CustomPopup
    # Container methods

    def getAllocatedSpace(self, child):
        popupExtra = self.calculatePopupExtra()
        return RenderSpace(RootPanel.get().getOffsetWidth() - popupExtra.getWidth(), RootPanel.get().getOffsetHeight() - popupExtra.getHeight())

    def calculatePopupExtra(self):
        """Calculate extra space taken by the popup decorations

        @return
        """
        pe = self._popup.getElement()
        ipe = self._popup.getContainerElement()
        # border + padding
        width = Util.getRequiredWidth(pe) - Util.getRequiredWidth(ipe)
        height = Util.getRequiredHeight(pe) - Util.getRequiredHeight(ipe)
        return Size(width, height)

    def hasChildComponent(self, component):
        if self._popup.popupComponentWidget is not None:
            return self._popup.popupComponentWidget == component
        else:
            return False

    def replaceChildComponent(self, oldComponent, newComponent):
        self._popup.setWidget(newComponent)
        self._popup.popupComponentWidget = newComponent

    def requestLayout(self, child):
        self._popup.updateShadowSizeAndPosition()
        return True

    def updateCaption(self, component, uidl):
        if VCaption.isNeeded(uidl):
            if self._popup.captionWrapper is not None:
                self._popup.captionWrapper.updateCaption(uidl)
            else:
                self._popup.captionWrapper = VCaptionWrapper(component, self._client)
                self._popup.setWidget(self._popup.captionWrapper)
                self._popup.captionWrapper.updateCaption(uidl)
        elif self._popup.captionWrapper is not None:
            self._popup.setWidget(self._popup.popupComponentWidget)
        self._popup.popupComponentWidget = component
        self._popup.popupComponentPaintable = component

    def onBrowserEvent(self, event):
        super(VPopupView, self).onBrowserEvent(event)
        if self._client is not None:
            self._client.handleTooltipEvent(event, self)

    def iterator(self):

        class _2_(Iterator):
            _pos = 0

            def hasNext(self):
                # There is a child widget only if next() has not been called.
                return self._pos == 0

            def next(self):
                # Next can be called only once to return the popup.
                if self._pos != 0:
                    raise NoSuchElementException()
                self._pos += 1
                return VPopupView_this._popup

            def remove(self):
                raise self.UnsupportedOperationException()

        _2_ = _2_()
        return _2_
