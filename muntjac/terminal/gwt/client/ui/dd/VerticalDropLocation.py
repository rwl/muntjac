# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class VerticalDropLocation(object):
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'
    MIDDLE = 'MIDDLE'
    _values = [TOP, BOTTOM, MIDDLE]

    @classmethod
    def values(cls):
        return cls._enum_values[:]
