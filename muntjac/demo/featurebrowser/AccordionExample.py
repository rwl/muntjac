# -*- coding: utf-8 -*-
# from com.vaadin.ui.Accordion import (Accordion,)


class AccordionExample(CustomComponent):
    """Accordion is a derivative of TabSheet, a vertical tabbed layout that places
    the tab contents between the vertical tabs.
    """

    def __init__(self):
        # Create a new accordion
        accordion = Accordion()
        self.setCompositionRoot(accordion)
        # Add a few tabs to the accordion.
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 5):
                break
            # Create a root component for a accordion tab
            layout = VerticalLayout()
            # The accordion tab label is taken from the caption of the root
            # component. Notice that layouts can have a caption too.
            layout.setCaption('Tab ' + i + 1)
            accordion.addComponent(layout)
            # Add some components in each accordion tab
            label = Label('These are the contents of Tab ' + i + 1 + '.')
            layout.addComponent(label)
            textfield = TextField('Some text field')
            layout.addComponent(textfield)
