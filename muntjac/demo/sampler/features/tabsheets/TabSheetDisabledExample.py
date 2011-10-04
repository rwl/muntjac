# -*- coding: utf-8 -*-


class TabSheetDisabledExample(VerticalLayout, TabSheet.SelectedTabChangeListener, Button.ClickListener):
    _icon1 = ThemeResource('../sampler/icons/action_save.gif')
    _icon2 = ThemeResource('../sampler/icons/comment_yellow.gif')
    _icon3 = ThemeResource('../sampler/icons/icon_info.gif')
    _t = None
    _toggleEnabled = None
    _toggleVisible = None
    _l1 = None
    _l2 = None
    _l3 = None
    _t1 = None
    _t2 = None
    _t3 = None

    def __init__(self):
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
        self._t.addListener(self)
        self._toggleEnabled = Button('Disable \'Notes\' tab')
        self._toggleEnabled.addListener(self)
        self._toggleVisible = Button('Hide \'Issues\' tab')
        self._toggleVisible.addListener(self)
        hl = HorizontalLayout()
        hl.setSpacing(True)
        hl.addComponent(self._toggleEnabled)
        hl.addComponent(self._toggleVisible)
        self.addComponent(self._t)
        self.addComponent(hl)

    def selectedTabChange(self, event):
        c = self._t.getTab(event.getTabSheet().getSelectedTab()).getCaption()
        self.getWindow().showNotification('Selected tab: ' + c)

    def buttonClick(self, event):
        if self._toggleEnabled == event.getButton():
            # toggleEnabled clicked
            self._t2.setEnabled(not self._t2.isEnabled())
            self._toggleEnabled.setCaption(('Disable' if self._t2.isEnabled() else 'Enable') + ' \'Notes\' tab')
        else:
            # toggleVisible clicked
            self._t3.setVisible(not self._t3.isVisible())
            self._toggleVisible.setCaption(('Hide' if self._t3.isVisible() else 'Show') + ' \'Issues\' tab')
        self._t.requestRepaint()
