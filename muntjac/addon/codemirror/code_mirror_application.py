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

from muntjac.api \
    import Application, Window, GridLayout, Select, Button

from muntjac.data.property \
    import IValueChangeListener

from muntjac.ui.button \
    import IClickListener

from muntjac.addon.codemirror.client.code_style \
    import CodeStyle

from muntjac.addon.codemirror.code_mirror \
    import CodeMirror


class CodeMirrorApplication(Application):

    _NL = '\n\n'

    _SAMPLE_CODE = ('<xml is=\"fun\"></xml>' + _NL
            + 'function js(isMoreFun) {alert(\"Yay!\");}' + _NL
            + 'public void java(String isAlsoCool) {\n\twith(\"Vaadin!\");\n}'
            + _NL + 'select * from web where you = i;')

    def init(self):
        mainWindow = Window('CodeMirror Sample Application')

        hl = GridLayout(2, 3)
        hl.setSpacing(True)
        mainWindow.addComponent(hl)
        # #1
        code = CodeMirror('Your Code', CodeStyle.XML)
        code.setValue(self._SAMPLE_CODE)
        code.setWidth('400px')
        code.setHeight('300px')
        hl.addComponent(code)

        # #2
        code2 = CodeMirror('Your Code Too', CodeStyle.XML)
        code2.setValue(self._SAMPLE_CODE)
        code2.setWidth('400px')
        code2.setHeight('300px')
        hl.addComponent(code2)

        codeStyle = Select('Select your style')
        for cs in CodeStyle.values():
            codeStyle.addItem(cs)

        codeStyle.setNewItemsAllowed(False)
        codeStyle.setImmediate(True)
        hl.addComponent(codeStyle)

        l = CodeStyleChangeListener(code, codeStyle)
        codeStyle.addListener(l, IValueChangeListener)
        codeStyle.setValue(CodeStyle.XML)

        codeStyle = Select('Select your style too')
        for cs in CodeStyle.values():
            codeStyle.addItem(cs)
        codeStyle.setNewItemsAllowed(False)
        codeStyle.setImmediate(True)
        hl.addComponent(codeStyle)

        l = CodeStyleChangeListener(code, codeStyle)
        codeStyle.addListener(l, IValueChangeListener)
        codeStyle.setValue(CodeStyle.JAVA)

        l = CopyClickListener(code, code2)
        hl.addComponent(Button('copy to -->', l))

        l = CopyClickListener(code2, code)
        hl.addComponent(Button('<- copy to', l))

        self.setMainWindow(mainWindow)


class CodeStyleChangeListener(IValueChangeListener):

    def __init__(self, code, codeStyle):
        self._code = code
        self._codeStyle = codeStyle

    def valueChange(self, event):
        self._code.setCodeStyle(self._codeStyle.getValue())


class CopyClickListener(IClickListener):

    def __init__(self, code1, code2):
        self._code1 = code1
        self._code2 = code2

    def buttonClick(self, event):
        self.code2.setValue(self.code1.getValue())
