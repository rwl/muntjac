# -*- coding: utf-8 -*-
# from com.google.gwt.xhr.client.XMLHttpRequest import (XMLHttpRequest,)


class SynchronousXHR(XMLHttpRequest):

    def __init__(self):
        pass

    def synchronousPost(self, uri, requestData):
        # -{
        #         try {
        #             this.open("POST", uri, false);
        #             this.setRequestHeader("Content-Type", "text/plain;charset=utf-8");
        #             this.send(requestData);
        #         } catch (e) {
        #            // No errors are managed as this is synchronous forceful send that can just fail
        #         }
        #     }-

        pass
