# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Defines a panel that contains two components and lays them out
horizontally."""

from muntjac.ui.abstract_split_panel import AbstractSplitPanel


class HorizontalSplitPanel(AbstractSplitPanel):
    """A horizontal split panel contains two components and lays them
    horizontally. The first component is on the left side::

         +---------------------++----------------------+
         |                     ||                      |
         | The first component || The second component |
         |                     ||                      |
         +---------------------++----------------------+

                               ^
                               |
                         the splitter

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    """

    CLIENT_WIDGET = None #ClientWidget(VSplitPanelHorizontal, LoadStyle.EAGER)

    def __init__(self):
        super(HorizontalSplitPanel, self).__init__()
        self.setSizeFull()
