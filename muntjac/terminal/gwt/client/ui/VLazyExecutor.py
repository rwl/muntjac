# -*- coding: utf-8 -*-


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
                    self.timer = None
                    self.cmd.execute()

            _0_ = self._0_()
            self._timer = _0_
        # Schedule automatically cancels any old schedule
        self._timer.schedule(self._delayMs)
