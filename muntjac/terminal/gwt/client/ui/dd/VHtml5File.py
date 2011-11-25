# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.google.gwt.core.client.JavaScriptObject import (JavaScriptObject,)


class VHtml5File(JavaScriptObject):
    """Wrapper for html5 File object."""

    def __init__(self):
        pass

    def getName(self):
        JS("""
        return @{{self}}.name;
     """)
        pass

    def getType(self):
        JS("""
        return @{{self}}.type;
     """)
        pass

    def getSize(self):
        JS("""
        return @{{self}}.size ? @{{self}}.size : 0;
    """)
        pass
