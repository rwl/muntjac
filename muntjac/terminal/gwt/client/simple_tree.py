# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.


from pyjamas import DOM

from pyjamas.ui.ComplexPanel import ComplexPanel
from pyjamas.ui.Label import Label


class SimpleTree(ComplexPanel):

    def __init__(self, caption=None):
        self._children = DOM.createDiv()
        self._handle = DOM.createSpanElement()
        self._text = DOM.createSpanElement()

        self.setElement(DOM.createDiv())
        style = self.getElement().getStyle()
        style.setProperty('whiteSpace', 'nowrap')
        style.setPadding(3, 'px')
        style = self._handle.getStyle()
        style.setDisplay('none')
        style.setProperty('textAlign', 'center')
        style.setWidth(10, 'px')
        style.setCursor('pointer')
        style.setBorderStyle('solid')
        style.setBorderColor('#666')
        style.setBorderWidth(1, 'px')
        style.setMarginRight(3, 'px')
        style.setProperty('borderRadius', '4px')
        self._handle.setInnerHTML('+')
        self.getElement().appendChild(self._handle)
        self.getElement().appendChild(self._text)
        style = self._children.getStyle()
        style.setPaddingLeft(20, 'px')
        style.setDisplay('none')
        self.getElement().appendChild(self._children)

        class TreeClickHandler(ClickHandler):

            def __init__(self, tree):
                self._tree = tree

            def onClick(self, event):
                if event.getNativeEvent().getEventTarget() == self._tree._handle:
                    if self._tree._children.getStyle().getDisplay().intern() == 'none':
                        self._tree.open(event.getNativeEvent().getShiftKey())
                    else:
                        self._tree.close()
                elif event.getNativeEvent().getEventTarget() == self._tree._text:
                    self._tree.select(event)

        self.addDomHandler(TreeClickHandler(self), ClickEvent.getType())

        if caption is not None:
            self.setText(caption)


    def select(self, event):
        pass


    def close(self):
        self._children.getStyle().setDisplay('none')
        self._handle.setInnerHTML('+')


    def open(self, recursive):
        self._handle.setInnerHTML('-')
        self._children.getStyle().setDisplay('block')
        if recursive:
            for w in self.getChildren():
                if isinstance(w, SimpleTree):
                    w.open(True)


    def setText(self, text):
        self._text.setInnerText(text)


    def addItem(self, text):
        label = Label(text)
        self.add(label, self._children)


    def add(self, child, container=None):
        if container is None:
            container = self._children

        super(SimpleTree, self).add(child, container)
        self._handle.getStyle().setDisplay('inline')
