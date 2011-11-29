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

from __pyjamas__ import (PREINC,)
from com.vaadin.terminal.gwt.client.ui.VLabel import (VLabel,)
from com.vaadin.terminal.gwt.client.DateTimeService import (DateTimeService,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.ui.VNativeSelect import (VNativeSelect,)
from com.vaadin.terminal.gwt.client.ui.FocusableFlexTable import (FocusableFlexTable,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.VDateField import (VDateField,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.SubPartAware import (SubPartAware,)
# from com.google.gwt.event.dom.client.MouseDownEvent import (MouseDownEvent,)
# from com.google.gwt.event.dom.client.MouseDownHandler import (MouseDownHandler,)
# from com.google.gwt.event.dom.client.MouseOutEvent import (MouseOutEvent,)
# from com.google.gwt.event.dom.client.MouseOutHandler import (MouseOutHandler,)
# from com.google.gwt.user.client.ui.InlineHTML import (InlineHTML,)
# from com.google.gwt.user.client.ui.ListBox import (ListBox,)
# from java.util.Date import (Date,)
# from java.util.Iterator import (Iterator,)


class VCalendarPanel(FocusableFlexTable, KeyDownHandler, KeyPressHandler, MouseOutHandler, MouseDownHandler, MouseUpHandler, BlurHandler, FocusHandler, SubPartAware):

    class SubmitListener(object):

        def onSubmit(self):
            """Called when calendar user triggers a submitting operation in calendar
            panel. Eg. clicking on day or hitting enter.
            """
            pass

        def onCancel(self):
            """On eg. ESC key."""
            pass

    class FocusOutListener(object):
        """Blur listener that listens to blur event from the panel"""

        def onFocusOut(self, event):
            """@return true if the calendar panel is not used after focus moves out"""
            pass

    class FocusChangeListener(object):
        """FocusChangeListener is notified when the panel changes its _focused_
        value. It can be set with
        """

        def focusChanged(self, focusedDate):
            pass

    class TimeChangeListener(object):
        """Dispatches an event when the panel when time is changed"""

        def changed(self, hour, min, sec, msec):
            pass

    class VEventButton(Button):
        """Represents a Date button in the calendar"""

        def __init__(self):
            self.addMouseDownHandler(VCalendarPanel_this)
            self.addMouseOutHandler(VCalendarPanel_this)
            self.addMouseUpHandler(VCalendarPanel_this)

    _CN_FOCUSED = 'focused'
    _CN_TODAY = 'today'
    _CN_SELECTED = 'selected'
    # Represents a click handler for when a user selects a value by using the
    # mouse

    # private ClickHandler dayClickHandler = new ClickHandler() {
    # /*
    # * (non-Javadoc)
    # *
    # * @see
    # * com.google.gwt.event.dom.client.ClickHandler#onClick(com.google.gwt
    # * .event.dom.client.ClickEvent)
    # */
    # public void onClick(ClickEvent event) {
    # Day day = (Day) event.getSource();
    # focusDay(day.getDay());
    # selectFocused();
    # onSubmit();
    # }
    # };
    _prevYear = None
    _nextYear = None
    _prevMonth = None
    _nextMonth = None
    _time = None
    _days = FlexTable()
    _resolution = VDateField.RESOLUTION_YEAR
    _focusedRow = None
    _mouseTimer = None
    _value = None
    _enabled = True
    _readonly = False
    _dateTimeService = None
    _showISOWeekNumbers = None
    _focusedDate = None
    _selectedDay = None
    _focusedDay = None
    _focusOutListener = None
    _submitListener = None
    _focusChangeListener = None
    _timeChangeListener = None
    _hasFocus = False

    def __init__(self):
        self.setStyleName(VDateField.CLASSNAME + '-calendarpanel')
        # Firefox auto-repeat works correctly only if we use a key press
        # handler, other browsers handle it correctly when using a key down
        # handler

        if BrowserInfo.get().isGecko():
            self.addKeyPressHandler(self)
        else:
            self.addKeyDownHandler(self)
        self.addFocusHandler(self)
        self.addBlurHandler(self)

    def focusDay(self, day):
        """Sets the focus to given day of current time. Used when moving in the
        calender with the keyboard.
             *
        @param day
                   The day number from by Date.getDate()
        """
        # Only used when calender body is present
        if self._resolution > VDateField.RESOLUTION_MONTH:
            if self._focusedDay is not None:
                self._focusedDay.removeStyleDependentName(self._CN_FOCUSED)
            if day > 0 and self._focusedDate is not None:
                self._focusedDate.setDate(day)
                rowCount = self._days.getRowCount()
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < rowCount):
                        break
                    cellCount = self._days.getCellCount(i)
                    _1 = True
                    j = 0
                    while True:
                        if _1 is True:
                            _1 = False
                        else:
                            j += 1
                        if not (j < cellCount):
                            break
                        widget = self._days.getWidget(i, j)
                        if widget is not None and isinstance(widget, self.Day):
                            curday = widget
                            if curday.getDay() == day:
                                curday.addStyleDependentName(self._CN_FOCUSED)
                                self._focusedDay = curday
                                self._focusedRow = i
                                return

    def selectDate(self, day):
        """Sets the selection hightlight to a given date of current time
             *
        @param day
        """
        if self._selectedDay is not None:
            self._selectedDay.removeStyleDependentName(self._CN_SELECTED)
        rowCount = self._days.getRowCount()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < rowCount):
                break
            cellCount = self._days.getCellCount(i)
            _1 = True
            j = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    j += 1
                if not (j < cellCount):
                    break
                widget = self._days.getWidget(i, j)
                if widget is not None and isinstance(widget, self.Day):
                    curday = widget
                    if curday.getDay() == day:
                        curday.addStyleDependentName(self._CN_SELECTED)
                        self._selectedDay = curday
                        return

    def selectFocused(self):
        """Updates year, month, day from focusedDate to value"""
        if self._focusedDate is not None:
            if self._value is None:
                # No previously selected value (set to null on server side).
                # Create a new date using current date and time
                self._value = Date()
            # #5594 set Date (day) to 1 in order to prevent any kind of
            # wrapping of months when later setting the month. (e.g. 31 ->
            # month with 30 days -> wraps to the 1st of the following month,
            # e.g. 31st of May -> 31st of April = 1st of May)

            self._value.setDate(1)
            if self._value.getYear() != self._focusedDate.getYear():
                self._value.setYear(self._focusedDate.getYear())
            if self._value.getMonth() != self._focusedDate.getMonth():
                self._value.setMonth(self._focusedDate.getMonth())
            if self._value.getDate() != self._focusedDate.getDate():
                pass
            # We always need to set the date, even if it hasn't changed, since
            # it was forced to 1 above.
            self._value.setDate(self._focusedDate.getDate())
            self.selectDate(self._focusedDate.getDate())
        else:
            VConsole.log('Trying to select a the focused date which is NULL!')

    def onValueChange(self):
        return False

    def getResolution(self):
        return self._resolution

    def setResolution(self, resolution):
        self._resolution = resolution
        if self._time is not None:
            self._time.removeFromParent()
            self._time = None

    def isReadonly(self):
        return self._readonly

    def isEnabled(self):
        return self._enabled

    def clearCalendarBody(self, remove):
        if not remove:
            # Leave the cells in place but clear their contents
            # This has the side effect of ensuring that the calendar always
            # contain 7 rows.
            _0 = True
            row = 1
            while True:
                if _0 is True:
                    _0 = False
                else:
                    row += 1
                if not (row < 7):
                    break
                _1 = True
                col = 0
                while True:
                    if _1 is True:
                        _1 = False
                    else:
                        col += 1
                    if not (col < 8):
                        break
                    self._days.setHTML(row, col, '&nbsp;')
        elif self.getRowCount() > 1:
            self.removeRow(1)
            self._days.clear()

    def buildCalendarHeader(self, needsMonth):
        """Builds the top buttons and current month and year header.
             *
        @param needsMonth
                   Should the month buttons be visible?
        """
        self.getRowFormatter().addStyleName(0, VDateField.CLASSNAME + '-calendarpanel-header')
        if self._prevMonth is None and needsMonth:
            self._prevMonth = self.VEventButton()
            self._prevMonth.setHTML('&lsaquo;')
            self._prevMonth.setStyleName('v-button-prevmonth')
            self._prevMonth.setTabIndex(-1)
            self._nextMonth = self.VEventButton()
            self._nextMonth.setHTML('&rsaquo;')
            self._nextMonth.setStyleName('v-button-nextmonth')
            self._nextMonth.setTabIndex(-1)
            self.getFlexCellFormatter().setStyleName(0, 3, VDateField.CLASSNAME + '-calendarpanel-nextmonth')
            self.getFlexCellFormatter().setStyleName(0, 1, VDateField.CLASSNAME + '-calendarpanel-prevmonth')
            self.setWidget(0, 3, self._nextMonth)
            self.setWidget(0, 1, self._prevMonth)
        elif self._prevMonth is not None and not needsMonth:
            # Remove month traverse buttons
            self.remove(self._prevMonth)
            self.remove(self._nextMonth)
            self._prevMonth = None
            self._nextMonth = None
        if self._prevYear is None:
            self._prevYear = self.VEventButton()
            self._prevYear.setHTML('&laquo;')
            self._prevYear.setStyleName('v-button-prevyear')
            self._prevYear.setTabIndex(-1)
            self._nextYear = self.VEventButton()
            self._nextYear.setHTML('&raquo;')
            self._nextYear.setStyleName('v-button-nextyear')
            self._nextYear.setTabIndex(-1)
            self.setWidget(0, 0, self._prevYear)
            self.setWidget(0, 4, self._nextYear)
            self.getFlexCellFormatter().setStyleName(0, 0, VDateField.CLASSNAME + '-calendarpanel-prevyear')
            self.getFlexCellFormatter().setStyleName(0, 4, VDateField.CLASSNAME + '-calendarpanel-nextyear')
        monthName = self.getDateTimeService().getMonth(self._focusedDate.getMonth()) if needsMonth else ''
        year = self._focusedDate.getYear() + 1900
        self.getFlexCellFormatter().setStyleName(0, 2, VDateField.CLASSNAME + '-calendarpanel-month')
        self.setHTML(0, 2, '<span class=\"' + VDateField.CLASSNAME + '-calendarpanel-month\">' + monthName + ' ' + year + '</span>')

    def getDateTimeService(self):
        return self._dateTimeService

    def setDateTimeService(self, dateTimeService):
        self._dateTimeService = dateTimeService

    def isShowISOWeekNumbers(self):
        """Returns whether ISO 8601 week numbers should be shown in the value
        selector or not. ISO 8601 defines that a week always starts with a Monday
        so the week numbers are only shown if this is the case.
             *
        @return true if week number should be shown, false otherwise
        """
        return self._showISOWeekNumbers

    def setShowISOWeekNumbers(self, showISOWeekNumbers):
        self._showISOWeekNumbers = showISOWeekNumbers

    def buildCalendarBody(self):
        """Builds the day and time selectors of the calendar."""
        weekColumn = 0
        firstWeekdayColumn = 1
        headerRow = 0
        self.setWidget(1, 0, self._days)
        self.setCellPadding(0)
        self.setCellSpacing(0)
        self.getFlexCellFormatter().setColSpan(1, 0, 5)
        self.getFlexCellFormatter().setStyleName(1, 0, VDateField.CLASSNAME + '-calendarpanel-body')
        self._days.getFlexCellFormatter().setStyleName(headerRow, weekColumn, 'v-week')
        self._days.setHTML(headerRow, weekColumn, '<strong></strong>')
        # Hide the week column if week numbers are not to be displayed.
        self._days.getFlexCellFormatter().setVisible(headerRow, weekColumn, self.isShowISOWeekNumbers())
        self._days.getRowFormatter().setStyleName(headerRow, VDateField.CLASSNAME + '-calendarpanel-weekdays')
        if self.isShowISOWeekNumbers():
            self._days.getFlexCellFormatter().setStyleName(headerRow, weekColumn, 'v-first')
            self._days.getFlexCellFormatter().setStyleName(headerRow, firstWeekdayColumn, '')
            self._days.getRowFormatter().addStyleName(headerRow, VDateField.CLASSNAME + '-calendarpanel-weeknumbers')
        else:
            self._days.getFlexCellFormatter().setStyleName(headerRow, weekColumn, '')
            self._days.getFlexCellFormatter().setStyleName(headerRow, firstWeekdayColumn, 'v-first')
        self._days.getFlexCellFormatter().setStyleName(headerRow, firstWeekdayColumn + 6, 'v-last')
        # Print weekday names
        firstDay = self.getDateTimeService().getFirstDayOfWeek()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 7):
                break
            day = i + firstDay
            if day > 6:
                day = 0
            if self.getResolution() > VDateField.RESOLUTION_MONTH:
                self._days.setHTML(headerRow, firstWeekdayColumn + i, '<strong>' + self.getDateTimeService().getShortDay(day) + '</strong>')
            else:
                self._days.setHTML(headerRow, firstWeekdayColumn + i, '')
        # The day of month that is selected, -1 if no day of this month is
        # selected (i.e, showing another month/year than selected or nothing is
        # selected)
        dayOfMonthSelected = -1
        # The day of month that is today, -1 if no day of this month is today
        # (i.e., showing another month/year than current)
        dayOfMonthToday = -1
        initiallyNull = self._value is None
        if (
            not initiallyNull and self._value.getMonth() == self._focusedDate.getMonth() and self._value.getYear() == self._focusedDate.getYear()
        ):
            dayOfMonthSelected = self._value.getDate()
        today = Date()
        if (
            today.getMonth() == self._focusedDate.getMonth() and today.getYear() == self._focusedDate.getYear()
        ):
            dayOfMonthToday = today.getDate()
        startWeekDay = self.getDateTimeService().getStartWeekDay(self._focusedDate)
        daysInMonth = DateTimeService.getNumberOfDaysInMonth(self._focusedDate)
        dayCount = 0
        curr = Date(self._focusedDate.getTime())
        # No month has more than 6 weeks so 6 is a safe maximum for rows.
        _1 = True
        weekOfMonth = 1
        while True:
            if _1 is True:
                _1 = False
            else:
                weekOfMonth += 1
            if not (weekOfMonth < 7):
                break
            weekNumberProcessed = [False, False, False, False, False, False, False]
            _2 = True
            dayOfWeek = 0
            while True:
                if _2 is True:
                    _2 = False
                else:
                    dayOfWeek += 1
                if not (dayOfWeek < 7):
                    break
                if not (weekOfMonth == 1 and dayOfWeek < startWeekDay):
                    if dayCount >= daysInMonth:
                        # All days printed and we are done
                        break
                    dayOfMonth = PREINC(globals(), locals(), 'dayCount')
                    curr.setDate(dayCount)
                    # Actually write the day of month
                    day = self.Day(dayOfMonth)
                    if dayOfMonthSelected == dayOfMonth:
                        day.addStyleDependentName(self._CN_SELECTED)
                        self._selectedDay = day
                    if dayOfMonthToday == dayOfMonth:
                        day.addStyleDependentName(self._CN_TODAY)
                    if dayOfMonth == self._focusedDate.getDate():
                        self._focusedDay = day
                        self._focusedRow = weekOfMonth
                        if self._hasFocus:
                            day.addStyleDependentName(self._CN_FOCUSED)
                    self._days.setWidget(weekOfMonth, firstWeekdayColumn + dayOfWeek, day)
                    # ISO week numbers if requested
                    if not weekNumberProcessed[weekOfMonth]:
                        self._days.getCellFormatter().setVisible(weekOfMonth, weekColumn, self.isShowISOWeekNumbers())
                        if self.isShowISOWeekNumbers():
                            baseCssClass = VDateField.CLASSNAME + '-calendarpanel-weeknumber'
                            weekCssClass = baseCssClass
                            weekNumber = DateTimeService.getISOWeekNumber(curr)
                            self._days.setHTML(weekOfMonth, 0, '<span class=\"' + weekCssClass + '\"' + '>' + weekNumber + '</span>')
                            weekNumberProcessed[weekOfMonth] = True

    def isTimeSelectorNeeded(self):
        """Do we need the time selector
             *
        @return True if it is required
        """
        return self.getResolution() > VDateField.RESOLUTION_DAY

    def renderCalendar(self):
        """Updates the calendar and text field with the selected dates."""
        if self._focusedDate is None:
            self._focusedDate = Date()
        if (
            self.getResolution() <= VDateField.RESOLUTION_MONTH and self._focusChangeListener is not None
        ):
            self._focusChangeListener.focusChanged(Date(self._focusedDate.getTime()))
        needsMonth = self.getResolution() > VDateField.RESOLUTION_YEAR
        needsBody = self.getResolution() >= VDateField.RESOLUTION_DAY
        self.buildCalendarHeader(needsMonth)
        self.clearCalendarBody(not needsBody)
        if needsBody:
            self.buildCalendarBody()
        if self.isTimeSelectorNeeded() and self._time is None:
            self._time = self.VTime()
            self.setWidget(2, 0, self._time)
            self.getFlexCellFormatter().setColSpan(2, 0, 5)
            self.getFlexCellFormatter().setStyleName(2, 0, VDateField.CLASSNAME + '-calendarpanel-time')
        elif self.isTimeSelectorNeeded():
            self._time.updateTimes()
        elif self._time is not None:
            self.remove(self._time)

    def focusNextMonth(self):
        """Selects the next month"""
        currentMonth = self._focusedDate.getMonth()
        self._focusedDate.setMonth(currentMonth + 1)
        requestedMonth = (currentMonth + 1) % 12
        # If the selected value was e.g. 31.3 the new value would be 31.4 but
        # this value is invalid so the new value will be 1.5. This is taken
        # care of by decreasing the value until we have the correct month.

        while self._focusedDate.getMonth() != requestedMonth:
            self._focusedDate.setDate(self._focusedDate.getDate() - 1)
        self.renderCalendar()

    def focusPreviousMonth(self):
        """Selects the previous month"""
        currentMonth = self._focusedDate.getMonth()
        self._focusedDate.setMonth(currentMonth - 1)
        # If the selected value was e.g. 31.12 the new value would be 31.11 but
        # this value is invalid so the new value will be 1.12. This is taken
        # care of by decreasing the value until we have the correct month.

        while self._focusedDate.getMonth() == currentMonth:
            self._focusedDate.setDate(self._focusedDate.getDate() - 1)
        self.renderCalendar()

    def focusPreviousYear(self, years):
        """Selects the previous year"""
        self._focusedDate.setYear(self._focusedDate.getYear() - years)
        self.renderCalendar()

    def focusNextYear(self, years):
        """Selects the next year"""
        self._focusedDate.setYear(self._focusedDate.getYear() + years)
        self.renderCalendar()

    def processClickEvent(self, sender):
        """Handles a user click on the component
             *
        @param sender
                   The component that was clicked
        @param updateVariable
                   Should the value field be updated
             *
        """
        # (non-Javadoc)
        #      *
        # @see
        # com.google.gwt.event.dom.client.KeyDownHandler#onKeyDown(com.google.gwt
        # .event.dom.client.KeyDownEvent)

        if (not self.isEnabled()) or self.isReadonly():
            return
        if sender == self._prevYear:
            self.focusPreviousYear(1)
        elif sender == self._nextYear:
            self.focusNextYear(1)
        elif sender == self._prevMonth:
            self.focusPreviousMonth()
        elif sender == self._nextMonth:
            self.focusNextMonth()

    def onKeyDown(self, event):
        # (non-Javadoc)
        #      *
        # @see
        # com.google.gwt.event.dom.client.KeyPressHandler#onKeyPress(com.google
        # .gwt.event.dom.client.KeyPressEvent)

        self.handleKeyPress(event)

    def onKeyPress(self, event):
        self.handleKeyPress(event)

    def handleKeyPress(self, event):
        """Handles the keypress from both the onKeyPress event and the onKeyDown
        event
             *
        @param event
                   The keydown/keypress event
        """
        if (
            self._time is not None and self._time.getElement().isOrHasChild(event.getNativeEvent().getEventTarget())
        ):
            nativeKeyCode = event.getNativeEvent().getKeyCode()
            if nativeKeyCode == self.getSelectKey():
                self.onSubmit()
                # submit happens if enter key hit down on listboxes
                event.preventDefault()
                event.stopPropagation()
            return
        # Check tabs
        keycode = event.getNativeEvent().getKeyCode()
        if keycode == KeyCodes.KEY_TAB and event.getNativeEvent().getShiftKey():
            if self.onTabOut(event):
                return
        # Handle the navigation
        if (
            self.handleNavigation(keycode, event.getNativeEvent().getCtrlKey() or event.getNativeEvent().getMetaKey(), event.getNativeEvent().getShiftKey())
        ):
            event.preventDefault()

    def onSubmit(self):
        """Notifies submit-listeners of a submit event"""
        if self.getSubmitListener() is not None:
            self.getSubmitListener().onSubmit()

    def onCancel(self):
        """Notifies submit-listeners of a cancel event"""
        if self.getSubmitListener() is not None:
            self.getSubmitListener().onCancel()

    def handleNavigationYearMode(self, keycode, ctrl, shift):
        """Handles the keyboard navigation when the resolution is set to years.
             *
        @param keycode
                   The keycode to process
        @param ctrl
                   Is ctrl pressed?
        @param shift
                   is shift pressed
        @return Returns true if the keycode was processed, else false
        """
        # Ctrl and Shift selection not supported
        if ctrl or shift:
            return False
        elif keycode == self.getPreviousKey():
            self.focusNextYear(10)
            # Add 10 years
            return True
        elif keycode == self.getForwardKey():
            self.focusNextYear(1)
            # Add 1 year
            return True
        elif keycode == self.getNextKey():
            self.focusPreviousYear(10)
            # Subtract 10 years
            return True
        elif keycode == self.getBackwardKey():
            self.focusPreviousYear(1)
            # Subtract 1 year
            return True
        elif keycode == self.getSelectKey():
            self._value = self._focusedDate.clone()
            self.onSubmit()
            return True
        elif keycode == self.getResetKey():
            # Restore showing value the selected value
            self._focusedDate.setTime(self._value.getTime())
            self.renderCalendar()
            return True
        elif keycode == self.getCloseKey():
            # TODO fire listener, on users responsibility??
            return True
        return False

    def handleNavigationMonthMode(self, keycode, ctrl, shift):
        """Handle the keyboard navigation when the resolution is set to MONTH
             *
        @param keycode
                   The keycode to handle
        @param ctrl
                   Was the ctrl key pressed?
        @param shift
                   Was the shift key pressed?
        @return
        """
        # Ctrl selection not supported
        if ctrl:
            return False
        elif keycode == self.getPreviousKey():
            self.focusNextYear(1)
            # Add 1 year
            return True
        elif keycode == self.getForwardKey():
            self.focusNextMonth()
            # Add 1 month
            return True
        elif keycode == self.getNextKey():
            self.focusPreviousYear(1)
            # Subtract 1 year
            return True
        elif keycode == self.getBackwardKey():
            self.focusPreviousMonth()
            # Subtract 1 month
            return True
        elif keycode == self.getSelectKey():
            self._value = self._focusedDate.clone()
            self.onSubmit()
            return True
        elif keycode == self.getResetKey():
            # Restore showing value the selected value
            self._focusedDate.setTime(self._value.getTime())
            self.renderCalendar()
            return True
        elif (keycode == self.getCloseKey()) or (keycode == KeyCodes.KEY_TAB):
            # TODO fire close event
            return True
        return False

    def handleNavigationDayMode(self, keycode, ctrl, shift):
        """Handle keyboard navigation what the resolution is set to DAY
             *
        @param keycode
                   The keycode to handle
        @param ctrl
                   Was the ctrl key pressed?
        @param shift
                   Was the shift key pressed?
        @return Return true if the key press was handled by the method, else
                return false.
        """
        # Ctrl key is not in use
        if ctrl:
            return False
        # Jumps to the next day.
        if keycode == self.getForwardKey() and not shift:
            # Calculate new showing value
            newCurrentDate = self._focusedDate.clone()
            newCurrentDate.setDate(newCurrentDate.getDate() + 1)
            if newCurrentDate.getMonth() == self._focusedDate.getMonth():
                # Month did not change, only move the selection
                self.focusDay(self._focusedDate.getDate() + 1)
            else:
                # If the month changed we need to re-render the calendar
                self._focusedDate.setDate(self._focusedDate.getDate() + 1)
                self.renderCalendar()
            return True
            # Jumps to the previous day
        elif keycode == self.getBackwardKey() and not shift:
            # Calculate new showing value
            newCurrentDate = self._focusedDate.clone()
            newCurrentDate.setDate(newCurrentDate.getDate() - 1)
            if newCurrentDate.getMonth() == self._focusedDate.getMonth():
                # Month did not change, only move the selection
                self.focusDay(self._focusedDate.getDate() - 1)
            else:
                # If the month changed we need to re-render the calendar
                self._focusedDate.setDate(self._focusedDate.getDate() - 1)
                self.renderCalendar()
            return True
            # Jumps one week back in the calendar
        elif keycode == self.getPreviousKey() and not shift:
            # Calculate new showing value
            newCurrentDate = self._focusedDate.clone()
            newCurrentDate.setDate(newCurrentDate.getDate() - 7)
            if (
                newCurrentDate.getMonth() == self._focusedDate.getMonth() and self._focusedRow > 1
            ):
                # Month did not change, only move the selection
                self.focusDay(self._focusedDate.getDate() - 7)
            else:
                # If the month changed we need to re-render the calendar
                self._focusedDate.setDate(self._focusedDate.getDate() - 7)
                self.renderCalendar()
            return True
            # Jumps one week forward in the calendar
        elif keycode == self.getNextKey() and not ctrl and not shift:
            # Calculate new showing value
            newCurrentDate = self._focusedDate.clone()
            newCurrentDate.setDate(newCurrentDate.getDate() + 7)
            if newCurrentDate.getMonth() == self._focusedDate.getMonth():
                # Month did not change, only move the selection
                self.focusDay(self._focusedDate.getDate() + 7)
            else:
                # If the month changed we need to re-render the calendar
                self._focusedDate.setDate(self._focusedDate.getDate() + 7)
                self.renderCalendar()
            return True
            # Selects the value that is chosen
        elif keycode == self.getSelectKey() and not shift:
            self.selectFocused()
            self.onSubmit()
            # submit
            return True
        elif keycode == self.getCloseKey():
            self.onCancel()
            # TODO close event
            return True
            # Jumps to the next month
        elif shift and keycode == self.getForwardKey():
            self.focusNextMonth()
            return True
            # Jumps to the previous month
        elif shift and keycode == self.getBackwardKey():
            self.focusPreviousMonth()
            return True
            # Jumps to the next year
        elif shift and keycode == self.getPreviousKey():
            self.focusNextYear(1)
            return True
            # Jumps to the previous year
        elif shift and keycode == self.getNextKey():
            self.focusPreviousYear(1)
            return True
            # Resets the selection
        elif keycode == self.getResetKey() and not shift:
            # Restore showing value the selected value
            self._focusedDate.setTime(self._value.getTime())
            self.renderCalendar()
            return True
        return False

    def handleNavigation(self, keycode, ctrl, shift):
        """Handles the keyboard navigation
             *
        @param keycode
                   The key code that was pressed
        @param ctrl
                   Was the ctrl key pressed
        @param shift
                   Was the shift key pressed
        @return Return true if key press was handled by the component, else
                return false
        """
        if (not self.isEnabled()) or self.isReadonly():
            return False
        elif self._resolution == VDateField.RESOLUTION_YEAR:
            return self.handleNavigationYearMode(keycode, ctrl, shift)
        elif self._resolution == VDateField.RESOLUTION_MONTH:
            return self.handleNavigationMonthMode(keycode, ctrl, shift)
        elif self._resolution == VDateField.RESOLUTION_DAY:
            return self.handleNavigationDayMode(keycode, ctrl, shift)
        else:
            return self.handleNavigationDayMode(keycode, ctrl, shift)

    def getResetKey(self):
        """Returns the reset key which will reset the calendar to the previous
        selection. By default this is backspace but it can be overriden to change
        the key to whatever you want.
             *
        @return
        """
        return KeyCodes.KEY_BACKSPACE

    def getSelectKey(self):
        """Returns the select key which selects the value. By default this is the
        enter key but it can be changed to whatever you like by overriding this
        method.
             *
        @return
        """
        return KeyCodes.KEY_ENTER

    def getCloseKey(self):
        """Returns the key that closes the popup window if this is a VPopopCalendar.
        Else this does nothing. By default this is the Escape key but you can
        change the key to whatever you want by overriding this method.
             *
        @return
        """
        return KeyCodes.KEY_ESCAPE

    def getForwardKey(self):
        """The key that selects the next day in the calendar. By default this is the
        right arrow key but by overriding this method it can be changed to
        whatever you like.
             *
        @return
        """
        return KeyCodes.KEY_RIGHT

    def getBackwardKey(self):
        """The key that selects the previous day in the calendar. By default this is
        the left arrow key but by overriding this method it can be changed to
        whatever you like.
             *
        @return
        """
        return KeyCodes.KEY_LEFT

    def getNextKey(self):
        """The key that selects the next week in the calendar. By default this is
        the down arrow key but by overriding this method it can be changed to
        whatever you like.
             *
        @return
        """
        return KeyCodes.KEY_DOWN

    def getPreviousKey(self):
        """The key that selects the previous week in the calendar. By default this
        is the up arrow key but by overriding this method it can be changed to
        whatever you like.
             *
        @return
        """
        # (non-Javadoc)
        #      *
        # @see
        # com.google.gwt.event.dom.client.MouseOutHandler#onMouseOut(com.google
        # .gwt.event.dom.client.MouseOutEvent)

        return KeyCodes.KEY_UP

    def onMouseOut(self, event):
        # (non-Javadoc)
        #      *
        # @see
        # com.google.gwt.event.dom.client.MouseDownHandler#onMouseDown(com.google
        # .gwt.event.dom.client.MouseDownEvent)

        if self._mouseTimer is not None:
            self._mouseTimer.cancel()

    def onMouseDown(self, event):
        # Allow user to click-n-hold for fast-forward or fast-rewind.
        # Timer is first used for a 500ms delay after mousedown. After that has
        # elapsed, another timer is triggered to go off every 150ms. Both
        # timers are cancelled on mouseup or mouseout.
        # (non-Javadoc)
        #      *
        # @see
        # com.google.gwt.event.dom.client.MouseUpHandler#onMouseUp(com.google.gwt
        # .event.dom.client.MouseUpEvent)

        if isinstance(event.getSource(), self.VEventButton):
            sender = event.getSource()
            self.processClickEvent(sender)

            class _1_(Timer):

                def run(self):

                    class _1_(Timer):

                        def run(self):
                            VCalendarPanel_this.processClickEvent(self.sender)

                    _1_ = _1_()
                    VCalendarPanel_this._mouseTimer = _1_
                    VCalendarPanel_this._mouseTimer.scheduleRepeating(150)

            _1_ = _1_()
            self._mouseTimer = _1_
            self._mouseTimer.schedule(500)

    def onMouseUp(self, event):
        if self._mouseTimer is not None:
            self._mouseTimer.cancel()

    def setDate(self, currentDate):
        """Sets the data of the Panel.
             *
        @param currentDate
                   The date to set
        """
        # Check that we are not re-rendering an already active date
        if currentDate == self._value and currentDate is not None:
            return
        oldFocusedValue = self._focusedDate
        self._value = currentDate
        if self._value is None:
            self._focusedDate = None
        else:
            self._focusedDate = self._value.clone()
        # Re-render calendar if month or year of focused date has changed
        if (
            (((oldFocusedValue is None) or (self._value is None)) or (oldFocusedValue.getYear() != self._value.getYear())) or (oldFocusedValue.getMonth() != self._value.getMonth())
        ):
            self.renderCalendar()
        else:
            self.focusDay(currentDate.getDate())
            self.selectFocused()
        if not self._hasFocus:
            self.focusDay(-1)

    def VTime(VCalendarPanel_this, *args, **kwargs):

        class VTime(FlowPanel, ChangeHandler):
            """TimeSelector is a widget consisting of list boxes that modifie the Date
            object that is given for.
                 *
            """
            _hours = None
            _mins = None
            _sec = None
            _msec = None
            _ampm = None

            def __init__(self):
                """Constructor"""
                super(VTime, self)()
                self.setStyleName(VDateField.CLASSNAME + '-time')
                self.buildTime()

            def createListBox(self):
                lb = ListBox()
                lb.setStyleName(VNativeSelect.CLASSNAME)
                lb.addChangeHandler(self)
                lb.addBlurHandler(VCalendarPanel_this)
                lb.addFocusHandler(VCalendarPanel_this)
                return lb

            def buildTime(self):
                """Constructs the ListBoxes and updates their value
                         *
                @param redraw
                           Should new instances of the listboxes be created
                """
                self.clear()
                self._hours = self.createListBox()
                if self.getDateTimeService().isTwelveHourClock():
                    self._hours.addItem('12')
                    _0 = True
                    i = 1
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            i += 1
                        if not (i < 12):
                            break
                        self._hours.addItem('0' + i if i < 10 else '' + i)
                else:
                    _1 = True
                    i = 0
                    while True:
                        if _1 is True:
                            _1 = False
                        else:
                            i += 1
                        if not (i < 24):
                            break
                        self._hours.addItem('0' + i if i < 10 else '' + i)
                self._hours.addChangeHandler(self)
                if self.getDateTimeService().isTwelveHourClock():
                    self._ampm = self.createListBox()
                    ampmText = self.getDateTimeService().getAmPmStrings()
                    self._ampm.addItem(ampmText[0])
                    self._ampm.addItem(ampmText[1])
                    self._ampm.addChangeHandler(self)
                if VCalendarPanel_this.getResolution() >= VDateField.RESOLUTION_MIN:
                    self._mins = self.createListBox()
                    _2 = True
                    i = 0
                    while True:
                        if _2 is True:
                            _2 = False
                        else:
                            i += 1
                        if not (i < 60):
                            break
                        self._mins.addItem('0' + i if i < 10 else '' + i)
                    self._mins.addChangeHandler(self)
                if VCalendarPanel_this.getResolution() >= VDateField.RESOLUTION_SEC:
                    self._sec = self.createListBox()
                    _3 = True
                    i = 0
                    while True:
                        if _3 is True:
                            _3 = False
                        else:
                            i += 1
                        if not (i < 60):
                            break
                        self._sec.addItem('0' + i if i < 10 else '' + i)
                    self._sec.addChangeHandler(self)
                if VCalendarPanel_this.getResolution() == VDateField.RESOLUTION_MSEC:
                    self._msec = self.createListBox()
                    _4 = True
                    i = 0
                    while True:
                        if _4 is True:
                            _4 = False
                        else:
                            i += 1
                        if not (i < 1000):
                            break
                        if i < 10:
                            self._msec.addItem('00' + i)
                        elif i < 100:
                            self._msec.addItem('0' + i)
                        else:
                            self._msec.addItem('' + i)
                    self._msec.addChangeHandler(self)
                delimiter = self.getDateTimeService().getClockDelimeter()
                if VCalendarPanel_this.isReadonly():
                    h = 0
                    if VCalendarPanel_this._value is not None:
                        h = VCalendarPanel_this._value.getHours()
                    if self.getDateTimeService().isTwelveHourClock():
                        h -= 0 if h < 12 else 12
                    self.add(VLabel('0' + h if h < 10 else '' + h))
                else:
                    self.add(self._hours)
                if VCalendarPanel_this.getResolution() >= VDateField.RESOLUTION_MIN:
                    self.add(VLabel(delimiter))
                    if VCalendarPanel_this.isReadonly():
                        m = self._mins.getSelectedIndex()
                        self.add(VLabel('0' + m if m < 10 else '' + m))
                    else:
                        self.add(self._mins)
                if VCalendarPanel_this.getResolution() >= VDateField.RESOLUTION_SEC:
                    self.add(VLabel(delimiter))
                    if VCalendarPanel_this.isReadonly():
                        s = self._sec.getSelectedIndex()
                        self.add(VLabel('0' + s if s < 10 else '' + s))
                    else:
                        self.add(self._sec)
                if VCalendarPanel_this.getResolution() == VDateField.RESOLUTION_MSEC:
                    self.add(VLabel('.'))
                    if VCalendarPanel_this.isReadonly():
                        m = self.getMilliseconds()
                        ms = '0' + m if m < 100 else '' + m
                        self.add(VLabel('0' + ms if m < 10 else ms))
                    else:
                        self.add(self._msec)
                if VCalendarPanel_this.getResolution() == VDateField.RESOLUTION_HOUR:
                    self.add(VLabel(delimiter + '00'))
                    # o'clock
                if self.getDateTimeService().isTwelveHourClock():
                    self.add(VLabel('&nbsp;'))
                    if VCalendarPanel_this.isReadonly():
                        i = 0
                        if VCalendarPanel_this._value is not None:
                            i = 0 if VCalendarPanel_this._value.getHours() < 12 else 1
                        self.add(VLabel(self._ampm.getItemText(i)))
                    else:
                        self.add(self._ampm)
                if VCalendarPanel_this.isReadonly():
                    return
                # Update times
                self.updateTimes()
                lastDropDown = self.getLastDropDown()

                class _3_(KeyDownHandler):

                    def onKeyDown(self, event):
                        shiftKey = event.getNativeEvent().getShiftKey()
                        if shiftKey:
                            return
                        else:
                            nativeKeyCode = event.getNativeKeyCode()
                            if nativeKeyCode == KeyCodes.KEY_TAB:
                                VCalendarPanel_this.onTabOut(event)

                _3_ = _3_()
                lastDropDown.addKeyDownHandler(_3_)

            def getLastDropDown(self):
                i = self.getWidgetCount() - 1
                while i >= 0:
                    widget = self.getWidget(i)
                    if isinstance(widget, ListBox):
                        return widget
                    i -= 1
                return None

            def updateTimes(self):
                """Updates the valus to correspond to the values in value"""
                selected = True
                if VCalendarPanel_this._value is None:
                    VCalendarPanel_this._value = Date()
                    selected = False
                if self.getDateTimeService().isTwelveHourClock():
                    h = VCalendarPanel_this._value.getHours()
                    self._ampm.setSelectedIndex(0 if h < 12 else 1)
                    h -= self._ampm.getSelectedIndex() * 12
                    self._hours.setSelectedIndex(h)
                else:
                    self._hours.setSelectedIndex(VCalendarPanel_this._value.getHours())
                if VCalendarPanel_this.getResolution() >= VDateField.RESOLUTION_MIN:
                    self._mins.setSelectedIndex(VCalendarPanel_this._value.getMinutes())
                if VCalendarPanel_this.getResolution() >= VDateField.RESOLUTION_SEC:
                    self._sec.setSelectedIndex(VCalendarPanel_this._value.getSeconds())
                if VCalendarPanel_this.getResolution() == VDateField.RESOLUTION_MSEC:
                    if selected:
                        self._msec.setSelectedIndex(self.getMilliseconds())
                    else:
                        self._msec.setSelectedIndex(0)
                if self.getDateTimeService().isTwelveHourClock():
                    self._ampm.setSelectedIndex(0 if VCalendarPanel_this._value.getHours() < 12 else 1)
                self._hours.setEnabled(VCalendarPanel_this.isEnabled())
                if self._mins is not None:
                    self._mins.setEnabled(VCalendarPanel_this.isEnabled())
                if self._sec is not None:
                    self._sec.setEnabled(VCalendarPanel_this.isEnabled())
                if self._msec is not None:
                    self._msec.setEnabled(VCalendarPanel_this.isEnabled())
                if self._ampm is not None:
                    self._ampm.setEnabled(VCalendarPanel_this.isEnabled())

            def getMilliseconds(self):
                return DateTimeService.getMilliseconds(VCalendarPanel_this._value)

            def getDateTimeService(self):
                # (non-Javadoc) VT
                #          *
                # @see
                # com.google.gwt.event.dom.client.ChangeHandler#onChange(com.google.gwt
                # .event.dom.client.ChangeEvent)

                if VCalendarPanel_this._dateTimeService is None:
                    VCalendarPanel_this._dateTimeService = DateTimeService()
                return VCalendarPanel_this._dateTimeService

            def onChange(self, event):
                # Value from dropdowns gets always set for the value. Like year and
                # month when resolution is month or year.

                if event.getSource() == self._hours:
                    h = self._hours.getSelectedIndex()
                    if self.getDateTimeService().isTwelveHourClock():
                        h = h + (self._ampm.getSelectedIndex() * 12)
                    VCalendarPanel_this._value.setHours(h)
                    if VCalendarPanel_this._timeChangeListener is not None:
                        VCalendarPanel_this._timeChangeListener.changed(h, VCalendarPanel_this._value.getMinutes(), VCalendarPanel_this._value.getSeconds(), DateTimeService.getMilliseconds(VCalendarPanel_this._value))
                    event.preventDefault()
                    event.stopPropagation()
                elif event.getSource() == self._mins:
                    m = self._mins.getSelectedIndex()
                    VCalendarPanel_this._value.setMinutes(m)
                    if VCalendarPanel_this._timeChangeListener is not None:
                        VCalendarPanel_this._timeChangeListener.changed(VCalendarPanel_this._value.getHours(), m, VCalendarPanel_this._value.getSeconds(), DateTimeService.getMilliseconds(VCalendarPanel_this._value))
                    event.preventDefault()
                    event.stopPropagation()
                elif event.getSource() == self._sec:
                    s = self._sec.getSelectedIndex()
                    VCalendarPanel_this._value.setSeconds(s)
                    if VCalendarPanel_this._timeChangeListener is not None:
                        VCalendarPanel_this._timeChangeListener.changed(VCalendarPanel_this._value.getHours(), VCalendarPanel_this._value.getMinutes(), s, DateTimeService.getMilliseconds(VCalendarPanel_this._value))
                    event.preventDefault()
                    event.stopPropagation()
                elif event.getSource() == self._msec:
                    ms = self._msec.getSelectedIndex()
                    DateTimeService.setMilliseconds(VCalendarPanel_this._value, ms)
                    if VCalendarPanel_this._timeChangeListener is not None:
                        VCalendarPanel_this._timeChangeListener.changed(VCalendarPanel_this._value.getHours(), VCalendarPanel_this._value.getMinutes(), VCalendarPanel_this._value.getSeconds(), ms)
                    event.preventDefault()
                    event.stopPropagation()
                elif event.getSource() == self._ampm:
                    h = self._hours.getSelectedIndex() + (self._ampm.getSelectedIndex() * 12)
                    VCalendarPanel_this._value.setHours(h)
                    if VCalendarPanel_this._timeChangeListener is not None:
                        VCalendarPanel_this._timeChangeListener.changed(h, VCalendarPanel_this._value.getMinutes(), VCalendarPanel_this._value.getSeconds(), DateTimeService.getMilliseconds(VCalendarPanel_this._value))
                    event.preventDefault()
                    event.stopPropagation()

        return VTime(*args, **kwargs)

    class Day(InlineHTML):
        _BASECLASS = VDateField.CLASSNAME + '-calendarpanel-day'
        _day = None

        def __init__(self, dayOfMonth):
            super(Day, self)('' + dayOfMonth)
            self.setStyleName(self._BASECLASS)
            self._day = dayOfMonth
            self.addClickHandler(self.dayClickHandler)

        def getDay(self):
            return self._day

    def getDate(self):
        return self._value

    def onTabOut(self, event):
        """If true should be returned if the panel will not be used after this
        event.
             *
        @param event
        @return
        """
        if self._focusOutListener is not None:
            return self._focusOutListener.onFocusOut(event)
        return False

    def setFocusOutListener(self, listener):
        """A focus out listener is triggered when the panel loosed focus. This can
        happen either after a user clicks outside the panel or tabs out.
             *
        @param listener
                   The listener to trigger
        """
        self._focusOutListener = listener

    def setSubmitListener(self, submitListener):
        """The submit listener is called when the user selects a value from the
        calender either by clicking the day or selects it by keyboard.
             *
        @param submitListener
                   The listener to trigger
        """
        self._submitListener = submitListener

    def setFocusChangeListener(self, listener):
        """The given FocusChangeListener is notified when the focused date changes
        by user either clicking on a new date or by using the keyboard.
             *
        @param listener
                   The FocusChangeListener to be notified
        """
        self._focusChangeListener = listener

    def setTimeChangeListener(self, listener):
        """The time change listener is triggered when the user changes the time.
             *
        @param listener
        """
        self._timeChangeListener = listener

    def getSubmitListener(self):
        """Returns the submit listener that listens to selection made from the panel
             *
        @return The listener or NULL if no listener has been set
        """
        # (non-Javadoc)
        #      *
        # @see
        # com.google.gwt.event.dom.client.BlurHandler#onBlur(com.google.gwt.event
        # .dom.client.BlurEvent)

        return self._submitListener

    def onBlur(self, event):
        # (non-Javadoc)
        #      *
        # @see
        # com.google.gwt.event.dom.client.FocusHandler#onFocus(com.google.gwt.event
        # .dom.client.FocusEvent)

        if isinstance(event.getSource(), VCalendarPanel):
            self._hasFocus = False
            self.focusDay(-1)

    def onFocus(self, event):
        if isinstance(event.getSource(), VCalendarPanel):
            self._hasFocus = True
            # Focuses the current day if the calendar shows the days
            if self._focusedDay is not None:
                self.focusDay(self._focusedDay.getDay())

    _SUBPART_NEXT_MONTH = 'nextmon'
    _SUBPART_PREV_MONTH = 'prevmon'
    _SUBPART_NEXT_YEAR = 'nexty'
    _SUBPART_PREV_YEAR = 'prevy'
    _SUBPART_HOUR_SELECT = 'h'
    _SUBPART_MINUTE_SELECT = 'm'
    _SUBPART_SECS_SELECT = 's'
    _SUBPART_MSECS_SELECT = 'ms'
    _SUBPART_AMPM_SELECT = 'ampm'
    _SUBPART_DAY = 'day'
    _SUBPART_MONTH_YEAR_HEADER = 'header'

    def getSubPartName(self, subElement):
        if self.contains(self._nextMonth, subElement):
            return self._SUBPART_NEXT_MONTH
        elif self.contains(self._prevMonth, subElement):
            return self._SUBPART_PREV_MONTH
        elif self.contains(self._nextYear, subElement):
            return self._SUBPART_NEXT_YEAR
        elif self.contains(self._prevYear, subElement):
            return self._SUBPART_PREV_YEAR
        elif self.contains(self._days, subElement):
            # Day, find out which dayOfMonth and use that as the identifier
            day = Util.findWidget(subElement, self.Day)
            if day is not None:
                return self._SUBPART_DAY + day.getDay()
        elif self._time is not None:
            if self.contains(self._time.hours, subElement):
                return self._SUBPART_HOUR_SELECT
            elif self.contains(self._time.mins, subElement):
                return self._SUBPART_MINUTE_SELECT
            elif self.contains(self._time.sec, subElement):
                return self._SUBPART_SECS_SELECT
            elif self.contains(self._time.msec, subElement):
                return self._SUBPART_MSECS_SELECT
            elif self.contains(self._time.ampm, subElement):
                return self._SUBPART_AMPM_SELECT
        elif self.getCellFormatter().getElement(0, 2).isOrHasChild(subElement):
            return self._SUBPART_MONTH_YEAR_HEADER
        return None

    def contains(self, w, subElement):
        """Checks if subElement is inside the widget DOM hierarchy.
             *
        @param w
        @param subElement
        @return true if {@code w} is a parent of subElement, false otherwise.
        """
        if (w is None) or (w.getElement() is None):
            return False
        return w.getElement().isOrHasChild(subElement)

    def getSubPartElement(self, subPart):
        if self._SUBPART_NEXT_MONTH == subPart:
            return self._nextMonth.getElement()
        if self._SUBPART_PREV_MONTH == subPart:
            return self._prevMonth.getElement()
        if self._SUBPART_NEXT_YEAR == subPart:
            return self._nextYear.getElement()
        if self._SUBPART_PREV_YEAR == subPart:
            return self._prevYear.getElement()
        if self._SUBPART_HOUR_SELECT == subPart:
            return self._time.hours.getElement()
        if self._SUBPART_MINUTE_SELECT == subPart:
            return self._time.mins.getElement()
        if self._SUBPART_SECS_SELECT == subPart:
            return self._time.sec.getElement()
        if self._SUBPART_MSECS_SELECT == subPart:
            return self._time.msec.getElement()
        if self._SUBPART_AMPM_SELECT == subPart:
            return self._time.ampm.getElement()
        if subPart.startswith(self._SUBPART_DAY):
            dayOfMonth = int(subPart[len(self._SUBPART_DAY):])
            iter = self._days
            while iter.hasNext():
                w = iter.next()
                if isinstance(w, self.Day):
                    day = w
                    if day.getDay() == dayOfMonth:
                        return day.getElement()
        if self._SUBPART_MONTH_YEAR_HEADER == subPart:
            return self.getCellFormatter().getElement(0, 2).getChild(0)
        return None

    def onDetach(self):
        super(VCalendarPanel, self).onDetach()
        if self._mouseTimer is not None:
            self._mouseTimer.cancel()
