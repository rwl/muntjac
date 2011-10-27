
from muntjac.api import GridLayout, Label, CheckBox, Alignment, VerticalLayout
from muntjac.ui.button import IClickListener


class LayoutMarginExample(GridLayout, IClickListener):

    def __init__(self):
        super(LayoutMarginExample, self).__init__(3, 3)

        self.setWidth('100%')
        self.setSpacing(True)

        self.addComponent(Label('Toggle layout margins with the checkboxes. '
                'The right side margin has a theme-specified value, while '
                'the other margins are the defaults.'), 0, 0, 2, 0)

        self.space()
        self._topMargin = CheckBox('Top', self)
        self._topMargin.setValue(True)
        self._topMargin.setImmediate(True)
        self.addComponent(self._topMargin)
        self.setComponentAlignment(self._topMargin, Alignment.TOP_CENTER)

        self.space()
        self._leftMargin = CheckBox('Left', self)
        self._leftMargin.setValue(True)
        self._leftMargin.setImmediate(True)
        self.addComponent(self._leftMargin)
        self.setComponentAlignment(self._leftMargin, Alignment.MIDDLE_LEFT)

        self._marginLayout = VerticalLayout()
        self._marginLayout.setStyleName('marginexample')
        self._marginLayout.setSizeUndefined()
        self._marginLayout.setMargin(True)
        self.addComponent(self._marginLayout)
        self._marginLayout.addComponent(Label('Margins all around?'))

        self._rightMargin = CheckBox('Right (100px)', self)
        self._rightMargin.setValue(True)
        self._rightMargin.setImmediate(True)
        self.addComponent(self._rightMargin)
        self.setComponentAlignment(self._rightMargin, Alignment.MIDDLE_LEFT)

        self.space()
        self._bottomMargin = CheckBox('Bottom', self)
        self._bottomMargin.setValue(True)
        self._bottomMargin.setImmediate(True)
        self.addComponent(self._bottomMargin)
        self.setComponentAlignment(self._bottomMargin, Alignment.TOP_CENTER)


    def buttonClick(self, event):
        self._marginLayout.setMargin(  # FIXME:
            self._topMargin.booleanValue(),
            self._rightMargin.booleanValue(),
            self._bottomMargin.booleanValue(),
            self._leftMargin.booleanValue()
        )
