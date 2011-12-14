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

from datetime import datetime as Date

from pyjamas.ui.FlowPanel import FlowPanel

from muntjac.terminal.gwt.client.date_time_service import DateTimeService
from muntjac.terminal.gwt.client.v_console import VConsole
from muntjac.terminal.gwt.client.paintable import IPaintable
from muntjac.terminal.gwt.client.v_tooltip import VTooltip

from muntjac.terminal.gwt.client.locale_not_loaded_exception \
    import LocaleNotLoadedException

from muntjac.terminal.gwt.client.ui.field import IField


class VDateField(FlowPanel, IPaintable, IField):

    CLASSNAME = 'v-datefield'

    RESOLUTION_YEAR = 1
    RESOLUTION_MONTH = 2
    RESOLUTION_DAY = 4
    RESOLUTION_HOUR = 8
    RESOLUTION_MIN = 16
    RESOLUTION_SEC = 32
    RESOLUTION_MSEC = 64

    WEEK_NUMBERS = 'wn'

    def __init__(self):
        self._id = None
        self._client = None
        self.immediate = None

        self.currentResolution = self.RESOLUTION_YEAR
        self.currentLocale = None
        self.readonly = None
        self.enabled = None

        # The date that is selected in the date field. Null if an invalid
        # date is specified.
        self._date = None
        self.dts = DateTimeService()
        self._showISOWeekNumbers = False

        self.setStyleName(self.CLASSNAME)
        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)


    @classmethod
    def resolutionToString(cls, res):
        if res > cls.RESOLUTION_DAY:
            return 'full'
        if res == cls.RESOLUTION_DAY:
            return 'day'
        if res == cls.RESOLUTION_MONTH:
            return 'month'
        return 'year'


    def onBrowserEvent(self, event):
        super(VDateField, self).onBrowserEvent(event)
        if self._client is not None:
            self._client.handleTooltipEvent(event, self)


    def updateFromUIDL(self, uidl, client):
        # Ensure correct implementation and let layout manage caption
        if client.updateComponent(self, uidl, True):
            return

        # Save details
        self._client = client
        self._id = uidl.getId()
        self.immediate = uidl.getBooleanAttribute('immediate')

        self.readonly = uidl.getBooleanAttribute('readonly')
        self.enabled = not uidl.getBooleanAttribute('disabled')

        if uidl.hasAttribute('locale'):
            locale = uidl.getStringAttribute('locale')
            try:
                self.dts.setLocale(locale)
                self.currentLocale = locale
            except LocaleNotLoadedException, e:
                self.currentLocale = self.dts.getLocale()
                VConsole.error('Tried to use an unloaded locale \"'
                        + locale + '\". Using default locale ('
                        + self.currentLocale + ').')
                VConsole.error(e)

        # We show week numbers only if the week starts with Monday, as ISO 8601
        # specifies
        self._showISOWeekNumbers = (uidl.getBooleanAttribute(self.WEEK_NUMBERS)
                and self.dts.getFirstDayOfWeek() == 1)

        if uidl.hasVariable('msec'):
            newResolution = self.RESOLUTION_MSEC
        elif uidl.hasVariable('sec'):
            newResolution = self.RESOLUTION_SEC
        elif uidl.hasVariable('min'):
            newResolution = self.RESOLUTION_MIN
        elif uidl.hasVariable('hour'):
            newResolution = self.RESOLUTION_HOUR
        elif uidl.hasVariable('day'):
            newResolution = self.RESOLUTION_DAY
        elif uidl.hasVariable('month'):
            newResolution = self.RESOLUTION_MONTH
        else:
            newResolution = self.RESOLUTION_YEAR

        self.currentResolution = newResolution

        # Add stylename that indicates current resolution
        self.addStyleName(self.CLASSNAME + '-'
                + self.resolutionToString(self.currentResolution))

        year = uidl.getIntVariable('year')
        month = uidl.getIntVariable('month') if self.currentResolution >= self.RESOLUTION_MONTH else -1
        day = uidl.getIntVariable('day') if self.currentResolution >= self.RESOLUTION_DAY else -1
        hour = uidl.getIntVariable('hour') if self.currentResolution >= self.RESOLUTION_HOUR else 0
        min_ = uidl.getIntVariable('min') if self.currentResolution >= self.RESOLUTION_MIN else 0
        sec = uidl.getIntVariable('sec') if self.currentResolution >= self.RESOLUTION_SEC else 0
        msec = uidl.getIntVariable('msec') if self.currentResolution >= self.RESOLUTION_MSEC else 0

        # Construct new date for this datefield (only if not null)
        if year > -1:
            self.setCurrentDate(Date(self.getTime(year, month, day, hour,
                    min_, sec, msec)))
        else:
            self.setCurrentDate(None)


    @classmethod
    def getTime(cls, y, m, d, h, mi, s, ms):
        # We need this redundant native function because the Date object
        # doesn't have a setMilliseconds method.
        JS("""
           try {
           	var date = new Date(2000,1,1,1); // don't use current date here
           	if(@{{y}} && @{{y}} >= 0) date.setFullYear(@{{y}});
           	if(@{{m}} && @{{m}} >= 1) date.setMonth(@{{m}}-1);
           	if(@{{d}} && @{{d}} >= 0) date.setDate(@{{d}});
           	if(@{{h}} >= 0) date.setHours(@{{h}});
           	if(@{{mi}} >= 0) date.setMinutes(@{{mi}});
           	if(@{{s}} >= 0) date.setSeconds(@{{s}});
           	if(@{{ms}} >= 0) date.setMilliseconds(@{{ms}});
           	return date.getTime();
           } catch (e) {
           	// TODO print some error message on the console
           	//console.log(e);
           	return (new Date()).getTime();
           }
        """)
        pass


    def getMilliseconds(self):
        return DateTimeService.getMilliseconds(self._date)


    def setMilliseconds(self, ms):
        DateTimeService.setMilliseconds(self._date, ms)


    def getCurrentResolution(self):
        return self.currentResolution


    def setCurrentResolution(self, currentResolution):
        self.currentResolution = currentResolution


    def getCurrentLocale(self):
        return self.currentLocale


    def setCurrentLocale(self, currentLocale):
        self.currentLocale = currentLocale


    def getCurrentDate(self):
        return self._date


    def setCurrentDate(self, date):
        self._date = date


    def isImmediate(self):
        return self.immediate


    def isReadonly(self):
        return self.readonly


    def isEnabled(self):
        return self.enabled


    def getDateTimeService(self):
        return self.dts


    def getId(self):
        return self._id


    def getClient(self):
        return self._client


    def isShowISOWeekNumbers(self):
        """Returns whether ISO 8601 week numbers should be shown in the date
        selector or not. ISO 8601 defines that a week always starts with a
        Monday so the week numbers are only shown if this is the case.

        @return: true if week number should be shown, false otherwise
        """
        return self._showISOWeekNumbers


    def getDate(self):
        """Returns a copy of the current date. Modifying the returned date will
        not modify the value of this VDateField. Use {@link #setDate(Date)} to
        change the current date.

        @return: A copy of the current date
        """
        current = self.getCurrentDate()
        if current is None:
            return None
        else:
            return self.getCurrentDate().clone()


    def setDate(self, date):
        """Sets the current date for this VDateField.

        @param date:
                   The new date to use
        """
        self._date = date
