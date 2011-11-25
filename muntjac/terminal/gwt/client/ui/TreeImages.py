# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.google.gwt.user.client.ui.AbstractImagePrototype import (AbstractImagePrototype,)
import pyjamas.ui.TreeImages


class TreeImages(pyjamas.ui.TreeImages.TreeImages):

    def treeOpen(self):
        """An image indicating an open branch.

        @return a prototype of this image
        @gwt.resource com/vaadin/terminal/gwt/public/default/tree/img/expanded
                      .png
        """
        pass

    def treeClosed(self):
        """An image indicating a closed branch.

        @return a prototype of this image
        @gwt.resource com/vaadin/terminal/gwt/public/default/tree/img/collapsed
                      .png
        """
        pass
