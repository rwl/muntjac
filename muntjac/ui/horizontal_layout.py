# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.ui.abstract_ordered_layout import AbstractOrderedLayout


class HorizontalLayout(AbstractOrderedLayout):
    """Horizontal layout.

    C{HorizontalLayout} is a component container, which shows
    the subcomponents in the order of their addition (horizontally).

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    """

    CLIENT_WIDGET = None #ClientWidget(VHorizontalLayout, LoadStyle.EAGER)

    def __init__(self):
        super(HorizontalLayout, self).__init__()
