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

from pyjamas import DOM, Window

from pyjamas.Timer import Timer
from pyjamas.ui import Event, KeyboardListener

from pyjamas.ui.Composite import Composite

from datetime import datetime as Date

from muntjac.terminal.gwt.client.paintable import IPaintable
from muntjac.terminal.gwt.client.v_tooltip import VTooltip
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.ui.menu_item import MenuItem
from muntjac.terminal.gwt.client.ui.field import IField
from muntjac.terminal.gwt.client.ui.v_lazy_executor import VLazyExecutor
from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.ui.sub_part_aware import ISubPartAware
from muntjac.terminal.gwt.client.ui.v_overlay import VOverlay
from muntjac.terminal.gwt.client.ui.menu_bar import MenuBar
from muntjac.terminal.gwt.client.focusable import IFocusable
from gwt.ui.FlowPanel import FlowPanel
from gwt.ui.Image import Image
from muntjac.terminal.gwt.client.event_id import IEventId


class VFilterSelect(Composite, IPaintable, IField, IFocusable):
        #KeyDownHandler, KeyUpHandler, ClickHandler, FocusHandler, BlurHandler):
    """Client side implementation of the Select component.

    TODO: needs major refactoring (to be extensible etc)
    """

    FILTERINGMODE_OFF = 0
    FILTERINGMODE_STARTSWITH = 1
    FILTERINGMODE_CONTAINS = 2
    _CLASSNAME = 'v-filterselect'
    _STYLE_NO_INPUT = 'no-input'

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
    # shown in unfocused empty field, disappears on focus (e.g "Search here")

    _CLASSNAME_PROMPT = 'prompt'
    _ATTR_INPUTPROMPT = 'prompt'
    ATTR_NO_TEXT_INPUT = 'noInput'

    def __init__(self):
        """Default constructor"""

        self.pageLength = 10
        self._panel = FlowPanel()

        self._selectedItemIcon = Image()
        self._client = None
        self._paintableId = None
        self._currentPage = None

        # A collection of available suggestions (options) as received from the
        # server.
        self._currentSuggestions = list()
        self._immediate = None
        self._selectedOptionKey = None
        self._filtering = False
        self._selecting = False
        self._tabPressed = False
        self._initDone = False
        self._lastFilter = ''
        self._lastIndex = -1

        # last selected index when using arrows
        # The current suggestion selected from the dropdown. This is one of the
        # values in currentSuggestions except when filtering, in this case
        # currentSuggestion might not be in currentSuggestions.
        self._currentSuggestion = None
        self._totalMatches = None
        self._allowNewItem = None
        self._nullSelectionAllowed = None
        self._nullSelectItem = None
        self._enabled = None
        self._readonly = None
        self._filteringmode = self.FILTERINGMODE_OFF

        self._inputPrompt = ''
        self._prompting = False

        # Set true when popupopened has been clicked. Cleared on each UIDL-update.
        # This handles the special case where are not filtering yet and the
        # selected value has changed on the server-side. See #2119
        self._popupOpenerClicked = None
        self._width = None
        self._textboxPadding = -1
        self._componentPadding = -1
        self._suggestionPopupMinWidth = 0
        self._popupWidth = -1

        # Stores the last new item string to avoid double submissions. Cleared on
        # uidl updates
        self._lastNewItemString = None
        self._focused = False
        self._horizPaddingAndBorder = 2

        # If set to false, the component should not allow entering text to the
        # field even for filtering.
        self._textInputEnabled = True

        # A flag which prevents a focus event from taking place
        self._iePreventNextFocus = False

        # A flag which cancels the blur event and sets the focus back to the
        # textfield if the Browser is IE
        self._preventNextBlurEventInIE = False

        self._selectedItemIcon.setStyleName('v-icon')

        class _0_(LoadHandler):

            def onLoad(self, event):
                self.updateRootWidth()
                self.updateSelectedIconPosition()
                # Workaround for an IE bug where the text is positioned below
                # the icon (#3991)

                if BrowserInfo.get().isIE():
                    Util.setStyleTemporarily(self.tb.getElement(),
                            'paddingLeft', '0')

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

        @return: true if a next page exists, else false if the current page
                 is the last page
        """
        if self._totalMatches > (self._currentPage + 1) * self.pageLength:
            return True
        else:
            return False


    def filterOptions(self, page, fltr=None):
        """Filters the options at certain page using the given filter

        @param page:
                   The page to filter
        @param filter:
                   The filter to apply to the components. Uses the text box
                   input by default.
        """
        if fltr is None:
            fltr = self.tb.getText()

        if fltr == self._lastFilter and self._currentPage == page:
            if not self.suggestionPopup.isAttached():
                self.suggestionPopup.showSuggestions(self._currentSuggestions,
                        self._currentPage, self._totalMatches)
            return

        if fltr != self._lastFilter:
            # we are on subsequent page and text has changed -> reset page
            if '' == fltr:
                # let server decide
                page = -1
            else:
                page = 0

        self._filtering = True
        self._client.updateVariable(self._paintableId, 'filter', fltr, False)
        self._client.updateVariable(self._paintableId, 'page', page, True)
        self._lastFilter = fltr
        self._currentPage = page


    def updateFromUIDL(self, uidl, client):
        self._paintableId = uidl.getId()
        self._client = client

        self._readonly = uidl.hasAttribute('readonly')
        self._enabled = not uidl.hasAttribute('disabled')

        self.tb.setEnabled(self._enabled)
        self.updateReadOnly()

        if client.updateComponent(self, uidl, True):
            return

        # Inverse logic here to make the default case (text input enabled)
        # work without additional UIDL messages
        noTextInput = (uidl.hasAttribute(self.ATTR_NO_TEXT_INPUT)
                and uidl.getBooleanAttribute(self.ATTR_NO_TEXT_INPUT))
        self.setTextInputEnabled(not noTextInput)

        # not a FocusWidget -> needs own tabindex handling
        if uidl.hasAttribute('tabindex'):
            self.tb.setTabIndex(uidl.getIntAttribute('tabindex'))

        if uidl.hasAttribute('filteringmode'):
            self._filteringmode = uidl.getIntAttribute('filteringmode')

        self._immediate = uidl.hasAttribute('immediate')

        self._nullSelectionAllowed = uidl.hasAttribute('nullselect')

        self._nullSelectItem = (uidl.hasAttribute('nullselectitem')
                and uidl.getBooleanAttribute('nullselectitem'))

        self._currentPage = uidl.getIntVariable('page')

        if uidl.hasAttribute('pagelength'):
            self.pageLength = uidl.getIntAttribute('pagelength')

        if uidl.hasAttribute(self._ATTR_INPUTPROMPT):
            # input prompt changed from server
            self._inputPrompt = uidl.getStringAttribute(self._ATTR_INPUTPROMPT)
        else:
            self._inputPrompt = ''

        self.suggestionPopup.setPagingEnabled(True)
        self.suggestionPopup.updateStyleNames(uidl)

        self._allowNewItem = uidl.hasAttribute('allownewitem')
        self._lastNewItemString = None

        self._currentSuggestions.clear()
        if not self._filtering:
            # Clear the current suggestions as the server response always
            # includes the new ones. Exception is when filtering, then we need
            # to retain the value if the user does not select any of the
            # options matching the filter.
            self._currentSuggestion = None

            # Also ensure no old items in menu. Unless cleared the old values
            # may cause odd effects on blur events. Suggestions in menu might
            # not necessary exist in select at all anymore.
            self.suggestionPopup.menu.clearItems()

        options = uidl.getChildUIDL(0)
        if uidl.hasAttribute('totalMatches'):
            self._totalMatches = uidl.getIntAttribute('totalMatches')

        # used only to calculate minimum popup width
        captions = Util.escapeHTML(self._inputPrompt)

        for optionUidl in options:
            suggestion = FilterSelectSuggestion(optionUidl)
            self._currentSuggestions.append(suggestion)
            if optionUidl.hasAttribute('selected'):
                if (not self._filtering) or self._popupOpenerClicked:
                    newSelectedOptionKey = str(suggestion.getOptionKey())
                    if ((newSelectedOptionKey != self._selectedOptionKey)
                            or (suggestion.getReplacementString()
                                    == self.tb.getText())):
                        # Update text field if we've got a new selection
                        # Also update if we've got the same text to retain old
                        # text selection behavior
                        self.setPromptingOff(suggestion.getReplacementString())
                        self._selectedOptionKey = newSelectedOptionKey

                self._currentSuggestion = suggestion
                self.setSelectedItemIcon(suggestion.getIconUri())

            # Collect captions so we can calculate minimum width for textarea
            if len(captions) > 0:
                captions += '|'

            captions += Util.escapeHTML(suggestion.getReplacementString())

        if ((not self._filtering) or self._popupOpenerClicked
                and uidl.hasVariable('selected')
                and uidl.getStringArrayVariable('selected').length == 0):
            # select nulled
            if (not self._filtering) or (not self._popupOpenerClicked):
                if not self._focused:
                    # client.updateComponent overwrites all styles so we must
                    # ALWAYS set the prompting style at this point, even though
                    # we think it has been set already...
                    self._prompting = False
                    self.setPromptingOn()
                else:
                    # we have focus in field, prompting can't be set on,
                    # instead just clear the input
                    self.tb.setValue('')

            self._selectedOptionKey = None

        if (self._filtering and
                (self._lastFilter.toLowerCase()
                        == uidl.getStringVariable('filter'))):
            self.suggestionPopup.showSuggestions(self._currentSuggestions,
                    self._currentPage, self._totalMatches)
            self._filtering = False
            if not self._popupOpenerClicked and self._lastIndex != -1:
                # we're paging w/ arrows
                if self._lastIndex == 0:
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
                self.tb.setSelectionRange(len(self._lastFilter),
                        len(activeMenuItem.getText()) - len(self._lastFilter))

                self._lastIndex = -1  # reset

            if self._selecting:
                self.suggestionPopup.menu.doPostFilterSelectedItemAction()

        # Calculate minumum textarea width
        self._suggestionPopupMinWidth = self.minWidth(captions)

        self._popupOpenerClicked = False

        if not self._initDone:
            self.updateRootWidth()

        # Focus dependent style names are lost during the update, so we add
        # them here back again
        if self._focused:
            self.addStyleDependentName('focus')

        self._initDone = True


    def updateReadOnly(self):
        self.tb.setReadOnly(self._readonly or (not self._textInputEnabled))


    def setTextInputEnabled(self, textInputEnabled):
        # Always update styles as they might have been overwritten
        if textInputEnabled:
            self.removeStyleDependentName(self._STYLE_NO_INPUT)
        else:
            self.addStyleDependentName(self._STYLE_NO_INPUT)

        if self._textInputEnabled == textInputEnabled:
            return

        self._textInputEnabled = textInputEnabled
        self.updateReadOnly()


    def setTextboxText(self, text):
        """Sets the text in the text box using a deferred command if on Gecko.
        This is required for performance reasons (see #3663).

        @param text:
                   the text to set in the text box
        """
        if BrowserInfo.get().isFF3():

            class _1_(Command):

                def execute(self):
                    self.tb.setText(self.text)

            _1_ = _1_()
            Scheduler.get().scheduleDeferred(_1_)
        else:
            self.tb.setText(text)


    def onAttach(self):
        super(VFilterSelect, self).onAttach()
        # We need to recalculate the root width when the select is attached,
        # so #2974 won't happen.
        self.updateRootWidth()


    def setPromptingOn(self):
        """Turns prompting on. When prompting is turned on a command prompt
        is shown in the text box if nothing has been entered.
        """
        if not self._prompting:
            self._prompting = True
            self.addStyleDependentName(self._CLASSNAME_PROMPT)
        self.setTextboxText(self._inputPrompt)


    def setPromptingOff(self, text):
        """Turns prompting off. When prompting is turned on a command prompt
        is shown in the text box if nothing has been entered.

        @param text:
                   The text the text box should contain.
        """
        self.setTextboxText(text)
        if self._prompting:
            self._prompting = False
            self.removeStyleDependentName(self._CLASSNAME_PROMPT)


    def onSuggestionSelected(self, suggestion):
        """Triggered when a suggestion is selected

        @param suggestion:
                   The suggestion that just got selected.
        """
        self._selecting = False
        self._currentSuggestion = suggestion
        if suggestion.key == '':
            # "nullselection"
            newKey = ''
        else:
            # normal selection
            newKey = str(suggestion.getOptionKey())

        text = suggestion.getReplacementString()
        if '' == newKey and not self._focused:
            self.setPromptingOn()
        else:
            self.setPromptingOff(text)

        self.setSelectedItemIcon(suggestion.getIconUri())

        if (not ((newKey == self._selectedOptionKey)
                    or ('' == newKey and self._selectedOptionKey is None))):
            self._selectedOptionKey = newKey
            self._client.updateVariable(self._paintableId, 'selected',
                    [self._selectedOptionKey], self._immediate)
            # currentPage = -1; // forget the page
        self.suggestionPopup.hide()


    def setSelectedItemIcon(self, iconUri):
        """Sets the icon URI of the selected item. The icon is shown on the
        left side of the item caption text. Set the URI to null to remove the
        icon.

        @param iconUri:
                   The URI of the icon
        """
        if (iconUri is None) or (iconUri == ''):
            self._panel.remove(self._selectedItemIcon)
            self.updateRootWidth()
        else:
            self._panel.insert(self._selectedItemIcon, 0)
            self._selectedItemIcon.setUrl(iconUri)
            self.updateRootWidth()
            self.updateSelectedIconPosition()


    def updateSelectedIconPosition(self):
        """Positions the icon vertically in the middle. Should be called after
        the icon has loaded
        """
        # Position icon vertically to middle
        availableHeight = 0
        if BrowserInfo.get().isIE6():
            self.getElement().getStyle().setOverflow('hidden')#Overflow.HIDDEN)
            availableHeight = self.getOffsetHeight()
            self.getElement().getStyle().setProperty('overflow', '')
        else:
            availableHeight = self.getOffsetHeight()
        iconHeight = Util.getRequiredHeight(self._selectedItemIcon)
        marginTop = (availableHeight - iconHeight) / 2
        DOM.setStyleAttribute(self._selectedItemIcon.getElement(),
                'marginTop', marginTop + 'px')


    def onKeyDown(self, event):
        if self._enabled and not self._readonly:
            if event.getNativeKeyCode() == KeyboardListener.KEY_ENTER:
                # Same reaction to enter no matter on whether the popup is open
                if self.suggestionPopup.isAttached():
                    self.filterOptions(self._currentPage)
                elif (self._currentSuggestion is not None
                      and (self.tb.getText()
                            == self._currentSuggestion.getReplacementString())):
                    # Retain behavior from #6686 by returning without stopping
                    # propagation if there's nothing to do
                    return

                if len(self._currentSuggestions) == 1 and not self._allowNewItem:
                    # If there is only one suggestion, select that
                    self.suggestionPopup.menu.selectItem(
                            self.suggestionPopup.menu.getItems().get(0))

                self.suggestionPopup.menu.doSelectedItemAction()

                event.stopPropagation()
                return
            elif self.suggestionPopup.isAttached():
                self.popupKeyDown(event)
            else:
                self.inputFieldKeyDown(event)


    def inputFieldKeyDown(self, event):
        """Triggered when a key is pressed in the text box

        @param event:
                   The KeyDownEvent
        """
        code = event.getNativeKeyCode()
        if code == KeyboardListener.KEY_DOWN:
            pass
        if code == KeyboardListener.KEY_UP:
            pass
        if code == KeyboardListener.KEY_PAGEDOWN:
            pass
        if code == KeyboardListener.KEY_PAGEUP:
            if not self.suggestionPopup.isAttached():
                # open popup as from gadget
                self.filterOptions(-1, '')
                self._lastFilter = ''
                self.tb.selectAll()

        elif code == KeyboardListener.KEY_TAB:
            if self.suggestionPopup.isAttached():
                self.filterOptions(self._currentPage, self.tb.getText())


    def popupKeyDown(self, event):
        """Triggered when a key was pressed in the suggestion popup.

        @param event:
                   The KeyDownEvent of the key
        """
        # Propagation of handled events is stopped so other handlers such as
        # shortcut key handlers do not also handle the same events.
        code = event.getNativeKeyCode()
        if code == KeyboardListener.KEY_DOWN:
            self.suggestionPopup.selectNextItem()
            DOM.eventPreventDefault(DOM.eventGetCurrentEvent())
            event.stopPropagation()

        elif code == KeyboardListener.KEY_UP:
            self.suggestionPopup.selectPrevItem()
            DOM.eventPreventDefault(DOM.eventGetCurrentEvent())
            event.stopPropagation()

        elif code == KeyboardListener.KEY_PAGEDOWN:
            if self.hasNextPage():
                self.filterOptions(self._currentPage + 1, self._lastFilter)
            event.stopPropagation()

        elif code == KeyboardListener.KEY_PAGEUP:
            if self._currentPage > 0:
                self.filterOptions(self._currentPage - 1, self._lastFilter)
            event.stopPropagation()

        elif code == KeyboardListener.KEY_TAB:
            if self.suggestionPopup.isAttached():
                self._tabPressed = True
                self.filterOptions(self._currentPage)
            # onBlur() takes care of the rest


    def onKeyUp(self, event):
        """Triggered when a key was depressed

        @param event:
                   The KeyUpEvent of the key depressed
        """
        if self._enabled and not self._readonly:
            code = event.getNativeKeyCode()
            if code == KeyboardListener.KEY_ENTER:
                pass
            if code == KeyboardListener.KEY_TAB:
                pass
            if code == KeyboardListener.KEY_SHIFT:
                pass
            if code == KeyboardListener.KEY_CTRL:
                pass
            if code == KeyboardListener.KEY_ALT:
                pass
            if code == KeyboardListener.KEY_DOWN:
                pass
            if code == KeyboardListener.KEY_UP:
                pass
            if code == KeyboardListener.KEY_PAGEDOWN:
                pass
            if code == KeyboardListener.KEY_PAGEUP:
                return # NOP

            if code == KeyboardListener.KEY_ESCAPE:
                self.reset()
                return

            if self._textInputEnabled:
                self.filterOptions(self._currentPage)


    def reset(self):
        """Resets the Select to its initial state"""
        if self._currentSuggestion is not None:
            text = self._currentSuggestion.getReplacementString()
            self.setPromptingOff(text)
            self._selectedOptionKey = self._currentSuggestion.key
        else:
            if self._focused:
                self.setPromptingOff('')
            else:
                self.setPromptingOn()
            self._selectedOptionKey = None

        self._lastFilter = ''
        self.suggestionPopup.hide()


    def onClick(self, event):
        """Listener for popupopener"""
        if (self._textInputEnabled
                and (event.getNativeEvent().getEventTarget()
                        == self.tb.getElement())):
            # Don't process clicks on the text field if text input is enabled
            return

        if self._enabled and not self._readonly:
            # ask suggestionPopup if it was just closed, we are using GWT
            # Popup's auto close feature
            if not self.suggestionPopup.isJustClosed():
                self.filterOptions(-1, '')
                self._popupOpenerClicked = True
                self._lastFilter = ''

            DOM.eventPreventDefault(DOM.eventGetCurrentEvent())
            self.focus()
            self.tb.selectAll()


    def minWidth(self, captions):
        """Calculate minimum width for FilterSelect textarea"""
        JS("""
            if(!@{{captions}} || @{{captions}}.length <= 0)
                    return 0;
            @{{captions}} = @{{captions}}.split("|");
            var d = $wnd.document.createElement("div");
            var html = "";
            for(var i=0; i < @{{captions}}.length; i++) {
                    html += "<div>" + @{{captions}}[i] + "</div>";
                    // TODO apply same CSS classname as in suggestionmenu
            }
            d.style.position = "absolute";
            d.style.top = "0";
            d.style.left = "0";
            d.style.visibility = "hidden";
            d.innerHTML = html;
            $wnd.document.body.appendChild(d);
            var w = d.offsetWidth;
            $wnd.document.body.removeChild(d);
            return w;
        """)
        pass


    def onFocus(self, event):
        # When we disable a blur event in ie we need to refocus the textfield.
        # This will cause a focus event we do not want to process, so in that
        # case we just ignore it.


        if BrowserInfo.get().isIE() and self._iePreventNextFocus:
            self._iePreventNextFocus = False
            return
        self._focused = True
        if self._prompting and not self._readonly:
            self.setPromptingOff('')
        self.addStyleDependentName('focus')
        if self._client.hasEventListeners(self, IEventId.FOCUS):
            self._client.updateVariable(self._paintableId, EventId.FOCUS,
                    '', True)


    def onBlur(self, event):

        if BrowserInfo.get().isIE() and self._preventNextBlurEventInIE:
            # Clicking in the suggestion popup or on the popup button in IE
            # causes a blur event to be sent for the field. In other browsers
            # this is prevented by canceling/preventing default behavior for
            # the focus event, in IE we handle it here by refocusing the text
            # field and ignoring the resulting focus event for the textfield
            # (in onFocus).
            self._preventNextBlurEventInIE = False

            focusedElement = Util.getIEFocusedElement()
            if (self.getElement().isOrHasChild(focusedElement)
                    or self.suggestionPopup.getElement().isOrHasChild(focusedElement)):
                # IF the suggestion popup or another part of the VFilterSelect
                # was focused, move the focus back to the textfield and prevent
                # the triggered focus event (in onFocus).
                self._iePreventNextFocus = True
                self.tb.setFocus(True)
                return

        self._focused = False
        if not self._readonly:
            # much of the TAB handling takes place here
            if self._tabPressed:
                self._tabPressed = False
                self.suggestionPopup.menu.doSelectedItemAction()
                self.suggestionPopup.hide()
            elif ((not self.suggestionPopup.isAttached())
                    or self.suggestionPopup.isJustClosed()):
                self.suggestionPopup.menu.doSelectedItemAction()

            if self._selectedOptionKey is None:
                self.setPromptingOn()
            elif self._currentSuggestion is not None:
                self.setPromptingOff(self._currentSuggestion.caption)

        self.removeStyleDependentName('focus')
        if self._client.hasEventListeners(self, IEventId.BLUR):
            self._client.updateVariable(self._paintableId, IEventId.BLUR,
                    '', True)


    def focus(self):
        self._focused = True
        if self._prompting and not self._readonly:
            self.setPromptingOff('')
        self.tb.setFocus(True)


    def setWidth(self, width):
        if (width is None) or (width == ''):
            self._width = None
        else:
            self._width = width

        if BrowserInfo.get().isIE6():
            # Required in IE when textfield is wider than this.width
            self.getElement().getStyle().setOverflow('hidden')#Overflow.HIDDEN)
            self._horizPaddingAndBorder = Util.setWidthExcludingPaddingAndBorder(self, width, self._horizPaddingAndBorder)
            self.getElement().getStyle().setProperty('overflow', '')
        else:
            self._horizPaddingAndBorder = Util.setWidthExcludingPaddingAndBorder(self, width, self._horizPaddingAndBorder)

        if self._initDone:
            self.updateRootWidth()


    def setHeight(self, height):
        super(VFilterSelect, self).setHeight(height)
        Util.setHeightExcludingPaddingAndBorder(self.tb, height, 3)


    def updateRootWidth(self):
        """Calculates the width of the select if the select has undefined width.
        Should be called when the width changes or when the icon changes.
        """
        if self._width is None:
            # When the width is not specified we must specify width for root
            # div so the popupopener won't wrap to the next line and also so
            # the size of the combobox won't change over time.
            tbWidth = Util.getRequiredWidth(self.tb)

            if self._popupWidth < 0:
                # Only use the first page popup width so the textbox will not
                # get resized whenever the popup is resized.
                self._popupWidth = Util.getRequiredWidth(self.popupOpener)

            # Note: iconWidth is here calculated as a negative pixel value so
            # you should consider this in further calculations.
            iconWidth = Util.measureMarginLeft(self.tb.getElement()) - Util.measureMarginLeft(self._selectedItemIcon.getElement()) if self._selectedItemIcon.isAttached() else 0

            w = tbWidth + self._popupWidth + iconWidth

            # When the select has a undefined with we need to check that we are
            # only setting the text box width relative to the first page width
            # of the items. If this is not done the text box width will change
            # when the popup is used to view longer items than the text box is
            # wide.

            if ((not self._initDone) or (self._currentPage + 1 < 0)
                    and self._suggestionPopupMinWidth > w):
                self.setTextboxWidth(self._suggestionPopupMinWidth)
                w = self._suggestionPopupMinWidth
            else:
                # Firefox3 has its own way of doing rendering so we need to
                # specify the width for the TextField to make sure it actually
                # is rendered as wide as FF3 says it is
                self.tb.setWidth((tbWidth - self.getTextboxPadding()) + 'px')

            super(VFilterSelect, self).setWidth(w + 'px')
            # Freeze the initial width, so that it won't change even if the
            # icon size changes
            self._width = w + 'px'
        else:
            # When the width is specified we also want to explicitly specify
            # widths for textbox and popupopener
            self.setTextboxWidth(self.getMainWidth()
                    - self.getComponentPadding())


    def getMainWidth(self):
        """Get the width of the select in pixels where the text area and icon
        has been included.

        @return: The width in pixels
        """
        if BrowserInfo.get().isIE6():
            # Required in IE when textfield is wider than this.width
            self.getElement().getStyle().setOverflow('hidden')#Overflow.HIDDEN)
            componentWidth = self.getOffsetWidth()
            self.getElement().getStyle().setProperty('overflow', '')
        else:
            componentWidth = self.getOffsetWidth()

        return componentWidth


    def setTextboxWidth(self, componentWidth):
        """Sets the text box width in pixels.

        @param componentWidth:
                   The width of the text box in pixels
        """
        padding = self.getTextboxPadding()
        popupOpenerWidth = Util.getRequiredWidth(self.popupOpener)
        iconWidth = Util.getRequiredWidth(self._selectedItemIcon) if self._selectedItemIcon.isAttached() else 0
        textboxWidth = componentWidth - padding - popupOpenerWidth - iconWidth
        if textboxWidth < 0:
            textboxWidth = 0
        self.tb.setWidth(textboxWidth + 'px')


    def getTextboxPadding(self):
        """Gets the horizontal padding of the text box in pixels. The
        measurement includes the border width.

        @return: The padding in pixels
        """
        if self._textboxPadding < 0:
            self._textboxPadding = Util.measureHorizontalPaddingAndBorder(self.tb.getElement(), 4)
        return self._textboxPadding


    def getComponentPadding(self):
        """Gets the horizontal padding of the select. The measurement includes
        the border width.

        @return: The padding in pixels
        """
        if self._componentPadding < 0:
            self._componentPadding = Util.measureHorizontalPaddingAndBorder(self.getElement(), 3)
        return self._componentPadding


    def handleMouseDownEvent(self, event):
        """Handles special behavior of the mouse down event
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
            if BrowserInfo.get().isIE() and self._focused:
                self._preventNextBlurEventInIE = True


    def onDetach(self):
        super(VFilterSelect, self).onDetach()
        self.suggestionPopup.hide()


class FilterSelectSuggestion(Suggestion, Command):
    """Represents a suggestion in the suggestion popup box"""

    def __init__(self, uidl, select):
        """Constructor

        @param uidl:
                   The UIDL recieved from the server
        """
        self._select = select

        self._key = None
        self._caption = None
        self._iconUri = None

        self._key = uidl.getStringAttribute('key')
        self._caption = uidl.getStringAttribute('caption')
        if uidl.hasAttribute('icon'):
            self._iconUri = self._select._client.translateVaadinUri(
                    uidl.getStringAttribute('icon'))


    def getDisplayString(self):
        """Gets the visible row in the popup as a HTML string. The string
        contains an image tag with the rows icon (if an icon has been
        specified) and the caption of the item
        """
        sb = str()
        if self._iconUri is not None:
            sb += '<img src=\"'
            sb += Util.escapeAttribute(self._iconUri)
            sb += '\" alt=\"\" class=\"v-icon\" />'
        sb += '<span>' + Util.escapeHTML(self._caption) + '</span>'
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



class SuggestionPopup(VOverlay):#, PositionCallback, CloseHandler):
    """Represents the popup box with the selection options. Wraps a
    suggestion menu.
    """

    _Z_INDEX = '30000'

    def __init__(self, select):
        """Default constructor"""
        self._select = select

        self._menu = None
        self._up = DOM.createDiv()
        self._down = DOM.createDiv()
        self._status = DOM.createDiv()
        self._isPagingEnabled = True
        self._lastAutoClosed = None
        self._popupOuterPadding = -1
        self._topPosition = None

        super(SuggestionPopup, self)(True, False, True)

        self._menu = SuggestionMenu()
        self.setWidget(self._menu)
        self.setStyleName(self._select._CLASSNAME + '-suggestpopup')
        DOM.setStyleAttribute(self.getElement(), 'zIndex', self._Z_INDEX)
        root = self.getContainerElement()
        DOM.setInnerHTML(self._up, '<span>Prev</span>')
        DOM.sinkEvents(self._up, Event.ONCLICK)
        DOM.setInnerHTML(self._down, '<span>Next</span>')
        DOM.sinkEvents(self._down, Event.ONCLICK)
        DOM.insertChild(root, self._up, 0)
        DOM.appendChild(root, self._down)
        DOM.appendChild(root, self._status)
        DOM.setElementProperty(self._status, 'className',
                self._select._CLASSNAME + '-status')
        DOM.sinkEvents(root, Event.ONMOUSEDOWN | Event.ONMOUSEWHEEL)
        self.addCloseHandler(self)


    def showSuggestions(self, currentSuggestions, currentPage,
                totalSuggestions):
        """Shows the popup where the user can see the filtered options

        @param currentSuggestions:
                   The filtered suggestions
        @param currentPage:
                   The current page number
        @param totalSuggestions:
                   The total amount of suggestions
        """
        # Add TT anchor point
        DOM.setElementProperty(self.getElement(), 'id',
                'VAADIN_COMBOBOX_OPTIONLIST')
        self._menu.setSuggestions(currentSuggestions)
        x = self._select.getAbsoluteLeft()
        self._topPosition = self.tb.getAbsoluteTop()
        self._topPosition += self.tb.getOffsetHeight()
        self.setPopupPosition(x, self._topPosition)
        nullOffset = 1 if self._select._nullSelectionAllowed and '' == self._select._lastFilter else 0
        firstPage = currentPage == 0
        first = ((currentPage * self._select.pageLength) + 1) - (0 if firstPage else nullOffset)
        last = (first + len(currentSuggestions)) - 1 - (nullOffset if firstPage and '' == self._select._lastFilter else 0)
        matches = totalSuggestions - nullOffset
        if last > 0:
            # nullsel not counted, as requested by user
            DOM.setInnerText(self._status, (0 if matches == 0 else first) + '-' + last + '/' + matches)
        else:
            DOM.setInnerText(self._status, '')
        # We don't need to show arrows or statusbar if there is only one
        # page
        if ((totalSuggestions <= self._select.pageLength)
                or (self._select.pageLength == 0)):
            self.setPagingEnabled(False)
        else:
            self.setPagingEnabled(True)

        self.setPrevButtonActive(first > 1)
        self.setNextButtonActive(last < matches)

        # clear previously fixed width
        self._menu.setWidth('')
        DOM.setStyleAttribute(DOM.getFirstChild(self._menu.getElement()),
                'width', '')
        self.setPopupPositionAndShow(self)


    def setNextButtonActive(self, active):
        """Should the next page button be visible to the user?
        """
        if active:
            DOM.sinkEvents(self._down, Event.ONCLICK)
            DOM.setElemAttribute(self._down, 'className',
                    self._select._CLASSNAME + '-nextpage')
        else:
            DOM.sinkEvents(self._down, 0)
            DOM.setElemAttribute(self._down, 'className',
                    self._select._CLASSNAME + '-nextpage-off')


    def setPrevButtonActive(self, active):
        """Should the previous page button be visible to the user
        """
        if active:
            DOM.sinkEvents(self._up, Event.ONCLICK)
            DOM.setElemAttribute(self._up, 'className',
                    self._select._CLASSNAME + '-prevpage')
        else:
            DOM.sinkEvents(self._up, 0)
            DOM.setElemAttribute(self._up, 'className',
                    self._select._CLASSNAME + '-prevpage-off')


    def selectNextItem(self):
        """Selects the next item in the filtered selections"""
        cur = self._menu.getSelectedItem()
        index = 1 + self._menu.getItems().index(cur)
        if len(self._menu.getItems()) > index:
            newSelectedItem = self._menu.getItems().get(index)
            self._menu.selectItem(newSelectedItem)
            self.tb.setText(newSelectedItem.getText())
            self.tb.setSelectionRange(len(self._select._lastFilter),
                len(newSelectedItem.getText()) - len(self._select._lastFilter))
        elif self._select.hasNextPage():
            self._select._lastIndex = index - 1
            # save for paging
            self.filterOptions(self._select._currentPage + 1,
                    self._select._lastFilter)


    def selectPrevItem(self):
        """Selects the previous item in the filtered selections"""

        cur = self._menu.getSelectedItem()
        index = -1 + self._menu.getItems().index(cur)
        if index > -1:
            newSelectedItem = self._menu.getItems().get(index)
            self._menu.selectItem(newSelectedItem)
            self.tb.setText(newSelectedItem.getText())
            self.tb.setSelectionRange(len(self._select._lastFilter),
                len(newSelectedItem.getText()) - len(self._select._lastFilter))
        elif index == -1:
            if self._select._currentPage > 0:
                self._select._lastIndex = index + 1
                # save for paging
                self.filterOptions(self._select._currentPage - 1,
                        self._select._lastFilter)
        else:
            newSelectedItem = \
                    self._menu.getItems().get(len(self._menu.getItems()) - 1)
            self._menu.selectItem(newSelectedItem)
            self.tb.setText(newSelectedItem.getText())
            self.tb.setSelectionRange(len(self._select._lastFilter),
                len(newSelectedItem.getText()) - len(self._select._lastFilter))


    # Using a timer to scroll up or down the pages so when we receive lots
    # of consecutive mouse wheel events the pages does not flicker.
    _lazyPageScroller = LazyPageScroller()


    class LazyPageScroller(Timer):

        def __init__(self, select):
            self._select = select
            self._pagesToScroll = 0

        def run(self):
            if self._pagesToScroll != 0:
                self.filterOptions(self._select._currentPage + self._pagesToScroll,
                        self._select._lastFilter)
                self._pagesToScroll = 0

        def scrollUp(self):
            if self._select._currentPage + self._pagesToScroll > 0:
                self._pagesToScroll -= 1
                self.cancel()
                self.schedule(100)

        def scrollDown(self):
            if (self._select._totalMatches > (self._select._currentPage
                        + self._pagesToScroll + 1) * self._select.pageLength):
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
        if self._select._currentPage > 0:
            # fix height to avoid height change when getting to last page
            self._menu.fixHeightTo(self._select.pageLength)

        offsetHeight = self.getOffsetHeight()
        desiredWidth = self.getMainWidth()

        naturalMenuWidth = DOM.getIntElemAttribute(
                DOM.getFirstChild(self._menu.getElement()), 'offsetWidth')

        if self._popupOuterPadding == -1:
            self._popupOuterPadding = Util.measureHorizontalPaddingAndBorder(
                    self.getElement(), 2)

        if naturalMenuWidth < desiredWidth:
            self._menu.setWidth((desiredWidth - self._popupOuterPadding) + 'px')
            DOM.setStyleAttribute(DOM.getFirstChild(self._menu.getElement()),
                    'width', '100%')
            naturalMenuWidth = desiredWidth

        if BrowserInfo.get().isIE():
            # IE requires us to specify the width for the container
            # element. Otherwise it will be 100% wide
            rootWidth = naturalMenuWidth - self._popupOuterPadding
            DOM.setStyleAttribute(self.getContainerElement(), 'width',
                    rootWidth + 'px')

        if (offsetHeight + self.getPopupTop() > Window.getClientHeight()
                + Window.getScrollTop()):
            # popup on top of input instead
            top = self.getPopupTop() - offsetHeight - self._select.getOffsetHeight()
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
        offsetWidth = DOM.getIntElemAttribute(DOM.getFirstChild(
                self._menu.getElement()), 'offsetWidth')
        if (offsetWidth + self.getPopupLeft() > Window.getClientWidth()
                + Window.getScrollLeft()):
            left = (self._select.getAbsoluteLeft()
                    + self._select.getOffsetWidth()
                    + Window.getScrollLeft()) - offsetWidth
            if left < 0:
                left = 0
        else:
            left = self.getPopupLeft()
        self.setPopupPosition(left, top)


    def isJustClosed(self):
        """Was the popup just closed?

        @return: true if popup was just closed
        """
        now = Date().getTime()
        return self._lastAutoClosed > 0 and now - self._lastAutoClosed < 200


    def onClose(self, event):
        if event.isAutoClosed():
            self._lastAutoClosed = Date().getTime()


    def updateStyleNames(self, uidl):
        """Updates style names in suggestion popup to help theme building."""
        if uidl.hasAttribute('style'):
            self.setStyleName(self._select._CLASSNAME + '-suggestpopup')
            styles = uidl.getStringAttribute('style').split(' ')
            for style in styles:
                self.addStyleDependentName(style)



class SuggestionMenu(MenuBar, ISubPartAware):#, LoadHandler):
    """The menu where the suggestions are rendered"""

    class _0_(ScheduledCommand):

        def execute(self):
            if self.suggestionPopup.isVisible() and self.suggestionPopup.isAttached():
                self.setWidth('')
                DOM.setStyleAttribute(DOM.getFirstChild(self.getElement()), 'width', '')
                self.suggestionPopup.setPopupPositionAndShow(self.suggestionPopup)

    _0_ = _0_()

    _delayedImageLoadExecutioner = VLazyExecutor(100, _0_)

    def __init__(self, select):
        """Default constructor"""
        self._select = select
        super(SuggestionMenu, self)(True)
        self.setStyleName(self._select._CLASSNAME + '-suggestmenu')
        self.addDomHandler(self, LoadEvent.getType())

    def fixHeightTo(self, pagelenth):
        """Fixes menus height to use same space as full page would use. Needed
        to avoid height changes when quickly "scrolling" to last page
        """
        if len(self._select._currentSuggestions) > 0:
            pixels = (pagelenth * (self.getOffsetHeight() - 2)) / len(self._select._currentSuggestions)
            self.setHeight(pixels + 2 + 'px')


    def setSuggestions(self, suggestions):
        """Sets the suggestions rendered in the menu

        @param suggestions:
                   The suggestions to be rendered in the menu
        """
        self.clearItems()
        for s in suggestions:
            mi = MenuItem(s.getDisplayString(), True, s)
            Util.sinkOnloadForImages(mi.getElement())
            self.addItem(mi)
            if s == self._select._currentSuggestion:
                self.selectItem(mi)


    def doSelectedItemAction(self):
        """Send the current selection to the server. Triggered when a selection
        is made or on a blur event.
        """
        # do not send a value change event if null was and stays selected
        enteredItemValue = self.tb.getText()
        if (self._select._nullSelectionAllowed and '' == enteredItemValue
                and (self._select._selectedOptionKey is not None)
                and ('' != self._select._selectedOptionKey)):
            if self._select._nullSelectItem:
                self.reset()
                return
            # null is not visible on pages != 0, and not visible when
            # filtering: handle separately
            self._select._client.updateVariable(self._select._paintableId,
                    'filter', '', False)
            self._select._client.updateVariable(self._select._paintableId,
                    'page', 0, False)
            self._select._client.updateVariable(self._select._paintableId,
                    'selected', [], self._select._immediate)
            self.suggestionPopup.hide()
            return

        self._select._selecting = self._select._filtering

        if not self._select._filtering:
            self.doPostFilterSelectedItemAction()


    def doPostFilterSelectedItemAction(self):
        """Triggered after a selection has been made"""
        item = self.getSelectedItem()
        enteredItemValue = self.tb.getText()
        self._select._selecting = False
        # check for exact match in menu
        p = len(self.getItems())
        if p > 0:
            for i in range(p):
                potentialExactMatch = self.getItems().get(i)
                if potentialExactMatch.getText() == enteredItemValue:
                    self.selectItem(potentialExactMatch)
                    # do not send a value change event if null was and
                    # stays selected
                    if (('' != enteredItemValue)
                            or (self._select._selectedOptionKey is not None
                                and ('' != self._select._selectedOptionKey))):
                        self.doItemAction(potentialExactMatch, True)
                    self.suggestionPopup.hide()
                    return

        if self._select._allowNewItem:
            if (not self._select._prompting
                    and (enteredItemValue != self._select._lastNewItemString)):
                # Store last sent new item string to avoid double sends
                self._select._lastNewItemString = enteredItemValue
                self._select._client.updateVariable(self._select._paintableId,
                        'newitem', enteredItemValue, self._select._immediate)
        elif (item is not None and ('' != self._select._lastFilter)
              and item.getText().toLowerCase().contains(self._select._lastFilter.toLowerCase()) if self._select._filteringmode == self._select.FILTERINGMODE_CONTAINS else item.getText().toLowerCase().startswith(self._select._lastFilter.toLowerCase())):
            self.doItemAction(item, True)
        elif (self._select._currentSuggestion is not None
              and (self._select._currentSuggestion.key != '')):
            # An item (not null) selected
            text = self._select._currentSuggestion.getReplacementString()
            self.tb.setText(text)
            self._select._selectedOptionKey = self._select._currentSuggestion.key
        else:
            # Null selected
            self.tb.setText('')
            self._select._selectedOptionKey = None

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
        while (menuItemRoot is not None
                and not menuItemRoot.getTagName().equalsIgnoreCase('td')):
            menuItemRoot = menuItemRoot.getParentElement()

        # "menuItemRoot" is now the root of the menu item
        itemCount = len(self.getItems())
        for i in range(itemCount):
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
