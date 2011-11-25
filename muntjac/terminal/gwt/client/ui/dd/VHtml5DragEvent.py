# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.google.gwt.core.client.JsArrayString import (JsArrayString,)


class VHtml5DragEvent(NativeEvent):
    """Helper class to access html5 style drag events.

    TODO Gears support ?
    """

    def __init__(self):
        pass

    def getTypes(self):
        JS("""
        // IE does not support types, return some basic values
        return @{{self}}.dataTransfer.types ? @{{self}}.dataTransfer.types : ["Text","Url","Html"];
     """)
        pass

    def getDataAsText(self, type):
        JS("""
         var v = @{{self}}.dataTransfer.getData(@{{type}});
         return v;
     """)
        pass

    def getFileAsString(self, index):
        """Works on FF 3.6 and possibly with gears.

        @param index
        @return
        """
        JS("""
        if(@{{self}}.dataTransfer.files.length > 0 && @{{self}}.dataTransfer.files[0].getAsText) {
            return @{{self}}.dataTransfer.files[@{{index}}].getAsText("UTF-8");
        }
        return null;
    """)
        pass

    def setDragEffect(self, effect):
        JS("""
        try {
            @{{self}}.dataTransfer.dropEffect = @{{effect}};
        } catch (e){}
     """)
        pass

    def getEffectAllowed(self):
        JS("""
            return @{{self}}.dataTransfer.effectAllowed;
     """)
        pass

    def getFileCount(self):
        JS("""
            return @{{self}}.dataTransfer.files ? @{{self}}.dataTransfer.files.length : 0;
     """)
        pass

    def getFile(self, fileIndex):
        JS("""
            return @{{self}}.dataTransfer.files[@{{fileIndex}}];
     """)
        pass
