
from muntjac.api import VerticalLayout, Label, TabSheet
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.ui.tab_sheet import ISelectedTabChangeListener


class TabSheetIconsExample(VerticalLayout, ISelectedTabChangeListener):

    # Icons for the table
    _icon1 = ThemeResource('../sampler/icons/action_save.gif')
    _icon2 = ThemeResource('../sampler/icons/comment_yellow.gif')
    _icon3 = ThemeResource('../sampler/icons/icon_info.gif')

    def __init__(self):
        super(TabSheetIconsExample, self).__init__()

        # Tab 1 content
        l1 = VerticalLayout()
        l1.setMargin(True)
        l1.addComponent(Label('There are no previously saved actions.'))

        # Tab 2 content
        l2 = VerticalLayout()
        l2.setMargin(True)
        l2.addComponent(Label('There are no saved notes.'))

        # Tab 3 content
        l3 = VerticalLayout()
        l3.setMargin(True)
        l3.addComponent(Label('There are currently no issues.'))

        self._t = TabSheet()
        self._t.setHeight('200px')
        self._t.setWidth('400px')
        self._t.addTab(l1, 'Saved actions', self._icon1)
        self._t.addTab(l2, 'Notes', self._icon2)
        self._t.addTab(l3, 'Issues', self._icon3)
        self._t.addListener(self, ISelectedTabChangeListener)

        self.addComponent(self._t)


    def selectedTabChange(self, event):
        tabsheet = event.getTabSheet()
        tab = tabsheet.getTab(tabsheet.getSelectedTab())
        if tab is not None:
            self.getWindow().showNotification('Selected tab: '
                    + tab.getCaption())
