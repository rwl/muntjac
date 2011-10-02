# -*- coding: utf-8 -*-
# from com.vaadin.ui.CheckBox import (CheckBox,)


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

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                self.grid.setSpacing(self.spacing.booleanValue())

        _0_ = _0_()
        spacing.addListener(_0_)
        self.addComponent(spacing)
        # Add the layout to the containing layout.
        self.addComponent(grid)
        # Populate the layout with components.
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 9):
                break
            grid.addComponent(Button('Component ' + i + 1))
        self.setSpacing(True)
        # enable spacing for the example itself
