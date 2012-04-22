# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class DragEventType(object):

    ENTER = 'ENTER'
    LEAVE = 'LEAVE'
    OVER = 'OVER'
    DROP = 'DROP'

    _values = [ENTER, LEAVE, OVER, DROP]

    @classmethod
    def values(cls):
        return cls._values[:]
