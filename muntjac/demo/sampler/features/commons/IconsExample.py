
from muntjac.api import VerticalLayout, Button, Label, Panel, Link
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.terminal.external_resource import ExternalResource


class IconsExample(VerticalLayout):

    def __init__(self):
        super(IconsExample, self).__init__()

        self.setSpacing(True)

        # Button w/ icon
        button = Button('Save')
        button.setIcon(ThemeResource('../sampler/icons/action_save.gif'))
        self.addComponent(button)

        # Label
        l = Label('Icons are very handy')
        l.setCaption('Comment')
        l.setIcon(ThemeResource('../sampler/icons/comment_yellow.gif'))
        self.addComponent(l)

        # Panel w/ links
        p = Panel('Handy links')
        p.setIcon(ThemeResource('../sampler/icons/icon_info.gif'))
        self.addComponent(p)
        lnk = Link('http://vaadin.com',
                ExternalResource('http://www.vaadin.com'))
        lnk.setIcon(ThemeResource('../sampler/icons/icon_world.gif'))
        p.addComponent(lnk)
        lnk = Link('http://vaadin.com/learn',
                ExternalResource('http://www.vaadin.com/learn'))
        lnk.setIcon(ThemeResource('../sampler/icons/icon_world.gif'))
        p.addComponent(lnk)
        lnk = Link('http://dev.vaadin.com/',
                ExternalResource('http://dev.vaadin.com/'))
        lnk.setIcon(ThemeResource('../sampler/icons/icon_world.gif'))
        p.addComponent(lnk)
        lnk = Link('http://vaadin.com/forum',
                ExternalResource('http://vaadin.com/forum'))
        lnk.setIcon(ThemeResource('../sampler/icons/icon_world.gif'))
        p.addComponent(lnk)
