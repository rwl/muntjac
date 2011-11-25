# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from java.util.HashSet import (HashSet,)
# from java.util.Set import (Set,)


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
