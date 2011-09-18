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

from com.vaadin.terminal.gwt.client.LocaleNotLoadedException import (LocaleNotLoadedException,)
# from java.util.HashMap import (HashMap,)
# from java.util.Map import (Map,)
# from java.util.Set import (Set,)


class LocaleService(object):
    """Date / time etc. localisation service for all widgets. Caches all loaded
    locales as JSONObjects.

    @author IT Mill Ltd.
    """
    _cache = dict()
    _defaultLocale = None

    @classmethod
    def addLocale(cls, valueMap):
        key = valueMap.getString('name')
        if key in cls._cache:
            cls._cache.remove(key)
        cls._cache.put(key, valueMap)
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
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(valueMapArray)):
                break
            cls.addLocale(valueMapArray.get(i))
