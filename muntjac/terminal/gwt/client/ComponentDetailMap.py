# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)


class ComponentDetailMap(JavaScriptObject):

    def __init__(self):
        pass

    @classmethod
    def create(cls):
        return JavaScriptObject.createObject()

    def isEmpty(self):
        return len(self) == 0

    def containsKey(self, key):
        JS("""
        return @{{self}}.hasOwnProperty(@{{key}});
    """)
        pass

    def get(self, key):
        JS("""
        return @{{self}}[@{{key}}];
    """)
        pass

    def put(self, id, value):
        JS("""
        @{{self}}[@{{id}}] = @{{value}};
    """)
        pass

    def remove(self, id):
        JS("""
        delete @{{self}}[@{{id}}];
    """)
        pass

    def size(self):
        JS("""
        var count = 0;
        for(var key in @{{self}}) {
            count++;
        }
        return count;
    """)
        pass

    def clear(self):
        JS("""
        for(var key in @{{self}}) {
            if(@{{self}}.hasOwnProperty(key)) {
                delete @{{self}}[key];
            }
        }
    """)
        pass

    def fillWithValues(self, list):
        JS("""
        for(var key in @{{self}}) {
            @{{list}}.@java.util.Collection::add(Ljava/lang/Object;)(@{{self}}[key]);
        }
    """)
        pass

    def values(self):
        list = list()
        self.fillWithValues(list)
        return list
