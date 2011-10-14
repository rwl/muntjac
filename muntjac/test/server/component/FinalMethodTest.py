# -*- coding: utf-8 -*-
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
