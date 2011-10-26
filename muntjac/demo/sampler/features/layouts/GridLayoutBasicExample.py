
from muntjac.api import VerticalLayout, GridLayout, Button, Alignment
from muntjac.terminal.sizeable import ISizeable


class GridLayoutBasicExample(VerticalLayout):

    def __init__(self):
        super(GridLayoutBasicExample, self).__init__()

        # Create a grid layout
        grid = GridLayout(3, 3)
        grid.setSpacing(True)

        # The style allows us to visualize the cell borders in this example.
        grid.addStyleName('gridexample')

        grid.setWidth(400, ISizeable.UNITS_PIXELS)
        grid.setHeight(400, ISizeable.UNITS_PIXELS)

        # First we insert four components that occupy one cell each
        topleft = Button('Top Left')
        grid.addComponent(topleft, 0, 0)
        grid.setComponentAlignment(topleft, Alignment.MIDDLE_CENTER)

        topcenter = Button('Top Center')
        grid.addComponent(topcenter, 1, 0)
        grid.setComponentAlignment(topcenter, Alignment.MIDDLE_CENTER)

        bottomleft = Button('Bottom Left')
        grid.addComponent(bottomleft, 0, 2)
        grid.setComponentAlignment(bottomleft, Alignment.MIDDLE_CENTER)

        bottomcenter = Button('Bottom Center')
        grid.addComponent(bottomcenter, 1, 2)
        grid.setComponentAlignment(bottomcenter, Alignment.MIDDLE_CENTER)

        # Insert a component that occupies all the rightmost cells
        topright = Button('Extra height')
        grid.addComponent(topright, 2, 0, 2, 2)
        grid.setComponentAlignment(topright, Alignment.MIDDLE_CENTER)

        # Insert a component that occupies two cells in horizontal direction
        middleleft = Button('This is a wide cell in GridLayout')
        grid.addComponent(middleleft, 0, 1, 1, 1)
        grid.setComponentAlignment(middleleft, Alignment.MIDDLE_CENTER)

        # Add the layout to the containing layout.
        self.addComponent(grid)

        # Align the grid itself within its container layout.
        self.setComponentAlignment(grid, Alignment.MIDDLE_CENTER)
