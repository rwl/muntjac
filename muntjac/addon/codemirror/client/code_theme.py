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


class CodeTheme(object):

    DEFAULT = None
    COBALT = None
    ECLIPSE = None
    ELEGANT = None
    MONOKAI = None
    NEAT = None
    NIGHT = None
    RUBYBLUE = None

    def __init__(self, name, Id, theme):
        self._name = name
        self._id = Id
        self._theme = None

        self.setTheme(theme)

    def __str__(self):
        return self._name

    @classmethod
    def byId(cls, Id):
        for s in CodeTheme.values():
            if s.getId() == Id:
                return s
        return None

    def setTheme(self, theme):
        self._theme = theme

    def getTheme(self):
        return self._theme

    def getId(self):
        return self._id

    _values = []

    @classmethod
    def values(cls):
        return cls._values


CodeTheme.DEFAULT = CodeTheme('Default', 1, 'default')
CodeTheme.COBALT = CodeTheme('Cobalt', 2, 'cobalt')
CodeTheme.ECLIPSE = CodeTheme('Eclipse', 3, 'eclipse')
CodeTheme.ELEGANT = CodeTheme('Elegant', 4, 'elegant')
CodeTheme.MONOKAI = CodeTheme('Monokai', 5, 'monokai')
CodeTheme.NEAT = CodeTheme('Neat', 6, 'neat')
CodeTheme.NIGHT = CodeTheme('Night', 7, 'night')
CodeTheme.RUBYBLUE = CodeTheme('Ruby Blue', 8, 'rubyblue')


CodeTheme._values = [CodeTheme.DEFAULT, CodeTheme.COBALT, CodeTheme.ECLIPSE,
        CodeTheme.ELEGANT, CodeTheme.MONOKAI, CodeTheme.NEAT, CodeTheme.NIGHT,
        CodeTheme.RUBYBLUE]
