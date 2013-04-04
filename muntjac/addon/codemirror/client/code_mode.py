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
