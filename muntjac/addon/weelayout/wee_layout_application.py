
from muntjac.api \
    import Application, Window, VerticalLayout, HorizontalLayout, \
    NativeButton, TextField, Alignment, Label

from muntjac.addon.weelayout.wee_layout import WeeLayout, Direction


class WeelayoutApplication(Application):

    def __init__(self):
        super(WeeLayout, self).__init__()

        self._core = False
        self._vertical = False


    def init(self):
        mainWindow = Window('Weelayout Application')
        self.setMainWindow(mainWindow)
        mainWindow.setContent(self.splitRecursive(1))
        self.setTheme('test')


    def splitRecursive(self, deep):
        l = None
        if self._core:
            l = VerticalLayout() if self._vertical else HorizontalLayout()
        else:
            if self._vertical:
                l = WeeLayout(Direction.VERTICAL)
            else:
                l = WeeLayout(Direction.HORIZONTAL)

        l.setSizeFull()
        if self._core:
            c = l
            b = NativeButton('One')
            b.setSizeFull()
            c.addComponent(b)
            c.setExpandRatio(b, 1)
            if deep > 0:
                deep -= 1
                c2 = self.splitRecursive(deep)
                c.addComponent(c2)
                c.setExpandRatio(c2, 9)
        else:
            wl = l
            wl.setClipping(True)
            b = NativeButton('Button')
            b.setSizeFull()
            if self._vertical:
                b.setHeight('10%')
            else:
                b.setWidth('10%')

            l.addComponent(b)
            if deep > 0:
                deep -= 1
                w = self.splitRecursive(deep)
                if self._vertical:
                    w.setHeight('90%')
                else:
                    w.setWidth('90%')

                l.addComponent(w)
            else:
                b.setSizeFull()

        return l


    def undefinedWithRelativeSizes(self):
        wl = WeeLayout(Direction.VERTICAL)
        wl.setHeight('100%')
        wl.addComponent()


        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                event.getButton().setCaption('Long caption' if event.getButton().getCaption() is None else None)


        _0_ = _0_()
        NativeButton('With long caption', _0_)
#        '100%', '30px', Alignment.TOP_LEFT)

        b = NativeButton('Two')
        b.addStyleName('test')
        wl.addComponent(b, '100%', '100%', Alignment.TOP_LEFT)
        wl.setSmartRelativeSizes(True)
        return wl

    def splitView(self):
        wl = WeeLayout(Direction.HORIZONTAL)
        wl.setSizeFull()
        wl.addComponent()


        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                event.getButton().setWidth('300px')


        _0_ = _0_()
        NativeButton('One', _0_)
#        '100px', '30px', Alignment.TOP_RIGHT)

        wl.addComponent(Label(''), '14px', '14px', Alignment.TOP_CENTER)
        wl.addComponent(NativeButton('Two'), '100%', '100%', Alignment.TOP_CENTER)
        # wl.setClipping(true);
        return wl


    def createVertical(self, recurse):
        wl = WeeLayout(Direction.VERTICAL)
        wl.setSizeFull()
        # wl.setWidth("100%");
        # wl.setHeight("50%");
        wl.addComponent(TextField('Left'), Alignment.TOP_LEFT)
        wl.addComponent(TextField('Center'), Alignment.TOP_CENTER)
        tf = TextField('Right')
        tf.setWidth('50%')
        wl.addComponent(tf, Alignment.TOP_RIGHT)
        if recurse > 0:
            recurse -= 1
            wl.addComponent(self.createHorizontal(recurse))
        return wl


    def createHorizontal(self, recurse):
        wl = WeeLayout(Direction.HORIZONTAL)
        wl.setSizeFull()
        # wl.setHeight("100%");
        wl.addComponent(TextField('Top'), Alignment.TOP_LEFT)
        wl.addComponent(TextField('Middle'), Alignment.MIDDLE_LEFT)
        tf = TextField('Bottom')
        tf.setHeight('50%')
        wl.addComponent(tf, Alignment.BOTTOM_LEFT)
        if recurse > 0:
            recurse -= 1
            wl.addComponent(self.createVertical(recurse))
        return wl


    def createCoreVertical(self, recurse):
        """Same with core layouts"""
        l = VerticalLayout()
        l.setSizeFull()
        tf = TextField('Left')
        l.addComponent(tf)
        l.setComponentAlignment(tf, Alignment.TOP_LEFT)
        tf = TextField('Center')
        l.addComponent(tf)
        l.setComponentAlignment(tf, Alignment.TOP_CENTER)
        tf = TextField('Right')
        l.addComponent(tf)
        tf.setWidth('50%')
        l.setComponentAlignment(tf, Alignment.TOP_RIGHT)
        if recurse > 0:
            recurse -= 1
            createCoreHorizontal = self.createCoreHorizontal(recurse)
            l.addComponent(createCoreHorizontal)
            l.setExpandRatio(createCoreHorizontal, 1)
        return l


    def createCoreHorizontal(self, recurse):
        l = HorizontalLayout()
        l.setSizeFull()
        tf = TextField('Top')
        l.addComponent(tf)
        l.setComponentAlignment(tf, Alignment.TOP_LEFT)
        tf = TextField('Middle')
        l.addComponent(tf)
        l.setComponentAlignment(tf, Alignment.MIDDLE_LEFT)
        tf = TextField('Bottom')
        l.addComponent(tf)
        tf.setWidth('50%')
        l.setComponentAlignment(tf, Alignment.BOTTOM_LEFT)
        if recurse > 0:
            recurse -= 1
            createCoreVertical = self.createCoreVertical(recurse)
            l.addComponent(createCoreVertical)
            l.setExpandRatio(createCoreVertical, 1)
        return l
