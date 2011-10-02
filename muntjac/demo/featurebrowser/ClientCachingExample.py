# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.vaadin.terminal.PaintException import (PaintException,)
# from com.vaadin.terminal.PaintTarget import (PaintTarget,)
# from com.vaadin.ui.Layout import (Layout,)
# from com.vaadin.ui.TabSheet import (TabSheet,)
# from com.vaadin.ui.VerticalLayout import (VerticalLayout,)


class ClientCachingExample(CustomComponent):
    """This example is a (simple) demonstration of client-side caching. The content
    in one tab is intentionally made very slow to produce server-side. When the
    user changes to this tab for the first time, there will be a 3 second wait
    before the content shows up, but the second time it shows up immediately
    since the content has not changed and is cached client-side.
     *
    @author IT Mill Ltd.
    """
    _msg = 'This example is a (simple) demonstration of client-side caching.' + ' The content in one tab is intentionally made very slow to' + ' \'produce\' server-side. When you changes to this tab for the' + ' first time, there will be a 3 second wait before the content' + ' shows up, but the second time it shows up immediately since the' + ' content has not changed and is cached client-side.'

    def __init__(self):
        main = VerticalLayout()
        main.setMargin(True)
        self.setCompositionRoot(main)
        main.addComponent(Label(self._msg))
        ts = TabSheet()
        main.addComponent(ts)
        layout = VerticalLayout()
        layout.setMargin(True)
        l = Label('This is a normal label, quick to render.')
        l.setCaption('A normal label')
        layout.addComponent(l)
        ts.addTab(layout, 'Normal', None)
        layout = VerticalLayout()
        layout.setMargin(True)

        class _0_(Label):

            def paintContent(self, target):
                # IGNORED
                try:
                    self.Thread.sleep(3000)
                except Exception, e:
                    pass # astStmt: [Stmt([]), None]
                super(_0_, self).paintContent(target)

        _0_ = _0_()
        l = _0_
        l.setCaption('A slow label')
        layout.addComponent(l)
        ts.addTab(layout, 'Slow', None)
