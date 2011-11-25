# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class HorizontalDropLocation(object):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    CENTER = 'CENTER'
    _values = [LEFT, RIGHT, CENTER]

    @classmethod
    def values(cls):
        return cls._enum_values[:]
