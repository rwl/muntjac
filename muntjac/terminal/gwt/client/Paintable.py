# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class Paintable(object):
    """An interface used by client-side widgets or paintable parts to receive
    updates from the corresponding server-side components in the form of
    {@link UIDL}.

    Updates can be sent back to the server using the
    {@link ApplicationConnection#updateVariable()} methods.
    """

    def updateFromUIDL(self, uidl, client):
        pass
