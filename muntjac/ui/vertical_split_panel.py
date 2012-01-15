# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Defines a panel that contains two components and lays them out
vertically."""

from muntjac.ui.abstract_split_panel import AbstractSplitPanel


class VerticalSplitPanel(AbstractSplitPanel):
    """A vertical split panel contains two components and lays them
    vertically. The first component is above the second component::

         +--------------------------+
         |                          |
         |  The first component     |
         |                          |
         +==========================+  <-- splitter
         |                          |
         |  The second component    |
         |                          |
         +--------------------------+
    """

    CLIENT_WIDGET = None #ClientWidget(VSplitPanelVertical, LoadStyle.EAGER)

    def __init__(self):
        super(VerticalSplitPanel, self).__init__()
        self.setSizeFull()
