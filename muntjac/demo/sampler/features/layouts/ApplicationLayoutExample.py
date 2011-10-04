# -*- coding: utf-8 -*-
from muntjac.demo.sampler.ExampleUtil import (ExampleUtil,)
# from com.vaadin.ui.themes.Reindeer import (Reindeer,)


class ApplicationLayoutExample(VerticalLayout):
    _win = ApplicationLayoutWindow()
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
                ApplicationLayoutExample_this._open.setEnabled(True)

        _0_ = _0_()
        self._win.addListener(_0_)
        # 'open sample' button
        self.addComponent(self._open)

        class _1_(Button.ClickListener):

            def buttonClick(self, event):
                self.getWindow().addWindow(ApplicationLayoutExample_this._win)
                ApplicationLayoutExample_this._open.setEnabled(False)

        _1_ = _1_()
        self._open.addListener(_1_)
        self.addComponent(ALabel('Don\'t worry: the content of the window is not supposed to make sense...'))

    class ApplicationLayoutWindow(Window):

        def __init__(self):
            # Our main layout is a horizontal layout
            main = HorizontalLayout()
            main.setSizeFull()
            self.setContent(main)
            # Tree to the left
            treePanel = Panel()
            # for scrollbars
            treePanel.setStyleName(Reindeer.PANEL_LIGHT)
            treePanel.setHeight('100%')
            treePanel.setWidth(None)
            treePanel.getContent().setSizeUndefined()
            self.addComponent(treePanel)
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
            treePanel.addComponent(tree)
            # vertically divide the right area
            left = VerticalLayout()
            left.setSizeFull()
            self.addComponent(left)
            main.setExpandRatio(left, 1.0)
            # use all available space
            # table on top
            tbl = Table()
            tbl.setWidth('100%')
            tbl.setContainerDataSource(ExampleUtil.getISO3166Container())
            tbl.setSortDisabled(True)
            tbl.setPageLength(7)
            left.addComponent(tbl)
            # Label on bottom
            textPanel = Panel()
            # for scrollbars
            textPanel.setStyleName(Reindeer.PANEL_LIGHT)
            textPanel.setSizeFull()
            left.addComponent(textPanel)
            left.setExpandRatio(textPanel, 1.0)
            # use all available space
            text = ALabel(ExampleUtil.lorem, ALabel.CONTENT_XHTML)
            text.setWidth('500px')
            # some limit is good for text
            textPanel.addComponent(text)
