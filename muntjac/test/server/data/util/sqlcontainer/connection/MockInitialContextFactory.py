# Copyright (C) 2010 IT Mill Ltd.
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
