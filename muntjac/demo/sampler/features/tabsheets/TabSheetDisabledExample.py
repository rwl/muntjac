
from muntjac.api import \
    VerticalLayout, Label, TabSheet, Button, HorizontalLayout

from muntjac.ui import tab_sheet, button

from muntjac.terminal.theme_resource import ThemeResource


class TabSheetDisabledExample(VerticalLayout,
            tab_sheet.ISelectedTabChangeListener, button.IClickListener):

    _icon1 = ThemeResource('../sampler/icons/action_save.gif')
    _icon2 = ThemeResource('../sampler/icons/comment_yellow.gif')
    _icon3 = ThemeResource('../sampler/icons/icon_info.gif')

    def __init__(self):
        super(TabSheetDisabledExample, self).__init__()

        self.setSpacing(True)

        # Tab 1 content
        self._l1 = VerticalLayout()
        self._l1.setMargin(True)
        self._l1.addComponent(Label('There are no previously saved actions.'))

        # Tab 2 content
        self._l2 = VerticalLayout()
        self._l2.setMargin(True)
        self._l2.addComponent(Label('There are no saved notes.'))

        # Tab 3 content
        self._l3 = VerticalLayout()
        self._l3.setMargin(True)
        self._l3.addComponent(Label('There are currently no issues.'))

        self._t = TabSheet()
        self._t.setHeight('200px')
        self._t.setWidth('400px')

        self._t1 = self._t.addTab(self._l1, 'Saved actions', self._icon1)
        self._t2 = self._t.addTab(self._l2, 'Notes', self._icon2)
        self._t3 = self._t.addTab(self._l3, 'Issues', self._icon3)

        self._t.addListener(self, tab_sheet.ISelectedTabChangeListener)

        self._toggleEnabled = Button('Disable \'Notes\' tab')
        self._toggleEnabled.addListener(self, button.IClickListener)

        self._toggleVisible = Button('Hide \'Issues\' tab')
        self._toggleVisible.addListener(self, button.IClickListener)

        hl = HorizontalLayout()
        hl.setSpacing(True)
        hl.addComponent(self._toggleEnabled)
        hl.addComponent(self._toggleVisible)

        self.addComponent(self._t)
        self.addComponent(hl)


    def selectedTabChange(self, event):
        selected = event.getTabSheet().getSelectedTab()
        c = self._t.getTab(selected).getCaption()
        self.getWindow().showNotification('Selected tab: ' + c)


    def buttonClick(self, event):
        if self._toggleEnabled == event.getButton():
            # toggleEnabled clicked
            self._t2.setEnabled(not self._t2.isEnabled())
            if self._t2.isEnabled():
                self._toggleEnabled.setCaption('Disable \'Notes\' tab')
            else:
                self._toggleEnabled.setCaption('Enable \'Notes\' tab')
        else:
            # toggleVisible clicked
            self._t3.setVisible(not self._t3.isVisible())
            if self._t3.isVisible():
                self._toggleVisible.setCaption('Hide \'Issues\' tab')
            else:
                self._toggleVisible.setCaption('Show \'Issues\' tab')
        self._t.requestRepaint()
