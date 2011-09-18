# -*- coding: utf-8 -*-
from com.vaadin.ui.AbstractSplitPanel import (AbstractSplitPanel,)


class VerticalSplitPanel(AbstractSplitPanel):
    """A vertical split panel contains two components and lays them vertically. The
    first component is above the second component.

    <pre>
         +--------------------------+
         |                          |
         |  The first component     |
         |                          |
         +==========================+  <-- splitter
         |                          |
         |  The second component    |
         |                          |
         +--------------------------+
    </pre>
    """

    def __init__(self):
        super(VerticalSplitPanel, self)()
        self.setSizeFull()
