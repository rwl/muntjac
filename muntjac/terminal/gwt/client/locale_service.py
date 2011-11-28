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

from muntjac.terminal.gwt.client.locale_not_loaded_exception \
    import LocaleNotLoadedException


class LocaleService(object):
    """Date / time etc. localisation service for all widgets. Caches all
    loaded locales as JSONObjects.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    """

    _cache = dict()
    _defaultLocale = None

    @classmethod
    def addLocale(cls, valueMap):
        key = valueMap.getString('name')
        if key in cls._cache:
            del cls._cache[key]
        cls._cache[key] = valueMap
        if len(cls._cache) == 1:
            cls.setDefaultLocale(key)


    @classmethod
    def setDefaultLocale(cls, locale):
        cls._defaultLocale = locale


    @classmethod
    def getDefaultLocale(cls):
        return cls._defaultLocale


    @classmethod
    def getAvailableLocales(cls):
        return cls._cache.keys()


    @classmethod
    def getMonthNames(cls, locale):
        if locale in cls._cache:
            l = cls._cache[locale]
            return l.getStringArray('mn')
        else:
            raise LocaleNotLoadedException(locale)


    @classmethod
    def getShortMonthNames(cls, locale):
        if locale in cls._cache:
            l = cls._cache[locale]
            return l.getStringArray('smn')
        else:
            raise LocaleNotLoadedException(locale)


    @classmethod
    def getDayNames(cls, locale):
        if locale in cls._cache:
            l = cls._cache[locale]
            return l.getStringArray('dn')
        else:
            raise LocaleNotLoadedException(locale)


    @classmethod
    def getShortDayNames(cls, locale):
        if locale in cls._cache:
            l = cls._cache[locale]
            return l.getStringArray('sdn')
        else:
            raise LocaleNotLoadedException(locale)


    @classmethod
    def getFirstDayOfWeek(cls, locale):
        if locale in cls._cache:
            l = cls._cache[locale]
            return l.getInt('fdow')
        else:
            raise LocaleNotLoadedException(locale)


    @classmethod
    def getDateFormat(cls, locale):
        if locale in cls._cache:
            l = cls._cache[locale]
            return l.getString('df')
        else:
            raise LocaleNotLoadedException(locale)


    @classmethod
    def isTwelveHourClock(cls, locale):
        if locale in cls._cache:
            l = cls._cache[locale]
            return l.getBoolean('thc')
        else:
            raise LocaleNotLoadedException(locale)


    @classmethod
    def getClockDelimiter(cls, locale):
        if locale in cls._cache:
            l = cls._cache[locale]
            return l.getString('hmd')
        else:
            raise LocaleNotLoadedException(locale)


    @classmethod
    def getAmPmStrings(cls, locale):
        if locale in cls._cache:
            l = cls._cache[locale]
            return l.getStringArray('ampm')
        else:
            raise LocaleNotLoadedException(locale)


    @classmethod
    def addLocales(cls, valueMapArray):
        for i in range(len(valueMapArray)):
            cls.addLocale(valueMapArray.get(i))
