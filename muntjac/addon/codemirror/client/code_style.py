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


class CodeStyle(object):

    TEXT = None
    XML = None
    JAVA = None
    JAVASCRIPT = None
    CSS = None
    SQL = None
    PHP = None
    PYTHON = None
    LUA = None

    def __init__(self, name, Id, parser, css):
        self._name = name
        self._id = Id
        self._parser = None
        self._css = None

        self.setParser(parser)
        self.setCss(css)

    def __str__(self):
        return self._name

    @classmethod
    def byId(cls, Id):
        for s in CodeStyle.values():
            if s.getId() == Id:
                return s
        return None

    def setParser(self, parser):
        self._parser = parser

    def getParser(self):
        return self._parser

    def setCss(self, css):
        self._css = css

    def getCss(self):
        return self._css

    def getId(self):
        return self._id

    _values = []

    @classmethod
    def values(cls):
        return cls._values


CodeStyle.TEXT = CodeStyle('Text', 1, '\'parsedummy.js\'', 'css/xmlcolors.css')
CodeStyle.XML = CodeStyle('XML', 2, '\'parsexml.js\'', 'css/xmlcolors.css')
CodeStyle.JAVA = CodeStyle('Java', 3, '\'java/parsejava.js\'', 'java/javacolors.css')
CodeStyle.JAVASCRIPT = CodeStyle('JavaScript', 4, '[\'tokenizejavascript.js\',\'parsejavascript.js\']', 'css/jscolors.css')
CodeStyle.CSS = CodeStyle('CSS', 5, '\'parsecss.js\'', 'css/csscolors.css')
CodeStyle.SQL = CodeStyle('SQL', 6, '\'sql/js/parsesql.js\'', 'sql/css/sqlcolors.css')
CodeStyle.PHP = CodeStyle('PHP', 7, '\'php/js/parsephp.js\'', 'php/css/phpcolors.css')
CodeStyle.PYTHON = CodeStyle('Python', 8, '\'python/js/parsepython.js\'', 'python/css/pythoncolors.css')
CodeStyle.LUA = CodeStyle('Lua', 9, '\'lua/js/parselua.js\'', 'lua/css/luacolors.css')

CodeStyle._values = [CodeStyle.TEXT, CodeStyle.XML, CodeStyle.JAVA,
        CodeStyle.JAVASCRIPT, CodeStyle.CSS, CodeStyle.SQL, CodeStyle.PHP,
        CodeStyle.PYTHON, CodeStyle.LUA]
