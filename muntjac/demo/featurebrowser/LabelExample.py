# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.vaadin.ui.CustomComponent import (CustomComponent,)
# from com.vaadin.ui.GridLayout import (GridLayout,)
# from com.vaadin.ui.Label import (Label,)
# from com.vaadin.ui.Panel import (Panel,)
# from com.vaadin.ui.themes.Reindeer import (Reindeer,)


class LabelExample(CustomComponent):
    """Shows a few variations of Labels, including the effects of XHTML- and
    pre-formatted mode.
     *
    @author IT Mill Ltd.
    """
    _xhtml = 'This text has <b>HTML</b> formatting.<br/>' + 'A plain <i>Label</i> will show the markup, while a <u>XHTML-mode</u>' + ' <i>Label</i> will show the formatted text.'
    _pre = 'This text has linebreaks.\n\n' + 'They will show up in a preformatted Label,\n' + 'but not in a \"plain\" Label.\n\n' + '       This is an indented row. \n       Same indentation here.'

    def __init__(self):
        g = GridLayout(2, 4)
        g.setMargin(True)
        self.setCompositionRoot(g)
        g.setWidth('100%')
        # plain w/o caption
        p = self.getExpamplePanel('Plain')
        l = Label('A plain label without caption.')
        p.addComponent(l)
        g.addComponent(p)
        # plain w/ caption
        p = self.getExpamplePanel('Plain w/ caption + tooltip')
        l = Label('A plain label with caption.')
        l.setCaption('Label caption')
        l.setDescription('This is a description (tooltip) for the label.')
        p.addComponent(l)
        g.addComponent(p)
        # plain w/ xhtml
        p = self.getExpamplePanel('Plain w/ XHTML content')
        l = Label(self._xhtml)
        p.addComponent(l)
        g.addComponent(p)
        # xhtml w/ xhtml
        p = self.getExpamplePanel('XHTML-mode w/ XHTML content')
        l = Label(self._xhtml)
        # l.setContentMode(Label.CONTENT_XHTML);
        p.addComponent(l)
        g.addComponent(p)
        # plain w/ preformatted
        p = self.getExpamplePanel('Plain w/ preformatted content')
        l = Label(self._pre)
        p.addComponent(l)
        g.addComponent(p)
        # preformatted w/ preformatted
        p = self.getExpamplePanel('Preformatted-mode w/ preformatted content')
        l = Label(self._pre)
        # l.setContentMode(Label.CONTENT_PREFORMATTED);
        p.addComponent(l)
        g.addComponent(p)

    def getExpamplePanel(self, caption):
        p = Panel(caption)
        p.addStyleName(Reindeer.PANEL_LIGHT)
        return p
