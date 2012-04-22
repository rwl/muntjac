# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class VerticalDropLocation(object):

    TOP = 'TOP'
    BOTTOM = 'BOTTOM'
    MIDDLE = 'MIDDLE'

    _values = [TOP, BOTTOM, MIDDLE]

    @classmethod
    def values(cls):
        return cls._values[:]

    @classmethod
    def valueOf(cls, name):
        for v in cls._values:
            if v.lower() == name.lower():
                return v
        else:
            return None
