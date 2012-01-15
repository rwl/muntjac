# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.


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
