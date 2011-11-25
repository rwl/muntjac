# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.google.gwt.core.client.impl.SchedulerImpl import (SchedulerImpl,)


class VSchedulerImpl(SchedulerImpl):
    # Keeps track of if there are deferred commands that are being executed. 0
    # == no deferred commands currently in progress, > 0 otherwise.

    _deferredCommandTrackers = 0

    def scheduleDeferred(self, cmd):
        self._deferredCommandTrackers += 1
        super(VSchedulerImpl, self).scheduleDeferred(cmd)

        class _0_(self.ScheduledCommand):

            def execute(self):
                VSchedulerImpl_this._deferredCommandTrackers -= 1

        _0_ = _0_()
        super(VSchedulerImpl, self).scheduleDeferred(_0_)

    def hasWorkQueued(self):
        hasWorkQueued = self._deferredCommandTrackers != 0
        return hasWorkQueued
