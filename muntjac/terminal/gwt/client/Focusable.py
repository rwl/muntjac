# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class Focusable(object):
    """GWT's HasFocus is way too overkill for just receiving focus in simple
    components. Vaadin uses this interface in addition to GWT's HasFocus to pass
    focus requests from server to actual ui widgets in browsers.

    So in to make your server side focusable component receive focus on client
    side it must either implement this or HasFocus interface.
    """

    def focus(self):
        """Sets focus to this widget."""
        pass
