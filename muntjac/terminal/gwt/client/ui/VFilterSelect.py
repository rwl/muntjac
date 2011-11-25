# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.MenuItem import (MenuItem,)
from com.vaadin.terminal.gwt.client.ui.Field import (Field,)
from com.vaadin.terminal.gwt.client.ui.VLazyExecutor import (VLazyExecutor,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.SubPartAware import (SubPartAware,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
from com.vaadin.terminal.gwt.client.ui.MenuBar import (MenuBar,)
from com.vaadin.terminal.gwt.client.Focusable import (Focusable,)
# from com.google.gwt.dom.client.Style.Overflow import (Overflow,)
# from com.google.gwt.event.dom.client.KeyUpEvent import (KeyUpEvent,)
# from com.google.gwt.event.dom.client.KeyUpHandler import (KeyUpHandler,)
# from com.google.gwt.event.dom.client.LoadEvent import (LoadEvent,)
# from com.google.gwt.event.dom.client.LoadHandler import (LoadHandler,)
# from com.google.gwt.event.logical.shared.CloseEvent import (CloseEvent,)
# from com.google.gwt.event.logical.shared.CloseHandler import (CloseHandler,)
# from com.google.gwt.user.client.ui.FlowPanel import (FlowPanel,)
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

    def FilterSelectSuggestion(VFilterSelect_this, *args, **kwargs):

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
                    self._iconUri = VFilterSelect_this._client.translateVaadinUri(uidl.getStringAttribute('icon'))

            def getDisplayString(self):
                """Gets the visible row in the popup as a HTML string. The string
                contains an image tag with the rows icon (if an icon has been
                specified) and the caption of the item
                """
                sb = str()
                if self._iconUri is not None:
                    sb.__add__('<img src=\"')
                    sb.__add__(Util.escapeAttribute(self._iconUri))
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

        return FilterSelectSuggestion(*args, **kwargs)

    def SuggestionPopup(VFilterSelect_this, *args, **kwargs):

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
                self._menu = VFilterSelect_this.SuggestionMenu()
                self.setWidget(self._menu)
                self.setStyleName(VFilterSelect_this._CLASSNAME + '-suggestpopup')
                DOM.setStyleAttribute(self.getElement(), 'zIndex', self._Z_INDEX)
                root = self.getContainerElement()
                DOM.setInnerHTML(self._up, '<span>Prev</span>')
                DOM.sinkEvents(self._up, Event.ONCLICK)
                DOM.setInnerHTML(self._down, '<span>Next</span>')
                DOM.sinkEvents(self._down, Event.ONCLICK)
                DOM.insertChild(root, self._up, 0)
                DOM.appendChild(root, self._down)
                DOM.appendChild(root, self._status)
                DOM.setElementProperty(self._status, 'className', VFilterSelect_this._CLASSNAME + '-status')
                DOM.sinkEvents(root, Event.ONMOUSEDOWN | Event.ONMOUSEWHEEL)
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
                x = VFilterSelect_this.getAbsoluteLeft()
                self._topPosition = self.tb.getAbsoluteTop()
                self._topPosition += self.tb.getOffsetHeight()
                self.setPopupPosition(x, self._topPosition)
                nullOffset = 1 if VFilterSelect_this._nullSelectionAllowed and '' == VFilterSelect_this._lastFilter else 0
                firstPage = currentPage == 0
                first = ((currentPage * VFilterSelect_this.pageLength) + 1) - (0 if firstPage else nullOffset)
                last = (first + len(currentSuggestions)) - 1 - (nullOffset if firstPage and '' == VFilterSelect_this._lastFilter else 0)
                matches = totalSuggestions - nullOffset
                if last > 0:
                    # nullsel not counted, as requested by user
                    DOM.setInnerText(self._status, (0 if matches == 0 else first) + '-' + last + '/' + matches)
                else:
                    DOM.setInnerText(self._status, '')
                # We don't need to show arrows or statusbar if there is only one
                # page
                if (
                    (totalSuggestions <= VFilterSelect_this.pageLength) or (VFilterSelect_this.pageLength == 0)
                ):
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
                    DOM.setElementProperty(self._down, 'className', VFilterSelect_this._CLASSNAME + '-nextpage')
                else:
                    DOM.sinkEvents(self._down, 0)
                    DOM.setElementProperty(self._down, 'className', VFilterSelect_this._CLASSNAME + '-nextpage-off')

            def setPrevButtonActive(self, active):
                """Should the previous page button be visible to the user

                @param active
                """
                if active:
                    DOM.sinkEvents(self._up, Event.ONCLICK)
                    DOM.setElementProperty(self._up, 'className', VFilterSelect_this._CLASSNAME + '-prevpage')
                else:
                    DOM.sinkEvents(self._up, 0)
                    DOM.setElementProperty(self._up, 'className', VFilterSelect_this._CLASSNAME + '-prevpage-off')

            def selectNextItem(self):
                """Selects the next item in the filtered selections"""
                cur = self._menu.getSelectedItem()
                index = 1 + self._menu.getItems().index(cur)
                if len(self._menu.getItems()) > index:
                    newSelectedItem = self._menu.getItems().get(index)
                    self._menu.selectItem(newSelectedItem)
                    self.tb.setText(newSelectedItem.getText())
                    self.tb.setSelectionRange(len(VFilterSelect_this._lastFilter), len(newSelectedItem.getText()) - len(VFilterSelect_this._lastFilter))
                elif VFilterSelect_this.hasNextPage():
                    VFilterSelect_this._lastIndex = index - 1
                    # save for paging
                    self.filterOptions(VFilterSelect_this._currentPage + 1, VFilterSelect_this._lastFilter)

            def selectPrevItem(self):
                """Selects the previous item in the filtered selections"""
                # Using a timer to scroll up or down the pages so when we receive lots
                # of consecutive mouse wheel events the pages does not flicker.

                cur = self._menu.getSelectedItem()
                index = -1 + self._menu.getItems().index(cur)
                if index > -1:
                    newSelectedItem = self._menu.getItems().get(index)
                    self._menu.selectItem(newSelectedItem)
                    self.tb.setText(newSelectedItem.getText())
                    self.tb.setSelectionRange(len(VFilterSelect_this._lastFilter), len(newSelectedItem.getText()) - len(VFilterSelect_this._lastFilter))
                elif index == -1:
                    if VFilterSelect_this._currentPage > 0:
                        VFilterSelect_this._lastIndex = index + 1
                        # save for paging
                        self.filterOptions(VFilterSelect_this._currentPage - 1, VFilterSelect_this._lastFilter)
                else:
                    newSelectedItem = self._menu.getItems().get(len(self._menu.getItems()) - 1)
                    self._menu.selectItem(newSelectedItem)
                    self.tb.setText(newSelectedItem.getText())
                    self.tb.setSelectionRange(len(VFilterSelect_this._lastFilter), len(newSelectedItem.getText()) - len(VFilterSelect_this._lastFilter))

            _lazyPageScroller = LazyPageScroller()

            class LazyPageScroller(Timer):
                # (non-Javadoc)
                # 
                # @see
                # com.google.gwt.user.client.ui.Widget#onBrowserEvent(com.google.gwt
                # .user.client.Event)

                _pagesToScroll = 0

                def run(self):
                    if self._pagesToScroll != 0:
                        self.filterOptions(VFilterSelect_this._currentPage + self._pagesToScroll, VFilterSelect_this._lastFilter)
                        self._pagesToScroll = 0

                def scrollUp(self):
                    if VFilterSelect_this._currentPage + self._pagesToScroll > 0:
                        self._pagesToScroll -= 1
                        self.cancel()
                        self.schedule(100)

                def scrollDown(self):
                    if (
                        VFilterSelect_this._totalMatches > (VFilterSelect_this._currentPage + self._pagesToScroll + 1) * VFilterSelect_this.pageLength
                    ):
                        self._pagesToScroll += 1
                        self.cancel()
                        self.schedule(100)

            def onBrowserEvent(self, event):
                if event.getTypeInt() == Event.ONCLICK:
                    target = DOM.eventGetTarget(event)
                    if (target == self._up) or (target == DOM.getChild(self._up, 0)):
                        self._lazyPageScroller.scrollUp()
                    elif (target == self._down) or (target == DOM.getChild(self._down, 0)):
                        self._lazyPageScroller.scrollDown()
                elif event.getTypeInt() == Event.ONMOUSEWHEEL:
                    velocity = event.getMouseWheelVelocityY()
                    if velocity > 0:
                        self._lazyPageScroller.scrollDown()
                    else:
                        self._lazyPageScroller.scrollUp()
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
                if VFilterSelect_this._currentPage > 0:
                    # fix height to avoid height change when getting to last page
                    self._menu.fixHeightTo(VFilterSelect_this.pageLength)
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
                    top = self.getPopupTop() - offsetHeight - VFilterSelect_this.getOffsetHeight()
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
                    left = (VFilterSelect_this.getAbsoluteLeft() + VFilterSelect_this.getOffsetWidth() + Window.getScrollLeft()) - offsetWidth
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
                    self.setStyleName(VFilterSelect_this._CLASSNAME + '-suggestpopup')
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

        return SuggestionPopup(*args, **kwargs)

    def SuggestionMenu(VFilterSelect_this, *args, **kwargs):

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
                self.setStyleName(VFilterSelect_this._CLASSNAME + '-suggestmenu')
                self.addDomHandler(self, LoadEvent.getType())

            def fixHeightTo(self, pagelenth):
                """Fixes menus height to use same space as full page would use. Needed
                to avoid height changes when quickly "scrolling" to last page
                """
                if len(VFilterSelect_this._currentSuggestions) > 0:
                    pixels = (pagelenth * (self.getOffsetHeight() - 2)) / len(VFilterSelect_this._currentSuggestions)
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
                    if s == VFilterSelect_this._currentSuggestion:
                        self.selectItem(mi)

            def doSelectedItemAction(self):
                """Send the current selection to the server. Triggered when a selection
                is made or on a blur event.
                """
                # do not send a value change event if null was and stays selected
                enteredItemValue = self.tb.getText()
                if (
                    VFilterSelect_this._nullSelectionAllowed and '' == enteredItemValue and VFilterSelect_this._selectedOptionKey is not None and not ('' == VFilterSelect_this._selectedOptionKey)
                ):
                    if VFilterSelect_this._nullSelectItem:
                        self.reset()
                        return
                    # null is not visible on pages != 0, and not visible when
                    # filtering: handle separately
                    VFilterSelect_this._client.updateVariable(VFilterSelect_this._paintableId, 'filter', '', False)
                    VFilterSelect_this._client.updateVariable(VFilterSelect_this._paintableId, 'page', 0, False)
                    VFilterSelect_this._client.updateVariable(VFilterSelect_this._paintableId, 'selected', [], VFilterSelect_this._immediate)
                    self.suggestionPopup.hide()
                    return
                VFilterSelect_this._selecting = VFilterSelect_this._filtering
                if not VFilterSelect_this._filtering:
                    self.doPostFilterSelectedItemAction()

            def doPostFilterSelectedItemAction(self):
                """Triggered after a selection has been made"""
                item = self.getSelectedItem()
                enteredItemValue = self.tb.getText()
                VFilterSelect_this._selecting = False
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
                                (not ('' == enteredItemValue)) or (VFilterSelect_this._selectedOptionKey is not None and not ('' == VFilterSelect_this._selectedOptionKey))
                            ):
                                self.doItemAction(potentialExactMatch, True)
                            self.suggestionPopup.hide()
                            return
                if VFilterSelect_this._allowNewItem:
                    if (
                        not VFilterSelect_this._prompting and not (enteredItemValue == VFilterSelect_this._lastNewItemString)
                    ):
                        # Store last sent new item string to avoid double sends
                        VFilterSelect_this._lastNewItemString = enteredItemValue
                        VFilterSelect_this._client.updateVariable(VFilterSelect_this._paintableId, 'newitem', enteredItemValue, VFilterSelect_this._immediate)
                elif (
                    item is not None and not ('' == VFilterSelect_this._lastFilter) and item.getText().toLowerCase().contains(VFilterSelect_this._lastFilter.toLowerCase()) if VFilterSelect_this._filteringmode == VFilterSelect_this.FILTERINGMODE_CONTAINS else item.getText().toLowerCase().startswith(VFilterSelect_this._lastFilter.toLowerCase())
                ):
                    self.doItemAction(item, True)
                elif (
                    VFilterSelect_this._currentSuggestion is not None and not (VFilterSelect_this._currentSuggestion.key == '')
                ):
                    # An item (not null) selected
                    text = VFilterSelect_this._currentSuggestion.getReplacementString()
                    self.tb.setText(text)
                    VFilterSelect_this._selectedOptionKey = VFilterSelect_this._currentSuggestion.key
                else:
                    # Null selected
                    self.tb.setText('')
                    VFilterSelect_this._selectedOptionKey = None
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

        return SuggestionMenu(*args, **kwargs)

    FILTERINGMODE_OFF = 0
    FILTERINGMODE_STARTSWITH = 1
    FILTERINGMODE_CONTAINS = 2
    _CLASSNAME = 'v-filterselect'
    _STYLE_NO_INPUT = 'no-input'
    pageLength = 10
    _panel = FlowPanel()
    # /**
    # * The text box where the filter is written
    # //
    # private final TextBox tb = new TextBox() {
    # /*
    # * (non-Javadoc)
    # *
    # * @see
    # * com.google.gwt.user.client.ui.TextBoxBase#onBrowserEvent(com.google
    # * .gwt.user.client.Event)
    # //
    # @Override
    # public void onBrowserEvent(Event event) {
    # super.onBrowserEvent(event);
    # if (client != null) {
    # client.handleTooltipEvent(event, VFilterSelect.this);
    # }
    # }
    # @Override
    # // Overridden to avoid selecting text when text input is disabled
    # public void setSelectionRange(int pos, int length) {
    # if (textInputEnabled) {
    # super.setSelectionRange(pos, length);
    # } else {
    # super.setSelectionRange(getValue().length(), 0);
    # }
    # };
    # };
    # private final SuggestionPopup suggestionPopup = new SuggestionPopup();
    # Used when measuring the width of the popup
    # private final HTML popupOpener = new HTML("") {
    # /*
    # * (non-Javadoc)
    # *
    # * @see
    # * com.google.gwt.user.client.ui.Widget#onBrowserEvent(com.google.gwt
    # * .user.client.Event)
    # //
    # @Override
    # public void onBrowserEvent(Event event) {
    # super.onBrowserEvent(event);
    # if (client != null) {
    # client.handleTooltipEvent(event, VFilterSelect.this);
    # }
    # /*
    # * Prevent the keyboard focus from leaving the textfield by
    # * preventing the default behaviour of the browser. Fixes #4285.
    # //
    # handleMouseDownEvent(event);
    # }
    # };
    _selectedItemIcon = Image()
    _client = None
    _paintableId = None
    _currentPage = None
    # A collection of available suggestions (options) as received from the
    # server.

    _currentSuggestions = list()
    _immediate = None
    _selectedOptionKey = None
    _filtering = False
    _selecting = False
    _tabPressed = False
    _initDone = False
    _lastFilter = ''
    _lastIndex = -1
    # last selected index when using arrows
    # The current suggestion selected from the dropdown. This is one of the
    # values in currentSuggestions except when filtering, in this case
    # currentSuggestion might not be in currentSuggestions.

    _currentSuggestion = None
    _totalMatches = None
    _allowNewItem = None
    _nullSelectionAllowed = None
    _nullSelectItem = None
    _enabled = None
    _readonly = None
    _filteringmode = FILTERINGMODE_OFF
    # shown in unfocused empty field, disappears on focus (e.g "Search here")
    _CLASSNAME_PROMPT = 'prompt'
    _ATTR_INPUTPROMPT = 'prompt'
    ATTR_NO_TEXT_INPUT = 'noInput'
    _inputPrompt = ''
    _prompting = False
    # Set true when popupopened has been clicked. Cleared on each UIDL-update.
    # This handles the special case where are not filtering yet and the
    # selected value has changed on the server-side. See #2119
    _popupOpenerClicked = None
    _width = None
    _textboxPadding = -1
    _componentPadding = -1
    _suggestionPopupMinWidth = 0
    _popupWidth = -1
    # Stores the last new item string to avoid double submissions. Cleared on
    # uidl updates

    _lastNewItemString = None
    _focused = False
    _horizPaddingAndBorder = 2
    # If set to false, the component should not allow entering text to the
    # field even for filtering.

    _textInputEnabled = True

    def __init__(self):
        """Default constructor"""
        self._selectedItemIcon.setStyleName('v-icon')

        class _0_(LoadHandler):

            def onLoad(self, event):
                self.updateRootWidth()
                self.updateSelectedIconPosition()
                # Workaround for an IE bug where the text is positioned below
                # the icon (#3991)

                if BrowserInfo.get().isIE():
                    Util.setStyleTemporarily(self.tb.getElement(), 'paddingLeft', '0')

        _0_ = _0_()
        self._selectedItemIcon.addLoadHandler(_0_)
        self.tb.sinkEvents(VTooltip.TOOLTIP_EVENTS)
        self.popupOpener.sinkEvents(VTooltip.TOOLTIP_EVENTS | Event.ONMOUSEDOWN)
        self._panel.add(self.tb)
        self._panel.add(self.popupOpener)
        self.initWidget(self._panel)
        self.setStyleName(self._CLASSNAME)
        self.tb.addKeyDownHandler(self)
        self.tb.addKeyUpHandler(self)
        self.tb.setStyleName(self._CLASSNAME + '-input')
        self.tb.addFocusHandler(self)
        self.tb.addBlurHandler(self)
        self.tb.addClickHandler(self)
        self.popupOpener.setStyleName(self._CLASSNAME + '-button')
        self.popupOpener.addClickHandler(self)

    def hasNextPage(self):
        """Does the Select have more pages?

        @return true if a next page exists, else false if the current page is the
                last page
        """
        # Filters the options at a certain page. Uses the text box input as a
        # filter
        # 
        # @param page
        #            The page which items are to be filtered

        # public void filterOptions(int page) {
        # filterOptions(page, tb.getText());
        # }
        # /**
        # * Filters the options at certain page using the given filter
        # *
        # * @param page
        # *            The page to filter
        # * @param filter
        # *            The filter to apply to the components
        # //
        # public void filterOptions(int page, String filter) {
        # if (filter.equals(lastFilter) && currentPage == page) {
        # if (!suggestionPopup.isAttached()) {
        # suggestionPopup.showSuggestions(currentSuggestions,
        # currentPage, totalMatches);
        # }
        # return;
        # }
        # if (!filter.equals(lastFilter)) {
        # // we are on subsequent page and text has changed -> reset page
        # if ("".equals(filter)) {
        # // let server decide
        # page = -1;
        # } else {
        # page = 0;
        # }
        # }
        # filtering = true;
        # client.updateVariable(paintableId, "filter", filter, false);
        # client.updateVariable(paintableId, "page", page, true);
        # lastFilter = filter;
        # currentPage = page;
        # }
        # /*
        # * (non-Javadoc)
        # *
        # * @see
        # * com.vaadin.terminal.gwt.client.Paintable#updateFromUIDL(com.vaadin.terminal
        # * .gwt.client.UIDL, com.vaadin.terminal.gwt.client.ApplicationConnection)
        # //
        # @SuppressWarnings("deprecation")
        # public void updateFromUIDL(UIDL uidl, ApplicationConnection client) {
        # paintableId = uidl.getId();
        # this.client = client;
        # readonly = uidl.hasAttribute("readonly");
        # enabled = !uidl.hasAttribute("disabled");
        # tb.setEnabled(enabled);
        # updateReadOnly();
        # if (client.updateComponent(this, uidl, true)) {
        # return;
        # }
        # // Inverse logic here to make the default case (text input enabled)
        # // work without additional UIDL messages
        # boolean noTextInput = uidl.hasAttribute(ATTR_NO_TEXT_INPUT)
        # && uidl.getBooleanAttribute(ATTR_NO_TEXT_INPUT);
        # setTextInputEnabled(!noTextInput);
        # // not a FocusWidget -> needs own tabindex handling
        # if (uidl.hasAttribute("tabindex")) {
        # tb.setTabIndex(uidl.getIntAttribute("tabindex"));
        # }
        # if (uidl.hasAttribute("filteringmode")) {
        # filteringmode = uidl.getIntAttribute("filteringmode");
        # }
        # immediate = uidl.hasAttribute("immediate");
        # nullSelectionAllowed = uidl.hasAttribute("nullselect");
        # nullSelectItem = uidl.hasAttribute("nullselectitem")
        # && uidl.getBooleanAttribute("nullselectitem");
        # currentPage = uidl.getIntVariable("page");
        # if (uidl.hasAttribute("pagelength")) {
        # pageLength = uidl.getIntAttribute("pagelength");
        # }
        # if (uidl.hasAttribute(ATTR_INPUTPROMPT)) {
        # // input prompt changed from server
        # inputPrompt = uidl.getStringAttribute(ATTR_INPUTPROMPT);
        # } else {
        # inputPrompt = "";
        # }
        # suggestionPopup.setPagingEnabled(true);
        # suggestionPopup.updateStyleNames(uidl);
        # allowNewItem = uidl.hasAttribute("allownewitem");
        # lastNewItemString = null;
        # currentSuggestions.clear();
        # if (!filtering) {
        # /*
        # * Clear the current suggestions as the server response always
        # * includes the new ones. Exception is when filtering, then we need
        # * to retain the value if the user does not select any of the
        # * options matching the filter.
        # //
        # currentSuggestion = null;
        # /*
        # * Also ensure no old items in menu. Unless cleared the old values
        # * may cause odd effects on blur events. Suggestions in menu might
        # * not necessary exist in select at all anymore.
        # //
        # suggestionPopup.menu.clearItems();
        # }
        # final UIDL options = uidl.getChildUIDL(0);
        # if (uidl.hasAttribute("totalMatches")) {
        # totalMatches = uidl.getIntAttribute("totalMatches");
        # }
        # // used only to calculate minimum popup width
        # String captions = Util.escapeHTML(inputPrompt);
        # for (Iterator<?> i = options.getChildIterator(); i.hasNext();) {
        # final UIDL optionUidl = (UIDL) i.next();
        # final FilterSelectSuggestion suggestion = new FilterSelectSuggestion(
        # optionUidl);
        # currentSuggestions.add(suggestion);
        # if (optionUidl.hasAttribute("selected")) {
        # if (!filtering || popupOpenerClicked) {
        # String newSelectedOptionKey = Integer.toString(suggestion
        # .getOptionKey());
        # if (!newSelectedOptionKey.equals(selectedOptionKey)
        # || suggestion.getReplacementString().equals(
        # tb.getText())) {
        # // Update text field if we've got a new selection
        # // Also update if we've got the same text to retain old
        # // text selection behavior
        # setPromptingOff(suggestion.getReplacementString());
        # selectedOptionKey = newSelectedOptionKey;
        # }
        # }
        # currentSuggestion = suggestion;
        # setSelectedItemIcon(suggestion.getIconUri());
        # }
        # // Collect captions so we can calculate minimum width for textarea
        # if (captions.length() > 0) {
        # captions += "|";
        # }
        # captions += Util.escapeHTML(suggestion.getReplacementString());
        # }
        # if ((!filtering || popupOpenerClicked) && uidl.hasVariable("selected")
        # && uidl.getStringArrayVariable("selected").length == 0) {
        # // select nulled
        # if (!filtering || !popupOpenerClicked) {
        # if (!focused) {
        # /*
        # * client.updateComponent overwrites all styles so we must
        # * ALWAYS set the prompting style at this point, even though
        # * we think it has been set already...
        # //
        # prompting = false;
        # setPromptingOn();
        # } else {
        # // we have focus in field, prompting can't be set on,
        # // instead just clear the input
        # tb.setValue("");
        # }
        # }
        # selectedOptionKey = null;
        # }
        # if (filtering
        # && lastFilter.toLowerCase().equals(
        # uidl.getStringVariable("filter"))) {
        # suggestionPopup.showSuggestions(currentSuggestions, currentPage,
        # totalMatches);
        # filtering = false;
        # if (!popupOpenerClicked && lastIndex != -1) {
        # // we're paging w/ arrows
        # MenuItem activeMenuItem;
        # if (lastIndex == 0) {
        # // going up, select last item
        # int lastItem = pageLength - 1;
        # List<MenuItem> items = suggestionPopup.menu.getItems();
        # /*
        # * The first page can contain less than 10 items if the null
        # * selection item is filtered away
        # //
        # if (lastItem >= items.size()) {
        # lastItem = items.size() - 1;
        # }
        # activeMenuItem = items.get(lastItem);
        # suggestionPopup.menu.selectItem(activeMenuItem);
        # } else {
        # // going down, select first item
        # activeMenuItem = suggestionPopup.menu.getItems().get(0);
        # suggestionPopup.menu.selectItem(activeMenuItem);
        # }
        # setTextboxText(activeMenuItem.getText());
        # tb.setSelectionRange(lastFilter.length(), activeMenuItem
        # .getText().length() - lastFilter.length());
        # lastIndex = -1; // reset
        # }
        # if (selecting) {
        # suggestionPopup.menu.doPostFilterSelectedItemAction();
        # }
        # }
        # // Calculate minumum textarea width
        # suggestionPopupMinWidth = minWidth(captions);
        # popupOpenerClicked = false;
        # if (!initDone) {
        # updateRootWidth();
        # }
        # // Focus dependent style names are lost during the update, so we add
        # // them here back again
        # if (focused) {
        # addStyleDependentName("focus");
        # }
        # initDone = true;
        # }
        # private void updateReadOnly() {
        # tb.setReadOnly(readonly || !textInputEnabled);
        # }
        # private void setTextInputEnabled(boolean textInputEnabled) {
        # // Always update styles as they might have been overwritten
        # if (textInputEnabled) {
        # removeStyleDependentName(STYLE_NO_INPUT);
        # } else {
        # addStyleDependentName(STYLE_NO_INPUT);
        # }
        # if (this.textInputEnabled == textInputEnabled) {
        # return;
        # }
        # this.textInputEnabled = textInputEnabled;
        # updateReadOnly();
        # }
        # /**
        # * Sets the text in the text box using a deferred command if on Gecko. This
        # * is required for performance reasons (see #3663).
        # *
        # * @param text
        # *            the text to set in the text box
        # //
        # private void setTextboxText(final String text) {
        # if (BrowserInfo.get().isFF3()) {
        # Scheduler.get().scheduleDeferred(new Command() {
        # public void execute() {
        # tb.setText(text);
        # }
        # });
        # } else {
        # tb.setText(text);
        # }
        # }
        # /*
        # * (non-Javadoc)
        # *
        # * @see com.google.gwt.user.client.ui.Composite#onAttach()
        # //
        # @Override
        # protected void onAttach() {
        # super.onAttach();
        # /*
        # * We need to recalculate the root width when the select is attached, so
        # * #2974 won't happen.
        # //
        # updateRootWidth();
        # }
        # /**
        # * Turns prompting on. When prompting is turned on a command prompt is shown
        # * in the text box if nothing has been entered.
        # //
        # private void setPromptingOn() {
        # if (!prompting) {
        # prompting = true;
        # addStyleDependentName(CLASSNAME_PROMPT);
        # }
        # setTextboxText(inputPrompt);
        # }
        # /**
        # * Turns prompting off. When prompting is turned on a command prompt is
        # * shown in the text box if nothing has been entered.
        # *
        # * @param text
        # *            The text the text box should contain.
        # //
        # private void setPromptingOff(String text) {
        # setTextboxText(text);
        # if (prompting) {
        # prompting = false;
        # removeStyleDependentName(CLASSNAME_PROMPT);
        # }
        # }
        # /**
        # * Triggered when a suggestion is selected
        # *
        # * @param suggestion
        # *            The suggestion that just got selected.
        # //
        # public void onSuggestionSelected(FilterSelectSuggestion suggestion) {
        # selecting = false;
        # currentSuggestion = suggestion;
        # String newKey;
        # if (suggestion.key.equals("")) {
        # // "nullselection"
        # newKey = "";
        # } else {
        # // normal selection
        # newKey = String.valueOf(suggestion.getOptionKey());
        # }
        # String text = suggestion.getReplacementString();
        # if ("".equals(newKey) && !focused) {
        # setPromptingOn();
        # } else {
        # setPromptingOff(text);
        # }
        # setSelectedItemIcon(suggestion.getIconUri());
        # if (!(newKey.equals(selectedOptionKey) || ("".equals(newKey) && selectedOptionKey == null))) {
        # selectedOptionKey = newKey;
        # client.updateVariable(paintableId, "selected",
        # new String[] { selectedOptionKey }, immediate);
        # // currentPage = -1; // forget the page
        # }
        # suggestionPopup.hide();
        # }
        # /**
        # * Sets the icon URI of the selected item. The icon is shown on the left
        # * side of the item caption text. Set the URI to null to remove the icon.
        # *
        # * @param iconUri
        # *            The URI of the icon
        # //
        # private void setSelectedItemIcon(String iconUri) {
        # if (iconUri == null || iconUri == "") {
        # panel.remove(selectedItemIcon);
        # updateRootWidth();
        # } else {
        # panel.insert(selectedItemIcon, 0);
        # selectedItemIcon.setUrl(iconUri);
        # updateRootWidth();
        # updateSelectedIconPosition();
        # }
        # }
        # /**
        # * Positions the icon vertically in the middle. Should be called after the
        # * icon has loaded
        # //
        # private void updateSelectedIconPosition() {
        # // Position icon vertically to middle
        # int availableHeight = 0;
        # if (BrowserInfo.get().isIE6()) {
        # getElement().getStyle().setOverflow(Overflow.HIDDEN);
        # availableHeight = getOffsetHeight();
        # getElement().getStyle().setProperty("overflow", "");
        # } else {
        # availableHeight = getOffsetHeight();
        # }
        # int iconHeight = Util.getRequiredHeight(selectedItemIcon);
        # int marginTop = (availableHeight - iconHeight) / 2;
        # DOM.setStyleAttribute(selectedItemIcon.getElement(), "marginTop",
        # marginTop + "px");
        # }
        # /*
        # * (non-Javadoc)
        # *
        # * @see
        # * com.google.gwt.event.dom.client.KeyDownHandler#onKeyDown(com.google.gwt
        # * .event.dom.client.KeyDownEvent)
        # //
        # public void onKeyDown(KeyDownEvent event) {
        # if (enabled && !readonly) {
        # if (event.getNativeKeyCode() == KeyCodes.KEY_ENTER) {
        # // Same reaction to enter no matter on whether the popup is open
        # if (suggestionPopup.isAttached()) {
        # filterOptions(currentPage);
        # } else if (currentSuggestion != null
        # && tb.getText().equals(
        # currentSuggestion.getReplacementString())) {
        # // Retain behavior from #6686 by returning without stopping
        # // propagation if there's nothing to do
        # return;
        # }
        # if (currentSuggestions.size() == 1 && !allowNewItem) {
        # // If there is only one suggestion, select that
        # suggestionPopup.menu.selectItem(suggestionPopup.menu
        # .getItems().get(0));
        # }
        # suggestionPopup.menu.doSelectedItemAction();
        # event.stopPropagation();
        # return;
        # } else if (suggestionPopup.isAttached()) {
        # popupKeyDown(event);
        # } else {
        # inputFieldKeyDown(event);
        # }
        # }
        # }
        # /**
        # * Triggered when a key is pressed in the text box
        # *
        # * @param event
        # *            The KeyDownEvent
        # //
        # private void inputFieldKeyDown(KeyDownEvent event) {
        # switch (event.getNativeKeyCode()) {
        # case KeyCodes.KEY_DOWN:
        # case KeyCodes.KEY_UP:
        # case KeyCodes.KEY_PAGEDOWN:
        # case KeyCodes.KEY_PAGEUP:
        # if (!suggestionPopup.isAttached()) {
        # // open popup as from gadget
        # filterOptions(-1, "");
        # lastFilter = "";
        # tb.selectAll();
        # }
        # break;
        # case KeyCodes.KEY_TAB:
        # if (suggestionPopup.isAttached()) {
        # filterOptions(currentPage, tb.getText());
        # }
        # break;
        # }
        # }
        # /**
        # * Triggered when a key was pressed in the suggestion popup.
        # *
        # * @param event
        # *            The KeyDownEvent of the key
        # //
        # private void popupKeyDown(KeyDownEvent event) {
        # // Propagation of handled events is stopped so other handlers such as
        # // shortcut key handlers do not also handle the same events.
        # switch (event.getNativeKeyCode()) {
        # case KeyCodes.KEY_DOWN:
        # suggestionPopup.selectNextItem();
        # DOM.eventPreventDefault(DOM.eventGetCurrentEvent());
        # event.stopPropagation();
        # break;
        # case KeyCodes.KEY_UP:
        # suggestionPopup.selectPrevItem();
        # DOM.eventPreventDefault(DOM.eventGetCurrentEvent());
        # event.stopPropagation();
        # break;
        # case KeyCodes.KEY_PAGEDOWN:
        # if (hasNextPage()) {
        # filterOptions(currentPage + 1, lastFilter);
        # }
        # event.stopPropagation();
        # break;
        # case KeyCodes.KEY_PAGEUP:
        # if (currentPage > 0) {
        # filterOptions(currentPage - 1, lastFilter);
        # }
        # event.stopPropagation();
        # break;
        # case KeyCodes.KEY_TAB:
        # if (suggestionPopup.isAttached()) {
        # tabPressed = true;
        # filterOptions(currentPage);
        # }
        # // onBlur() takes care of the rest
        # break;
        # }
        # }
        # /**
        # * Triggered when a key was depressed
        # *
        # * @param event
        # *            The KeyUpEvent of the key depressed
        # //
        # public void onKeyUp(KeyUpEvent event) {
        # if (enabled && !readonly) {
        # switch (event.getNativeKeyCode()) {
        # case KeyCodes.KEY_ENTER:
        # case KeyCodes.KEY_TAB:
        # case KeyCodes.KEY_SHIFT:
        # case KeyCodes.KEY_CTRL:
        # case KeyCodes.KEY_ALT:
        # case KeyCodes.KEY_DOWN:
        # case KeyCodes.KEY_UP:
        # case KeyCodes.KEY_PAGEDOWN:
        # case KeyCodes.KEY_PAGEUP:
        # ; // NOP
        # break;
        # case KeyCodes.KEY_ESCAPE:
        # reset();
        # break;
        # default:
        # if (textInputEnabled) {
        # filterOptions(currentPage);
        # }
        # break;
        # }
        # }
        # }
        # /**
        # * Resets the Select to its initial state
        # //
        # private void reset() {
        # if (currentSuggestion != null) {
        # String text = currentSuggestion.getReplacementString();
        # setPromptingOff(text);
        # selectedOptionKey = currentSuggestion.key;
        # } else {
        # if (focused) {
        # setPromptingOff("");
        # } else {
        # setPromptingOn();
        # }
        # selectedOptionKey = null;
        # }
        # lastFilter = "";
        # suggestionPopup.hide();
        # }
        # /**
        # * Listener for popupopener
        # //
        # public void onClick(ClickEvent event) {
        # if (textInputEnabled
        # && event.getNativeEvent().getEventTarget().cast() == tb
        # .getElement()) {
        # // Don't process clicks on the text field if text input is enabled
        # return;
        # }
        # if (enabled && !readonly) {
        # // ask suggestionPopup if it was just closed, we are using GWT
        # // Popup's auto close feature
        # if (!suggestionPopup.isJustClosed()) {
        # filterOptions(-1, "");
        # popupOpenerClicked = true;
        # lastFilter = "";
        # }
        # DOM.eventPreventDefault(DOM.eventGetCurrentEvent());
        # focus();
        # tb.selectAll();
        # }
        # }
        # /**
        # * Calculate minimum width for FilterSelect textarea
        # //
        # private native int minWidth(String captions)
        # /*-{
        # if(!captions || captions.length <= 0)
        # return 0;
        # captions = captions.split("|");
        # var d = $wnd.document.createElement("div");
        # var html = "";
        # for(var i=0; i < captions.length; i++) {
        # html += "<div>" + captions[i] + "</div>";
        # // TODO apply same CSS classname as in suggestionmenu
        # }
        # d.style.position = "absolute";
        # d.style.top = "0";
        # d.style.left = "0";
        # d.style.visibility = "hidden";
        # d.innerHTML = html;
        # $wnd.document.body.appendChild(d);
        # var w = d.offsetWidth;
        # $wnd.document.body.removeChild(d);
        # return w;
        # }-*/;
        # /**
        # * A flag which prevents a focus event from taking place
        # //
        # boolean iePreventNextFocus = false;
        # /*
        # * (non-Javadoc)
        # *
        # * @see
        # * com.google.gwt.event.dom.client.FocusHandler#onFocus(com.google.gwt.event
        # * .dom.client.FocusEvent)
        # //
        # public void onFocus(FocusEvent event) {
        # /*
        # * When we disable a blur event in ie we need to refocus the textfield.
        # * This will cause a focus event we do not want to process, so in that
        # * case we just ignore it.
        # //
        # if (BrowserInfo.get().isIE() && iePreventNextFocus) {
        # iePreventNextFocus = false;
        # return;
        # }
        # focused = true;
        # if (prompting && !readonly) {
        # setPromptingOff("");
        # }
        # addStyleDependentName("focus");
        # if (client.hasEventListeners(this, EventId.FOCUS)) {
        # client.updateVariable(paintableId, EventId.FOCUS, "", true);
        # }
        # }
        # /**
        # * A flag which cancels the blur event and sets the focus back to the
        # * textfield if the Browser is IE
        # //
        # boolean preventNextBlurEventInIE = false;
        # /*
        # * (non-Javadoc)
        # *
        # * @see
        # * com.google.gwt.event.dom.client.BlurHandler#onBlur(com.google.gwt.event
        # * .dom.client.BlurEvent)
        # //
        # public void onBlur(BlurEvent event) {
        # if (BrowserInfo.get().isIE() && preventNextBlurEventInIE) {
        # /*
        # * Clicking in the suggestion popup or on the popup button in IE
        # * causes a blur event to be sent for the field. In other browsers
        # * this is prevented by canceling/preventing default behavior for
        # * the focus event, in IE we handle it here by refocusing the text
        # * field and ignoring the resulting focus event for the textfield
        # * (in onFocus).
        # //
        # preventNextBlurEventInIE = false;
        # Element focusedElement = Util.getIEFocusedElement();
        # if (getElement().isOrHasChild(focusedElement)
        # || suggestionPopup.getElement()
        # .isOrHasChild(focusedElement)) {
        # // IF the suggestion popup or another part of the VFilterSelect
        # // was focused, move the focus back to the textfield and prevent
        # // the triggered focus event (in onFocus).
        # iePreventNextFocus = true;
        # tb.setFocus(true);
        # return;
        # }
        # }
        # focused = false;
        # if (!readonly) {
        # // much of the TAB handling takes place here
        # if (tabPressed) {
        # tabPressed = false;
        # suggestionPopup.menu.doSelectedItemAction();
        # suggestionPopup.hide();
        # } else if (!suggestionPopup.isAttached()
        # || suggestionPopup.isJustClosed()) {
        # suggestionPopup.menu.doSelectedItemAction();
        # }
        # if (selectedOptionKey == null) {
        # setPromptingOn();
        # } else if (currentSuggestion != null) {
        # setPromptingOff(currentSuggestion.caption);
        # }
        # }
        # removeStyleDependentName("focus");
        # if (client.hasEventListeners(this, EventId.BLUR)) {
        # client.updateVariable(paintableId, EventId.BLUR, "", true);
        # }
        # }
        # /*
        # * (non-Javadoc)
        # *
        # * @see com.vaadin.terminal.gwt.client.Focusable#focus()
        # //
        # public void focus() {
        # focused = true;
        # if (prompting && !readonly) {
        # setPromptingOff("");
        # }
        # tb.setFocus(true);
        # }
        # /*
        # * (non-Javadoc)
        # *
        # * @see com.google.gwt.user.client.ui.UIObject#setWidth(java.lang.String)
        # //
        # @Override
        # public void setWidth(String width) {
        # if (width == null || width.equals("")) {
        # this.width = null;
        # } else {
        # this.width = width;
        # }
        # if (BrowserInfo.get().isIE6()) {
        # // Required in IE when textfield is wider than this.width
        # getElement().getStyle().setOverflow(Overflow.HIDDEN);
        # horizPaddingAndBorder = Util.setWidthExcludingPaddingAndBorder(
        # this, width, horizPaddingAndBorder);
        # getElement().getStyle().setProperty("overflow", "");
        # } else {
        # horizPaddingAndBorder = Util.setWidthExcludingPaddingAndBorder(
        # this, width, horizPaddingAndBorder);
        # }
        # if (initDone) {
        # updateRootWidth();
        # }
        # }
        # /*
        # * (non-Javadoc)
        # *
        # * @see com.google.gwt.user.client.ui.UIObject#setHeight(java.lang.String)
        # //
        # @Override
        # public void setHeight(String height) {
        # super.setHeight(height);
        # Util.setHeightExcludingPaddingAndBorder(tb, height, 3);
        # }
        # /**
        # * Calculates the width of the select if the select has undefined width.
        # * Should be called when the width changes or when the icon changes.
        # //
        # private void updateRootWidth() {
        # if (width == null) {
        # /*
        # * When the width is not specified we must specify width for root
        # * div so the popupopener won't wrap to the next line and also so
        # * the size of the combobox won't change over time.
        # //
        # int tbWidth = Util.getRequiredWidth(tb);
        # if (popupWidth < 0) {
        # /*
        # * Only use the first page popup width so the textbox will not
        # * get resized whenever the popup is resized.
        # //
        # popupWidth = Util.getRequiredWidth(popupOpener);
        # }
        # /*
        # * Note: iconWidth is here calculated as a negative pixel value so
        # * you should consider this in further calculations.
        # //
        # int iconWidth = selectedItemIcon.isAttached() ? Util
        # .measureMarginLeft(tb.getElement())
        # - Util.measureMarginLeft(selectedItemIcon.getElement()) : 0;
        # int w = tbWidth + popupWidth + iconWidth;
        # /*
        # * When the select has a undefined with we need to check that we are
        # * only setting the text box width relative to the first page width
        # * of the items. If this is not done the text box width will change
        # * when the popup is used to view longer items than the text box is
        # * wide.
        # //
        # if ((!initDone || currentPage + 1 < 0)
        # && suggestionPopupMinWidth > w) {
        # setTextboxWidth(suggestionPopupMinWidth);
        # w = suggestionPopupMinWidth;
        # } else {
        # /*
        # * Firefox3 has its own way of doing rendering so we need to
        # * specify the width for the TextField to make sure it actually
        # * is rendered as wide as FF3 says it is
        # //
        # tb.setWidth((tbWidth - getTextboxPadding()) + "px");
        # }
        # super.setWidth((w) + "px");
        # // Freeze the initial width, so that it won't change even if the
        # // icon size changes
        # width = w + "px";
        # } else {
        # /*
        # * When the width is specified we also want to explicitly specify
        # * widths for textbox and popupopener
        # //
        # setTextboxWidth(getMainWidth() - getComponentPadding());
        # }
        # }
        # /**
        # * Get the width of the select in pixels where the text area and icon has
        # * been included.
        # *
        # * @return The width in pixels
        # //
        # private int getMainWidth() {
        # int componentWidth;
        # if (BrowserInfo.get().isIE6()) {
        # // Required in IE when textfield is wider than this.width
        # getElement().getStyle().setOverflow(Overflow.HIDDEN);
        # componentWidth = getOffsetWidth();
        # getElement().getStyle().setProperty("overflow", "");
        # } else {
        # componentWidth = getOffsetWidth();
        # }
        # return componentWidth;
        # }
        # /**
        # * Sets the text box width in pixels.
        # *
        # * @param componentWidth
        # *            The width of the text box in pixels
        # //
        # private void setTextboxWidth(int componentWidth) {
        # int padding = getTextboxPadding();
        # int popupOpenerWidth = Util.getRequiredWidth(popupOpener);
        # int iconWidth = selectedItemIcon.isAttached() ? Util
        # .getRequiredWidth(selectedItemIcon) : 0;
        # int textboxWidth = componentWidth - padding - popupOpenerWidth
        # - iconWidth;
        # if (textboxWidth < 0) {
        # textboxWidth = 0;
        # }
        # tb.setWidth(textboxWidth + "px");
        # }
        # /**
        # * Gets the horizontal padding of the text box in pixels. The measurement
        # * includes the border width.
        # *
        # * @return The padding in pixels
        # //
        # private int getTextboxPadding() {
        # if (textboxPadding < 0) {
        # textboxPadding = Util.measureHorizontalPaddingAndBorder(
        # tb.getElement(), 4);
        # }
        # return textboxPadding;
        # }
        # /**
        # * Gets the horizontal padding of the select. The measurement includes the
        # * border width.
        # *
        # * @return The padding in pixels
        # //
        # private int getComponentPadding() {
        # if (componentPadding < 0) {
        # componentPadding = Util.measureHorizontalPaddingAndBorder(
        # getElement(), 3);
        # }
        # return componentPadding;
        # }
        # /**
        # * Handles special behavior of the mouse down event
        # *
        # * @param event
        # //
        # private void handleMouseDownEvent(Event event) {
        # /*
        # * Prevent the keyboard focus from leaving the textfield by preventing
        # * the default behaviour of the browser. Fixes #4285.
        # //
        # if (event.getTypeInt() == Event.ONMOUSEDOWN) {
        # event.preventDefault();
        # event.stopPropagation();
        # /*
        # * In IE the above wont work, the blur event will still trigger. So,
        # * we set a flag here to prevent the next blur event from happening.
        # * This is not needed if do not already have focus, in that case
        # * there will not be any blur event and we should not cancel the
        # * next blur.
        # //
        # if (BrowserInfo.get().isIE() && focused) {
        # preventNextBlurEventInIE = true;
        # }
        # }
        # }
        # @Override
        # protected void onDetach() {
        # super.onDetach();
        # suggestionPopup.hide();
        # }
        if self._totalMatches > (self._currentPage + 1) * self.pageLength:
            return True
        else:
            return False
