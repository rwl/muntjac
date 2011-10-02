# -*- coding: utf-8 -*-
# from com.vaadin.ui.RichTextArea import (RichTextArea,)
# from com.vaadin.ui.themes.BaseTheme import (BaseTheme,)


class TooltipsExample(VerticalLayout):
    _editTxt = 'Edit tooltip'
    _applyTxt = 'Apply'

    def __init__(self):
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
        rich.setDescription('<h2><img src=\"../VAADIN/themes/sampler/icons/comment_yellow.gif\"/>A richtext tooltip</h2>' + '<ul>' + '<li>HTML formatting</li><li>Images<br/>' + '</li><li>etc...</li></ul>')
        self.addComponent(rich)
        # Edit
        rte = RichTextArea()
        rte.setValue('Click <b>' + self._editTxt + '</b> to edit this tooltip, then <b>' + self._applyTxt + '</b>')
        rte.setVisible(False)
        # hide editor initially
        rte.setWidth('100%')
        self.addComponent(rte)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                if self.rte.isVisible():
                    self.rte.setVisible(False)
                    event.getButton().setDescription(self.rte.getValue())
                    event.getButton().setCaption(TooltipsExample_this._editTxt)
                else:
                    self.rte.setVisible(True)
                    event.getButton().setCaption(TooltipsExample_this._applyTxt)

        _0_ = _0_()
        apply = Button(self._editTxt, _0_)
        apply.setDescription(rte.getValue())
        self.addComponent(apply)
