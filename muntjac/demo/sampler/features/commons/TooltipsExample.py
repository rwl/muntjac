
from muntjac.api import VerticalLayout, Button, RichTextArea
from muntjac.ui.themes import BaseTheme
from muntjac.ui.button import IClickListener


class TooltipsExample(VerticalLayout):

    _editTxt = 'Edit tooltip'
    _applyTxt = 'Apply'

    def __init__(self):
        super(TooltipsExample, self).__init__()

        self.setSpacing(True)

        # Plain tooltip (description)
        plain = Button('Mouse over for plain tooltip')
        plain.setStyleName(BaseTheme.BUTTON_LINK)
        # add the tooltip:
        plain.setDescription('A simple plaintext tooltip')
        self.addComponent(plain)

        # Richtext tooltip (description)
        rich = Button('Mouse over for richtext tooltip')
        rich.setStyleName(BaseTheme.BUTTON_LINK)
        # add the tooltip:
        rich.setDescription(('<h2><img src=\"../VAADIN/themes/sampler/'
                'icons/comment_yellow.gif\"/>A richtext tooltip</h2>'
                '<ul>'
                '<li>HTML formatting</li><li>Images<br/>'
                '</li><li>etc...</li></ul>'))
        self.addComponent(rich)

        # Edit
        rte = RichTextArea()
        rte.setValue(('Click <b>'
                + self._editTxt
                + '</b> to edit this tooltip, then <b>'
                + self._applyTxt
                + '</b>'))
        rte.setVisible(False)  # hide editor initially
        rte.setWidth('100%')
        self.addComponent(rte)

        aply = Button(self._editTxt, EditListener(self, rte))
        aply.setDescription(rte.getValue())
        self.addComponent(aply)


class EditListener(IClickListener):

    def __init__(self, component, rte):
        self._component = component
        self._rte = rte

    def buttonClick(self, event):
        if self._rte.isVisible():
            self._rte.setVisible(False)
            event.getButton().setDescription(self._rte.getValue())
            event.getButton().setCaption(self._component._editTxt)
        else:
            self._rte.setVisible(True)
            event.getButton().setCaption(self._component._applyTxt)
