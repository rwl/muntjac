
from muntjac.ui import VerticalLayout, GridLayout, CheckBox, button, Button


class LayoutSpacingExample(VerticalLayout):

    def __init__(self):
        # Create a grid layout.
        grid = GridLayout(3, 3)

        # Enable spacing for the example layout (this is the one we'll toggle
        # with the checkbox)
        grid.setSpacing(True)

        # CheckBox for toggling spacing on and off
        spacing = CheckBox('Spacing enabled')
        spacing.setValue(True)
        spacing.setImmediate(True)

        class SpacingListener(button.IClickListener):

            def __init__(self, grid):
                self._grid = grid

            def buttonClick(self, event):
                self._grid.setSpacing(bool(self.spacing))

        spacing.addListener(SpacingListener(grid))
        self.addComponent(spacing)

        # Add the layout to the containing layout.
        self.addComponent(grid)

        # Populate the layout with components.
        for i in range(9):
            grid.addComponent(Button('Component ' + i + 1))

        self.setSpacing(True)  # enable spacing for the example itself
