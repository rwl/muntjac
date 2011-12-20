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

from muntjac.addon.codemirror.client.code_style import CodeStyle


class CodeMirror(TextField):
    """Server side component for the VCodeMirrorTextField2 widget."""

    CLIENT_WIDGET = None #ClientWidget(VCodeMirror)

    def __init__(self, caption, codeStyle=None):
        if codeStyle is None:
            codeStyle = CodeStyle.TEXT

        self._codeStyle = None
        self._showLineNumbers = True

        super(CodeMirror, self).__init__(caption)
        self.setCodeStyle(codeStyle)


    def paintContent(self, target):
        super(CodeMirror, self).paintContent(target)
        target.addAttribute('codestyle', self.getCodeStyle().getId())
        target.addAttribute('showLineNumbers', self.isShowLineNumbers())


    def setCodeStyle(self, codeStyle):
        self._codeStyle = codeStyle
        self.requestRepaint()


    def getCodeStyle(self):
        return self._codeStyle


    def setShowLineNumbers(self, showLineNumbers):
        self._showLineNumbers = showLineNumbers
        self.requestRepaint()


    def isShowLineNumbers(self):
        return self._showLineNumbers
