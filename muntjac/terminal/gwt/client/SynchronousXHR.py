# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.google.gwt.xhr.client.XMLHttpRequest import (XMLHttpRequest,)


class SynchronousXHR(XMLHttpRequest):

    def __init__(self):
        pass

    def synchronousPost(self, uri, requestData):
        JS("""
        try {
            @{{self}}.open("POST", @{{uri}}, false);
            @{{self}}.setRequestHeader("Content-Type", "text/plain;charset=utf-8");
            @{{self}}.send(@{{requestData}});
        } catch (e) {
           // No errors are managed as @{{self}} is synchronous forceful send that can just fail
        }
    """)
        pass
