# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class HorizontalDropLocation(object):

    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    CENTER = 'CENTER'

    _values = [LEFT, RIGHT, CENTER]

    @classmethod
    def values(cls):
        return cls._enum_values[:]

    @classmethod
    def valueOf(cls, name):
        for v in cls._values:
            if v.lower() == name.lower():
                return v
        else:
            return None
