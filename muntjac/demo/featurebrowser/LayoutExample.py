# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class LayoutExample(CustomComponent):
    """A few examples of layout possibilities.

    @author IT Mill Ltd.
    """

    def __init__(self):
        main = VerticalLayout()
        main.setMargin(True)
        self.setCompositionRoot(main)
        g = GridLayout(2, 5)
        g.setWidth('100%')
        main.addComponent(g)
        # panel
        p = Panel('This is a normal panel')
        l = Label('A normal panel.')
        p.addComponent(l)
        g.addComponent(p)
        # lightpanel
        p = Panel('This is a light panel')
        p.setStyleName(Reindeer.PANEL_LIGHT)
        l = Label('A light-style panel.')
        p.addComponent(l)
        g.addComponent(p)
        ts = TabSheet()
        g.addComponent(ts, 0, 1, 1, 1)
        ol = VerticalLayout()
        ol.setMargin(True)
        ol.addComponent(Label('Component 1'))
        ol.addComponent(Label('Component 2'))
        ol.addComponent(Label('Component 3'))
        ts.addTab(ol, 'Vertical OrderedLayout', None)
        hl = HorizontalLayout()
        hl.setMargin(True)
        hl.addComponent(Label('Component 1'))
        hl.addComponent(Label('Component 2'))
        hl.addComponent(Label('Component 3'))
        ts.addTab(hl, 'Horizontal OrderedLayout', None)
        gl = GridLayout(3, 3)
        gl.setMargin(True)
        gl.addComponent(Label('Component 1.1'))
        gl.addComponent(Label('Component 1.2'))
        gl.addComponent(Label('Component 1.3'))
        gl.addComponent(Label('Component 2.2'), 1, 1)
        gl.addComponent(Label('Component 3.1'), 0, 2)
        gl.addComponent(Label('Component 3.3'), 2, 2)
        ts.addTab(gl, 'GridLayout', None)
        # - TODO spitpanel removed for now - do we need it here?
        #         ts = new TabSheet();
        #         ts.setHeight(150);
        #         g.addComponent(ts, 0, 2, 1, 2);
        # 
        #         SplitPanel sp = new SplitPanel();
        #         sp.addComponent(new Label("Component 1"));
        #         sp.addComponent(new Label("Component 2"));
        #         ts.addTab(sp, "Vertical SplitPanel", null);
        # 
        #         sp = new SplitPanel(SplitPanel.ORIENTATION_HORIZONTAL);
        #         sp.addComponent(new Label("Component 1"));
        #         sp.addComponent(new Label("Component 2"));
        #         ts.addTab(sp, "Horizontal SplitPanel", null);
        #         -
