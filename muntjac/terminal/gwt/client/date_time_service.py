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

from datetime import date

from muntjac.terminal.gwt.client.v_console import VConsole
from muntjac.terminal.gwt.client.locale_not_loaded_exception import LocaleNotLoadedException
from muntjac.terminal.gwt.client.locale_service import LocaleService
from muntjac.terminal.gwt.client.ui.v_date_field import VDateField


class DateTimeService(object):
    """This class provides date/time parsing services to all components on the
    client side.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    """

    _maxDaysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    _DEFAULT_AMPM_STRINGS = ['AM', 'PM']

    def __init__(self, locale=None):
        """Creates a new date time service with the given locale.

        @param locale:
                   e.g. fi, en etc.
        @raise: LocaleNotLoadedException
        """
        self._currentLocale = None

        if locale is None:
            self._currentLocale = LocaleService.getDefaultLocale()
        else:
            self.setLocale(locale)


    def setLocale(self, locale):
        if locale in LocaleService.getAvailableLocales():
            self._currentLocale = locale
        else:
            raise LocaleNotLoadedException(locale)


    def getLocale(self):
        return self._currentLocale


    def getMonth(self, month):
        try:
            return LocaleService.getMonthNames(self._currentLocale)[month]
        except LocaleNotLoadedException, e:
            VConsole.error(e)
            return None


    def getShortMonth(self, month):
        try:
            return LocaleService.getShortMonthNames(self._currentLocale)[month]
        except LocaleNotLoadedException, e:
            VConsole.error(e)
            return None


    def getDay(self, day):
        try:
            return LocaleService.getDayNames(self._currentLocale)[day]
        except LocaleNotLoadedException, e:
            VConsole.error(e)
            return None


    def getShortDay(self, day):
        try:
            return LocaleService.getShortDayNames(self._currentLocale)[day]
        except LocaleNotLoadedException, e:
            VConsole.error(e)
            return None


    def getFirstDayOfWeek(self):
        try:
            return LocaleService.getFirstDayOfWeek(self._currentLocale)
        except LocaleNotLoadedException, e:
            VConsole.error(e)
            return 0


    def isTwelveHourClock(self):
        try:
            return LocaleService.isTwelveHourClock(self._currentLocale)
        except LocaleNotLoadedException, e:
            VConsole.error(e)
            return False


    def getClockDelimeter(self):
        try:
            return LocaleService.getClockDelimiter(self._currentLocale)
        except LocaleNotLoadedException, e:
            VConsole.error(e)
            return ':'


    def getAmPmStrings(self):
        try:
            return LocaleService.getAmPmStrings(self._currentLocale)
        except LocaleNotLoadedException, e:
            # TODO: can this practically even happen? Should die instead?
            VConsole.error('Locale not loaded, using fallback : AM/PM')
            VConsole.error(e)
            return self._DEFAULT_AMPM_STRINGS


    def getStartWeekDay(self, date):
        dateForFirstOfThisMonth = date(date.getYear(), date.getMonth(), 1)
        try:
            firstDay = LocaleService.getFirstDayOfWeek(self._currentLocale)
        except LocaleNotLoadedException, e:
            VConsole.error('Locale not loaded, using fallback 0')
            VConsole.error(e)
            firstDay = 0

        start = dateForFirstOfThisMonth.getDay() - firstDay

        if start < 0:
            start = 6

        return start


    @classmethod
    def setMilliseconds(cls, date, ms):
        date.setTime(((date.getTime() / 1000) * 1000) + ms)


    @classmethod
    def getMilliseconds(cls, date):
        if date is None:
            return 0
        return date.getTime() - ((date.getTime() / 1000) * 1000)


    @classmethod
    def getNumberOfDaysInMonth(cls, date):
        month = date.getMonth()

        if month == 1 and True == cls.isLeapYear(date):
            return 29

        return cls._maxDaysInMonth[month]


    @classmethod
    def isLeapYear(cls, d):
        # Instantiate the date for 1st March of that year
        firstMarch = date(d.getYear(), 2, 1)

        # Go back 1 day
        firstMarchTime = firstMarch.getTime()
        lastDayTimeFeb = firstMarchTime - (24 * 60 * 60 * 1000)

        # NUM_MILLISECS_A_DAY
        # Instantiate new Date with this time
        febLastDay = date(lastDayTimeFeb)

        # Check for date in this new instance
        return True if 29 == febLastDay.getDate() else False


    @classmethod
    def isSameDay(cls, d1, d2):
        return cls.getDayInt(d1) == cls.getDayInt(d2)


    @classmethod
    def isInRange(cls, date, rangeStart, rangeEnd, resolution):
        if rangeStart.after(rangeEnd):
            s = rangeEnd
            e = rangeStart
        else:
            e = rangeEnd
            s = rangeStart

        start = s.getYear() * 10000000000L
        end = e.getYear() * 10000000000L
        target = date.getYear() * 10000000000L

        if resolution == VDateField.RESOLUTION_YEAR:
            return start <= target and end >= target

        start += s.getMonth() * 100000000L
        end += e.getMonth() * 100000000L
        target += date.getMonth() * 100000000L
        if resolution == VDateField.RESOLUTION_MONTH:
            return start <= target and end >= target

        start += s.getDate() * 1000000L
        end += e.getDate() * 1000000L
        target += date.getDate() * 1000000L
        if resolution == VDateField.RESOLUTION_DAY:
            return start <= target and end >= target

        start += s.getHours() * 10000L
        end += e.getHours() * 10000L
        target += date.getHours() * 10000L
        if resolution == VDateField.RESOLUTION_HOUR:
            return start <= target and end >= target

        start += s.getMinutes() * 100L
        end += e.getMinutes() * 100L
        target += date.getMinutes() * 100L
        if resolution == VDateField.RESOLUTION_MIN:
            return start <= target and end >= target

        start += s.getSeconds()
        end += e.getSeconds()
        target += date.getSeconds()
        return start <= target and end >= target


    @classmethod
    def getDayInt(cls, date):
        y = date.getYear()
        m = date.getMonth()
        d = date.getDate()
        return (((y + 1900) * 10000) + (m * 100) + d) * 1000000000


    @classmethod
    def getISOWeekNumber(cls, d):
        """Returns the ISO-8601 week number of the given date.

        @param date:
                   The date for which the week number should be resolved
        @return: The ISO-8601 week number for C{date}
        """
        MILLISECONDS_PER_DAY = 24 * 3600 * 1000
        dayOfWeek = d.getDay()  # 0 == Sunday

        # ISO 8601 use weeks that start on Monday so we use
        # mon=1,tue=2,...sun=7;
        if dayOfWeek == 0:
            dayOfWeek = 7

        # Find nearest thursday (defines the week in ISO 8601). The week number
        # for the nearest thursday is the same as for the target date.
        nearestThursdayDiff = 4 - dayOfWeek  # 4 is thursday
        nearestThursday = date(d.getTime()
                + (nearestThursdayDiff * MILLISECONDS_PER_DAY))

        firstOfJanuary = date(nearestThursday.getYear(), 0, 1)
        timeDiff = nearestThursday.getTime() - firstOfJanuary.getTime()
        daysSinceFirstOfJanuary = timeDiff / MILLISECONDS_PER_DAY

        weekNumber = (daysSinceFirstOfJanuary / 7) + 1

        return weekNumber


    def formatDate(self, date, formatStr):
        """Check if format contains the month name. If it does we manually
        convert it to the month name since DateTimeFormat.format always uses
        the current locale and will replace the month name wrong if current
        locale is different from the locale set for the DateField.

        MMMM is converted into long month name, MMM is converted into short
        month name. '' are added around the name to avoid that DateTimeFormat
        parses the month name as a pattern.

        @param date:
                   The date to convert
        @param formatStr:
                   The format string that might contain MMM or MMMM
        @param dateTimeService:
                   Reference to the Muntjac DateTimeService
        """
        # Format month names separately when locale for the DateTimeService
        # is not the same as the browser locale
        formatStr = self.formatMonthNames(date, formatStr)

        # Format uses the browser locale
        format = DateTimeFormat.getFormat(formatStr)

        result = format.format(date)

        return result


    def formatMonthNames(self, date, formatStr):
        if 'MMMM' in formatStr:
            monthName = self.getMonth(date.getMonth())

            if monthName is not None:
                # Replace 4 or more M:s with the quoted month name. Also
                # concatenate generated string with any other string prepending
                # or following the MMMM pattern, i.e. 'MMMM'ta ' becomes
                # 'MONTHta ' and not 'MONTH''ta ', 'ab'MMMM becomes 'abMONTH',
                # 'x'MMMM'y' becomes 'xMONTHy'.
                formatStr = formatStr.replace('\'([M]{4,})\'', monthName)
                formatStr = formatStr.replace('([M]{4,})\'', '\'' + monthName)
                formatStr = formatStr.replace('\'([M]{4,})', monthName + '\'')
                formatStr = formatStr.replace('[M]{4,}', '\'' + monthName + '\'')

        if 'MMM' in formatStr:
            monthName = self.getShortMonth(date.getMonth())

            if monthName is not None:
                # Replace 3 or more M:s with the quoted month name. Also
                # concatenate generated string with any other string prepending
                # or following the MMM pattern, i.e. 'MMM'ta ' becomes 'MONTHta
                # ' and not 'MONTH''ta ', 'ab'MMM becomes 'abMONTH', 'x'MMM'y'
                # becomes 'xMONTHy'.
                formatStr = formatStr.replace('\'([M]{3,})\'', monthName)
                formatStr = formatStr.replace('([M]{3,})\'', '\'' + monthName)
                formatStr = formatStr.replace('\'([M]{3,})', monthName + '\'')
                formatStr = formatStr.replace('[M]{3,}', '\'' + monthName + '\'')

        return formatStr


    def parseMonthName(self, enteredDate, formatString):
        """Replaces month names in the entered date with the name in the
        current browser locale.

        @param enteredDate:
                   Date string e.g. "5 May 2010"
        @param formatString:
                   Format string e.g. "d M yyyy"
        @return: The date string where the month names have been replaced
                 by the browser locale version
        """
        browserLocale = LocaleInfo.getCurrentLocale()
        if browserLocale.getLocaleName() == self.getLocale():
            # No conversion needs to be done when locales match
            return enteredDate

        browserMonthNames = browserLocale.getDateTimeConstants().months()
        browserShortMonthNames = browserLocale.getDateTimeConstants().shortMonths()

        if 'MMMM' in formatString:
            # Full month name
            for i in range(12):
                enteredDate = enteredDate.replace(self.getMonth(i),
                        browserMonthNames[i])
        if 'MMM' in formatString:
            # Short month name
            for i in range(12):
                enteredDate = enteredDate.replaceAll(self.getShortMonth(i),
                        browserShortMonthNames[i])
        return enteredDate


    def parseDate(self, dateString, formatString, lenient):
        """Parses the given date string using the given fmt string and the
        locale set in this DateTimeService instance.

        @param dateString:
                   Date string e.g. "1 February 2010"
        @param formatString:
                   Format string e.g. "d MMMM yyyy"
        @param lenient:
                   true to use lenient parsing, false to use strict parsing
        @return: A Date object representing the dateString. Never returns null.
        @raise ValueError:
                    if the parsing fails
        """
        # DateTimeFormat uses the browser's locale
        fmt = DateTimeFormat.getFormat(formatString)

        # Parse month names separately when locale for the DateTimeService is
        # not the same as the browser locale
        dateString = self.parseMonthName(dateString, formatString)

        if lenient:
            date = fmt.parse(dateString)
        else:
            date = fmt.parseStrict(dateString)

        # Some version of Firefox sets the timestamp to 0 if parsing fails.
        if date is not None and date.getTime() == 0:
            raise ValueError('Parsing of \'' + dateString
                    + '\' failed')

        return date
