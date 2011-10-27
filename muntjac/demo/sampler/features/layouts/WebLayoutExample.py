
from muntjac.demo.sampler.ExampleUtil import ExampleUtil

from muntjac.api import \
    VerticalLayout, Button, Label, HorizontalLayout, Tree, Window, Table

from muntjac.ui import window, button


class WebLayoutExample(VerticalLayout):

    def __init__(self):
        super(VerticalLayout, self).__init__()

        self._win = WebLayoutWindow()
        self._open = Button('Open sample in subwindow')

        self.setMargin(True)

        # We'll open this example in a separate window, configure it
        self._win.setWidth('70%')
        self._win.setHeight('70%')
        self._win.center()

        # Allow opening window again when closed
        self._win.addListener(WindowListener(self), window.ICloseListener)

        # 'open sample' button
        self.addComponent(self._open)

        self._open.addListener(OpenListener(self), button.IClickListener)
        self.addComponent(Label('Don\'t worry: the content of the window '
                'is not supposed to make sense...'))


class WindowListener(window.ICloseListener):

    def __init__(self, c):
        self._c = c

    def windowClose(self, e):
        self._c._open.setEnabled(True)


class OpenListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c.getWindow().addWindow(self._c._win)
        self._c._open.setEnabled(False)


class WebLayoutWindow(Window):

    def __init__(self):
        super(WebLayoutWindow, self).__init__()

        # Our main layout is a horizontal layout
        main = HorizontalLayout()
        main.setMargin(True)
        main.setSpacing(True)
        self.setContent(main)

        # Tree to the left
        tree = Tree()
        tree.setContainerDataSource( ExampleUtil.getHardwareContainer() )
        tree.setItemCaptionPropertyId( ExampleUtil.hw_PROPERTY_NAME )
        for idd in tree.rootItemIds():
            tree.expandItemsRecursively(idd)
        self.addComponent(tree)

        # vertically divide the right area
        left = VerticalLayout()
        left.setSpacing(True)
        self.addComponent(left)

        # table on top
        tbl = Table()
        tbl.setWidth('500px')
        tbl.setContainerDataSource( ExampleUtil.getISO3166Container() )
        tbl.setSortDisabled(True)
        tbl.setPageLength(7)
        left.addComponent(tbl)

        # Label on bottom
        text = Label(ExampleUtil.lorem, Label.CONTENT_XHTML)
        text.setWidth('500px')  # some limit is good for text
        left.addComponent(text)
