
from muntjac.api import VerticalLayout, GridLayout, CheckBox, Button
from muntjac.ui.button import IClickListener


class LayoutSpacingExample(VerticalLayout, IClickListener):

    def __init__(self):
        super(LayoutSpacingExample, self).__init__()

        # Create a grid layout.
        self.grid = GridLayout(3, 3)

        # Enable sp for the example layout (this is the one we'll toggle
        # with the checkbox)
        self.grid.setSpacing(False)

        # CheckBox for toggling sp on and off
        self.sp = CheckBox("Spacing enabled")
#        self.sp.setValue(True)  # FIXME:
        self.sp.setImmediate(True)

        self.sp.addListener(self, IClickListener)
        self.addComponent(self.sp)

        # Add the layout to the containing layout.
        self.addComponent(self.grid)

        # Populate the layout with components.
        for i in range(9):
            self.grid.addComponent(Button('Component %d' % (i + 1)))

        self.setSpacing(True)  # enable sp for the example itself


    def buttonClick(self, event):
        enabled = self.sp.booleanValue()
        self.grid.setSpacing(enabled)
