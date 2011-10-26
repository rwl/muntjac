
from muntjac.api import VerticalLayout, GridLayout, Button, Alignment
from muntjac.terminal.gwt.client.ui.alignment_info import Bits


class LayoutAlignmentExample(VerticalLayout):

    def __init__(self):
        super(LayoutAlignmentExample, self).__init__()

        # Create a grid layout
        grid = GridLayout(1, 9)
        grid.setSpacing(True)

        # The style allows us to visualize the cell borders in this example.
        grid.addStyleName('gridexample')

        grid.setWidth('300px')
        grid.setHeight('500px')

        # Put a component in each cell with respective alignment.
        # We'll use different ways to set the alignment: constants, bitmasks,
        # and string-shorthand.

        # Here we use the shorthand constants to set the alignment:
        # Alignment.TOP_LEFT, Alignment.TOP_CENTER, Alignment.TOP_RIGHT
        # Alignment.MIDDLE_LEFT, Alignment.MIDDLE_CENTER,
        # Alignment.MIDDLE_RIGHT
        # Alignment.BOTTOM_LEFT, Alignment.BOTTOM_CENTER,
        # Alignment.BOTTOM_RIGHT

        topleft = Button('Top Left')
        grid.addComponent(topleft)
        grid.setComponentAlignment(topleft, Alignment.TOP_LEFT)

        topcenter = Button('Top Center')
        grid.addComponent(topcenter)
        grid.setComponentAlignment(topcenter, Alignment.TOP_CENTER)

        topright = Button('Top Right')
        grid.addComponent(topright)
        grid.setComponentAlignment(topright, Alignment.TOP_RIGHT)

        # Here we use bit additions to set the alignment:
        # Bits.ALIGNMENT_LEFT, Bits.ALIGNMENT_RIGHT
        # Bits.ALIGNMENT_TOP, Bits.ALIGNMENT_BOTTOM
        # Bits.ALIGNMENT_VERTICAL_CENTER, Bits.ALIGNMENT_HORIZONTAL_CENTER

        middleleft = Button('Middle Left')
        grid.addComponent(middleleft)
        grid.setComponentAlignment(middleleft, Alignment(
            Bits.ALIGNMENT_VERTICAL_CENTER | Bits.ALIGNMENT_LEFT))

        middlecenter = Button('Middle Center')
        grid.addComponent(middlecenter)
        grid.setComponentAlignment(middlecenter, Alignment(
            Bits.ALIGNMENT_VERTICAL_CENTER | Bits.ALIGNMENT_HORIZONTAL_CENTER))

        middleright = Button('Middle Right')
        grid.addComponent(middleright)
        grid.setComponentAlignment(middleright, Alignment(
            Bits.ALIGNMENT_VERTICAL_CENTER | Bits.ALIGNMENT_RIGHT))

        # Here we'll use the convenient string-shorthand:

        bottomleft = Button('Bottom Left')
        grid.addComponent(bottomleft)
        grid.setComponentAlignment(bottomleft, Alignment.BOTTOM_LEFT)

        bottomcenter = Button('Bottom Center')
        grid.addComponent(bottomcenter)
        grid.setComponentAlignment(bottomcenter, Alignment.BOTTOM_CENTER)

        bottomright = Button('Bottom Right')
        grid.addComponent(bottomright)
        grid.setComponentAlignment(bottomright, Alignment.BOTTOM_RIGHT)

        # Add the layout to the containing layout.
        self.addComponent(grid)

        # Align the grid itself within its container layout.
        self.setComponentAlignment(grid, Alignment.MIDDLE_CENTER)
