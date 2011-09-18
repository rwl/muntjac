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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.EventId import (EventId,)
from com.vaadin.terminal.gwt.client.Focusable import (Focusable,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.VLazyExecutor import (VLazyExecutor,)
from com.vaadin.terminal.gwt.client.ui.MenuItem import (MenuItem,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.Field import (Field,)
from com.vaadin.terminal.gwt.client.ui.SubPartAware import (SubPartAware,)
from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.ui.MenuBar import (MenuBar,)
# from com.google.gwt.core.client.Scheduler import (Scheduler,)
# from com.google.gwt.core.client.Scheduler.ScheduledCommand import (ScheduledCommand,)
# from com.google.gwt.dom.client.Style.Overflow import (Overflow,)
# from com.google.gwt.event.dom.client.BlurEvent import (BlurEvent,)
# from com.google.gwt.event.dom.client.BlurHandler import (BlurHandler,)
# from com.google.gwt.event.dom.client.ClickEvent import (ClickEvent,)
# from com.google.gwt.event.dom.client.ClickHandler import (ClickHandler,)
# from com.google.gwt.event.dom.client.FocusEvent import (FocusEvent,)
# from com.google.gwt.event.dom.client.FocusHandler import (FocusHandler,)
# from com.google.gwt.event.dom.client.KeyCodes import (KeyCodes,)
# from com.google.gwt.event.dom.client.KeyDownEvent import (KeyDownEvent,)
# from com.google.gwt.event.dom.client.KeyDownHandler import (KeyDownHandler,)
# from com.google.gwt.event.dom.client.KeyUpEvent import (KeyUpEvent,)
# from com.google.gwt.event.dom.client.KeyUpHandler import (KeyUpHandler,)
# from com.google.gwt.event.dom.client.LoadEvent import (LoadEvent,)
# from com.google.gwt.event.dom.client.LoadHandler import (LoadHandler,)
# from com.google.gwt.event.logical.shared.CloseEvent import (CloseEvent,)
# from com.google.gwt.event.logical.shared.CloseHandler import (CloseHandler,)
# from com.google.gwt.user.client.Command import (Command,)
# from com.google.gwt.user.client.DOM import (DOM,)
# from com.google.gwt.user.client.Element import (Element,)
# from com.google.gwt.user.client.Event import (Event,)
# from com.google.gwt.user.client.Window import (Window,)
# from com.google.gwt.user.client.ui.Composite import (Composite,)
# from com.google.gwt.user.client.ui.FlowPanel import (FlowPanel,)
# from com.google.gwt.user.client.ui.HTML import (HTML,)
# from com.google.gwt.user.client.ui.Image import (Image,)
# from com.google.gwt.user.client.ui.PopupPanel import (PopupPanel,)
# from com.google.gwt.user.client.ui.PopupPanel.PositionCallback import (PositionCallback,)
# from com.google.gwt.user.client.ui.SuggestOracle.Suggestion import (Suggestion,)
# from com.google.gwt.user.client.ui.TextBox import (TextBox,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)
# from java.util.Date import (Date,)
# from java.util.Iterator import (Iterator,)
# from java.util.List import (List,)


class VFilterSelect(Composite, Paintable, Field, KeyDownHandler, KeyUpHandler, ClickHandler, FocusHandler, BlurHandler, Focusable):
    """Client side implementation of the Select component.

    TODO needs major refactoring (to be extensible etc)
    """

    class FilterSelectSuggestion(Suggestion, Command):
        """Represents a suggestion in the suggestion popup box"""
        _key = None
        _caption = None
        _iconUri = None

        def __init__(self, uidl):
            """Constructor

            @param uidl
                       The UIDL recieved from the server
            """
            self._key = uidl.getStringAttribute('key')
            self._caption = uidl.getStringAttribute('caption')
            if uidl.hasAttribute('icon'):
                self._iconUri = self.client.translateVaadinUri(uidl.getStringAttribute('icon'))

        def getDisplayString(self):
            """Gets the visible row in the popup as a HTML string. The string
            contains an image tag with the rows icon (if an icon has been
            specified) and the caption of the item
            """
            sb = str()
            if self._iconUri is not None:
                sb.__add__('<img src=\"')
                sb.__add__(self._iconUri)
                sb.__add__('\" alt=\"\" class=\"v-icon\" />')
            sb.__add__('<span>' + Util.escapeHTML(self._caption) + '</span>')
            return str(sb)

        def getReplacementString(self):
            """Get a string that represents this item. This is used in the text box."""
            return self._caption

        def getOptionKey(self):
            """Get the option key which represents the item on the server side.

            @return The key of the item
            """
            return int(self._key)

        def getIconUri(self):
            """Get the URI of the icon. Used when constructing the displayed option.

            @return
            """
            return self._iconUri

        def execute(self):
            """Executes a selection of this item."""
            self.onSuggestionSelected(self)

    class SuggestionPopup(VOverlay, PositionCallback, CloseHandler):
        """Represents the popup box with the selection options. Wraps a suggestion
        menu.
        """
        _Z_INDEX = '30000'
        _menu = None
        _up = DOM.createDiv()
        _down = DOM.createDiv()
        _status = DOM.createDiv()
        _isPagingEnabled = True
        _lastAutoClosed = None
        _popupOuterPadding = -1
        _topPosition = None

        def __init__(self):
            """Default constructor"""
            super(SuggestionPopup, self)(True, False, True)
            self._menu = self.SuggestionMenu()
            self.setWidget(self._menu)
            self.setStyleName(self.CLASSNAME + '-suggestpopup')
            DOM.setStyleAttribute(self.getElement(), 'zIndex', self._Z_INDEX)
            root = self.getContainerElement()
            DOM.setInnerHTML(self._up, '<span>Prev</span>')
            DOM.sinkEvents(self._up, Event.ONCLICK)
            DOM.setInnerHTML(self._down, '<span>Next</span>')
            DOM.sinkEvents(self._down, Event.ONCLICK)
            DOM.insertChild(root, self._up, 0)
            DOM.appendChild(root, self._down)
            DOM.appendChild(root, self._status)
            DOM.setElementProperty(self._status, 'className', self.CLASSNAME + '-status')
            DOM.sinkEvents(root, Event.ONMOUSEDOWN)
            self.addCloseHandler(self)

        def showSuggestions(self, currentSuggestions, currentPage, totalSuggestions):
            """Shows the popup where the user can see the filtered options

            @param currentSuggestions
                       The filtered suggestions
            @param currentPage
                       The current page number
            @param totalSuggestions
                       The total amount of suggestions
            """
            # Add TT anchor point
            DOM.setElementProperty(self.getElement(), 'id', 'VAADIN_COMBOBOX_OPTIONLIST')
            self._menu.setSuggestions(currentSuggestions)
            x = _VFilterSelect_this.getAbsoluteLeft()
            self._topPosition = self.tb.getAbsoluteTop()
            self._topPosition += self.tb.getOffsetHeight()
            self.setPopupPosition(x, self._topPosition)
            nullOffset = 1 if self.nullSelectionAllowed and '' == self.lastFilter else 0
            firstPage = currentPage == 0
            first = ((currentPage * self.pageLength) + 1) - (0 if firstPage else nullOffset)
            last = (first + len(currentSuggestions)) - 1 - (nullOffset if firstPage and '' == self.lastFilter else 0)
            matches = totalSuggestions - nullOffset
            if last > 0:
                # nullsel not counted, as requested by user
                DOM.setInnerText(self._status, (0 if matches == 0 else first) + '-' + last + '/' + matches)
            else:
                DOM.setInnerText(self._status, '')
            # We don't need to show arrows or statusbar if there is only one
            # page
            if (totalSuggestions <= self.pageLength) or (self.pageLength == 0):
                self.setPagingEnabled(False)
            else:
                self.setPagingEnabled(True)
            self.setPrevButtonActive(first > 1)
            self.setNextButtonActive(last < matches)
            # clear previously fixed width
            self._menu.setWidth('')
            DOM.setStyleAttribute(DOM.getFirstChild(self._menu.getElement()), 'width', '')
            self.setPopupPositionAndShow(self)

        def setNextButtonActive(self, active):
            """Should the next page button be visible to the user?

            @param active
            """
            if active:
                DOM.sinkEvents(self._down, Event.ONCLICK)
                DOM.setElementProperty(self._down, 'className', self.CLASSNAME + '-nextpage')
            else:
                DOM.sinkEvents(self._down, 0)
                DOM.setElementProperty(self._down, 'className', self.CLASSNAME + '-nextpage-off')

        def setPrevButtonActive(self, active):
            """Should the previous page button be visible to the user

            @param active
            """
            if active:
                DOM.sinkEvents(self._up, Event.ONCLICK)
                DOM.setElementProperty(self._up, 'className', self.CLASSNAME + '-prevpage')
            else:
                DOM.sinkEvents(self._up, 0)
                DOM.setElementProperty(self._up, 'className', self.CLASSNAME + '-prevpage-off')

        def selectNextItem(self):
            """Selects the next item in the filtered selections"""
            cur = self._menu.getSelectedItem()
            index = 1 + self._menu.getItems().index(cur)
            if len(self._menu.getItems()) > index:
                newSelectedItem = self._menu.getItems().get(index)
                self._menu.selectItem(newSelectedItem)
                self.tb.setText(newSelectedItem.getText())
                self.tb.setSelectionRange(len(self.lastFilter), len(newSelectedItem.getText()) - len(self.lastFilter))
            elif self.hasNextPage():
                self.lastIndex = index - 1
                # save for paging
                self.filterOptions(self.currentPage + 1, self.lastFilter)

        def selectPrevItem(self):
            """Selects the previous item in the filtered selections"""
            # (non-Javadoc)
            #
            # @see
            # com.google.gwt.user.client.ui.Widget#onBrowserEvent(com.google.gwt
            # .user.client.Event)

            cur = self._menu.getSelectedItem()
            index = -1 + self._menu.getItems().index(cur)
            if index > -1:
                newSelectedItem = self._menu.getItems().get(index)
                self._menu.selectItem(newSelectedItem)
                self.tb.setText(newSelectedItem.getText())
                self.tb.setSelectionRange(len(self.lastFilter), len(newSelectedItem.getText()) - len(self.lastFilter))
            elif index == -1:
                if self.currentPage > 0:
                    self.lastIndex = index + 1
                    # save for paging
                    self.filterOptions(self.currentPage - 1, self.lastFilter)
            else:
                newSelectedItem = self._menu.getItems().get(len(self._menu.getItems()) - 1)
                self._menu.selectItem(newSelectedItem)
                self.tb.setText(newSelectedItem.getText())
                self.tb.setSelectionRange(len(self.lastFilter), len(newSelectedItem.getText()) - len(self.lastFilter))

        def onBrowserEvent(self, event):
            if event.getTypeInt() == Event.ONCLICK:
                target = DOM.eventGetTarget(event)
                if (target == self._up) or (target == DOM.getChild(self._up, 0)):
                    self.filterOptions(self.currentPage - 1, self.lastFilter)
                elif (target == self._down) or (target == DOM.getChild(self._down, 0)):
                    self.filterOptions(self.currentPage + 1, self.lastFilter)
            # Prevent the keyboard focus from leaving the textfield by
            # preventing the default behaviour of the browser. Fixes #4285.

            self.handleMouseDownEvent(event)

        def setPagingEnabled(self, paging):
            """Should paging be enabled. If paging is enabled then only a certain
            amount of items are visible at a time and a scrollbar or buttons are
            visible to change page. If paging is turned of then all options are
            rendered into the popup menu.

            @param paging
                       Should the paging be turned on?
            """
            # (non-Javadoc)
            #
            # @see
            # com.google.gwt.user.client.ui.PopupPanel$PositionCallback#setPosition
            # (int, int)

            if self._isPagingEnabled == paging:
                return
            if paging:
                DOM.setStyleAttribute(self._down, 'display', '')
                DOM.setStyleAttribute(self._up, 'display', '')
                DOM.setStyleAttribute(self._status, 'display', '')
            else:
                DOM.setStyleAttribute(self._down, 'display', 'none')
                DOM.setStyleAttribute(self._up, 'display', 'none')
                DOM.setStyleAttribute(self._status, 'display', 'none')
            self._isPagingEnabled = paging

        def setPosition(self, offsetWidth, offsetHeight):
            top = -1
            left = -1
            # reset menu size and retrieve its "natural" size
            self._menu.setHeight('')
            if self.currentPage > 0:
                # fix height to avoid height change when getting to last page
                self._menu.fixHeightTo(self.pageLength)
            offsetHeight = self.getOffsetHeight()
            desiredWidth = self.getMainWidth()
            naturalMenuWidth = DOM.getElementPropertyInt(DOM.getFirstChild(self._menu.getElement()), 'offsetWidth')
            if self._popupOuterPadding == -1:
                self._popupOuterPadding = Util.measureHorizontalPaddingAndBorder(self.getElement(), 2)
            if naturalMenuWidth < desiredWidth:
                self._menu.setWidth((desiredWidth - self._popupOuterPadding) + 'px')
                DOM.setStyleAttribute(DOM.getFirstChild(self._menu.getElement()), 'width', '100%')
                naturalMenuWidth = desiredWidth
            if BrowserInfo.get().isIE():
                # IE requires us to specify the width for the container
                # element. Otherwise it will be 100% wide

                rootWidth = naturalMenuWidth - self._popupOuterPadding
                DOM.setStyleAttribute(self.getContainerElement(), 'width', rootWidth + 'px')
            if (
                offsetHeight + self.getPopupTop() > Window.getClientHeight() + Window.getScrollTop()
            ):
                # popup on top of input instead
                top = self.getPopupTop() - offsetHeight - _VFilterSelect_this.getOffsetHeight()
                if top < 0:
                    top = 0
            else:
                top = self.getPopupTop()
                # Take popup top margin into account. getPopupTop() returns the
                # top value including the margin but the value we give must not
                # include the margin.

                topMargin = top - self._topPosition
                top -= topMargin
            # fetch real width (mac FF bugs here due GWT popups overflow:auto )
            offsetWidth = DOM.getElementPropertyInt(DOM.getFirstChild(self._menu.getElement()), 'offsetWidth')
            if (
                offsetWidth + self.getPopupLeft() > Window.getClientWidth() + Window.getScrollLeft()
            ):
                left = (_VFilterSelect_this.getAbsoluteLeft() + _VFilterSelect_this.getOffsetWidth() + Window.getScrollLeft()) - offsetWidth
                if left < 0:
                    left = 0
            else:
                left = self.getPopupLeft()
            self.setPopupPosition(left, top)

        def isJustClosed(self):
            """Was the popup just closed?

            @return true if popup was just closed
            """
            # (non-Javadoc)
            #
            # @see
            # com.google.gwt.event.logical.shared.CloseHandler#onClose(com.google
            # .gwt.event.logical.shared.CloseEvent)

            now = Date().getTime()
            return self._lastAutoClosed > 0 and now - self._lastAutoClosed < 200

        def onClose(self, event):
            if event.isAutoClosed():
                self._lastAutoClosed = Date().getTime()

        def updateStyleNames(self, uidl):
            """Updates style names in suggestion popup to help theme building."""
            if uidl.hasAttribute('style'):
                self.setStyleName(self.CLASSNAME + '-suggestpopup')
                styles = uidl.getStringAttribute('style').split(' ')
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(styles)):
                        break
                    self.addStyleDependentName(styles[i])

    class SuggestionMenu(MenuBar, SubPartAware, LoadHandler):
        """The menu where the suggestions are rendered"""
        _delayedImageLoadExecutioner =
        class _0_(ScheduledCommand):

            def execute(self):
                if self.suggestionPopup.isVisible() and self.suggestionPopup.isAttached():
                    self.setWidth('')
                    DOM.setStyleAttribute(DOM.getFirstChild(self.getElement()), 'width', '')
                    self.suggestionPopup.setPopupPositionAndShow(self.suggestionPopup)

        _0_ = _0_()
        VLazyExecutor(100, _0_)

        def __init__(self):
            """Default constructor"""
            super(SuggestionMenu, self)(True)
            self.setStyleName(self.CLASSNAME + '-suggestmenu')
            self.addDomHandler(self, LoadEvent.getType())

        def fixHeightTo(self, pagelenth):
            """Fixes menus height to use same space as full page would use. Needed
            to avoid height changes when quickly "scrolling" to last page
            """
            if len(self.currentSuggestions) > 0:
                pixels = (pagelenth * (self.getOffsetHeight() - 2)) / len(self.currentSuggestions)
                self.setHeight(pixels + 2 + 'px')

        def setSuggestions(self, suggestions):
            """Sets the suggestions rendered in the menu

            @param suggestions
                       The suggestions to be rendered in the menu
            """
            self.clearItems()
            it = suggestions
            while it.hasNext():
                s = it.next()
                mi = MenuItem(s.getDisplayString(), True, s)
                Util.sinkOnloadForImages(mi.getElement())
                self.addItem(mi)
                if s == self.currentSuggestion:
                    self.selectItem(mi)

        def doSelectedItemAction(self):
            """Send the current selection to the server. Triggered when a selection
            is made or on a blur event.
            """
            # do not send a value change event if null was and stays selected
            enteredItemValue = self.tb.getText()
            if (
                self.nullSelectionAllowed and '' == enteredItemValue and self.selectedOptionKey is not None and not ('' == self.selectedOptionKey)
            ):
                if self.nullSelectItem:
                    self.reset()
                    return
                # null is not visible on pages != 0, and not visible when
                # filtering: handle separately
                self.client.updateVariable(self.paintableId, 'filter', '', False)
                self.client.updateVariable(self.paintableId, 'page', 0, False)
                self.client.updateVariable(self.paintableId, 'selected', [], self.immediate)
                self.suggestionPopup.hide()
                return
            self.selecting = self.filtering
            if not self.filtering:
                self.doPostFilterSelectedItemAction()

        def doPostFilterSelectedItemAction(self):
            """Triggered after a selection has been made"""
            item = self.getSelectedItem()
            enteredItemValue = self.tb.getText()
            self.selecting = False
            # check for exact match in menu
            p = len(self.getItems())
            if p > 0:
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < p):
                        break
                    potentialExactMatch = self.getItems().get(i)
                    if potentialExactMatch.getText() == enteredItemValue:
                        self.selectItem(potentialExactMatch)
                        # do not send a value change event if null was and
                        # stays selected
                        if (
                            (not ('' == enteredItemValue)) or (self.selectedOptionKey is not None and not ('' == self.selectedOptionKey))
                        ):
                            self.doItemAction(potentialExactMatch, True)
                        self.suggestionPopup.hide()
                        return
            if self.allowNewItem:
                if not self.prompting and not (enteredItemValue == self.lastNewItemString):
                    # Store last sent new item string to avoid double sends
                    self.lastNewItemString = enteredItemValue
                    self.client.updateVariable(self.paintableId, 'newitem', enteredItemValue, self.immediate)
            elif (
                item is not None and not ('' == self.lastFilter) and item.getText().toLowerCase().contains(self.lastFilter.toLowerCase()) if self.filteringmode == self.FILTERINGMODE_CONTAINS else item.getText().toLowerCase().startswith(self.lastFilter.toLowerCase())
            ):
                self.doItemAction(item, True)
            elif (
                self.currentSuggestion is not None and not (self.currentSuggestion.key == '')
            ):
                # An item (not null) selected
                text = self.currentSuggestion.getReplacementString()
                self.tb.setText(text)
                self.selectedOptionKey = self.currentSuggestion.key
            else:
                # Null selected
                self.tb.setText('')
                self.selectedOptionKey = None
            # currentSuggestion has key="" for nullselection
            self.suggestionPopup.hide()

        _SUBPART_PREFIX = 'item'

        def getSubPartElement(self, subPart):
            index = int(subPart[len(self._SUBPART_PREFIX):])
            item = self.getItems().get(index)
            return item.getElement()

        def getSubPartName(self, subElement):
            if not self.getElement().isOrHasChild(subElement):
                return None
            menuItemRoot = subElement
            while (
                menuItemRoot is not None and not menuItemRoot.getTagName().equalsIgnoreCase('td')
            ):
                menuItemRoot = menuItemRoot.getParentElement()
            # "menuItemRoot" is now the root of the menu item
            itemCount = len(self.getItems())
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < itemCount):
                    break
                if self.getItems().get(i).getElement() == menuItemRoot:
                    name = self._SUBPART_PREFIX + i
                    return name
            return None

        def onLoad(self, event):
            if BrowserInfo.get().isIE6():
                # Ensure PNG transparency works in IE6
                Util.doIE6PngFix(Element.as_(event.getNativeEvent().getEventTarget()))
            # Handle icon onload events to ensure shadow is resized
            # correctly
            self._delayedImageLoadExecutioner.trigger()

    FILTERINGMODE_OFF = 0
    FILTERINGMODE_STARTSWITH = 1
    FILTERINGMODE_CONTAINS = 2

#    private static final String CLASSNAME = "v-filterselect";
#
#    protected int pageLength = 10;
#
#    private final FlowPanel panel = new FlowPanel();
#
#    /**
#     * The text box where the filter is written
#     */
#    private final TextBox tb = new TextBox() {
#        /*
#         * (non-Javadoc)
#         *
#         * @see
#         * com.google.gwt.user.client.ui.TextBoxBase#onBrowserEvent(com.google
#         * .gwt.user.client.Event)
#         */
#        @Override
#        public void onBrowserEvent(Event event) {
#            super.onBrowserEvent(event);
#            if (client != null) {
#                client.handleTooltipEvent(event, VFilterSelect.this);
#            }
#        }
#    };
#
#    private final SuggestionPopup suggestionPopup = new SuggestionPopup();
#
#    /**
#     * Used when measuring the width of the popup
#     */
#    private final HTML popupOpener = new HTML("") {
#
#        /*
#         * (non-Javadoc)
#         *
#         * @see
#         * com.google.gwt.user.client.ui.Widget#onBrowserEvent(com.google.gwt
#         * .user.client.Event)
#         */
#        @Override
#        public void onBrowserEvent(Event event) {
#            super.onBrowserEvent(event);
#            if (client != null) {
#                client.handleTooltipEvent(event, VFilterSelect.this);
#            }
#
#            /*
#             * Prevent the keyboard focus from leaving the textfield by
#             * preventing the default behaviour of the browser. Fixes #4285.
#             */
#            handleMouseDownEvent(event);
#        }
#    };
#
#    private final Image selectedItemIcon = new Image();
#
#    private ApplicationConnection client;
#
#    private String paintableId;
#
#    private int currentPage;
#
#    /**
#     * A collection of available suggestions (options) as received from the
#     * server.
#     */
#    private final Collection<FilterSelectSuggestion> currentSuggestions = new ArrayList<FilterSelectSuggestion>();
#
#    private boolean immediate;
#
#    private String selectedOptionKey;
#
#    private boolean filtering = false;
#    private boolean selecting = false;
#    private boolean tabPressed = false;
#    private boolean initDone = false;
#
#    private String lastFilter = "";
#    private int lastIndex = -1; // last selected index when using arrows
#
#    /**
#     * The current suggestion selected from the dropdown. This is one of the
#     * values in currentSuggestions except when filtering, in this case
#     * currentSuggestion might not be in currentSuggestions.
#     */
#    private FilterSelectSuggestion currentSuggestion;
#
#    private int totalMatches;
#    private boolean allowNewItem;
#    private boolean nullSelectionAllowed;
#    private boolean nullSelectItem;
#    private boolean enabled;
#    private boolean readonly;
#
#    private int filteringmode = FILTERINGMODE_OFF;
#
#    // shown in unfocused empty field, disappears on focus (e.g "Search here")
#    private static final String CLASSNAME_PROMPT = "prompt";
#    private static final String ATTR_INPUTPROMPT = "prompt";
#    private String inputPrompt = "";
#    private boolean prompting = false;
#
#    // Set true when popupopened has been clicked. Cleared on each UIDL-update.
#    // This handles the special case where are not filtering yet and the
#    // selected value has changed on the server-side. See #2119
#    private boolean popupOpenerClicked;
#    private String width = null;
#    private int textboxPadding = -1;
#    private int componentPadding = -1;
#    private int suggestionPopupMinWidth = 0;
#    private int popupWidth = -1;
#    /*
#     * Stores the last new item string to avoid double submissions. Cleared on
#     * uidl updates
#     */
#    private String lastNewItemString;
#    private boolean focused = false;
#    private int horizPaddingAndBorder = 2;

    def __init__(self):
        """Default constructor"""
        self.selectedItemIcon.setStyleName('v-icon')

        class _0_(LoadHandler):

            def onLoad(self, event):
                self.updateRootWidth()
                self.updateSelectedIconPosition()
                # Workaround for an IE bug where the text is positioned below
                # the icon (#3991)

                if BrowserInfo.get().isIE():
                    Util.setStyleTemporarily(self.tb.getElement(), 'paddingLeft', '0')

        _0_ = self._0_()
        self.selectedItemIcon.addLoadHandler(_0_)
        self.tb.sinkEvents(VTooltip.TOOLTIP_EVENTS)
        self.popupOpener.sinkEvents(VTooltip.TOOLTIP_EVENTS | Event.ONMOUSEDOWN)
        self.panel.add(self.tb)
        self.panel.add(self.popupOpener)
        self.initWidget(self.panel)
        self.setStyleName(self.CLASSNAME)
        self.tb.addKeyDownHandler(self)
        self.tb.addKeyUpHandler(self)
        self.tb.setStyleName(self.CLASSNAME + '-input')
        self.tb.addFocusHandler(self)
        self.tb.addBlurHandler(self)
        self.popupOpener.setStyleName(self.CLASSNAME + '-button')
        self.popupOpener.addClickHandler(self)

    def hasNextPage(self):
        """Does the Select have more pages?

        @return true if a next page exists, else false if the current page is the
                last page
        """
        if self.totalMatches > (self.currentPage + 1) * self.pageLength:
            return True
        else:
            return False

    def filterOptions(self, *args):
        """Filters the options at a certain page. Uses the text box input as a
        filter

        @param page
                   The page which items are to be filtered
        ---
        Filters the options at certain page using the given filter

        @param page
                   The page to filter
        @param filter
                   The filter to apply to the components
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            page, = _0
            self.filterOptions(page, self.tb.getText())
        elif _1 == 2:
            page, filter = _0
            if filter == self.lastFilter and self.currentPage == page:
                if not self.suggestionPopup.isAttached():
                    self.suggestionPopup.showSuggestions(self.currentSuggestions, self.currentPage, self.totalMatches)
                return
            if not (filter == self.lastFilter):
                # we are on subsequent page and text has changed -> reset page
                if '' == filter:
                    # let server decide
                    page = -1
                else:
                    page = 0
            self.filtering = True
            self.client.updateVariable(self.paintableId, 'filter', filter, False)
            self.client.updateVariable(self.paintableId, 'page', page, True)
            self.lastFilter = filter
            self.currentPage = page
        else:
            raise ARGERROR(1, 2)

    # (non-Javadoc)
    #
    # @see
    # com.vaadin.terminal.gwt.client.Paintable#updateFromUIDL(com.vaadin.terminal
    # .gwt.client.UIDL, com.vaadin.terminal.gwt.client.ApplicationConnection)

    def updateFromUIDL(self, uidl, client):
        self.paintableId = uidl.getId()
        self.client = client
        self.readonly = uidl.hasAttribute('readonly')
        self.enabled = not uidl.hasAttribute('disabled')
        self.tb.setEnabled(self.enabled)
        self.tb.setReadOnly(self.readonly)
        if client.updateComponent(self, uidl, True):
            return
        # not a FocusWidget -> needs own tabindex handling
        if uidl.hasAttribute('tabindex'):
            self.tb.setTabIndex(uidl.getIntAttribute('tabindex'))
        if uidl.hasAttribute('filteringmode'):
            self.filteringmode = uidl.getIntAttribute('filteringmode')
        self.immediate = uidl.hasAttribute('immediate')
        self.nullSelectionAllowed = uidl.hasAttribute('nullselect')
        self.nullSelectItem = uidl.hasAttribute('nullselectitem') and uidl.getBooleanAttribute('nullselectitem')
        self.currentPage = uidl.getIntVariable('page')
        if uidl.hasAttribute('pagelength'):
            self.pageLength = uidl.getIntAttribute('pagelength')
        if uidl.hasAttribute(self.ATTR_INPUTPROMPT):
            # input prompt changed from server
            self.inputPrompt = uidl.getStringAttribute(self.ATTR_INPUTPROMPT)
        else:
            self.inputPrompt = ''
        self.suggestionPopup.setPagingEnabled(True)
        self.suggestionPopup.updateStyleNames(uidl)
        self.allowNewItem = uidl.hasAttribute('allownewitem')
        self.lastNewItemString = None
        self.currentSuggestions.clear()
        if not self.filtering:
            # Clear the current suggestions as the server response always
            # includes the new ones. Exception is when filtering, then we need
            # to retain the value if the user does not select any of the
            # options matching the filter.

            self.currentSuggestion = None
            # Also ensure no old items in menu. Unless cleared the old values
            # may cause odd effects on blur events. Suggestions in menu might
            # not necessary exist in select at all anymore.

            self.suggestionPopup.menu.clearItems()
        options = uidl.getChildUIDL(0)
        if uidl.hasAttribute('totalMatches'):
            self.totalMatches = uidl.getIntAttribute('totalMatches')
        captions = self.inputPrompt
        _0 = True
        i = options.getChildIterator()
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            optionUidl = i.next()
            suggestion = self.FilterSelectSuggestion(optionUidl)
            self.currentSuggestions.add(suggestion)
            if optionUidl.hasAttribute('selected'):
                if (not self.filtering) or self.popupOpenerClicked:
                    newSelectedOptionKey = str(suggestion.getOptionKey())
                    if (
                        (not (newSelectedOptionKey == self.selectedOptionKey)) or (suggestion.getReplacementString() == self.tb.getText())
                    ):
                        # Update text field if we've got a new selection
                        # Also update if we've got the same text to retain old
                        # text selection behavior
                        self.setPromptingOff(suggestion.getReplacementString())
                        self.selectedOptionKey = newSelectedOptionKey
                self.currentSuggestion = suggestion
                self.setSelectedItemIcon(suggestion.getIconUri())
            # Collect captions so we can calculate minimum width for textarea
            if len(captions) > 0:
                captions += '|'
            captions += suggestion.getReplacementString()
        if (
            (not self.filtering) or self.popupOpenerClicked and uidl.hasVariable('selected') and uidl.getStringArrayVariable('selected').length == 0
        ):
            # select nulled
            if (not self.filtering) or (not self.popupOpenerClicked):
                if not self.focused:
                    # client.updateComponent overwrites all styles so we must
                    # ALWAYS set the prompting style at this point, even though
                    # we think it has been set already...

                    self.prompting = False
                    self.setPromptingOn()
                else:
                    # we have focus in field, prompting can't be set on,
                    # instead just clear the input
                    self.tb.setValue('')
            self.selectedOptionKey = None
        if (
            self.filtering and self.lastFilter.toLowerCase() == uidl.getStringVariable('filter')
        ):
            self.suggestionPopup.showSuggestions(self.currentSuggestions, self.currentPage, self.totalMatches)
            self.filtering = False
            if not self.popupOpenerClicked and self.lastIndex != -1:
                # we're paging w/ arrows
                if self.lastIndex == 0:
                    # going up, select last item
                    lastItem = self.pageLength - 1
                    items = self.suggestionPopup.menu.getItems()
                    # The first page can contain less than 10 items if the null
                    # selection item is filtered away

                    if lastItem >= len(items):
                        lastItem = len(items) - 1
                    activeMenuItem = items[lastItem]
                    self.suggestionPopup.menu.selectItem(activeMenuItem)
                else:
                    # going down, select first item
                    activeMenuItem = self.suggestionPopup.menu.getItems().get(0)
                    self.suggestionPopup.menu.selectItem(activeMenuItem)
                self.setTextboxText(activeMenuItem.getText())
                self.tb.setSelectionRange(len(self.lastFilter), len(activeMenuItem.getText()) - len(self.lastFilter))
                self.lastIndex = -1
                # reset
            if self.selecting:
                self.suggestionPopup.menu.doPostFilterSelectedItemAction()
        # Calculate minumum textarea width
        self.suggestionPopupMinWidth = self.minWidth(captions)
        self.popupOpenerClicked = False
        if not self.initDone:
            self.updateRootWidth()
        # Focus dependent style names are lost during the update, so we add
        # them here back again
        if self.focused:
            self.addStyleDependentName('focus')
        self.initDone = True

    def setTextboxText(self, text):
        """Sets the text in the text box using a deferred command if on Gecko. This
        is required for performance reasons (see #3663).

        @param text
                   the text to set in the text box
        """
        # (non-Javadoc)
        #
        # @see com.google.gwt.user.client.ui.Composite#onAttach()

        if BrowserInfo.get().isFF3():

            class _1_(Command):

                def execute(self):
                    self.tb.setText(self.text)

            _1_ = self._1_()
            Scheduler.get().scheduleDeferred(_1_)
        else:
            self.tb.setText(text)

    def onAttach(self):
        super(VFilterSelect, self).onAttach()
        # We need to recalculate the root width when the select is attached, so
        # #2974 won't happen.

        self.updateRootWidth()

    def setPromptingOn(self):
        """Turns prompting on. When prompting is turned on a command prompt is shown
        in the text box if nothing has been entered.
        """
        if not self.prompting:
            self.prompting = True
            self.addStyleDependentName(self.CLASSNAME_PROMPT)
        self.setTextboxText(self.inputPrompt)

    def setPromptingOff(self, text):
        """Turns prompting off. When prompting is turned on a command prompt is
        shown in the text box if nothing has been entered.

        @param text
                   The text the text box should contain.
        """
        self.setTextboxText(text)
        if self.prompting:
            self.prompting = False
            self.removeStyleDependentName(self.CLASSNAME_PROMPT)

    def onSuggestionSelected(self, suggestion):
        """Triggered when a suggestion is selected

        @param suggestion
                   The suggestion that just got selected.
        """
        self.selecting = False
        self.currentSuggestion = suggestion
        if suggestion.key == '':
            # "nullselection"
            newKey = ''
        else:
            # normal selection
            newKey = String.valueOf.valueOf(suggestion.getOptionKey())
        text = suggestion.getReplacementString()
        if '' == newKey and not self.focused:
            self.setPromptingOn()
        else:
            self.setPromptingOff(text)
        self.setSelectedItemIcon(suggestion.getIconUri())
        if (
            not ((newKey == self.selectedOptionKey) or ('' == newKey and self.selectedOptionKey is None))
        ):
            self.selectedOptionKey = newKey
            self.client.updateVariable(self.paintableId, 'selected', [self.selectedOptionKey], self.immediate)
            # currentPage = -1; // forget the page
        self.suggestionPopup.hide()

    def setSelectedItemIcon(self, iconUri):
        """Sets the icon URI of the selected item. The icon is shown on the left
        side of the item caption text. Set the URI to null to remove the icon.

        @param iconUri
                   The URI of the icon
        """
        if (iconUri is None) or (iconUri == ''):
            self.panel.remove(self.selectedItemIcon)
            self.updateRootWidth()
        else:
            self.panel.insert(self.selectedItemIcon, 0)
            self.selectedItemIcon.setUrl(iconUri)
            self.updateRootWidth()
            self.updateSelectedIconPosition()

    def updateSelectedIconPosition(self):
        """Positions the icon vertically in the middle. Should be called after the
        icon has loaded
        """
        # Position icon vertically to middle
        # (non-Javadoc)
        #
        # @see
        # com.google.gwt.event.dom.client.KeyDownHandler#onKeyDown(com.google.gwt
        # .event.dom.client.KeyDownEvent)

        availableHeight = 0
        if BrowserInfo.get().isIE6():
            self.getElement().getStyle().setOverflow(Overflow.HIDDEN)
            availableHeight = self.getOffsetHeight()
            self.getElement().getStyle().setProperty('overflow', '')
        else:
            availableHeight = self.getOffsetHeight()
        iconHeight = Util.getRequiredHeight(self.selectedItemIcon)
        marginTop = (availableHeight - iconHeight) / 2
        DOM.setStyleAttribute(self.selectedItemIcon.getElement(), 'marginTop', marginTop + 'px')

    def onKeyDown(self, event):
        if self.enabled and not self.readonly:
            if event.getNativeKeyCode() == KeyCodes.KEY_ENTER:
                # Same reaction to enter no matter on whether the popup is open
                if self.suggestionPopup.isAttached():
                    self.filterOptions(self.currentPage)
                elif (
                    self.currentSuggestion is not None and self.tb.getText() == self.currentSuggestion.getReplacementString()
                ):
                    # Retain behavior from #6686 by returning without stopping
                    # propagation if there's nothing to do
                    return
                if len(self.currentSuggestions) == 1 and not self.allowNewItem:
                    # If there is only one suggestion, select that
                    self.suggestionPopup.menu.selectItem(self.suggestionPopup.menu.getItems().get(0))
                self.suggestionPopup.menu.doSelectedItemAction()
                event.stopPropagation()
                return
            elif self.suggestionPopup.isAttached():
                self.popupKeyDown(event)
            else:
                self.inputFieldKeyDown(event)

    def inputFieldKeyDown(self, event):
        """Triggered when a key is pressed in the text box

        @param event
                   The KeyDownEvent
        """
        _0 = event.getNativeKeyCode()
        _1 = False
        while True:
            if _0 == KeyCodes.KEY_DOWN:
                _1 = True
            if (_1 is True) or (_0 == KeyCodes.KEY_UP):
                _1 = True
            if (_1 is True) or (_0 == KeyCodes.KEY_PAGEDOWN):
                _1 = True
            if (_1 is True) or (_0 == KeyCodes.KEY_PAGEUP):
                _1 = True
                if not self.suggestionPopup.isAttached():
                    # open popup as from gadget
                    self.filterOptions(-1, '')
                    self.lastFilter = ''
                    self.tb.selectAll()
                break
            if (_1 is True) or (_0 == KeyCodes.KEY_TAB):
                _1 = True
                if self.suggestionPopup.isAttached():
                    self.filterOptions(self.currentPage, self.tb.getText())
                break
            break

    def popupKeyDown(self, event):
        """Triggered when a key was pressed in the suggestion popup.

        @param event
                   The KeyDownEvent of the key
        """
        # Propagation of handled events is stopped so other handlers such as
        # shortcut key handlers do not also handle the same events.
        _0 = event.getNativeKeyCode()
        _1 = False
        while True:
            if _0 == KeyCodes.KEY_DOWN:
                _1 = True
                self.suggestionPopup.selectNextItem()
                DOM.eventPreventDefault(DOM.eventGetCurrentEvent())
                event.stopPropagation()
                break
            if (_1 is True) or (_0 == KeyCodes.KEY_UP):
                _1 = True
                self.suggestionPopup.selectPrevItem()
                DOM.eventPreventDefault(DOM.eventGetCurrentEvent())
                event.stopPropagation()
                break
            if (_1 is True) or (_0 == KeyCodes.KEY_PAGEDOWN):
                _1 = True
                if self.hasNextPage():
                    self.filterOptions(self.currentPage + 1, self.lastFilter)
                event.stopPropagation()
                break
            if (_1 is True) or (_0 == KeyCodes.KEY_PAGEUP):
                _1 = True
                if self.currentPage > 0:
                    self.filterOptions(self.currentPage - 1, self.lastFilter)
                event.stopPropagation()
                break
            if (_1 is True) or (_0 == KeyCodes.KEY_TAB):
                _1 = True
                if self.suggestionPopup.isAttached():
                    self.tabPressed = True
                    self.filterOptions(self.currentPage)
                # onBlur() takes care of the rest
                break
            break

    def onKeyUp(self, event):
        """Triggered when a key was depressed

        @param event
                   The KeyUpEvent of the key depressed
        """
        if self.enabled and not self.readonly:
            _0 = event.getNativeKeyCode()
            _1 = False
            while True:
                if _0 == KeyCodes.KEY_ENTER:
                    _1 = True
                if (_1 is True) or (_0 == KeyCodes.KEY_TAB):
                    _1 = True
                if (_1 is True) or (_0 == KeyCodes.KEY_SHIFT):
                    _1 = True
                if (_1 is True) or (_0 == KeyCodes.KEY_CTRL):
                    _1 = True
                if (_1 is True) or (_0 == KeyCodes.KEY_ALT):
                    _1 = True
                if (_1 is True) or (_0 == KeyCodes.KEY_DOWN):
                    _1 = True
                if (_1 is True) or (_0 == KeyCodes.KEY_UP):
                    _1 = True
                if (_1 is True) or (_0 == KeyCodes.KEY_PAGEDOWN):
                    _1 = True
                if (_1 is True) or (_0 == KeyCodes.KEY_PAGEUP):
                    _1 = True
                    # NOP
                    break
                if (_1 is True) or (_0 == KeyCodes.KEY_ESCAPE):
                    _1 = True
                    self.reset()
                    break
                if True:
                    _1 = True
                    self.filterOptions(self.currentPage)
                    break
                break

    def reset(self):
        """Resets the Select to its initial state"""
        if self.currentSuggestion is not None:
            text = self.currentSuggestion.getReplacementString()
            self.setPromptingOff(text)
            self.selectedOptionKey = self.currentSuggestion.key
        else:
            if self.focused:
                self.setPromptingOff('')
            else:
                self.setPromptingOn()
            self.selectedOptionKey = None
        self.lastFilter = ''
        self.suggestionPopup.hide()

    def onClick(self, event):
        """Listener for popupopener"""
        if self.enabled and not self.readonly:
            # ask suggestionPopup if it was just closed, we are using GWT
            # Popup's auto close feature
            if not self.suggestionPopup.isJustClosed():
                self.filterOptions(-1, '')
                self.popupOpenerClicked = True
                self.lastFilter = ''
            DOM.eventPreventDefault(DOM.eventGetCurrentEvent())
            self.focus()
            self.tb.selectAll()

    def minWidth(self, captions):
        """Calculate minimum width for FilterSelect textarea"""
        # -{
        #         if(!captions || captions.length <= 0)
        #                 return 0;
        #         captions = captions.split("|");
        #         var d = $wnd.document.createElement("div");
        #         var html = "";
        #         for(var i=0; i < captions.length; i++) {
        #                 html += "<div>" + captions[i] + "</div>";
        #                 // TODO apply same CSS classname as in suggestionmenu
        #         }
        #         d.style.position = "absolute";
        #         d.style.top = "0";
        #         d.style.left = "0";
        #         d.style.visibility = "hidden";
        #         d.innerHTML = html;
        #         $wnd.document.body.appendChild(d);
        #         var w = d.offsetWidth;
        #         $wnd.document.body.removeChild(d);
        #         return w;
        #     }-

        # A flag which prevents a focus event from taking place
        pass

    _iePreventNextFocus = False
    # (non-Javadoc)
    #
    # @see
    # com.google.gwt.event.dom.client.FocusHandler#onFocus(com.google.gwt.event
    # .dom.client.FocusEvent)

    def onFocus(self, event):
        # When we disable a blur event in ie we need to refocus the textfield.
        # This will cause a focus event we do not want to process, so in that
        # case we just ignore it.

        # A flag which cancels the blur event and sets the focus back to the
        # textfield if the Browser is IE

        if BrowserInfo.get().isIE() and self._iePreventNextFocus:
            self._iePreventNextFocus = False
            return
        self.focused = True
        if self.prompting and not self.readonly:
            self.setPromptingOff('')
        self.addStyleDependentName('focus')
        if self.client.hasEventListeners(self, EventId.FOCUS):
            self.client.updateVariable(self.paintableId, EventId.FOCUS, '', True)

    _preventNextBlurEventInIE = False
    # (non-Javadoc)
    #
    # @see
    # com.google.gwt.event.dom.client.BlurHandler#onBlur(com.google.gwt.event
    # .dom.client.BlurEvent)

    def onBlur(self, event):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.gwt.client.Focusable#focus()

        if BrowserInfo.get().isIE() and self._preventNextBlurEventInIE:
            # Clicking in the suggestion popup or on the popup button in IE
            # causes a blur event to be sent for the field. In other browsers
            # this is prevented by canceling/preventing default behavior for
            # the focus event, in IE we handle it here by refocusing the text
            # field and ignoring the resulting focus event for the textfield
            # (in onFocus).

            self._preventNextBlurEventInIE = False
            focusedElement = Util.getIEFocusedElement()
            if (
                self.getElement().isOrHasChild(focusedElement) or self.suggestionPopup.getElement().isOrHasChild(focusedElement)
            ):
                # IF the suggestion popup or another part of the VFilterSelect
                # was focused, move the focus back to the textfield and prevent
                # the triggered focus event (in onFocus).
                self._iePreventNextFocus = True
                self.tb.setFocus(True)
                return
        self.focused = False
        if not self.readonly:
            # much of the TAB handling takes place here
            if self.tabPressed:
                self.tabPressed = False
                self.suggestionPopup.menu.doSelectedItemAction()
                self.suggestionPopup.hide()
            elif (
                (not self.suggestionPopup.isAttached()) or self.suggestionPopup.isJustClosed()
            ):
                self.suggestionPopup.menu.doSelectedItemAction()
            if self.selectedOptionKey is None:
                self.setPromptingOn()
            elif self.currentSuggestion is not None:
                self.setPromptingOff(self.currentSuggestion.caption)
        self.removeStyleDependentName('focus')
        if self.client.hasEventListeners(self, EventId.BLUR):
            self.client.updateVariable(self.paintableId, EventId.BLUR, '', True)

    def focus(self):
        # (non-Javadoc)
        #
        # @see com.google.gwt.user.client.ui.UIObject#setWidth(java.lang.String)

        self.focused = True
        if self.prompting and not self.readonly:
            self.setPromptingOff('')
        self.tb.setFocus(True)

    def setWidth(self, width):
        # (non-Javadoc)
        #
        # @see com.google.gwt.user.client.ui.UIObject#setHeight(java.lang.String)

        if (width is None) or (width == ''):
            self.width = None
        else:
            self.width = width
        if BrowserInfo.get().isIE6():
            # Required in IE when textfield is wider than this.width
            self.getElement().getStyle().setOverflow(Overflow.HIDDEN)
            self.horizPaddingAndBorder = Util.setWidthExcludingPaddingAndBorder(self, width, self.horizPaddingAndBorder)
            self.getElement().getStyle().setProperty('overflow', '')
        else:
            self.horizPaddingAndBorder = Util.setWidthExcludingPaddingAndBorder(self, width, self.horizPaddingAndBorder)
        if self.initDone:
            self.updateRootWidth()

    def setHeight(self, height):
        super(VFilterSelect, self).setHeight(height)
        Util.setHeightExcludingPaddingAndBorder(self.tb, height, 3)

    def updateRootWidth(self):
        """Calculates the width of the select if the select has undefined width.
        Should be called when the width changes or when the icon changes.
        """
        if self.width is None:
            # When the width is not specified we must specify width for root
            # div so the popupopener won't wrap to the next line and also so
            # the size of the combobox won't change over time.

            tbWidth = Util.getRequiredWidth(self.tb)
            if self.popupWidth < 0:
                # Only use the first page popup width so the textbox will not
                # get resized whenever the popup is resized.

                self.popupWidth = Util.getRequiredWidth(self.popupOpener)
            # Note: iconWidth is here calculated as a negative pixel value so
            # you should consider this in further calculations.

            iconWidth = Util.measureMarginLeft(self.tb.getElement()) - Util.measureMarginLeft(self.selectedItemIcon.getElement()) if self.selectedItemIcon.isAttached() else 0
            w = tbWidth + self.popupWidth + iconWidth
            # When the select has a undefined with we need to check that we are
            # only setting the text box width relative to the first page width
            # of the items. If this is not done the text box width will change
            # when the popup is used to view longer items than the text box is
            # wide.

            if (
                (not self.initDone) or (self.currentPage + 1 < 0) and self.suggestionPopupMinWidth > w
            ):
                self.setTextboxWidth(self.suggestionPopupMinWidth)
                w = self.suggestionPopupMinWidth
            else:
                # Firefox3 has its own way of doing rendering so we need to
                # specify the width for the TextField to make sure it actually
                # is rendered as wide as FF3 says it is

                self.tb.setWidth((tbWidth - self.getTextboxPadding()) + 'px')
            super(VFilterSelect, self).setWidth(w + 'px')
            # Freeze the initial width, so that it won't change even if the
            # icon size changes
            self.width = w + 'px'
        else:
            # When the width is specified we also want to explicitly specify
            # widths for textbox and popupopener

            self.setTextboxWidth(self.getMainWidth() - self.getComponentPadding())

    def getMainWidth(self):
        """Get the width of the select in pixels where the text area and icon has
        been included.

        @return The width in pixels
        """
        if BrowserInfo.get().isIE6():
            # Required in IE when textfield is wider than this.width
            self.getElement().getStyle().setOverflow(Overflow.HIDDEN)
            componentWidth = self.getOffsetWidth()
            self.getElement().getStyle().setProperty('overflow', '')
        else:
            componentWidth = self.getOffsetWidth()
        return componentWidth

    def setTextboxWidth(self, componentWidth):
        """Sets the text box width in pixels.

        @param componentWidth
                   The width of the text box in pixels
        """
        padding = self.getTextboxPadding()
        popupOpenerWidth = Util.getRequiredWidth(self.popupOpener)
        iconWidth = Util.getRequiredWidth(self.selectedItemIcon) if self.selectedItemIcon.isAttached() else 0
        textboxWidth = componentWidth - padding - popupOpenerWidth - iconWidth
        if textboxWidth < 0:
            textboxWidth = 0
        self.tb.setWidth(textboxWidth + 'px')

    def getTextboxPadding(self):
        """Gets the horizontal padding of the text box in pixels. The measurement
        includes the border width.

        @return The padding in pixels
        """
        if self.textboxPadding < 0:
            self.textboxPadding = Util.measureHorizontalPaddingAndBorder(self.tb.getElement(), 4)
        return self.textboxPadding

    def getComponentPadding(self):
        """Gets the horizontal padding of the select. The measurement includes the
        border width.

        @return The padding in pixels
        """
        if self.componentPadding < 0:
            self.componentPadding = Util.measureHorizontalPaddingAndBorder(self.getElement(), 3)
        return self.componentPadding

    def handleMouseDownEvent(self, event):
        """Handles special behavior of the mouse down event

        @param event
        """
        # Prevent the keyboard focus from leaving the textfield by preventing
        # the default behaviour of the browser. Fixes #4285.

        if event.getTypeInt() == Event.ONMOUSEDOWN:
            event.preventDefault()
            event.stopPropagation()
            # In IE the above wont work, the blur event will still trigger. So,
            # we set a flag here to prevent the next blur event from happening.
            # This is not needed if do not already have focus, in that case
            # there will not be any blur event and we should not cancel the
            # next blur.

            if BrowserInfo.get().isIE() and self.focused:
                self._preventNextBlurEventInIE = True

    def onDetach(self):
        super(VFilterSelect, self).onDetach()
        self.suggestionPopup.hide()
