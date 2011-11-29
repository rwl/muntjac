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

# from com.google.gwt.user.client.Timer import (Timer,)


class VLazyExecutor(object):
    """Executes the given command {@code delayMs} milliseconds after a call to
    {@link #trigger()}. Calling {@link #trigger()} again before the command has
    been executed causes the execution to be rescheduled to {@code delayMs} after
    the second call.
    """
    _timer = None
    _delayMs = None
    _cmd = None

    def __init__(self, delayMs, cmd):
        """@param delayMs
                   Delay in milliseconds to wait before executing the command
        @param cmd
                   The command to execute
        """
        self._delayMs = delayMs
        self._cmd = cmd

    def trigger(self):
        """Triggers execution of the command. Each call reschedules any existing
        execution to {@link #delayMs} milliseconds from that point in time.
        """
        if self._timer is None:

            class _0_(Timer):

                def run(self):
                    VLazyExecutor_this._timer = None
                    VLazyExecutor_this._cmd.execute()

            _0_ = _0_()
            self._timer = _0_
        # Schedule automatically cancels any old schedule
        self._timer.schedule(self._delayMs)
