# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.
from muntjac.ui.check_box import CheckBox

from muntjac.api \
    import Application, Window, GridLayout, Select, Button

from muntjac.data.property \
    import IValueChangeListener

from muntjac.ui.button \
    import IClickListener

from muntjac.addon.codemirror.client.code_mode \
    import CodeMode

from muntjac.addon.codemirror.client.code_theme \
    import CodeTheme

from muntjac.addon.codemirror.code_mirror \
    import CodeMirror


class CodeMirrorApplication(Application):

    _NL = '\n\n'

    _SAMPLE_CODE = ('<xml is="fun"></xml>' + _NL
            + 'function js(isMoreFun) {alert("Yay!");}' + _NL
            + 'public void java(String isAlsoCool) {\n\twith("Vaadin!");\n}'
            + _NL + 'def python(isCooler): print "with Muntjac!"'
            + _NL + 'select * from web where you = i;')

    def init(self):
        mainWindow = Window('CodeMirror Sample Application')

        hl = GridLayout(2, 5)
        hl.setSpacing(True)
        mainWindow.addComponent(hl)

        # #1
        code = CodeMirror('Your Code', CodeMode.TEXT)
        code.setValue(self._SAMPLE_CODE)
        code.setWidth('500px')
        code.setHeight('350px')
        hl.addComponent(code)

        # #2
        code2 = CodeMirror('Your Code Too', CodeMode.PYTHON)
        code2.setValue(self._SAMPLE_CODE)
#        code2.setWidth('400px')
#        code2.setHeight('300px')
        hl.addComponent(code2)


        codeMode = Select('Select your mode')
        for cs in CodeMode.values():
            codeMode.addItem(cs)
        codeMode.setNewItemsAllowed(False)
        codeMode.setNullSelectionAllowed(False)
        codeMode.setImmediate(True)
        hl.addComponent(codeMode)

        l = CodeModeChangeListener(code, codeMode)
        codeMode.addListener(l, IValueChangeListener)
        codeMode.setValue(CodeMode.TEXT)

        codeMode = Select('Select your mode too')
        for cs in CodeMode.values():
            codeMode.addItem(cs)
        codeMode.setNewItemsAllowed(False)
        codeMode.setNullSelectionAllowed(False)
        codeMode.setImmediate(True)
        hl.addComponent(codeMode)

        l = CodeModeChangeListener(code2, codeMode)
        codeMode.addListener(l, IValueChangeListener)
        codeMode.setValue(CodeMode.PYTHON)


        codeTheme = Select('Select your theme')
        for ct in CodeTheme.values():
            codeTheme.addItem(ct)
        codeTheme.setNewItemsAllowed(False)
        codeTheme.setImmediate(True)
        hl.addComponent(codeTheme)

        l = CodeThemeChangeListener(code, codeTheme)
        codeTheme.addListener(l, IValueChangeListener)
        codeTheme.setValue(CodeTheme.DEFAULT)

        codeTheme = Select('Select your theme too')
        for ct in CodeTheme.values():
            codeTheme.addItem(ct)
        codeTheme.setNewItemsAllowed(False)
        codeTheme.setImmediate(True)
        hl.addComponent(codeTheme)

        l = CodeThemeChangeListener(code2, codeTheme)
        codeTheme.addListener(l, IValueChangeListener)
        codeTheme.setValue(CodeTheme.ECLIPSE)


        l = CopyClickListener(code, code2)
        hl.addComponent(Button('copy to -->', l))

        l = CopyClickListener(code2, code)
        hl.addComponent(Button('<- copy to', l))


        l = ShowLineNumbersListener(code)
        cb = CheckBox("Show line numbers", l)
        cb.setImmediate(True)
        hl.addComponent(cb)

        l = ShowLineNumbersListener(code2)
        cb = CheckBox("Show line numbers", l)
        cb.setImmediate(True)
        hl.addComponent(cb)


        self.setMainWindow(mainWindow)


class CodeModeChangeListener(IValueChangeListener):

    def __init__(self, code, codeMode):
        self._code = code
        self._codeMode = codeMode

    def valueChange(self, event):
        self._code.setCodeMode(self._codeMode.getValue())


class CopyClickListener(IClickListener):

    def __init__(self, code1, code2):
        self._code1 = code1
        self._code2 = code2

    def buttonClick(self, event):
        self._code2.setValue(self._code1.getValue())


class CodeThemeChangeListener(IValueChangeListener):

    def __init__(self, code, codeTheme):
        self._code = code
        self._codeTheme = codeTheme

    def valueChange(self, event):
        self._code.setCodeTheme(self._codeTheme.getValue())


class ShowLineNumbersListener(IClickListener):

    def __init__(self, code):
        self._code = code

    def buttonClick(self, event):
        self._code.setShowLineNumbers(event.getButton().booleanValue())


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(CodeMirrorApplication, nogui=True, forever=True, debug=True)
