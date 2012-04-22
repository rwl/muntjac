# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.ui.abstract_ordered_layout import AbstractOrderedLayout


class VerticalLayout(AbstractOrderedLayout):
    """Vertical layout.

    C{VerticalLayout} is a component container, which shows the
    subcomponents in the order of their addition (vertically). A vertical
    layout is by default 100% wide.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    """

    CLIENT_WIDGET = None #ClientWidget(VVerticalLayout, LoadStyle.EAGER)

    def __init__(self):
        super(VerticalLayout, self).__init__()

        self.setWidth('100%')
