# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class VHasDropHandler(object):
    """Used to detect Widget from widget tree that has {@link #getDropHandler()}

    Decide whether to get rid of this class. If so, {@link VAbstractDropHandler}
    must extend {@link Paintable}.
    """

    def getDropHandler(self):
        pass
