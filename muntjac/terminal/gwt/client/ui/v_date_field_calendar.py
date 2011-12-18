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

from datetime import datetime as Date

from muntjac.terminal.gwt.client.date_time_service import DateTimeService
from muntjac.terminal.gwt.client.ui.v_date_field import VDateField

from muntjac.terminal.gwt.client.ui.v_calendar_panel \
    import IFocusChangeListener, ISubmitListener, ITimeChangeListener, \
    VCalendarPanel


class VDateFieldCalendar(VDateField):
    """A client side implementation for InlineDateField"""

    def __init__(self):
        super(VDateFieldCalendar, self).__init__()

        self._calendarPanel = VCalendarPanel()
        self.add(self._calendarPanel)

        class _0_(ISubmitListener):

            def onSubmit(self):
                VDateFieldCalendar_this.updateValueFromPanel()

            def onCancel(self):
                # TODO Auto-generated method stub
                pass

        _0_ = _0_()
        self._calendarPanel.setSubmitListener(_0_)

        class _1_(IFocusOutListener):

            def onFocusOut(self, event):
                VDateFieldCalendar_this.updateValueFromPanel()
                return False

        _1_ = _1_()
        self._calendarPanel.setFocusOutListener(_1_)


    def updateFromUIDL(self, uidl, client):
        super(VDateFieldCalendar, self).updateFromUIDL(uidl, client)

        self._calendarPanel.setShowISOWeekNumbers(self.isShowISOWeekNumbers())
        self._calendarPanel.setDateTimeService(self.getDateTimeService())
        self._calendarPanel.setResolution(self.getCurrentResolution())

        currentDate = self.getCurrentDate()

        if currentDate is not None:
            self._calendarPanel.setDate(Date(currentDate.getTime()))
        else:
            self._calendarPanel.setDate(None)

        if self.currentResolution > self.RESOLUTION_DAY:

            class _2_(ITimeChangeListener):

                def changed(self, hour, min, sec, msec):
                    d = self.getDate()
                    if d is None:
                        # date currently null, use the value from calendarPanel
                        # (~ client time at the init of the widget)
                        d = VDateFieldCalendar_this._calendarPanel.getDate().clone()
                    d.setHours(hour)
                    d.setMinutes(min)
                    d.setSeconds(sec)
                    DateTimeService.setMilliseconds(d, msec)
                    # Always update time changes to the server
                    VDateFieldCalendar_this._calendarPanel.setDate(d)
                    VDateFieldCalendar_this.updateValueFromPanel()

            _2_ = _2_()
            self._calendarPanel.setTimeChangeListener(_2_)

        if self.currentResolution <= self.RESOLUTION_MONTH:

            class _3_(IFocusChangeListener):

                def focusChanged(self, date):
                    date2 = Date()
                    if VDateFieldCalendar_this._calendarPanel.getDate() is not None:
                        date2.setTime(VDateFieldCalendar_this._calendarPanel.getDate().getTime())
                    # Update the value of calendarPanel
                    date2.setYear(date.getYear())
                    date2.setMonth(date.getMonth())
                    VDateFieldCalendar_this._calendarPanel.setDate(date2)
                    # Then update the value from panel to server
                    VDateFieldCalendar_this.updateValueFromPanel()

            _3_ = _3_()
            self._calendarPanel.setFocusChangeListener(_3_)
        else:
            self._calendarPanel.setFocusChangeListener(None)

        # Update possible changes
        self._calendarPanel.renderCalendar()


    def updateValueFromPanel(self):
        """TODO: refactor: almost same method as in
        VPopupCalendar.updateValue"""
        date2 = self._calendarPanel.getDate()
        currentDate = self.getCurrentDate()
        if (currentDate is None) or (date2.getTime() != currentDate.getTime()):
            self.setCurrentDate(date2.clone())
            self.getClient().updateVariable(self.getId(), 'year',
                    date2.getYear() + 1900, False)
            if self.getCurrentResolution() > VDateField.RESOLUTION_YEAR:
                self.getClient().updateVariable(self.getId(), 'month',
                        date2.getMonth() + 1, False)
                if self.getCurrentResolution() > self.RESOLUTION_MONTH:
                    self.getClient().updateVariable(self.getId(), 'day',
                            date2.getDate(), False)
                    if self.getCurrentResolution() > self.RESOLUTION_DAY:
                        self.getClient().updateVariable(self.getId(), 'hour',
                                date2.getHours(), False)
                        if self.getCurrentResolution() > self.RESOLUTION_HOUR:
                            self.getClient().updateVariable(self.getId(),
                                    'min', date2.getMinutes(), False)
                            if self.getCurrentResolution() > self.RESOLUTION_MIN:
                                self.getClient().updateVariable(self.getId(),
                                        'sec', date2.getSeconds(), False)
                                if self.getCurrentResolution() > self.RESOLUTION_SEC:
                                    self.getClient().updateVariable(self.getId(),
                                            'msec',
                                            DateTimeService.getMilliseconds(date2),
                                            False)

            if self.isImmediate():
                self.getClient().sendPendingVariableChanges()
