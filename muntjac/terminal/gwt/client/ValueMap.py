# Copyright (C) 2011 Vaadin Ltd
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

# from java.util.HashSet import (HashSet,)
# from java.util.Set import (Set,)


class ValueMap(JavaScriptObject):

    def __init__(self):
        pass

    def getRawNumber(self, name):
        # -{
        #         return this[name];
        #     }-

        pass

    def getInt(self, name):
        # -{
        #         return this[name];
        #     }-

        pass

    def getBoolean(self, name):
        # -{
        #         return Boolean(this[name]);
        #     }-

        pass

    def getString(self, name):
        # -{
        #         return this[name];
        #     }-

        pass

    def getKeyArray(self):
        # -{
        #         var a = new Array();
        #         var attr = this;
        #         for(var j in attr) {
        #             // workaround for the infamous chrome hosted mode hack (__gwt_ObjectId)
        #             if(attr.hasOwnProperty(j))
        #                 a.push(j);
        #         }
        #         return a;
        #     }-

        pass

    def getKeySet(self):
        attrs = set()
        attributeNamesArray = self.getKeyArray()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(attributeNamesArray)):
                break
            attrs.add(attributeNamesArray.get(i))
        return attrs

    def getJSStringArray(self, name):
        # -{
        #         return this[name];
        #     }-

        pass

    def getJSValueMapArray(self, name):
        # -{
        #         return this[name];
        #     }-

        pass

    def getStringArray(self, name):
        stringArrayAttribute = self.getJSStringArray(name)
        s = [None] * len(stringArrayAttribute)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(stringArrayAttribute)):
                break
            s[i] = stringArrayAttribute.get(i)
        return s

    def getIntArray(self, name):
        stringArrayAttribute = self.getJSStringArray(name)
        s = [None] * len(stringArrayAttribute)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(stringArrayAttribute)):
                break
            s[i] = int(stringArrayAttribute.get(i))
        return s

    def containsKey(self, name):
        # -{
        #          return name in this;
        #     }-

        pass

    def getValueMap(self, name):
        # -{
        #         return this[name];
        #     }-

        pass

    def getAsString(self, name):
        # -{
        #         return '' + this[name];
        #     }-

        pass
