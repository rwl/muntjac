# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Exception for cases where a container does not support a specific
type of filters."""

class UnsupportedFilterException(RuntimeError):
    """Exception for cases where a container does not support a specific
    type of filters.

    If possible, this should be thrown already when adding a filter to a
    container. If a problem is not detected at that point, an
    L{NotImplementedError} can be thrown when attempting to perform filtering.
    """

    def __init__(self, *args):
        nargs = len(args)
        if nargs == 0:
            pass
        elif nargs == 1:
            if isinstance(args[0], Exception):
                cause, = args
                super(UnsupportedFilterException, self).__init__(cause)
            else:
                message, = args
                super(UnsupportedFilterException, self).__init__(message)
        elif nargs == 2:
            message, cause = args
            super(UnsupportedFilterException, self).__init__(message, cause)
        else:
            raise ValueError
