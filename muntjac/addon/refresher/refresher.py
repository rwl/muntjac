# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.ui.abstract_component import AbstractComponent
from muntjac.addon.refresher.ui.v_refresher import VRefresher


class Refresher(AbstractComponent):
    """A Refresher is an non-visual component that polls the server for
    GUI updates.

    This makes asynchronous UI changes possible, that will be rendered even
    if the user doesn't initiate a server-cycle explicitly.

    @author Henrik Paul
    """

    CLIENT_WIDGET = None #ClientWidget(com.github.wolfie.refresher.client.ui.VRefresher)

    TYPE_MAPPING = 'com.github.wolfie.refresher.Refresher'

    _DEFAULT_REFRESH_INTERVAL = 1000

    def __init__(self):
        """Creates a new L{Refresher} instance, with a default refresh interval
        of L{Refresher.DEFAULT_REFRESH_INTERVAL}.
        """
        super(Refresher, self).__init__()

        self._refreshListeners = list()
        self._refreshIntervalInMillis = self._DEFAULT_REFRESH_INTERVAL


    def paintContent(self, target):
        target.addAttribute('pollinginterval', self._refreshIntervalInMillis)


    def setRefreshInterval(self, intervalInMillis):
        """Define a refresh interval.

        @param intervalInMillis:
                 The desired refresh interval in milliseconds. An interval
                 of zero or less temporarily inactivates the refresh.
        """
        self._refreshIntervalInMillis = intervalInMillis
        self.requestRepaint()


    def getRefreshInterval(self):
        """Get the currently used refreshing interval.

        @return: The refresh interval in milliseconds. A result of zero or
                 less means that the refresher is currently inactive.
        """
        return self._refreshIntervalInMillis


    def changeVariables(self, source, variables):
        super(Refresher, self).changeVariables(source, variables)

        if VRefresher.VARIABLE_REFRESH_EVENT in variables:
            self.fireRefreshEvents()


    def fireRefreshEvents(self):
        for listener in self._refreshListeners:
            listener.refresh(self)


    def addListener(self, listener, iface=None):
        """Add a listener that will be triggered whenever this instance
        refreshes itself

        @param listener:
                 the listener
        @return: C{True} if the adding was successful. C{False} if the
                 adding was unsuccessful, or C{listener} is C{None}.
        """
        if isinstance(listener, RefreshListener):
            self._refreshListeners.append(listener)
        else:
            super(Refresher, self).addListener(listener, iface)


    def removeListener(self, listener, iface=None):
        """Removes a L{RefreshListener} from this instance.

        @param listener:
                 the listener to be removed.
        @return: C{True} if removal was successful. A C{False} most often
                 means that C{listener} wasn't added to this instance to
                 begin with.
        """
        if isinstance(listener, RefreshListener):
            self._refreshListeners.remove(listener)
        else:
            super(Refresher, self).removeListener(listener, iface)


class RefreshListener(object):

    def refresh(self, source):
        pass
