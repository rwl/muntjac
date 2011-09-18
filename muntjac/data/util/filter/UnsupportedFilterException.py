# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
# from java.io.Serializable import (Serializable,)


class UnsupportedFilterException(RuntimeError, Serializable):
    """Exception for cases where a container does not support a specific type of
    filters.

    If possible, this should be thrown already when adding a filter to a
    container. If a problem is not detected at that point, an
    {@link UnsupportedOperationException} can be throws when attempting to
    perform filtering.

    @since 6.6
    """

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            pass # astStmt: [Stmt([]), None]
        elif _1 == 1:
            if isinstance(_0[0], Exception):
                cause, = _0
                super(UnsupportedFilterException, self)(cause)
            else:
                message, = _0
                super(UnsupportedFilterException, self)(message)
        elif _1 == 2:
            message, cause = _0
            super(UnsupportedFilterException, self)(message, cause)
        else:
            raise ARGERROR(0, 2)
