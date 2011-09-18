# -*- coding: utf-8 -*-
from com.vaadin.terminal.gwt.client.ui.UploadIFrameOnloadStrategy import (UploadIFrameOnloadStrategy,)


class UploadIFrameOnloadStrategyIE(UploadIFrameOnloadStrategy):
    """IE does not have onload, detect onload via readystatechange"""

    def hookEvents(self, iframe, upload):
        # -{
        #       iframe.onreadystatechange = function() {
        #         if (iframe.readyState == 'complete') {
        #           upload.@com.vaadin.terminal.gwt.client.ui.VUpload::onSubmitComplete()();
        #         }
        #       };
        #     }-

        pass

    def unHookEvents(self, iframe):
        # -{
        #       iframe.onreadystatechange = null;
        #     }-

        pass
