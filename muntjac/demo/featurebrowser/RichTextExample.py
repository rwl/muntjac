# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.vaadin.ui.RichTextArea import (RichTextArea,)


class RichTextExample(CustomComponent):
    """An example using a RichTextArea to edit a Label in XHTML-mode.
     *
    """
    txt = '<h1>RichText editor example</h1>' + 'To edit this text, press the <b>Edit</b> button below.' + '<br/>' + 'See the <A href=\"http://www.vaadin.com/book\">Book of Vaadin</a> ' + 'for more information.'
    _main = None
    _l = None
    _editor = RichTextArea()
    _b = None

    def __init__(self):
        # main layout
        self._main = VerticalLayout()
        self._main.setMargin(True)
        self.setCompositionRoot(self._main)
        self._editor.setWidth('100%')
        # Add the label
        self._l = Label(self.txt)
        # l.setContentMode(Label.CONTENT_XHTML);
        self._main.addComponent(self._l)
        # Edit button with inline click-listener

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                # swap Label <-> RichTextArea
                if (
                    RichTextExample_this._main.getComponentIterator().next() == RichTextExample_this._l
                ):
                    RichTextExample_this._editor.setValue(RichTextExample_this._l.getValue())
                    RichTextExample_this._main.replaceComponent(RichTextExample_this._l, RichTextExample_this._editor)
                    RichTextExample_this._b.setCaption('Save')
                else:
                    RichTextExample_this._l.setValue(RichTextExample_this._editor.getValue())
                    RichTextExample_this._main.replaceComponent(RichTextExample_this._editor, RichTextExample_this._l)
                    RichTextExample_this._b.setCaption('Edit')

        _0_ = _0_()
        Button('Edit', _0_)
        self._b = _0_
        self._main.addComponent(self._b)
        self._main.setComponentAlignment(self._b, Alignment.MIDDLE_RIGHT)
