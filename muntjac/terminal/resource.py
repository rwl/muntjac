# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class IResource(object):
    """C{IResource} provided to the client terminal. Support for
    actually displaying the resource type is left to the terminal.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    """

    def getMIMEType(self):
        """Gets the MIME type of the resource.

        @return: the MIME type of the resource.
        """
        raise NotImplementedError
