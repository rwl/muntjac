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

from muntjac.ui.text_field import TextField

from muntjac.addon.codemirror.client.code_mode import CodeMode
from muntjac.addon.codemirror.client.code_theme import CodeTheme


class CodeMirror(TextField):
    """Server side component for the VCodeMirrorTextField2 widget."""

    CLIENT_WIDGET = None #ClientWidget(VCodeMirror)

    TYPE_MAPPING = 'org.vaadin.codemirror2.CodeMirror'

    def __init__(self, caption, codeMode=None, codeTheme=None):
        if codeMode is None:
            codeMode = CodeMode.TEXT

        if codeTheme is None:
            codeTheme = CodeTheme.DEFAULT

        self._codeStyle = None
        self._showLineNumbers = False
        self._codeTheme = None

        super(CodeMirror, self).__init__(caption)

        self.setCodeMode(codeMode)
        self.setCodeTheme(codeTheme)


    def paintContent(self, target):
        super(CodeMirror, self).paintContent(target)

        if self.getCodeMode() is not None:
            target.addAttribute('codeMode', self.getCodeMode().getId())

        target.addAttribute('showLineNumbers', self.isShowLineNumbers())

        if self.getCodeTheme() is not None:
            target.addAttribute('codeTheme', self.getCodeTheme().getId())


    def setCodeMode(self, codeMode):
        self._codeMode = codeMode
        self.requestRepaint()


    def getCodeMode(self):
        return self._codeMode


    def setShowLineNumbers(self, showLineNumbers):
        self._showLineNumbers = showLineNumbers
        self.requestRepaint()


    def isShowLineNumbers(self):
        return self._showLineNumbers


    def setCodeTheme(self, codeTheme):
        self._codeTheme = codeTheme
        self.requestRepaint()


    def getCodeTheme(self):
        return self._codeTheme
