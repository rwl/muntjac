# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.MenuItem import (MenuItem,)
from com.vaadin.terminal.gwt.client.ui.VLazyExecutor import (VLazyExecutor,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.SubPartAware import (SubPartAware,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
from com.vaadin.terminal.gwt.client.ui.MenuBar import (MenuBar,)
from com.vaadin.terminal.gwt.client.Focusable import (Focusable,)
# from com.google.gwt.user.client.ui.MenuBar import (MenuBar,)
# from com.google.gwt.user.client.ui.MenuItem import (MenuItem,)


class VContextMenu(VOverlay, SubPartAware):
    _actionOwner = None
    _menu = CMenuBar()
    _left = None
    _top = None
    _delayedImageLoadExecutioner = 
    class _1_(ScheduledCommand):

        def execute(self):
            VContextMenu_this.imagesLoaded()

    _1_ = _1_()
    VLazyExecutor(100, _1_)

    def __init__(self):
        """This method should be used only by Client object as only one per client
        should exists. Request an instance via client.getContextMenu();

        @param cli
                   to be set as an owner of menu
        """
        super(VContextMenu, self)(True, False, True)
        self.setWidget(self._menu)
        self.setStyleName('v-contextmenu')

    def imagesLoaded(self):
        if self.isVisible():
            self.show()

    def setActionOwner(self, ao):
        """Sets the element from which to build menu

        @param ao
        """
        self._actionOwner = ao

    def showAt(self, *args):
        """Shows context menu at given location IF it contain at least one item.

        @param left
        @param top
        """
        _0 = args
        _1 = len(args)
        if _1 == 2:
            left, top = _0
            actions = self._actionOwner.getActions()
            if (actions is None) or (len(actions) == 0):
                # Only show if there really are actions
                return
            self._left = left
            self._top = top
            self._menu.clearItems()
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(actions)):
                    break
                a = actions[i]
                self._menu.addItem(MenuItem(a.getHTML(), True, a))
            # Attach onload listeners to all images
            Util.sinkOnloadForImages(self._menu.getElement())
            VContextMenu_this = self

            class _2_(self.PositionCallback):

                def setPosition(self, offsetWidth, offsetHeight):
                    # mac FF gets bad width due GWT popups overflow hacks,
                    # re-determine width
                    offsetWidth = VContextMenu_this._menu.getOffsetWidth()
                    left = VContextMenu_this._left
                    top = VContextMenu_this._top
                    if offsetWidth + left > Window.getClientWidth():
                        left = left - offsetWidth
                        if left < 0:
                            left = 0
                    if offsetHeight + top > Window.getClientHeight():
                        top = top - offsetHeight
                        if top < 0:
                            top = 0
                    self.setPopupPosition(left, top)
                    # Move keyboard focus to menu, deferring the focus setting so
                    # the focus is certainly moved to the menu in all browser after
                    # the positioning has been done.

                    class _2_(Command):

                        def execute(self):
                            # Focus the menu.
                            VContextMenu_this._menu.setFocus(True)
                            # Unselect previously selected items
                            VContextMenu_this._menu.selectItem(None)

                    _2_ = _2_()
                    Scheduler.get().scheduleDeferred(_2_)

            _2_ = _2_()
            self.setPopupPositionAndShow(_2_)
        elif _1 == 3:
            ao, left, top = _0
            self.setActionOwner(ao)
            self.showAt(left, top)
        else:
            raise ARGERROR(2, 3)

    def CMenuBar(VContextMenu_this, *args, **kwargs):

        class CMenuBar(MenuBar, HasFocusHandlers, HasBlurHandlers, HasKeyDownHandlers, HasKeyPressHandlers, Focusable, LoadHandler):
            """Extend standard Gwt MenuBar to set proper settings and to override
            onPopupClosed method so that PopupPanel gets closed.
            """

            def __init__(self):
                super(CMenuBar, self)(True)
                self.addDomHandler(self, LoadEvent.getType())

            def onPopupClosed(self, sender, autoClosed):
                # public void onBrowserEvent(Event event) { // Remove current selection
                # when mouse leaves if (DOM.eventGetType(event) == Event.ONMOUSEOUT) {
                # Element to = DOM.eventGetToElement(event); if
                # (!DOM.isOrHasChild(getElement(), to)) { DOM.setElementProperty(
                # super.getSelectedItem().getElement(), "className",
                # super.getSelectedItem().getStylePrimaryName()); } }
                # 
                # super.onBrowserEvent(event); }

                super(CMenuBar, self).onPopupClosed(sender, autoClosed)
                # make focusable, as we don't need access key magic we don't need
                # to
                # use FocusImpl.createFocusable
                self.getElement().setTabIndex(0)
                self.hide()

            def getItem(self, index):
                return super(CMenuBar, self).getItems().get(index)

            def addFocusHandler(self, handler):
                return self.addDomHandler(handler, FocusEvent.getType())

            def addBlurHandler(self, handler):
                return self.addDomHandler(handler, BlurEvent.getType())

            def addKeyDownHandler(self, handler):
                return self.addDomHandler(handler, KeyDownEvent.getType())

            def addKeyPressHandler(self, handler):
                return self.addDomHandler(handler, KeyPressEvent.getType())

            def setFocus(self, focus):
                if focus:
                    FocusImpl.getFocusImplForPanel().focus(self.getElement())
                else:
                    FocusImpl.getFocusImplForPanel().blur(self.getElement())

            def focus(self):
                self.setFocus(True)

            def onLoad(self, event):
                # Handle icon onload events to ensure shadow is resized correctly
                if BrowserInfo.get().isIE6():
                    # Ensure PNG transparency works in IE6
                    Util.doIE6PngFix(Element.as_(event.getNativeEvent().getEventTarget()))
                VContextMenu_this._delayedImageLoadExecutioner.trigger()

        return CMenuBar(*args, **kwargs)

    def getSubPartElement(self, subPart):
        index = int(subPart[6:])
        # ApplicationConnection.getConsole().log(
        # "Searching element for selection index " + index);
        item = self._menu.getItem(index)
        # ApplicationConnection.getConsole().log("Item: " + item);
        # Item refers to the td, which is the parent of the clickable element
        return item.getElement().getFirstChildElement()

    def getSubPartName(self, subElement):
        if self.getElement().isOrHasChild(subElement):
            e = subElement
            while e is not None and not (e.getTagName().toLowerCase() == 'tr'):
                e = e.getParentElement()
                # ApplicationConnection.getConsole().log("Found row");
            parentElement = e.getParentElement()
            rows = parentElement.getRows()
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < rows.getLength()):
                    break
                if rows.getItem(i) == e:
                    # ApplicationConnection.getConsole().log(
                    # "Found index for row" + 1);
                    return 'option' + i
            return None
        else:
            return None

    def ensureHidden(self, actionOwner):
        """Hides context menu if it is currently shown by given action owner.

        @param actionOwner
        """
        if self._actionOwner == actionOwner:
            self.hide()
