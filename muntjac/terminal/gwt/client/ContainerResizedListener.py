# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class ContainerResizedListener(object):
    """ContainerResizedListener interface is useful for Widgets that support
    relative sizes and who need some additional sizing logic.
    """

    def iLayout(self):
        """This function is run when container box has been resized. Object
        implementing ContainerResizedListener is responsible to call the same
        function on its ancestors that implement NeedsLayout in case their
        container has resized. runAnchestorsLayout(HasWidgets parent) function
        from Util class may be a good helper for this.
        """
        pass
