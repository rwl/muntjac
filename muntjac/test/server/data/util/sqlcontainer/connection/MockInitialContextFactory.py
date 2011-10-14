# -*- coding: utf-8 -*-
# from javax.naming.Context import (Context,)
# from javax.naming.NamingException import (NamingException,)
# from javax.naming.spi.InitialContextFactory import (InitialContextFactory,)
# from org.junit.Test import (Test,)


class MockInitialContextFactory(InitialContextFactory):
    """Provides a JNDI initial context factory for the MockContext."""
    _mockCtx = None

    def testDummy(self):
        # Added dummy test so JUnit will not complain about "No runnable methods".
        pass

    @classmethod
    def setMockContext(cls, ctx):
        cls._mockCtx = ctx

    def getInitialContext(self, environment):
        if self._mockCtx is None:
            raise self.IllegalStateException('mock context was not set.')
        return self._mockCtx
