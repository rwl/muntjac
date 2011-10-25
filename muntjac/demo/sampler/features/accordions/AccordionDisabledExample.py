
from muntjac.terminal.theme_resource import ThemeResource

from muntjac.api import \
    VerticalLayout, HorizontalLayout, Label, Accordion, Button

from muntjac.ui import tab_sheet, button


class AccordionDisabledExample(VerticalLayout,
            tab_sheet.ISelectedTabChangeListener, button.IClickListener):

    _icon1 = ThemeResource('../sampler/icons/action_save.gif')
    _icon2 = ThemeResource('../sampler/icons/comment_yellow.gif')
    _icon3 = ThemeResource('../sampler/icons/icon_info.gif')

    def __init__(self):
        super(AccordionDisabledExample, self).__init__()

        self.setSpacing(True)

        self._l1 = Label('There are no previously saved actions.')
        self._l2 = Label('There are no saved notes.')
        self._l3 = Label('There are currently no issues.')

        self._a = Accordion()
        self._a.setHeight('300px')
        self._a.setWidth('400px')
        self._t1 = self._a.addTab(self._l1, 'Saved actions', self._icon1)
        self._t2 = self._a.addTab(self._l2, 'Notes', self._icon2)
        self._t3 = self._a.addTab(self._l3, 'Issues', self._icon3)
        self._a.addListener(self, tab_sheet.ISelectedTabChangeListener)

        self._b1 = Button('Disable \'Notes\' tab')
        self._b2 = Button('Hide \'Issues\' tab')
        self._b1.addListener(self, button.IClickListener)
        self._b2.addListener(self, button.IClickListener)

        hl = HorizontalLayout()
        hl.setSpacing(True)
        hl.addComponent(self._b1)
        hl.addComponent(self._b2)

        self.addComponent(self._a)
        self.addComponent(hl)


    def selectedTabChange(self, event):
        c = self._a.getTab(event.getTabSheet().getSelectedTab()).getCaption()
        self.getWindow().showNotification('Selected tab: ' + c)


    def buttonClick(self, event):
        if self._b1 == event.getButton():  # b1 clicked
            if self._t2.isEnabled():
                self._t2.setEnabled(False)
                self._b1.setCaption('Enable \'Notes\' tab')
            else:
                self._t2.setEnabled(True)
                self._b1.setCaption('Disable \'Notes\' tab')
        else:  # b2 clicked
            if self._t3.isVisible():
                self._t3.setVisible(False)
                self._b2.setCaption('Show \'Issues\' tab')
            else:
                self._t3.setVisible(True)
                self._b2.setCaption('Hide \'Issues\' tab')

        self._a.requestRepaint()
