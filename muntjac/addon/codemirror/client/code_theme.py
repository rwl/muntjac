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
