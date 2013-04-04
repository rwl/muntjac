# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.


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
