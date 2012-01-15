# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Defines a component container, that can contain two components which are
split by divider element."""

from muntjac.ui.abstract_split_panel import AbstractSplitPanel


class SplitPanel(AbstractSplitPanel):
    """SplitPanel.

    C{SplitPanel} is a component container, that can contain two
    components (possibly containers) which are split by divider element.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    @deprecated: Use L{HorizontalSplitPanel} or L{VerticalSplitPanel} instead.
    """

    CLIENT_WIDGET = None #ClientWidget(VSplitPanelHorizontal, LoadStyle.EAGER)

    #: Components are to be laid out vertically.
    ORIENTATION_VERTICAL = 0

    #: Components are to be laid out horizontally.
    ORIENTATION_HORIZONTAL = 1


    def __init__(self, orientation=None):
        """Creates a new split panel. The orientation of the panels is
        C{ORIENTATION_VERTICAL} by default.

        @param orientation:
                   the orientation of the layout.
        """
        super(SplitPanel, self).__init__()

        # Orientation of the layout.
        if orientation is None:
            self._orientation = self.ORIENTATION_VERTICAL
        else:
            self.setOrientation(orientation)

        self.setSizeFull()


    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   the Paint Event.
        @raise PaintException:
                    if the paint operation failed.
        """
        super(SplitPanel, self).paintContent(target)
        if self._orientation == self.ORIENTATION_VERTICAL:
            target.addAttribute('vertical', True)


    def getOrientation(self):
        """Gets the orientation of the split panel.

        @return: the Value of property orientation.
        """
        return self._orientation


    def setOrientation(self, orientation):
        """Sets the orientation of the split panel.

        @param orientation:
                   the New value of property orientation.
        """
        # Checks the validity of the argument
        if (orientation < self.ORIENTATION_VERTICAL
                or orientation > self.ORIENTATION_HORIZONTAL):
            raise ValueError

        self._orientation = orientation
        self.requestRepaint()
