# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
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
