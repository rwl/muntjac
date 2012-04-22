# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Interface implemented by classes wishing to provide application
resources."""

from muntjac.terminal.resource import IResource


class IApplicationResource(IResource):
    """This interface must be implemented by classes wishing to provide
    Application resources.

    C{IApplicationResource} are a set of named resources (pictures, sounds,
    etc) associated with some specific application. Having named application
    resources provides a convenient method for having inter-theme common
    resources for an application.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    """

    DEFAULT_CACHETIME = 1000 * 60 * 60 * 24

    def getStream(self):
        """Gets resource as stream."""
        raise NotImplementedError


    def getApplication(self):
        """Gets the application of the resource."""
        raise NotImplementedError


    def getFilename(self):
        """Gets the virtual filename for this resource.

        @return: the file name associated to this resource.
        """
        raise NotImplementedError


    def getCacheTime(self):
        """Gets the length of cache expiration time.

        This gives the adapter the possibility cache streams sent to the
        client. The caching may be made in adapter or at the client if the
        client supports caching. Default is C{DEFAULT_CACHETIME}.

        @return: Cache time in milliseconds
        """
        raise NotImplementedError


    def getBufferSize(self):
        """Gets the size of the download buffer used for this resource.

        If the buffer size is 0, the buffer size is decided by the terminal
        adapter. The default value is 0.

        @return: the size of the buffer in bytes.
        """
        raise NotImplementedError
