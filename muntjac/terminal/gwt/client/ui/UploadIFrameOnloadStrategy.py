# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class UploadIFrameOnloadStrategy(object):

    def hookEvents(self, iframe, upload):
        JS("""
        @{{iframe}}.onload = function() {
            @{{upload}}.@com.vaadin.terminal.gwt.client.ui.VUpload::onSubmitComplete()();
        };
    """)
        pass

    def unHookEvents(self, iframe):
        """@param iframe
                   the iframe whose onLoad event is to be cleaned
        """
        JS("""
        @{{iframe}}.onload = null;
    """)
        pass
