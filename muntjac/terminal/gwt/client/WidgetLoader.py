# -*- coding: utf-8 -*-
from com.vaadin.terminal.gwt.client.ApplicationConfiguration import (ApplicationConfiguration,)
# from com.google.gwt.core.client.RunAsyncCallback import (RunAsyncCallback,)


class WidgetLoader(RunAsyncCallback):
    """A helper class used by WidgetMap implementation. Used by the generated code."""

    def onFailure(self, reason):
        ApplicationConfiguration.endWidgetLoading()

    def onSuccess(self):
        self.addInstantiator()
        ApplicationConfiguration.endWidgetLoading()

    def addInstantiator(self):
        pass
