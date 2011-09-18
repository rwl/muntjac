# Copyright (C) 2011 Vaadin Ltd
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

from com.vaadin.terminal.gwt.server.WebApplicationContext import (WebApplicationContext,)
from com.vaadin.terminal.gwt.server.ApplicationServlet import (ApplicationServlet,)
# from com.google.appengine.api.datastore.Blob import (Blob,)
# from com.google.appengine.api.datastore.DatastoreService import (DatastoreService,)
# from com.google.appengine.api.datastore.DatastoreServiceFactory import (DatastoreServiceFactory,)
# from com.google.appengine.api.datastore.Entity import (Entity,)
# from com.google.appengine.api.datastore.EntityNotFoundException import (EntityNotFoundException,)
# from com.google.appengine.api.datastore.FetchOptions.Builder import (Builder,)
# from com.google.appengine.api.datastore.Key import (Key,)
# from com.google.appengine.api.datastore.KeyFactory import (KeyFactory,)
# from com.google.appengine.api.datastore.PreparedQuery import (PreparedQuery,)
# from com.google.appengine.api.datastore.Query import (Query,)
# from com.google.appengine.api.datastore.Query.FilterOperator import (FilterOperator,)
# from com.google.appengine.api.memcache.Expiration import (Expiration,)
# from com.google.appengine.api.memcache.MemcacheService import (MemcacheService,)
# from com.google.appengine.api.memcache.MemcacheServiceFactory import (MemcacheServiceFactory,)
# from com.google.apphosting.api.DeadlineExceededException import (DeadlineExceededException,)
# from java.io.ByteArrayInputStream import (ByteArrayInputStream,)
# from java.io.ByteArrayOutputStream import (ByteArrayOutputStream,)
# from java.io.IOException import (IOException,)
# from java.io.NotSerializableException import (NotSerializableException,)
# from java.io.ObjectInputStream import (ObjectInputStream,)
# from java.io.ObjectOutputStream import (ObjectOutputStream,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Date import (Date,)
# from java.util.List import (List,)
# from java.util.logging.Level import (Level,)
# from java.util.logging.Logger import (Logger,)
# from javax.servlet.ServletException import (ServletException,)
# from javax.servlet.http.HttpServletRequest import (HttpServletRequest,)
# from javax.servlet.http.HttpServletResponse import (HttpServletResponse,)
# from javax.servlet.http.HttpSession import (HttpSession,)


class GAEApplicationServlet(ApplicationServlet):
    """ApplicationServlet to be used when deploying to Google App Engine, in
    web.xml:

    <pre>
         &lt;servlet&gt;
                 &lt;servlet-name&gt;HelloWorld&lt;/servlet-name&gt;
                 &lt;servlet-class&gt;com.vaadin.terminal.gwt.server.GAEApplicationServlet&lt;/servlet-class&gt;
                 &lt;init-param&gt;
                         &lt;param-name&gt;application&lt;/param-name&gt;
                         &lt;param-value&gt;com.vaadin.demo.HelloWorld&lt;/param-value&gt;
                 &lt;/init-param&gt;
         &lt;/servlet&gt;
    </pre>

    Session support must be enabled in appengine-web.xml:

    <pre>
         &lt;sessions-enabled&gt;true&lt;/sessions-enabled&gt;
    </pre>

    Appengine datastore cleanup can be invoked by calling one of the applications
    with an additional path "/CLEAN". This can be set up as a cron-job in
    cron.xml (see appengine documentation for more information):

    <pre>
    &lt;cronentries&gt;
      &lt;cron&gt;
        &lt;url&gt;/HelloWorld/CLEAN&lt;/url&gt;
        &lt;description&gt;Clean up sessions&lt;/description&gt;
        &lt;schedule&gt;every 2 hours&lt;/schedule&gt;
      &lt;/cron&gt;
    &lt;/cronentries&gt;
    </pre>

    It is recommended (but not mandatory) to extract themes and widgetsets and
    have App Engine server these statically. Extract VAADIN folder (and it's
    contents) 'next to' the WEB-INF folder, and add the following to
    appengine-web.xml:

    <pre>
         &lt;static-files&gt;
              &lt;include path=&quot;/VAADIN/**&quot; /&gt;
         &lt;/static-files&gt;
    </pre>

    Additional limitations:
    <ul>
    <li/>Do not change application state when serving an ApplicationResource.
    <li/>Avoid changing application state in transaction handlers, unless you're
    confident you fully understand the synchronization issues in App Engine.
    <li/>The application remains locked while uploading - no progressbar is
    possible.
    </ul>
    """
    _logger = Logger.getLogger(GAEApplicationServlet.getName())
    # memcache mutex is MUTEX_BASE + sessio id
    _MUTEX_BASE = '_vmutex'
    # used identify ApplicationContext in memcache and datastore
    _AC_BASE = '_vac'
    # UIDL requests will attempt to gain access for this long before telling
    # the client to retry
    _MAX_UIDL_WAIT_MILLISECONDS = 5000
    # Tell client to retry after this delay.
    # Note: currently interpreting Retry-After as ms, not sec
    _RETRY_AFTER_MILLISECONDS = 100
    # Properties used in the datastore
    _PROPERTY_EXPIRES = 'expires'
    _PROPERTY_DATA = 'data'
    # path used for cleanup
    _CLEANUP_PATH = '/CLEAN'
    # max entities to clean at once
    _CLEANUP_LIMIT = 200
    # appengine session kind
    _APPENGINE_SESSION_KIND = '_ah_SESSION'
    # appengine session expires-parameter
    _PROPERTY_APPENGINE_EXPIRES = '_expires'

    def sendDeadlineExceededNotification(self, request, response):
        self.criticalNotification(request, response, 'Deadline Exceeded', 'I\'m sorry, but the operation took too long to complete. We\'ll try reloading to see where we\'re at, please take note of any unsaved data...', '', None)

    def sendNotSerializableNotification(self, request, response):
        self.criticalNotification(request, response, 'NotSerializableException', 'I\'m sorry, but there seems to be a serious problem, please contact the administrator. And please take note of any unsaved data...', '', str(self.getApplicationUrl(request)) + '?restartApplication')

    def sendCriticalErrorNotification(self, request, response):
        self.criticalNotification(request, response, 'Critical error', 'I\'m sorry, but there seems to be a serious problem, please contact the administrator. And please take note of any unsaved data...', '', str(self.getApplicationUrl(request)) + '?restartApplication')

    def service(self, request, response):
        if self.isCleanupRequest(request):
            self.cleanDatastore()
            return
        requestType = self.getRequestType(request)
        if requestType == self.RequestType.STATIC_FILE:
            # no locking needed, let superclass handle
            super(GAEApplicationServlet, self).service(request, response)
            self.cleanSession(request)
            return
        if requestType == self.RequestType.APPLICATION_RESOURCE:
            # no locking needed, let superclass handle
            self.getApplicationContext(request, MemcacheServiceFactory.getMemcacheService())
            super(GAEApplicationServlet, self).service(request, response)
            self.cleanSession(request)
            return
        session = request.getSession(self.requestCanCreateApplication(request, requestType))
        if session is None:
            self.handleServiceSessionExpired(request, response)
            self.cleanSession(request)
            return
        locked = False
        memcache = None
        mutex = self._MUTEX_BASE + session.getId()
        memcache = MemcacheServiceFactory.getMemcacheService()
        try:
            started = Date().getTime()
            # non-UIDL requests will try indefinitely
            while (
                (requestType != self.RequestType.UIDL) or (Date().getTime() - started < self._MAX_UIDL_WAIT_MILLISECONDS)
            ):
                locked = memcache.put(mutex, 1, Expiration.byDeltaSeconds(40), MemcacheService.SetPolicy.ADD_ONLY_IF_NOT_PRESENT)
                if locked:
                    break
                try:
                    self.Thread.sleep(self._RETRY_AFTER_MILLISECONDS)
                except InterruptedException, e:
                    self._logger.finer('Thread.sleep() interrupted while waiting for lock. Trying again. ' + e)
            if not locked:
                # Not locked; only UIDL can get trough here unlocked: tell
                # client to retry
                response.setStatus(HttpServletResponse.SC_SERVICE_UNAVAILABLE)
                # Note: currently interpreting Retry-After as ms, not sec
                response.setHeader('Retry-After', '' + self._RETRY_AFTER_MILLISECONDS)
                return
            # de-serialize or create application context, store in session
            ctx = self.getApplicationContext(request, memcache)
            super(GAEApplicationServlet, self).service(request, response)
            # serialize
            started = Date().getTime()
            baos = ByteArrayOutputStream()
            oos = ObjectOutputStream(baos)
            oos.writeObject(ctx)
            oos.flush()
            bytes = baos.toByteArray()
            started = Date().getTime()
            id = self._AC_BASE + session.getId()
            expire = Date(started + (session.getMaxInactiveInterval() * 1000))
            expires = Expiration.onDate(expire)
            memcache.put(id, bytes, expires)
            ds = DatastoreServiceFactory.getDatastoreService()
            entity = Entity(self._AC_BASE, id)
            entity.setProperty(self._PROPERTY_EXPIRES, expire.getTime())
            entity.setProperty(self._PROPERTY_DATA, Blob(bytes))
            ds.put(entity)
        except DeadlineExceededException, e:
            self._logger.warning('DeadlineExceeded for ' + session.getId())
            self.sendDeadlineExceededNotification(request, response)
        except NotSerializableException, e:
            self._logger.log(Level.SEVERE, 'Not serializable!', e)
            # TODO this notification is usually not shown - should we redirect
            # in some other way - can we?
            self.sendNotSerializableNotification(request, response)
        except Exception, e:
            self._logger.log(Level.WARNING, 'An exception occurred while servicing request.', e)
            self.sendCriticalErrorNotification(request, response)
        finally:
            if locked:
                memcache.delete(mutex)
            self.cleanSession(request)
        # try to get lock
        # "Next, please!"

    def getApplicationContext(self, request, memcache):
        session = request.getSession()
        id = self._AC_BASE + session.getId()
        serializedAC = memcache.get(id)
        if serializedAC is None:
            ds = DatastoreServiceFactory.getDatastoreService()
            key = KeyFactory.createKey(self._AC_BASE, id)
            entity = None
            # Ok, we were a bit optimistic; we'll create a new one later
            try:
                entity = ds.get(key)
            except EntityNotFoundException, e:
                pass # astStmt: [Stmt([]), None]
            if entity is not None:
                blob = entity.getProperty(self._PROPERTY_DATA)
                serializedAC = blob.getBytes()
                # bring it to memcache
                memcache.put(self._AC_BASE + session.getId(), serializedAC, Expiration.byDeltaSeconds(session.getMaxInactiveInterval()), MemcacheService.SetPolicy.ADD_ONLY_IF_NOT_PRESENT)
        if serializedAC is not None:
            bais = ByteArrayInputStream(serializedAC)
            try:
                ois = ObjectInputStream(bais)
                applicationContext = ois.readObject()
                session.setAttribute(WebApplicationContext.getName(), applicationContext)
            except IOException, e:
                self._logger.log(Level.WARNING, 'Could not de-serialize ApplicationContext for ' + session.getId() + ' A new one will be created. ', e)
            except ClassNotFoundException, e:
                self._logger.log(Level.WARNING, 'Could not de-serialize ApplicationContext for ' + session.getId() + ' A new one will be created. ', e)
        # will create new context if the above did not
        return self.getApplicationContext(session)

    def isCleanupRequest(self, request):
        path = self.getRequestPathInfo(request)
        if path is not None and path == self._CLEANUP_PATH:
            return True
        return False

    def cleanSession(self, request):
        """Removes the ApplicationContext from the session in order to minimize the
        data serialized to datastore and memcache.

        @param request
        """
        session = request.getSession(False)
        if session is not None:
            session.removeAttribute(WebApplicationContext.getName())

    def cleanDatastore(self):
        """This will look at the timestamp and delete expired persisted Vaadin and
        appengine sessions from the datastore.

        TODO Possible improvements include: 1. Use transactions (requires entity
        groups - overkill?) 2. Delete one-at-a-time, catch possible exception,
        continue w/ next.
        """
        expire = Date().getTime()
        # Also cleanup GAE sessions
        try:
            ds = DatastoreServiceFactory.getDatastoreService()
            # Vaadin stuff first
            q = Query(self._AC_BASE)
            q.setKeysOnly()
            q.addFilter(self._PROPERTY_EXPIRES, FilterOperator.LESS_THAN_OR_EQUAL, expire)
            pq = ds.prepare(q)
            entities = pq.asList(Builder.withLimit(self._CLEANUP_LIMIT))
            if entities is not None:
                self._logger.info('Vaadin cleanup deleting ' + len(entities) + ' expired Vaadin sessions.')
                keys = list()
                for e in entities:
                    keys.add(e.getKey())
                ds.delete(keys)
            q = Query(self._APPENGINE_SESSION_KIND)
            q.setKeysOnly()
            q.addFilter(self._PROPERTY_APPENGINE_EXPIRES, FilterOperator.LESS_THAN_OR_EQUAL, expire)
            pq = ds.prepare(q)
            entities = pq.asList(Builder.withLimit(self._CLEANUP_LIMIT))
            if entities is not None:
                self._logger.info('Vaadin cleanup deleting ' + len(entities) + ' expired appengine sessions.')
                keys = list()
                for e in entities:
                    keys.add(e.getKey())
                ds.delete(keys)
        except Exception, e:
            self._logger.log(Level.WARNING, 'Exception while cleaning.', e)
