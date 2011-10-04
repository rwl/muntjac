# -*- coding: utf-8 -*-
from muntjac.demo.sampler.ExampleUtil import (ExampleUtil,)
# from com.vaadin.ui.ALabel import (ALabel,)
# from com.vaadin.ui.Button import (Button,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)
# from com.vaadin.ui.Table import (Table,)
# from com.vaadin.ui.Tree import (Tree,)
# from com.vaadin.ui.Window import (Window,)
# from com.vaadin.ui.Window.CloseEvent import (CloseEvent,)
# from java.util.Iterator import (Iterator,)


class WebLayoutExample(VerticalLayout):
    _win = WebLayoutWindow()
    _open = Button('Open sample in subwindow')

    def __init__(self):
        self.setMargin(True)
        # We'll open this example in a separate window, configure it
        self._win.setWidth('70%')
        self._win.setHeight('70%')
        self._win.center()
        # Allow opening window again when closed

        class _0_(Window.CloseListener):

            def windowClose(self, e):
                WebLayoutExample_this._open.setEnabled(True)

        _0_ = _0_()
        self._win.addListener(_0_)
        # 'open sample' button
        self.addComponent(self._open)

        class _1_(Button.ClickListener):

            def buttonClick(self, event):
                self.getWindow().addWindow(WebLayoutExample_this._win)
                WebLayoutExample_this._open.setEnabled(False)

        _1_ = _1_()
        self._open.addListener(_1_)
        self.addComponent(ALabel('Don\'t worry: the content of the window is not supposed to make sense...'))

    class WebLayoutWindow(Window):

        def __init__(self):
            # Our main layout is a horiozontal layout
            main = HorizontalLayout()
            main.setMargin(True)
            main.setSpacing(True)
            self.setContent(main)
            # Tree to the left
            tree = Tree()
            tree.setContainerDataSource(ExampleUtil.getHardwareContainer())
            tree.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
            _0 = True
            it = tree.rootItemIds()
            while True:
                if _0 is True:
                    _0 = False
                if not it.hasNext():
                    break
                tree.expandItemsRecursively(it.next())
            self.addComponent(tree)
            # vertically divide the right area
            left = VerticalLayout()
            left.setSpacing(True)
            self.addComponent(left)
            # table on top
            tbl = Table()
            tbl.setWidth('500px')
            tbl.setContainerDataSource(ExampleUtil.getISO3166Container())
            tbl.setSortDisabled(True)
            tbl.setPageLength(7)
            left.addComponent(tbl)
            # Label on bottom
            text = ALabel(ExampleUtil.lorem, ALabel.CONTENT_XHTML)
            text.setWidth('500px')
            # some limit is good for text
            left.addComponent(text)
