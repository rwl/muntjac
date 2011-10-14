# -*- coding: utf-8 -*-
# from com.vaadin.terminal.gwt.client.DateTimeService import (DateTimeService,)
# from java.util.Calendar import (Calendar,)
# from java.util.Date import (Date,)
# from java.util.HashMap import (HashMap,)
# from java.util.Map import (Map,)
# from junit.framework.TestCase import (TestCase,)


class WeekNumberCalculation(TestCase):
    MILLISECONDS_PER_DAY = 24 * 3600 * 1000
    isoWeekNumbers = dict()
    isoWeekNumbers.put(getDate(2005, 2, 2), 5)
    isoWeekNumbers.put(getDate(2005, 1, 1), 53)
    isoWeekNumbers.put(getDate(2005, 1, 2), 53)
    isoWeekNumbers.put(getDate(2005, 1, 3), 1)
    isoWeekNumbers.put(getDate(2005, 1, 4), 1)
    isoWeekNumbers.put(getDate(2005, 1, 5), 1)
    isoWeekNumbers.put(getDate(2005, 1, 6), 1)
    isoWeekNumbers.put(getDate(2005, 1, 7), 1)
    isoWeekNumbers.put(getDate(2005, 1, 8), 1)
    isoWeekNumbers.put(getDate(2005, 1, 9), 1)
    isoWeekNumbers.put(getDate(2005, 1, 10), 2)
    isoWeekNumbers.put(getDate(2005, 12, 31), 52)
    isoWeekNumbers.put(getDate(2005, 12, 30), 52)
    isoWeekNumbers.put(getDate(2005, 12, 29), 52)
    isoWeekNumbers.put(getDate(2005, 12, 28), 52)
    isoWeekNumbers.put(getDate(2005, 12, 27), 52)
    isoWeekNumbers.put(getDate(2005, 12, 26), 52)
    isoWeekNumbers.put(getDate(2005, 12, 25), 51)
    isoWeekNumbers.put(getDate(2007, 1, 1), 1)
    isoWeekNumbers.put(getDate(2007, 12, 30), 52)
    isoWeekNumbers.put(getDate(2007, 12, 31), 1)
    isoWeekNumbers.put(getDate(2008, 1, 1), 1)
    isoWeekNumbers.put(getDate(2008, 12, 28), 52)
    isoWeekNumbers.put(getDate(2008, 12, 29), 1)
    isoWeekNumbers.put(getDate(2008, 12, 30), 1)
    isoWeekNumbers.put(getDate(2008, 12, 31), 1)
    isoWeekNumbers.put(getDate(2009, 1, 1), 1)
    isoWeekNumbers.put(getDate(2009, 12, 31), 53)
    isoWeekNumbers.put(getDate(2010, 1, 1), 53)
    isoWeekNumbers.put(getDate(2010, 1, 2), 53)
    isoWeekNumbers.put(getDate(2010, 1, 3), 53)
    isoWeekNumbers.put(getDate(2010, 1, 4), 1)
    isoWeekNumbers.put(getDate(2010, 1, 5), 1)
    isoWeekNumbers.put(getDate(2010, 10, 10), 40)

    def testISOWeekNumbers(self):
        """Test all dates from 1990-1992 + some more and see that {@link Calendar}
        calculates the ISO week number like we do.
        """
        c = Calendar.getInstance()
        c.set(1990, 1, 1)
        start = c.getTimeInMillis()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 1000):
                break
            d = Date(start + (i * self.MILLISECONDS_PER_DAY))
            expected = self.getCalendarISOWeekNr(d)
            calculated = DateTimeService.getISOWeekNumber(d)
            self.assertEquals(d + ' should be week ' + expected, expected, calculated)

    def testSampleISOWeekNumbers(self):
        """Verify that special cases are handled correctly by us (and
        {@link Calendar}).
        """
        for d in self.isoWeekNumbers.keys():
            # System.out.println("Sample: " + d);
            expected = self.isoWeekNumbers[d]
            calculated = DateTimeService.getISOWeekNumber(d)
            self.assertEquals(d + ' should be week ' + expected + ' (Java Calendar is wrong?)', expected, self.getCalendarISOWeekNr(d))
            self.assertEquals(d + ' should be week ' + expected, expected, calculated)

    def getCalendarISOWeekNr(self, d):
        c = Calendar.getInstance()
        c.setFirstDayOfWeek(Calendar.MONDAY)
        c.setMinimalDaysInFirstWeek(4)
        c.setTime(d)
        return c.get(Calendar.WEEK_OF_YEAR)

    @classmethod
    def getDate(cls, year, month, date):
        c = Calendar.getInstance()
        c.clear()
        c.set(year, month - 1, date)
        return c.getTime()
