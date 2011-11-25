# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.DateTimeService import (DateTimeService,)
# from java.util.Date import (Date,)


class CalendarEntry(object):
    _styleName = None
    _start = None
    _end = None
    _title = None
    _description = None
    _notime = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 5:
            styleName, start, end, title, description = _0
            self.__init__(styleName, start, end, title, description, False)
        elif _1 == 6:
            styleName, start, end, title, description, notime = _0
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
        else:
            raise ARGERROR(5, 6)

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
        # TODO format from DateTimeService
        s = ''
        if not self._notime:
            if not DateTimeService.isSameDay(d, self._start):
                s += self._start.getYear() + 1900 + '.' + self._start.getMonth() + 1 + '.' + self._start.getDate() + ' '
            i = self._start.getHours()
            s += ('0' if i < 10 else '') + i
            s += ':'
            i = self._start.getMinutes()
            s += ('0' if i < 10 else '') + i
            if not (self._start == self._end):
                s += ' - '
                if not DateTimeService.isSameDay(self._start, self._end):
                    s += self._end.getYear() + 1900 + '.' + self._end.getMonth() + 1 + '.' + self._end.getDate() + ' '
                i = self._end.getHours()
                s += ('0' if i < 10 else '') + i
                s += ':'
                i = self._end.getMinutes()
                s += ('0' if i < 10 else '') + i
            s += ' '
        if self._title is not None:
            s += self._title
        return s
