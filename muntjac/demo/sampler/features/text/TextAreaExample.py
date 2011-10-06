
from muntjac.ui import HorizontalLayout, Button, Label
from muntjac.data.property import IValueChangeListener


class TextAreaExample(HorizontalLayout, IValueChangeListener):

    _initialText = 'The quick brown fox jumps over the lazy dog.'

    def __init__(self):
        self.setSpacing(True)

        self.setWidth('100%')

        self._editor = self.com.vaadin.ui.TextArea(None, self._initialText)
        self._editor.setRows(20)
        self._editor.setColumns(20)
        self._editor.addListener(self)
        self._editor.setImmediate(True)
        self.addComponent(self._editor)

        # the TextArea is immediate, and it's valueCahnge updates the Label,
        # so this button actually does nothing
        self.addComponent(Button('>'))
        self._plainText = Label(self._initialText)
        self._plainText.setContentMode(Label.CONTENT_XHTML)
        self.addComponent(self._plainText)
        self.setExpandRatio(self._plainText, 1)

    # Catch the valuechange event of the textfield and update the value of the
    # label component
    def valueChange(self, event):
        text = self._editor.getValue()
        if text is not None:
            # replace newline with BR, because we're using Label.CONTENT_XHTML
            text = text.replaceAll('\n', '<br/>')
        self._plainText.setValue(text)
