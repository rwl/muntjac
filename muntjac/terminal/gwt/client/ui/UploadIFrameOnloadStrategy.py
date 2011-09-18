# -*- coding: utf-8 -*-


class UploadIFrameOnloadStrategy(object):

    def hookEvents(self, iframe, upload):
        # -{
        #         iframe.onload = function() {
        #             upload.@com.vaadin.terminal.gwt.client.ui.VUpload::onSubmitComplete()();
        #         };
        #     }-

        pass

    def unHookEvents(self, iframe):
        """@param iframe
                   the iframe whose onLoad event is to be cleaned
        """
        # -{
        #         iframe.onload = null;
        #     }-

        pass
