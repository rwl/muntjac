
from muntjac.ui.themes import Reindeer

from muntjac.api import \
    (VerticalLayout, Button, Label, Window, HorizontalLayout,
     Panel, Tree, Table)

from muntjac.ui.window import ICloseListener
from muntjac.ui.button import IClickListener

from muntjac.demo.sampler.ExampleUtil import ExampleUtil


class ApplicationLayoutExample(VerticalLayout):

    def __init__(self):
        super(ApplicationLayoutExample, self).__init__()

        self.setMargin(True)

        self._win = ApplicationLayoutWindow()
        self._open = Button('Open sample in subwindow')

        # We'll open this example in a separate window, configure it
        self._win.setWidth('70%')
        self._win.setHeight('70%')
        self._win.center()

        self._win.addListener(WindowCloseListener(self), ICloseListener)
        # 'open sample' button
        self.addComponent(self._open)

        self._open.addListener(ClickListener(self), IClickListener)
        self.addComponent(Label('Don\'t worry: the content of the window '
                'is not supposed to make sense...'))


class WindowCloseListener(ICloseListener):

    def __init__(self, c):
        self._c = c

    def windowClose(self, e):
        # Allow opening window again when closed
        self._c._open.setEnabled(True)


class ClickListener(IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c.getWindow().addWindow(self._c._win)
        self._c._open.setEnabled(False)


class ApplicationLayoutWindow(Window):

    def __init__(self):
        super(ApplicationLayoutWindow, self).__init__()

        # Our main layout is a horizontal layout
        main = HorizontalLayout()
        main.setSizeFull()
        self.setContent(main)

        # Tree to the left
        treePanel = Panel()  # for scrollbars
        treePanel.setStyleName(Reindeer.PANEL_LIGHT)
        treePanel.setHeight('100%')
        treePanel.setWidth(None)
        treePanel.getContent().setSizeUndefined()
        self.addComponent(treePanel)

        tree = Tree()
        tree.setContainerDataSource(ExampleUtil.getHardwareContainer())
        tree.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
        for idd in tree.rootItemIds():
            tree.expandItemsRecursively(idd)
        treePanel.addComponent(tree)

        # vertically divide the right area
        left = VerticalLayout()
        left.setSizeFull()
        self.addComponent(left)
        main.setExpandRatio(left, 1.0)  # use all available space

        # table on top
        tbl = Table()
        tbl.setWidth('100%')
        tbl.setContainerDataSource(ExampleUtil.getISO3166Container())
        tbl.setSortDisabled(True)
        tbl.setPageLength(7)
        left.addComponent(tbl)

        # Label on bottom
        textPanel = Panel()  # for scrollbars
        textPanel.setStyleName(Reindeer.PANEL_LIGHT)
        textPanel.setSizeFull()
        left.addComponent(textPanel)
        left.setExpandRatio(textPanel, 1.0)  # use all available space

        text = Label(ExampleUtil.lorem, Label.CONTENT_XHTML)
        text.setWidth('500px')  # some limit is good for text
        textPanel.addComponent(text)
