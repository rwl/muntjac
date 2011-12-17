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

from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.ui.menu_item import MenuItem
from muntjac.terminal.gwt.client.ui.v_lazy_executor import VLazyExecutor
from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.ui.sub_part_aware import SubPartAware
from muntjac.terminal.gwt.client.ui.v_overlay import VOverlay
from muntjac.terminal.gwt.client.ui.menu_bar import MenuBar
from muntjac.terminal.gwt.client.focusable import IFocusable


class VContextMenu(VOverlay, SubPartAware):


    def __init__(self):
        """This method should be used only by Client object as only one per
        client should exists. Request an instance via client.getContextMenu();

        @param cli:
                   to be set as an owner of menu
        """
        self._actionOwner = None
        self._menu = CMenuBar()
        self._left = None
        self._top = None

        class _1_(ScheduledCommand):

            def execute(self):
                VContextMenu_this.imagesLoaded()

        _1_ = _1_()
        self._delayedImageLoadExecutioner = VLazyExecutor(100, _1_)

        super(VContextMenu, self)(True, False, True)

        self.setWidget(self._menu)
        self.setStyleName('v-contextmenu')


    def imagesLoaded(self):
        if self.isVisible():
            self.show()


    def setActionOwner(self, ao):
        """Sets the element from which to build menu
        """
        self._actionOwner = ao


    def showAt(self, *args):
        """Shows context menu at given location IF it contain at least one
        item.
        """
        nargs = len(args)
        if nargs == 2:
            left, top = args
            actions = self._actionOwner.getActions()
            if (actions is None) or (len(actions) == 0):
                # Only show if there really are actions
                return
            self._left = left
            self._top = top
            self._menu.clearItems()
            for i in range(len(actions)):
                a = actions[i]
                self._menu.addItem(MenuItem(a.getHTML(), True, a))

            # Attach onload listeners to all images
            Util.sinkOnloadForImages(self._menu.getElement())
#            VContextMenu_this = self

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
        elif nargs == 3:
            ao, left, top = args
            self.setActionOwner(ao)
            self.showAt(left, top)
        else:
            raise ValueError


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

            for i in range(rows.getLength()):
                if rows.getItem(i) == e:
                    # ApplicationConnection.getConsole().log(
                    # "Found index for row" + 1);
                    return 'option' + i

            return None
        else:
            return None


    def ensureHidden(self, actionOwner):
        """Hides context menu if it is currently shown by given action owner.
        """
        if self._actionOwner == actionOwner:
            self.hide()


class CMenuBar(MenuBar, IFocusable):
#    HasFocusHandlers, HasBlurHandlers, HasKeyDownHandlers, HasKeyPressHandlers, LoadHandler):
    """Extend standard Gwt MenuBar to set proper settings and to override
    onPopupClosed method so that PopupPanel gets closed.
    """

    def __init__(self):
        super(CMenuBar, self).__init__(True)
        self.addDomHandler(self, LoadEvent.getType())


    def onPopupClosed(self, sender, autoClosed):
        super(CMenuBar, self).onPopupClosed(sender, autoClosed)

        # make focusable, as we don't need access key magic we don't need
        # to use FocusImpl.createFocusable
        self.getElement().setTabIndex(0)
        self.hide()


    # public void onBrowserEvent(Event event) { // Remove current selection
    # when mouse leaves if (DOM.eventGetType(event) == Event.ONMOUSEOUT) {
    # Element to = DOM.eventGetToElement(event); if
    # (!DOM.isOrHasChild(getElement(), to)) { DOM.setElementProperty(
    # super.getSelectedItem().getElement(), "className",
    # super.getSelectedItem().getStylePrimaryName()); } }
    #
    # super.onBrowserEvent(event); }


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
