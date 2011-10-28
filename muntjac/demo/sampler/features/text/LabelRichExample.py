
from muntjac.api import VerticalLayout, RichTextArea, Label, Button
from muntjac.ui.button import IClickListener


class LabelRichExample(VerticalLayout, IClickListener):

    def __init__(self):
        super(LabelRichExample, self).__init__()

        self.setSpacing(True)

        self._editor = RichTextArea()
        self._richText = Label('<h1>Rich text example</h1>'
                '<p>The <b>quick</b> brown fox jumps <sup>over</sup> '
                'the <b>lazy</b> dog.</p>'
                '<p>This text can be edited with the <i>Edit</i> -button</p>')
        self._richText.setContentMode(Label.CONTENT_XHTML)
        self.addComponent(self._richText)

        self._b = Button('Edit')
        self._b.addListener(self, IClickListener)
        self.addComponent(self._b)

        self._editor.setWidth('100%')


    def buttonClick(self, event):
        if self.getComponentIterator().next() == self._richText:
            self._editor.setValue(self._richText.getValue())
            self.replaceComponent(self._richText, self._editor)
            self._b.setCaption('Apply')
        else:
            self._richText.setValue(self._editor.getValue())
            self.replaceComponent(self._editor, self._richText)
            self._b.setCaption('Edit')
