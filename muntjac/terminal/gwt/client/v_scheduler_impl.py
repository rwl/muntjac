# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.


class VSchedulerImpl(SchedulerImpl):

    def __init__(self):
        # Keeps track of if there are deferred commands that are being
        # executed. 0 == no deferred commands currently in progress, > 0
        # otherwise.
        self._deferredCommandTrackers = 0


    def scheduleDeferred(self, cmd):
        self._deferredCommandTrackers += 1
        super(VSchedulerImpl, self).scheduleDeferred(cmd)

        class VScheduledCommand(ScheduledCommand):

            def __init__(self, scheduler):
                self._scheduler = scheduler

            def execute(self):
                self._scheduler._deferredCommandTrackers -= 1

        super(VSchedulerImpl, self).scheduleDeferred(VScheduledCommand(self))


    def hasWorkQueued(self):
        hasWorkQueued = self._deferredCommandTrackers != 0
        return hasWorkQueued
