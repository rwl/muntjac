# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.vaadin.ui.Alignment import (Alignment,)
# from com.vaadin.ui.TextArea import (TextArea,)
# from java.util.Date import (Date,)


class JavaScriptAPIExample(CustomComponent):
    """An example using a RichTextArea to edit a Label in XHTML-mode.
     *
    """
    txt = '<p>For advanced client side programmers Vaadin offers a simple method which can be used to force sync client with server. This may be needed for example if another part of a mashup changes things on server.</p> (more examples will be added here as the APIs are made public)<br/><br/><A href=\"javascript:vaadin.forceSync();\">javascript:vaadin.forceSync();</A>'
    _main = None
    _l = None
    _editor = TextArea()

    def __init__(self):
        # main layout
        self._main = VerticalLayout()
        self._main.setMargin(True)
        self.setCompositionRoot(self._main)
        self._editor.setRows(7)
        self._editor.setColumns(50)
        # Add the label
        self._l = Label(self.txt)
        # l.setContentMode(Label.CONTENT_XHTML);
        self._main.addComponent(self._l)
        # Edit button with inline click-listener

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                # swap Label <-> RichTextArea
                if (
                    JavaScriptAPIExample_this._main.getComponentIterator().next() == JavaScriptAPIExample_this._l
                ):
                    JavaScriptAPIExample_this._editor.setValue(JavaScriptAPIExample_this._l.getValue())
                    JavaScriptAPIExample_this._main.replaceComponent(JavaScriptAPIExample_this._l, JavaScriptAPIExample_this._editor)
                    event.getButton().setCaption('Save')
                else:
                    JavaScriptAPIExample_this._l.setValue(JavaScriptAPIExample_this._editor.getValue())
                    JavaScriptAPIExample_this._main.replaceComponent(JavaScriptAPIExample_this._editor, JavaScriptAPIExample_this._l)
                    event.getButton().setCaption('Edit')

        _0_ = _0_()
        b = Button('Edit', _0_)
        self._main.addComponent(b)
        self._main.setComponentAlignment(b, Alignment.MIDDLE_RIGHT)

        class l(Label):

            def paintContent(self, target):
                super(_0_, self).paintContent(target)
                d = JavaScriptAPIExample_this.Delay(self)
                d.start()

        self._main.addComponent(l)

    class Delay(CustomComponent.Thread):
        _label = None

        def __init__(self, l):
            self._label = l

        def run(self):
            try:
                self.Thread.sleep(500)
                self._label.setValue(str(Date()))
            except Exception, e:
                e.printStackTrace()
