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

from __pyjamas__ import JS


class ValueMap(JavaScriptObject):

    def __init__(self):
        pass


    def getRawNumber(self, name):
        JS("""
            return @{{self}}[@{{name}}];
        """)
        pass


    def getInt(self, name):
        JS("""
            return @{{self}}[@{{name}}];
        """)
        pass


    def getBoolean(self, name):
        JS("""
            return Boolean(@{{self}}[@{{name}}]);
        """)
        pass


    def getString(self, name):
        JS("""
            return @{{self}}[@{{name}}];
        """)
        pass


    def getKeyArray(self):
        JS("""
            var a = new Array();
            var attr = @{{self}};
            for(var j in attr) {
                // workaround for the infamous chrome hosted mode hack (__gwt_ObjectId)
                if(attr.hasOwnProperty(j))
                    a.push(j);
            }
            return a;
        """)
        pass


    def getKeySet(self):
        attrs = set()
        attributeNamesArray = self.getKeyArray()
        for i in range(len(attributeNamesArray)):
            attrs.add(attributeNamesArray.get(i))
        return attrs


    def getJSStringArray(self, name):
        JS("""
            return @{{self}}[@{{name}}];
        """)
        pass


    def getJSValueMapArray(self, name):
        JS("""
            return @{{self}}[@{{name}}];
        """)
        pass


    def getStringArray(self, name):
        stringArrayAttribute = self.getJSStringArray(name)
        s = [None] * len(stringArrayAttribute)
        for i in range(len(stringArrayAttribute)):
            s[i] = stringArrayAttribute.get(i)
        return s


    def getIntArray(self, name):
        stringArrayAttribute = self.getJSStringArray(name)
        s = [None] * len(stringArrayAttribute)
        for i in range(len(stringArrayAttribute)):
            s[i] = int(stringArrayAttribute.get(i))
        return s


    def containsKey(self, name):
        JS("""
             return @{{name}} in @{{self}};
        """)
        pass


    def getValueMap(self, name):
        JS("""
            return @{{self}}[@{{name}}];
        """)
        pass


    def getAsString(self, name):
        JS("""
            return '' + @{{self}}[@{{name}}];
        """)
        pass
