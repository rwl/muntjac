# Copyright (C) 2010 IT Mill Ltd.
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

from unittest import TestCase


class WeekNumberCalculation(TestCase):

    MILLISECONDS_PER_DAY = 24 * 3600 * 1000

    def setUp(self):
        TestCase.setUp(self)

        self.isoWeekNumbers = {
                self.getDate(2005, 2, 2) : 5,
                self.getDate(2005, 1, 1) : 53,
                self.getDate(2005, 1, 2) : 53,
                self.getDate(2005, 1, 3) : 1,
                self.getDate(2005, 1, 4) : 1,
                self.getDate(2005, 1, 5) : 1,
                self.getDate(2005, 1, 6) : 1,
                self.getDate(2005, 1, 7) : 1,
                self.getDate(2005, 1, 8) : 1,
                self.getDate(2005, 1, 9) : 1,
                self.getDate(2005, 1, 10) : 2,
                self.getDate(2005, 12, 31) : 52,
                self.getDate(2005, 12, 30) : 52,
                self.getDate(2005, 12, 29) : 52,
                self.getDate(2005, 12, 28) : 52,
                self.getDate(2005, 12, 27) : 52,
                self.getDate(2005, 12, 26) : 52,
                self.getDate(2005, 12, 25) : 51,
                self.getDate(2007, 1, 1) : 1,
                self.getDate(2007, 12, 30) : 52,
                self.getDate(2007, 12, 31) : 1,
                self.getDate(2008, 1, 1) : 1,
                self.getDate(2008, 12, 28) : 52,
                self.getDate(2008, 12, 29) : 1,
                self.getDate(2008, 12, 30) : 1,
                self.getDate(2008, 12, 31) : 1,
                self.getDate(2009, 1, 1) : 1,
                self.getDate(2009, 12, 31) : 53,
                self.getDate(2010, 1, 1) : 53,
                self.getDate(2010, 1, 2) : 53,
                self.getDate(2010, 1, 3) : 53,
                self.getDate(2010, 1, 4) : 1,
                self.getDate(2010, 1, 5) : 1,
                self.getDate(2010, 10, 10) : 40
        }


    def testISOWeekNumbers(self):
        """Test all dates from 1990-1992 + some more and see that L{datetime}
        calculates the ISO week number like we do.
        """
        c = Calendar.getInstance()
        c.set(1990, 1, 1)
        start = c.getTimeInMillis()

        for i in range(1000):
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
            self.assertEquals(d + ' should be week ' + expected + ' (datetime is wrong?)', expected, self.getCalendarISOWeekNr(d))
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
