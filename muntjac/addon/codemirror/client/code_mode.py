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


class CodeMode(object):

    TEXT = None
    XML = None
    JAVA = None
    JAVASCRIPT = None
    CSS = None
    SQL = None
    PHP = None
    PYTHON = None
    LUA = None

    def __init__(self, name, Id, mode):
        self._name = name
        self._id = Id
        self._mode = None

        self.setMode(mode)

    def __str__(self):
        return self._name

    @classmethod
    def byId(cls, Id):
        for s in CodeMode.values():
            if s.getId() == Id:
                return s
        return None

    def setMode(self, mode):
        self._mode = mode

    def getMode(self):
        return self._mode

    def getId(self):
        return self._id

    _values = []

    @classmethod
    def values(cls):
        return cls._values


CodeMode.TEXT = CodeMode('Text', 1, 'rst')
CodeMode.XML = CodeMode('XML', 2, 'xml')
CodeMode.JAVA = CodeMode('Java', 3, 'clike')
CodeMode.JAVASCRIPT = CodeMode('JavaScript', 4, 'javascript')
CodeMode.CSS = CodeMode('CSS', 5, 'css')
CodeMode.SQL = CodeMode('SQL', 6, 'plsql')
CodeMode.PHP = CodeMode('PHP', 7, 'php')
CodeMode.PYTHON = CodeMode('Python', 8, 'python')
CodeMode.LUA = CodeMode('Lua', 9, 'lua')

CodeMode._values = [CodeMode.TEXT, CodeMode.XML, CodeMode.JAVA,
        CodeMode.JAVASCRIPT, CodeMode.CSS, CodeMode.SQL, CodeMode.PHP,
        CodeMode.PYTHON, CodeMode.LUA]
