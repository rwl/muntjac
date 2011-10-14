# -*- coding: utf-8 -*-
# from com.vaadin.service.ApplicationContext.TransactionListener import (TransactionListener,)
# from com.vaadin.terminal.gwt.server.AbstractWebApplicationContext import (AbstractWebApplicationContext,)
# from com.vaadin.terminal.gwt.server.WebApplicationContext import (WebApplicationContext,)
# from java.lang.Thread.UncaughtExceptionHandler import (UncaughtExceptionHandler,)
# from java.lang.reflect.InvocationTargetException import (InvocationTargetException,)
# from java.net.MalformedURLException import (MalformedURLException,)
# from java.net.URL import (URL,)
# from java.util.Properties import (Properties,)
# from java.util.Random import (Random,)
# from javax.servlet.http.HttpSession import (HttpSession,)
# from junit.framework.TestCase import (TestCase,)
# from org.easymock.EasyMock import (EasyMock,)
# from org.easymock.EasyMock.createMock import (createMock,)


class TransactionListenersConcurrency(TestCase):

    def testTransactionListeners(self):
        """This test starts N threads concurrently. Each thread creates an
        application which adds a transaction listener to the context. A
        transaction is then started for each application. Some semi-random delays
        are included so that calls to addTransactionListener and
        WebApplicationContext.startTransaction are mixed.
        """
        exceptions = list()
        session = self.createSession()
        context = WebApplicationContext.getApplicationContext(session)
        threads = list()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 5):
                break

            class _1_(self.Runnable):

                def run(self):

                    class app(Application):

                        def init(self):
                            # Sleep 0-1000ms so another transaction has time to
                            # start before we add the transaction listener.
                            # TODO Auto-generated catch block
                            try:
                                self.Thread.sleep(1000 * Random().nextDouble())
                            except self.InterruptedException, e:
                                e.printStackTrace()
                            self.getContext().addTransactionListener(TransactionListenersConcurrency_this.DelayTransactionListener(2000))

                    # Start the application so the transaction listener is
                    # called later on.
                    # TODO Auto-generated catch block
                    try:
                        app.start(URL('http://localhost/'), Properties(), self.context)
                    except MalformedURLException, e:
                        e.printStackTrace()
                    # Call the transaction listener using reflection as
                    # startTransaction is protected.
                    try:
                        m = AbstractWebApplicationContext.getDeclaredMethod('startTransaction', Application, self.Object)
                        m.setAccessible(True)
                        m.invoke(self.context, app, None)
                    except Exception, e:
                        raise RuntimeError(e)

            _1_ = _1_()
            t = self.Thread(_1_)
            threads.add(t)

            class _2_(UncaughtExceptionHandler):

                def uncaughtException(self, t, e):
                    e = e.getCause()
                    self.exceptions.add(e)

            _2_ = _2_()
            t.setUncaughtExceptionHandler(_2_)
        # Start the threads and wait for all of them to finish
        for t in threads:
            t.start()
        running = len(threads)
        while running > 0:
            _1 = True
            i = threads
            while True:
                if _1 is True:
                    _1 = False
                if not i.hasNext():
                    break
                t = i.next()
                if not t.isAlive():
                    running -= 1
                    i.remove()
        for t in exceptions:
            if isinstance(t, InvocationTargetException):
                t = t.getCause()
            t.printStackTrace(System.err)
            self.fail(t.getClass().getName())
        print 'Done, all ok'

    @classmethod
    def createSession(cls):
        """Creates a HttpSession mock"""
        session = createMock(HttpSession)
        EasyMock.expect(session.getAttribute(WebApplicationContext.getName())).andReturn(None).anyTimes()
        session.setAttribute(EasyMock.eq(WebApplicationContext.getName()), EasyMock.anyObject())
        EasyMock.replay(session)
        return session

    class DelayTransactionListener(TransactionListener):
        """A transaction listener that just sleeps for the given amount of time in
        transactionStart and transactionEnd.
        """
        _delay = None

        def __init__(self, delay):
            self._delay = delay

        def transactionStart(self, application, transactionData):
            try:
                self.Thread.sleep(self._delay)
            except self.InterruptedException, e:
                e.printStackTrace()

        def transactionEnd(self, application, transactionData):
            try:
                self.Thread.sleep(self._delay)
            except self.InterruptedException, e:
                e.printStackTrace()
