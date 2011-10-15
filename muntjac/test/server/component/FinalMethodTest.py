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

# from java.lang.reflect.Modifier import (Modifier,)
# from junit.framework.TestCase import (TestCase,)


class FinalMethodTest(TestCase):
    # public void testThatContainersHaveNoFinalMethods() {
    # HashSet<Class<?>> tested = new HashSet<Class<?>>();
    # for (Class<?> c : VaadinClasses.getAllServerSideClasses()) {
    # if (Container.class.isAssignableFrom(c)) {
    # ensureNoFinalMethods(c, tested);
    # }
    # }
    # }

    def testThatComponentsHaveNoFinalMethods(self):
        tested = set()
        for c in VaadinClasses.getComponents():
            self.ensureNoFinalMethods(c, tested)

    def ensureNoFinalMethods(self, c, tested):
        if c in tested:
            return
        tested.add(c)
        if c == self.Object:
            return
        print 'Checking ' + c.getName()
        for m in c.getDeclaredMethods():
            if self.isPrivate(m):
                continue
            if self.isFinal(m):
                error = 'Class ' + c.getName() + ' contains a ' + ('public' if self.isPublic(m) else 'non-public') + ' final method: ' + m.getName()
                # System.err.println(error);
                raise RuntimeError(error)
        self.ensureNoFinalMethods(c.getSuperclass(), tested)

    def isFinal(self, m):
        return Modifier.isFinal(m.getModifiers())

    def isPrivate(self, m):
        return Modifier.isPrivate(m.getModifiers())

    def isPublic(self, m):
        return Modifier.isPublic(m.getModifiers())
