# -*- coding: utf-8 -*-
# from com.vaadin.ui.CssLayout import (CssLayout,)
# from com.vaadin.ui.Panel import (Panel,)


class ExamplePanel(Panel):

    def __init__(self):
        super(ExamplePanel, self)(CssLayout())
        self.setWidth('100%')
        self.setHeight('500px')
        self.getContent().setSizeFull()
