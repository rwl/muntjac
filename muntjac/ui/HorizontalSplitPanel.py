# -*- coding: utf-8 -*-
from com.vaadin.ui.AbstractSplitPanel import (AbstractSplitPanel,)


class HorizontalSplitPanel(AbstractSplitPanel):
    """A horizontal split panel contains two components and lays them horizontally.
    The first component is on the left side.

    <pre>

         +---------------------++----------------------+
         |                     ||                      |
         | The first component || The second component |
         |                     ||                      |
         +---------------------++----------------------+

                               ^
                               |
                         the splitter

    </pre>

    @author Vaadin Ltd.
    @version
    @VERSION@
    @since 6.5
    """

    def __init__(self):
        super(HorizontalSplitPanel, self)()
        self.setSizeFull()
