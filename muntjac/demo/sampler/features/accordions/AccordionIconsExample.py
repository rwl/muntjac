
from muntjac.ui import HorizontalLayout, Accordion, tab_sheet, Label
from muntjac.terminal.theme_resource import ThemeResource


class AccordionIconsExample(HorizontalLayout,
            tab_sheet.ISelectedTabChangeListener):

    _icon1 = ThemeResource('../sampler/icons/action_save.gif')
    _icon2 = ThemeResource('../sampler/icons/comment_yellow.gif')
    _icon3 = ThemeResource('../sampler/icons/icon_info.gif')

    def __init__(self):
        self.setSpacing(True)

        l1 = Label('There are no previously saved actions.')
        l2 = Label('There are no saved notes.')
        l3 = Label('There are currently no issues.')

        self._a = Accordion()
        self._a.setHeight('300px')
        self._a.setWidth('400px')
        self._a.addTab(l1, 'Saved actions', self._icon1)
        self._a.addTab(l2, 'Notes', self._icon2)
        self._a.addTab(l3, 'Issues', self._icon3)
        self._a.addListener(self)

        self.addComponent(self._a)


    def selectedTabChange(self, event):
        tabsheet = event.getTabSheet()
        tab = tabsheet.getTab(tabsheet.getSelectedTab())
        if tab is not None:
            self.getWindow().showNotification('Selected tab: '
                    + tab.getCaption())
