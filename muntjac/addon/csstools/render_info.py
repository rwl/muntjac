# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class RenderInfo(object):
    """Class for fetching render information from the client side widgets.

    @author: jouni@vaadin.com
    @author: Richard Lincoln
    """

    @classmethod
    def get(cls, c, cb, *props):
        """Initiate a request to get the render information for a given component.

        The information can be for example the exact pixel size and position, the
        font size, visibility, margin, padding or border of the component in the
        browser. See possible values from the {@link CssProperty} enumerable.

        The information will be delivered asynchronously from the client, and
        passed as a parameter to the callback method.

        You can limit the amount of properties transmitted over the connection by
        passing the desired property names as the last parameter for the method.

        @param c:
                   The component whose render information you wish to get.
        @param cb:
                   The callback object which will receive the information when it
                   is available.
        @param props:
                   Optional. The list of CSS properties you wish to get from the
                   client (limit the amount of transferred data). You can pass
                   any type of objects here, the C{__str__()} method
                   will be used to convert them to actual property names.
                   Preferably use the L{CssProperty} enumerable for feasible values.
        """
        if c.getApplication() is None:
            raise ValueError('The component must be attached to the application before you try to get it\'s RenderInfo')

        from muntjac.addon.csstools.render_info_fetcher \
            import RenderInfoFetcher

        fetcher = RenderInfoFetcher(c, cb, *props)
        c.getApplication().getMainWindow().addWindow(fetcher)


    def __init__(self, obj):
        self._props = obj


    def getProperty(self, prop):
        return self._props[str(prop)]


class ICallback(object):
    """The callback interface for RenderInformation requests.

    @author: jouni@vaadin.com
    @author: Richard Lincoln
    """

    def infoReceived(self, info):
        """This method is called when a RenderInfo request is returned from the
        client and the RenderInfo for that request is available.

        @param info:
                   The RenderInfo object for the request, containing the
                   requested properties (or all possible properties if no
                   specific properties were requested).
        """
        raise NotImplementedError
