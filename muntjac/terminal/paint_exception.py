# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class PaintException(IOError):
    """C{PaintExcepection} is thrown if painting of a
    component fails.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    """

    def __init__(self, arg):
        """Constructs an instance of C{PaintExeception} with the specified
        detail message or an instance of C{PaintExeception} from IOException.

        @param arg:
                   the detail message or the original exception
        """
        super(PaintException, self).__init__( str(arg) )
