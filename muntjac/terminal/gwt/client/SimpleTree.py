# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
# from com.google.gwt.dom.client.SpanElement import (SpanElement,)
# from com.google.gwt.dom.client.Style.BorderStyle import (BorderStyle,)
# from com.google.gwt.dom.client.Style.Cursor import (Cursor,)
# from com.google.gwt.dom.client.Style.Display import (Display,)
# from com.google.gwt.user.client.ui.ComplexPanel import (ComplexPanel,)


class SimpleTree(ComplexPanel):
    _children = Document.get().createDivElement()
    _handle = Document.get().createSpanElement()
    _text = Document.get().createSpanElement()

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.setElement(Document.get().createDivElement())
            style = self.getElement().getStyle()
            style.setProperty('whiteSpace', 'nowrap')
            style.setPadding(3, Unit.PX)
            style = self._handle.getStyle()
            style.setDisplay(Display.NONE)
            style.setProperty('textAlign', 'center')
            style.setWidth(10, Unit.PX)
            style.setCursor(Cursor.POINTER)
            style.setBorderStyle(BorderStyle.SOLID)
            style.setBorderColor('#666')
            style.setBorderWidth(1, Unit.PX)
            style.setMarginRight(3, Unit.PX)
            style.setProperty('borderRadius', '4px')
            self._handle.setInnerHTML('+')
            self.getElement().appendChild(self._handle)
            self.getElement().appendChild(self._text)
            style = self._children.getStyle()
            style.setPaddingLeft(20, Unit.PX)
            style.setDisplay(Display.NONE)
            self.getElement().appendChild(self._children)

            class _0_(ClickHandler):

                def onClick(self, event):
                    if event.getNativeEvent().getEventTarget() == SimpleTree_this._handle:
                        if (
                            SimpleTree_this._children.getStyle().getDisplay().intern() == Display.NONE.getCssName()
                        ):
                            SimpleTree_this.open(event.getNativeEvent().getShiftKey())
                        else:
                            SimpleTree_this.close()
                    elif event.getNativeEvent().getEventTarget() == SimpleTree_this._text:
                        SimpleTree_this.select(event)

            _0_ = _0_()
            self.addDomHandler(_0_, ClickEvent.getType())
        elif _1 == 1:
            caption, = _0
            self.__init__()
            self.setText(caption)
        else:
            raise ARGERROR(0, 1)

    def select(self, event):
        pass

    def close(self):
        self._children.getStyle().setDisplay(Display.NONE)
        self._handle.setInnerHTML('+')

    def open(self, recursive):
        self._handle.setInnerHTML('-')
        self._children.getStyle().setDisplay(Display.BLOCK)
        if recursive:
            for w in self.getChildren():
                if isinstance(w, SimpleTree):
                    str = w
                    str.open(True)

    def setText(self, text):
        self._text.setInnerText(text)

    def addItem(self, text):
        label = Label(text)
        self.add(label, self._children)

    def add(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            child, = _0
            self.add(child, self._children)
        elif _1 == 2:
            child, container = _0
            super(SimpleTree, self).add(child, container)
            self._handle.getStyle().setDisplay(Display.INLINE_BLOCK)
        else:
            raise ARGERROR(1, 2)
