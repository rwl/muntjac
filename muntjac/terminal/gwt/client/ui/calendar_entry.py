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

from datetime import date as Date

from muntjac.terminal.gwt.client.date_time_service import DateTimeService


class CalendarEntry(object):

    def __init__(self, styleName, start, end, title, description, notime=False):
        self._start = None
        self._end = None

        self._styleName = styleName
        if notime:
            d = Date(start.getTime())
            d.setSeconds(0)
            d.setMinutes(0)
            self._start = d
            if end is not None:
                d = Date(end.getTime())
                d.setSeconds(0)
                d.setMinutes(0)
                self._end = d
            else:
                end = start
        else:
            self._start = start
            self._end = end

        self._title = title
        self._description = description
        self._notime = notime


    def getStyleName(self):
        return self._styleName


    def getStart(self):
        return self._start


    def setStart(self, start):
        self._start = start


    def getEnd(self):
        return self._end


    def setEnd(self, end):
        self._end = end


    def getTitle(self):
        return self._title


    def setTitle(self, title):
        self._title = title


    def getDescription(self):
        return self._description


    def setDescription(self, description):
        self._description = description


    def isNotime(self):
        return self._notime


    def setNotime(self, notime):
        self._notime = notime


    def getStringForDate(self, d):
        # TODO: format from DateTimeService
        s = ''
        if not self._notime:
            if not DateTimeService.isSameDay(d, self._start):
                s += (self._start.getYear() + 1900 + '.'
                      + self._start.getMonth() + 1 + '.'
                      + self._start.getDate() + ' ')
            i = self._start.getHours()
            s += ('0' if i < 10 else '') + i
            s += ':'
            i = self._start.getMinutes()
            s += ('0' if i < 10 else '') + i
            if not (self._start == self._end):
                s += ' - '
                if not DateTimeService.isSameDay(self._start, self._end):
                    s += (self._end.getYear() + 1900 + '.'
                          + self._end.getMonth() + 1 + '.'
                          + self._end.getDate() + ' ')
                i = self._end.getHours()
                s += ('0' if i < 10 else '') + i
                s += ':'
                i = self._end.getMinutes()
                s += ('0' if i < 10 else '') + i
            s += ' '
        if self._title is not None:
            s += self._title
        return s
