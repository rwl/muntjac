# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.UploadIFrameOnloadStrategy import (UploadIFrameOnloadStrategy,)


class UploadIFrameOnloadStrategyIE(UploadIFrameOnloadStrategy):
    """IE does not have onload, detect onload via readystatechange"""

    def hookEvents(self, iframe, upload):
        JS("""
      @{{iframe}}.onreadystatechange = function() {
        if (@{{iframe}}.readyState == 'complete') {
          @{{upload}}.@com.vaadin.terminal.gwt.client.ui.VUpload::onSubmitComplete()();
        }
      };
    """)
        pass

    def unHookEvents(self, iframe):
        JS("""
      @{{iframe}}.onreadystatechange = null;
    """)
        pass
