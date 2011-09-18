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
from com.vaadin.terminal.gwt.client.ui.VDateField import (VDateField,)
from com.vaadin.terminal.gwt.client.ui.SubPartAware import (SubPartAware,)
from com.vaadin.terminal.gwt.client.DateTimeService import (DateTimeService,)
from com.vaadin.terminal.gwt.client.ui.VCalendarPanel import (VCalendarPanel,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.Field import (Field,)
from com.vaadin.terminal.gwt.client.ui.VTextualDate import (VTextualDate,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
# from java.util.Date import (Date,)


class VPopupCalendar(VTextualDate, Paintable, Field, ClickHandler, CloseHandler, SubPartAware):
    """Represents a date selection component with a text field and a popup date
    selector.

    <b>Note:</b> To change the keyboard assignments used in the popup dialog you
    should extend <code>com.vaadin.terminal.gwt.client.ui.VCalendarPanel</code>
    and then pass set it by calling the
    <code>setCalendarPanel(VCalendarPanel panel)</code> method.
    """
    _calendarToggle = None
    _calendar = None
    _popup = None
    _open = False
    _parsable = True

    def __init__(self):
        super(VPopupCalendar, self)()
        self._calendarToggle = self.Button()
        self._calendarToggle.setStyleName(self.CLASSNAME + '-button')
        self._calendarToggle.setText('')
        self._calendarToggle.addClickHandler(self)
        self._calendarToggle.getElement().setTabIndex(-1)
        self.add(self._calendarToggle)
        self._calendar = self.GWT.create(VCalendarPanel)

        class _1_(FocusOutListener):

            def onFocusOut(self, event):
                event.preventDefault()
                self.closeCalendarPanel()
                return True

        _1_ = self._1_()
        self._calendar.setFocusOutListener(_1_)

        class _2_(SubmitListener):

            def onSubmit(self):
                # Update internal value and send valuechange event if immediate
                self.updateValue(self.calendar.getDate())
                # Update text field (a must when not immediate).
                self.buildDate(True)
                self.closeCalendarPanel()

            def onCancel(self):
                self.closeCalendarPanel()

        _2_ = self._2_()
        self._calendar.setSubmitListener(_2_)
        self._popup = VOverlay(True, True, True)
        self._popup.setStyleName(VDateField.CLASSNAME + '-popup')
        self._popup.setWidget(self._calendar)
        self._popup.addCloseHandler(self)
        self.DOM.setElementProperty(self._calendar.getElement(), 'id', 'PID_VAADIN_POPUPCAL')
        self.sinkEvents(self.Event.ONKEYDOWN)

    def updateValue(self, newDate):
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.terminal.gwt.client.ui.VTextualDate#updateFromUIDL(com.vaadin
        # .terminal.gwt.client.UIDL,
        # com.vaadin.terminal.gwt.client.ApplicationConnection)

        currentDate = self.getCurrentDate()
        if (currentDate is None) or (newDate.getTime() != currentDate.getTime()):
            self.setCurrentDate(newDate.clone())
            self.getClient().updateVariable(self.getId(), 'year', newDate.getYear() + 1900, False)
            if self.getCurrentResolution() > VDateField.RESOLUTION_YEAR:
                self.getClient().updateVariable(self.getId(), 'month', newDate.getMonth() + 1, False)
                if self.getCurrentResolution() > self.RESOLUTION_MONTH:
                    self.getClient().updateVariable(self.getId(), 'day', newDate.getDate(), False)
                    if self.getCurrentResolution() > self.RESOLUTION_DAY:
                        self.getClient().updateVariable(self.getId(), 'hour', newDate.getHours(), False)
                        if self.getCurrentResolution() > self.RESOLUTION_HOUR:
                            self.getClient().updateVariable(self.getId(), 'min', newDate.getMinutes(), False)
                            if self.getCurrentResolution() > self.RESOLUTION_MIN:
                                self.getClient().updateVariable(self.getId(), 'sec', newDate.getSeconds(), False)
                                if self.getCurrentResolution() == self.RESOLUTION_MSEC:
                                    self.getClient().updateVariable(self.getId(), 'msec', DateTimeService.getMilliseconds(newDate), False)
            if self.isImmediate():
                self.getClient().sendPendingVariableChanges()

    def updateFromUIDL(self, uidl, client):
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.user.client.ui.UIObject#setStyleName(java.lang.String)

        lastReadOnlyState = self.readonly
        self._parsable = uidl.getBooleanAttribute('parsable')
        super(VPopupCalendar, self).updateFromUIDL(uidl, client)
        self._popup.setStyleName(VDateField.CLASSNAME + '-popup ' + VDateField.CLASSNAME + '-' + self.resolutionToString(self.currentResolution))
        self._calendar.setDateTimeService(self.getDateTimeService())
        self._calendar.setShowISOWeekNumbers(self.isShowISOWeekNumbers())
        if self._calendar.getResolution() != self.currentResolution:
            self._calendar.setResolution(self.currentResolution)
            if self._calendar.getDate() is not None:
                self._calendar.setDate(self.getCurrentDate().clone())
                # force re-render when changing resolution only
                self._calendar.renderCalendar()
        self._calendarToggle.setEnabled(self.enabled)
        if self.currentResolution <= self.RESOLUTION_MONTH:

            class _3_(FocusChangeListener):

                def focusChanged(self, date):
                    self.updateValue(date)
                    self.buildDate()
                    date2 = self.calendar.getDate()
                    date2.setYear(date.getYear())
                    date2.setMonth(date.getMonth())

            _3_ = self._3_()
            self._calendar.setFocusChangeListener(_3_)
        else:
            self._calendar.setFocusChangeListener(None)
        if self.currentResolution > self.RESOLUTION_DAY:

            class _4_(TimeChangeListener):

                def changed(self, hour, min, sec, msec):
                    d = self.getDate()
                    if d is None:
                        # date currently null, use the value from calendarPanel
                        # (~ client time at the init of the widget)
                        d = self.calendar.getDate().clone()
                    d.setHours(hour)
                    d.setMinutes(min)
                    d.setSeconds(sec)
                    DateTimeService.setMilliseconds(d, msec)
                    # Always update time changes to the server
                    self.updateValue(d)
                    # Update text field
                    self.buildDate()

            _4_ = self._4_()
            self._calendar.setTimeChangeListener(_4_)
        if self.readonly:
            self._calendarToggle.addStyleName(self.CLASSNAME + '-button-readonly')
        else:
            self._calendarToggle.removeStyleName(self.CLASSNAME + '-button-readonly')
        if lastReadOnlyState != self.readonly:
            self.updateWidth()
        self._calendarToggle.setEnabled(True)

    def setStyleName(self, style):
        # make sure the style is there before size calculation
        super(VPopupCalendar, self).setStyleName(style + ' ' + self.CLASSNAME + '-popupcalendar')

    def openCalendarPanel(self):
        """Opens the calendar panel popup"""
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.dom.client.ClickHandler#onClick(com.google.gwt.event
        # .dom.client.ClickEvent)

        if not self._open and not self.readonly:
            self._open = True
            if self.getCurrentDate() is not None:
                self._calendar.setDate(self.getCurrentDate().clone())
            else:
                self._calendar.setDate(Date())
            # clear previous values
            self._popup.setWidth('')
            self._popup.setHeight('')

            class _6_(PositionCallback):

                def setPosition(self, offsetWidth, offsetHeight):
                    w = offsetWidth
                    h = offsetHeight
                    browserWindowWidth = self.Window.getClientWidth() + self.Window.getScrollLeft()
                    browserWindowHeight = self.Window.getClientHeight() + self.Window.getScrollTop()
                    t = self.calendarToggle.getAbsoluteTop()
                    l = self.calendarToggle.getAbsoluteLeft()
                    # Add a little extra space to the right to avoid
                    # problems with IE6/IE7 scrollbars and to make it look
                    # nicer.
                    extraSpace = 30
                    overflowRight = False
                    if l + (w + ) + extraSpace > browserWindowWidth:
                        overflowRight = True
                        # Part of the popup is outside the browser window
                        # (to the right)
                        l = browserWindowWidth - w - extraSpace
                    if t + h + self.calendarToggle.getOffsetHeight() + 30 > browserWindowHeight:
                        # Part of the popup is outside the browser window
                        # (below)
                        t = browserWindowHeight - h - self.calendarToggle.getOffsetHeight() - 30
                        if not overflowRight:
                            # Show to the right of the popup button unless we
                            # are in the lower right corner of the screen
                            l += self.calendarToggle.getOffsetWidth()
                    # fix size
                    self.popup.setWidth(w + 'px')
                    self.popup.setHeight(h + 'px')
                    self.popup.setPopupPosition(l, t + self.calendarToggle.getOffsetHeight() + 2)
                    # We have to wait a while before focusing since the popup
                    # needs to be opened before we can focus

                    class focusTimer(Timer):

                        def run(self):
                            self.setFocus(True)

                    self.focusTimer.schedule(100)

            _6_ = self._6_()
            self._popup.setPopupPositionAndShow(_6_)
        else:
            VConsole.error('Cannot reopen popup, it is already open!')

    def onClick(self, event):
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.logical.shared.CloseHandler#onClose(com.google.gwt
        # .event.logical.shared.CloseEvent)

        if event.getSource() == self._calendarToggle and self.isEnabled():
            self.openCalendarPanel()

    def onClose(self, event):
        if event.getSource() == self._popup:
            self.buildDate()
            if not BrowserInfo.get().isTouchDevice():
                # Move focus to textbox, unless on touch device (avoids opening
                # virtual keyboard).

                self.focus()
            # TODO resolve what the "Sigh." is all about and document it here
            # Sigh.

            class t(Timer):

                def run(self):
                    self.open = False

            self.t.schedule(100)

    def setFocus(self, focus):
        """Sets focus to Calendar panel.

        @param focus
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.terminal.gwt.client.ui.VTextualDate#getFieldExtraWidth()

        self._calendar.setFocus(focus)

    def getFieldExtraWidth(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.terminal.gwt.client.ui.VTextualDate#buildDate()

        if self.fieldExtraWidth < 0:
            self.fieldExtraWidth = super(VPopupCalendar, self).getFieldExtraWidth()
            self.fieldExtraWidth += self._calendarToggle.getOffsetWidth()
        return self.fieldExtraWidth

    def buildDate(self, *args):
        """None
        ---
        Update the text field contents from the date. See {@link #buildDate()}.

        @param forceValid
                   true to force the text field to be updated, false to only
                   update if the parsable flag is true.
        """
        # Save previous value
        _0 = args
        _1 = len(args)
        if _1 == 0:
            previousValue = self.getText()
            super(VPopupCalendar, self).buildDate()
            # Restore previous value if the input could not be parsed
            if not self._parsable:
                self.setText(previousValue)
        elif _1 == 1:
            forceValid, = _0
            if forceValid:
                self._parsable = True
            self.buildDate()
        else:
            raise ARGERROR(0, 1)

    # (non-Javadoc)
    # 
    # @see
    # com.vaadin.terminal.gwt.client.ui.VDateField#onBrowserEvent(com.google
    # .gwt.user.client.Event)

    def onBrowserEvent(self, event):
        super(VPopupCalendar, self).onBrowserEvent(event)
        if (
            self.DOM.eventGetType(event) == self.Event.ONKEYDOWN and event.getKeyCode() == self.getOpenCalenderPanelKey()
        ):
            self.openCalendarPanel()
            event.preventDefault()

    def getOpenCalenderPanelKey(self):
        """Get the key code that opens the calendar panel. By default it is the down
        key but you can override this to be whatever you like

        @return
        """
        return self.KeyCodes.KEY_DOWN

    def closeCalendarPanel(self):
        """Closes the open popup panel"""
        if self._open:
            self._popup.hide(True)

    _CALENDAR_TOGGLE_ID = 'popupButton'

    def getSubPartElement(self, subPart):
        if subPart == self._CALENDAR_TOGGLE_ID:
            return self._calendarToggle.getElement()
        return super(VPopupCalendar, self).getSubPartElement(subPart)

    def getSubPartName(self, subElement):
        if self._calendarToggle.getElement().isOrHasChild(subElement):
            return self._CALENDAR_TOGGLE_ID
        return super(VPopupCalendar, self).getSubPartName(subElement)
