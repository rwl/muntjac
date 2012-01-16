# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

"""Defines a common base class for the server-side implementations of
the communication system between the client code and the server side
components."""

import re
import uuid
import logging

from warnings import warn

from sys import stderr
from urlparse import urljoin

try:
    from cStringIO import StringIO as cStringIO
    from StringIO import StringIO
except ImportError, e:
    from StringIO import StringIO as cStringIO
    from StringIO import StringIO

from babel import Locale

from muntjac.util import clsname

from muntjac.terminal.gwt.server.json_paint_target import JsonPaintTarget
from muntjac.terminal.gwt.server.exceptions import UploadException
from muntjac.terminal.paintable import IPaintable, IRepaintRequestListener
from muntjac.terminal.terminal import IErrorEvent as TerminalErrorEvent
from muntjac.terminal.uri_handler import IErrorEvent as URIHandlerErrorEvent

from muntjac.ui.abstract_component import AbstractComponent
from muntjac.ui.window import Window
from muntjac.ui.component import IComponent
from muntjac.ui.abstract_field import AbstractField

from muntjac.terminal.gwt.server.streaming_events import \
    StreamingStartEventImpl, StreamingErrorEventImpl, StreamingEndEventImpl

from muntjac.terminal.gwt.server.drag_and_drop_service import \
    DragAndDropService

from muntjac.terminal.gwt.client.application_connection import \
    ApplicationConnection

from muntjac.terminal.gwt.server.exceptions import \
    NoInputStreamException, NoOutputStreamException

from muntjac.terminal.gwt.server.abstract_application_servlet import \
    AbstractApplicationServlet, URIHandlerErrorImpl

from muntjac.terminal.gwt.server.change_variables_error_event import \
    ChangeVariablesErrorEvent

from muntjac.terminal.gwt.server.streaming_events import \
    StreamingProgressEventImpl


logger = logging.getLogger(__file__)


class AbstractCommunicationManager(IPaintable, IRepaintRequestListener):
    """This is a common base class for the server-side implementations of
    the communication system between the client code (compiled with GWT
    into JavaScript) and the server side components. Its client side
    counterpart is L{ApplicationConnection}.

    A server side component sends its state to the client in a paint request
    (see L{IPaintable} and L{PaintTarget} on the server side). The
    client widget receives these paint requests as calls to
    L{muntjac.terminal.gwt.client.IPaintable.updateFromUIDL}. The
    client component communicates back to the server by sending a list of
    variable changes (see L{ApplicationConnection.updateVariable} and
    L{VariableOwner.changeVariables}).
    """

    _DASHDASH = '--'

    _GET_PARAM_REPAINT_ALL = 'repaintAll'

    # flag used in the request to indicate that the security token should be
    # written to the response
    _WRITE_SECURITY_TOKEN_FLAG = 'writeSecurityToken'

    # Variable records indexes
    _VAR_PID = 1
    _VAR_NAME = 2
    _VAR_TYPE = 3
    _VAR_VALUE = 0

    _VTYPE_PAINTABLE = 'p'
    _VTYPE_BOOLEAN = 'b'
    _VTYPE_DOUBLE = 'd'
    _VTYPE_FLOAT = 'f'
    _VTYPE_LONG = 'l'
    _VTYPE_INTEGER = 'i'
    _VTYPE_STRING = 's'
    _VTYPE_ARRAY = 'a'
    _VTYPE_STRINGARRAY = 'c'
    _VTYPE_MAP = 'm'

    _VAR_RECORD_SEPARATOR = u'\u001e'

    _VAR_FIELD_SEPARATOR = u'\u001f'

    VAR_BURST_SEPARATOR = u'\u001d'

    VAR_ARRAYITEM_SEPARATOR = u'\u001c'

    VAR_ESCAPE_CHARACTER = u'\u001b'

    _MAX_BUFFER_SIZE = 64 * 1024

    # Same as in apache commons file upload library that was previously used.
    _MAX_UPLOAD_BUFFER_SIZE = 4 * 1024

    _GET_PARAM_ANALYZE_LAYOUTS = 'analyzeLayouts'

    _nextUnusedWindowSuffix = 1

    _LF = '\n'
    _CRLF = '\r\n'
    _UTF8 = 'UTF8'

    _GET_PARAM_HIGHLIGHT_COMPONENT = "highlightComponent"


    def __init__(self, application):

        self._application = application

        self._currentlyOpenWindowsInClient = dict()

        self._dirtyPaintables = list()

        self._paintableIdMap = dict()

        self._idPaintableMap = dict()

        self._idSequence = 0

        # Note that this is only accessed from synchronized block and
        # thus should be thread-safe.
        self._closingWindowName = None

        self._locales = None

        self._pendingLocalesIndex = None

        self._timeoutInterval = -1

        self._dragAndDropService = None

        self._requestThemeName = None

        self._maxInactiveInterval = None

        self.requireLocale(str(application.getLocale()))

        self._typeToKey = dict()
        self._nextTypeKey = 0

        self._highLightedPaintable = None


    def getApplication(self):
        return self._application


    @classmethod
    def _readLine(cls, stream):
        return stream.readline()


    def doHandleSimpleMultipartFileUpload(self, request, response,
                streamVariable, variableName, owner, boundary):
        """Method used to stream content from a multipart request (either
        from servlet or portlet request) to given StreamVariable.

        @raise IOException:
        """
        # multipart parsing, supports only one file for request, but that is
        # fine for our current terminal

        inputStream = request.getInputStream()

        contentLength = request.getContentLength()

        atStart = False
        firstFileFieldFound = False

        rawfilename = 'unknown'
        rawMimeType = 'application/octet-stream'

        # Read the stream until the actual file starts (empty line). Read
        # filename and content type from multipart headers.
        while not atStart:
            readLine = inputStream.readline()
            contentLength -= len(readLine) + 2
            if (readLine.startswith('Content-Disposition:')
                    and readLine.find('filename=') > 0):
                rawfilename = readLine.replace('.*filename=', '')
                parenthesis = rawfilename[:1]
                rawfilename = rawfilename[1:]
                rawfilename = rawfilename[:rawfilename.find(parenthesis)]
                firstFileFieldFound = True
            elif firstFileFieldFound and readLine == '':
                atStart = True
            elif readLine.startswith('Content-Type'):
                rawMimeType = readLine.split(': ')[1]

        contentLength -= (len(boundary) + len(self._CRLF)
                + (2 * len(self._DASHDASH)) + 2)  # 2 == CRLF

        # Reads bytes from the underlying stream. Compares the read bytes to
        # the boundary string and returns -1 if met.
        #
        # The matching happens so that if the read byte equals to the first
        # char of boundary string, the stream goes to "buffering mode". In
        # buffering mode bytes are read until the character does not match
        # the corresponding from boundary string or the full boundary string
        # is found.
        #
        # Note, if this is someday needed elsewhere, don't shoot yourself to
        # foot and split to a top level helper class.
        simpleMultiPartReader = \
                SimpleMultiPartInputStream(inputStream, boundary, self)

        # Should report only the filename even if the browser sends the path
        filename = self.removePath(rawfilename)
        mimeType = rawMimeType

        try:
            # safe cast as in GWT terminal all variable owners are expected
            # to be components.
            component = owner
            if component.isReadOnly():
                raise UploadException('Warning: file upload ignored '
                        'because the component was read-only')

            forgetVariable = self.streamToReceiver(simpleMultiPartReader,
                    streamVariable, filename, mimeType, contentLength)
            if forgetVariable:
                self.cleanStreamVariable(owner, variableName)
        except Exception, e:
            self.handleChangeVariablesError(self._application,
                    owner, e, dict())

        self.sendUploadResponse(request, response)


    def doHandleXhrFilePost(self, request, response, streamVariable,
                variableName, owner, contentLength):
        """Used to stream plain file post (aka XHR2.post(File))

        @raise IOException:
        """
        # These are unknown in filexhr ATM, maybe add to Accept header that
        # is accessible in portlets
        filename = 'unknown'
        mimeType = filename
        stream = request.getInputStream()

        try:
            # safe cast as in GWT terminal all variable owners are expected
            # to be components.
            component = owner
            if component.isReadOnly():
                raise UploadException('Warning: file upload ignored'
                        ' because the component was read-only')

            forgetVariable = self.streamToReceiver(stream, streamVariable,
                    filename, mimeType, contentLength)
            if forgetVariable:
                self.cleanStreamVariable(owner, variableName)
        except Exception, e:
            self.handleChangeVariablesError(self._application, owner, e,
                    dict())

        self.sendUploadResponse(request, response)


    def streamToReceiver(self, inputStream, streamVariable, filename, typ,
                contentLength):
        """@return: true if the streamvariable has informed that the terminal
                    can forget this variable
        @raise UploadException:
        """
        if streamVariable is None:
            raise ValueError, 'StreamVariable for the post not found'

        out = None
        totalBytes = 0
        startedEvent = StreamingStartEventImpl(filename, typ, contentLength)

        try:
            streamVariable.streamingStarted(startedEvent)
            out = streamVariable.getOutputStream()
            listenProgress = streamVariable.listenProgress()

            # Gets the output target stream
            if out is None:
                raise NoOutputStreamException()

            if inputStream is None:
                # No file, for instance non-existent filename in html upload
                raise NoInputStreamException()

            bufferSize = self._MAX_UPLOAD_BUFFER_SIZE
            bytesReadToBuffer = 0
            while totalBytes < len(inputStream):
                buff = inputStream.read(bufferSize)
                bytesReadToBuffer = inputStream.pos - bytesReadToBuffer

                out.write(buff)
                totalBytes += bytesReadToBuffer

                if listenProgress:
                    # update progress if listener set and contentLength
                    # received
                    progressEvent = StreamingProgressEventImpl(filename,
                            typ, contentLength, totalBytes)
                    streamVariable.onProgress(progressEvent)

                if streamVariable.isInterrupted():
                    raise UploadInterruptedException()

            # upload successful
            out.close()
            event = StreamingEndEventImpl(filename, typ, totalBytes)
            streamVariable.streamingFinished(event)
        except UploadInterruptedException, e:
            # Download interrupted by application code
            self.tryToCloseStream(out)
            event = StreamingErrorEventImpl(filename, typ, contentLength,
                    totalBytes, e)
            streamVariable.streamingFailed(event)
            # Note, we are not throwing interrupted exception forward as
            # it is not a terminal level error like all other exception.
        except Exception, e:
            self.tryToCloseStream(out)
            event = StreamingErrorEventImpl(filename, typ, contentLength,
                    totalBytes, e)
            streamVariable.streamingFailed(event)
            # throw exception for terminal to be handled (to be passed
            # to terminalErrorHandler)
            raise UploadException(e)

        return startedEvent.isDisposed()


    def tryToCloseStream(self, out):
        try:
            # try to close output stream (e.g. file handle)
            if out is not None:
                out.close()
        except IOError:
            pass  # NOP


    @classmethod
    def removePath(cls, filename):
        """Removes any possible path information from the filename and
        returns the filename. Separators / and \\ are used.
        """
        if filename is not None:
            filename = re.sub('^.*[/\\\\]', '', filename)

        return filename


    def sendUploadResponse(self, request, response):
        """@raise IOException:
        """
        response.setContentType('text/html')
        out = response.getOutputStream()
        out.write('<html><body>download handled</body></html>')
        out.flush()
        out.close()


    def doHandleUidlRequest(self, request, response, callback, window):
        """Internally process a UIDL request from the client.

        This method calls L{handleVariables} to process any changes to
        variables by the client and then repaints affected components
        using L{paintAfterVariableChanges}.

        Also, some cleanup is done when a request arrives for an application
        that has already been closed.

        The method handleUidlRequest() in subclasses should call this method.

        @param request:
        @param response:
        @param callback:
        @param window:
                   target window for the UIDL request, can be null if target
                   not found
        @raise IOException:
        @raise InvalidUIDLSecurityKeyException:
        """
        self._requestThemeName = request.getParameter('theme')

        self._maxInactiveInterval = \
                request.getSession().getMaxInactiveInterval()

        # repaint requested or session has timed out and new one is created
        repaintAll = request.getParameter(
                self._GET_PARAM_REPAINT_ALL) is not None
        # || (request.getSession().isNew()); FIXME: What the h*ll is this??

        out = response.getOutputStream()

        analyzeLayouts = False
        if repaintAll:
            # analyzing can be done only with repaintAll
            analyzeLayouts = request.getParameter(
                    self._GET_PARAM_ANALYZE_LAYOUTS) is not None

            param = request.getParameter(self._GET_PARAM_HIGHLIGHT_COMPONENT)
            if param != None:
                pid = request.getParameter(self._GET_PARAM_HIGHLIGHT_COMPONENT)
                highLightedPaintable = self._idPaintableMap.get(pid)
                self.highlightPaintable(highLightedPaintable)

        outWriter = out

        # The rest of the process is synchronized with the application
        # in order to guarantee that no parallel variable handling is
        # made
        if self._application.isRunning():
            # Returns if no window found
            if window is None:
                # This should not happen, no windows exists but
                # application is still open.
                logger.warning('Could not get window for application '
                               'with request ID ' + request.getRequestID())
                return
        else:
            # application has been closed
            self.endApplication(request, response, self._application)
            return

        # Change all variables based on request parameters
        if not self.handleVariables(request, response, callback,
                self._application, window):

            # var inconsistency; the client is probably out-of-sync
            ci = None
            try:
                ci = self._application.__class__.getSystemMessages()
            except Exception:
                # FIXME: Handle exception
                # Not critical, but something is still wrong;
                # print stacktrace
                logger.warning('getSystemMessages() failed - continuing')

            if ci is not None:
                msg = ci.getOutOfSyncMessage()
                cap = ci.getOutOfSyncCaption()
                if (msg is not None) or (cap is not None):
                    callback.criticalNotification(request, response, cap,
                            msg, None, ci.getOutOfSyncURL())
                    # will reload page after this
                    return

            # No message to show, let's just repaint all.
            repaintAll = True

        self.paintAfterVariableChanges(request, response, callback, repaintAll,
                outWriter, window, analyzeLayouts)

        if self._closingWindowName is not None:
            if self._closingWindowName in self._currentlyOpenWindowsInClient:
                del self._currentlyOpenWindowsInClient[self._closingWindowName]

            self._closingWindowName = None

        # Finds the window within the application
        #outWriter.close()
        self._requestThemeName = None


    def highlightPaintable(self, highLightedPaintable2):
        sb = StringIO()
        sb.write("*** Debug details of a component:  *** \n")
        sb.write("Type: ")
        sb.write(clsname(highLightedPaintable2))
        if isinstance(highLightedPaintable2, AbstractComponent):
            component = highLightedPaintable2
            sb.write("\nId:")
            idd = self._paintableIdMap.get(component)
            sb.write(idd if idd is not None else 'null')
            if component.getCaption() is not None:
                sb.write("\nCaption:")
                sb.write(component.getCaption())

            self.printHighlightedComponentHierarchy(sb, component)

        logger.info(sb.getvalue())
        sb.close()


    def printHighlightedComponentHierarchy(self, sb, component):
        h = list()
        h.append(component)
        parent = component.getParent()
        while parent is not None:
            h.insert(0, parent)
            parent = parent.getParent()

        sb.write("\nComponent hierarchy:\n")
        application2 = component.getApplication()
        sb.write(clsname(application2))
        sb.write(".")
        sb.write(application2.__class__.__name__)
        sb.write("(")
        sb.write(application2.__class__.__name__);
        sb.write(".java")
        sb.write(":1)")
        l = 1
        for component2 in h:
            sb.write("\n")
            for _ in range(l):
                sb.write("  ")
            l += 1
            componentClass = component2.__class__
            topClass = componentClass
            #while topClass.getEnclosingClass() != None:
            #    topClass = topClass.getEnclosingClass()

            sb.write(clsname(componentClass))
            sb.write(".")
            sb.write(componentClass.__name__);
            sb.write("(")
            sb.write(topClass.__name__)
            sb.write(".java:1)")


    def paintAfterVariableChanges(self, request, response, callback,
                repaintAll, outWriter, window, analyzeLayouts):
        """@raise PaintException:
        @raise IOException:
        """
        if repaintAll:
            self.makeAllPaintablesDirty(window)

        # Removes application if it has stopped during variable changes
        if not self._application.isRunning():
            self.endApplication(request, response, self._application)
            return

        self.openJsonMessage(outWriter, response)

        # security key
        writeSecurityTokenFlag = \
                request.getAttribute(self._WRITE_SECURITY_TOKEN_FLAG, None)

        if writeSecurityTokenFlag is not None:
            seckey = request.getSession().getAttribute(
                    ApplicationConnection.UIDL_SECURITY_TOKEN_ID, None)
            if seckey is None:
                seckey = str( uuid.uuid4() )
                request.getSession().setAttribute(
                        ApplicationConnection.UIDL_SECURITY_TOKEN_ID, seckey)

            outWriter.write('\"'
                    + ApplicationConnection.UIDL_SECURITY_TOKEN_ID + '\":\"')
            outWriter.write(seckey)
            outWriter.write('\",')

        # If the browser-window has been closed - we do not need to paint
        # it at all
        if window.getName() == self._closingWindowName:
            outWriter.write('\"changes\":[]')
        else:
            # re-get window - may have been changed
            newWindow = self.doGetApplicationWindow(request, callback,
                    self._application, window)
            if newWindow != window:
                window = newWindow
                repaintAll = True

            self.writeUidlResponce(callback, repaintAll, outWriter, window,
                    analyzeLayouts)

        self.closeJsonMessage(outWriter)

        #outWriter.close()


    def writeUidlResponce(self, callback, repaintAll, outWriter, window,
                analyzeLayouts):

        outWriter.write('\"changes\":[')

        paintables = None

        invalidComponentRelativeSizes = None

        paintTarget = JsonPaintTarget(self, outWriter, not repaintAll)
        windowCache = self._currentlyOpenWindowsInClient.get(window.getName())
        if windowCache is None:
            windowCache = OpenWindowCache()
            self._currentlyOpenWindowsInClient[window.getName()] = windowCache

        # Paints components
        if repaintAll:
            paintables = list()
            paintables.append(window)

            # Reset sent locales
            self._locales = None
            self.requireLocale( self._application.getLocale() )
        else:
            # remove detached components from paintableIdMap so they
            # can be GC'ed
            # TODO figure out if we could move this beyond the painting phase,
            # "respond as fast as possible, then do the cleanup". Beware of
            # painting the dirty detatched components.
            for p in self._paintableIdMap.keys():
                if p.getApplication() is None:
                    self.unregisterPaintable(p)
                    if self._paintableIdMap[p] in self._idPaintableMap:
                        del self._idPaintableMap[self._paintableIdMap[p]]
                    if p in self._paintableIdMap:
                        del self._paintableIdMap[p]
                    if p in self._dirtyPaintables:
                        self._dirtyPaintables.remove(p)

            paintables = self.getDirtyVisibleComponents(window)

        if paintables is not None:
            # We need to avoid painting children before parent.
            # This is ensured by ordering list by depth in component
            # tree

            def compare(c1, c2):
                d1 = 0
                while c1.getParent() is not None:
                    d1 += 1
                    c1 = c1.getParent()
                d2 = 0
                while c2.getParent() is not None:
                    d2 += 1
                    c2 = c2.getParent()
                if d1 < d2:
                    return -1
                if d1 > d2:
                    return 1
                return 0

            paintables.sort(cmp=compare)

            for p in paintables:
                # TODO CLEAN
                if isinstance(p, Window):
                    w = p
                    if w.getTerminal() is None:
                        w.setTerminal(
                            self._application.getMainWindow().getTerminal())

                # This does not seem to happen in tk5, but remember this case:
                # else if (p instanceof IComponent) { if (((IComponent)
                # p).getParent() == null || ((IComponent) p).getApplication() ==
                # null) { // IComponent requested repaint, but is no // longer
                # attached: skip paintablePainted(p); continue; } }

                # TODO we may still get changes that have been
                # rendered already (changes with only cached flag)
                if paintTarget.needsToBePainted(p):
                    paintTarget.startTag('change')
                    paintTarget.addAttribute('format', 'uidl')
                    pid = self.getPaintableId(p)
                    paintTarget.addAttribute('pid', pid)

                    p.paint(paintTarget)

                    paintTarget.endTag('change')

                self.paintablePainted(p)

                if analyzeLayouts:

                    # FIXME: circular import
                    from muntjac.terminal.gwt.server.component_size_validator \
                        import ComponentSizeValidator

                    w = p
                    invalidComponentRelativeSizes = ComponentSizeValidator.\
                            validateComponentRelativeSizes(w.getContent(),
                                    None, None)

                    # Also check any existing subwindows
                    if w.getChildWindows() is not None:
                        for subWindow in w.getChildWindows():
                            invalidComponentRelativeSizes = \
                                    ComponentSizeValidator.\
                                    validateComponentRelativeSizes(
                                            subWindow.getContent(),
                                            invalidComponentRelativeSizes,
                                            None)

        paintTarget.close()
        outWriter.write(']')  # close changes

        outWriter.write(', \"meta\" : {')
        metaOpen = False

        if repaintAll:
            metaOpen = True
            outWriter.write('\"repaintAll\":true')
            if analyzeLayouts:
                outWriter.write(', \"invalidLayouts\":')
                outWriter.write('[')
                if invalidComponentRelativeSizes is not None:
                    first = True
                    for invalidLayout in invalidComponentRelativeSizes:
                        if not first:
                            outWriter.write(',')
                        else:
                            first = False
                        invalidLayout.reportErrors(outWriter, self, stderr)
                outWriter.write(']')

            if self._highLightedPaintable is not None:
                outWriter.write(", \"hl\":\"")
                idd = self._paintableIdMap.get(self._highLightedPaintable)
                outWriter.write(idd if idd is not None else 'null')
                outWriter.write("\"")
                self._highLightedPaintable = None

        ci = None
        try:
            ci = self._application.getSystemMessages()
        except AttributeError, e:
            logger.warning('getSystemMessages() failed - continuing')

        # meta instruction for client to enable auto-forward to
        # sessionExpiredURL after timer expires.
        if ((ci is not None) and (ci.getSessionExpiredMessage() is None)
                and (ci.getSessionExpiredCaption() is None)
                and ci.isSessionExpiredNotificationEnabled()):
            newTimeoutInterval = self.getTimeoutInterval()
            if repaintAll or (self._timeoutInterval != newTimeoutInterval):
                if ci.getSessionExpiredURL() is None:
                    escapedURL = ''
                else:
                    escapedURL = ci.getSessionExpiredURL().replace('/', '\\/')
                if metaOpen:
                    outWriter.write(',')

                outWriter.write('\"timedRedirect\":{\"interval\":'
                        + newTimeoutInterval + 15 + ',\"url\":\"'
                        + escapedURL + '\"}')
                metaOpen = True

            self._timeoutInterval = newTimeoutInterval

        outWriter.write('}, \"resources\" : {')

        # Precache custom layouts

        # TODO We should only precache the layouts that are not
        # cached already (plagiate from usedPaintableTypes)
        resourceIndex = 0
        for resource in paintTarget.getUsedResources():
            is_ = None
            try:
                is_ = callback.getThemeResourceAsStream(self.getTheme(window),
                        resource)
            except IOError, e:
                # FIXME: Handle exception
                logger.info('Failed to get theme resource stream.')

            if is_ is not None:
                outWriter.write((', ' if resourceIndex > 0 else '')
                        + '\"' + resource + '\" : ')
                resourceIndex += 1  # post increment
                layout = str()
                try:
                    layout = is_.read()
                except IOError, e:
                    # FIXME: Handle exception
                    logger.info('Resource transfer failed: ' + str(e))

                outWriter.write('\"%s\"' % JsonPaintTarget.escapeJSON(layout))
            else:
                # FIXME: Handle exception
                logger.critical('CustomLayout not found: ' + resource)

        outWriter.write('}')

        usedPaintableTypes = paintTarget.getUsedPaintableTypes()
        typeMappingsOpen = False
        for class1 in usedPaintableTypes:
            if windowCache.cache(class1):
                # client does not know the mapping key for this type,
                # send mapping to client
                if not typeMappingsOpen:
                    typeMappingsOpen = True
                    outWriter.write(', \"typeMappings\" : { ')
                else:
                    outWriter.write(' , ')
                canonicalName = clsname(class1)

                if canonicalName.startswith('muntjac.ui'):
                    # use Muntjac package names  FIXME: Python client side
                    canonicalName = 'com.vaadin.ui.' + class1.__name__
                elif canonicalName.startswith('muntjac.demo.sampler'):
                    canonicalName = 'com.vaadin.demo.sampler.' + class1.__name__
                elif hasattr(class1, 'TYPE_MAPPING'):
                    canonicalName = getattr(class1, 'TYPE_MAPPING')
                else:
                    raise ValueError('type mapping name [%s]' % canonicalName)

                outWriter.write('\"')
                outWriter.write(canonicalName)
                outWriter.write('\" : ')
                outWriter.write(self.getTagForType(class1))

        if typeMappingsOpen:
            outWriter.write(' }')

        # add any pending locale definitions requested by the client
        self.printLocaleDeclarations(outWriter)

        if self._dragAndDropService is not None:
            self._dragAndDropService.printJSONResponse(outWriter)


    def getTimeoutInterval(self):
        return self._maxInactiveInterval


    def getTheme(self, window):
        themeName = window.getTheme()
        requestThemeName = self.getRequestTheme()

        if requestThemeName is not None:
            themeName = requestThemeName

        if themeName is None:
            themeName = AbstractApplicationServlet.getDefaultTheme()

        return themeName


    def getRequestTheme(self):
        return self._requestThemeName


    def makeAllPaintablesDirty(self, window):
        # If repaint is requested, clean all ids in this root window
        for key in self._idPaintableMap.keys():
            c = self._idPaintableMap[key]

            if self.isChildOf(window, c):
                if key in self._idPaintableMap:
                    del self._idPaintableMap[key]

                if c in self._paintableIdMap:
                    del self._paintableIdMap[c]

        # clean WindowCache
        openWindowCache = \
                self._currentlyOpenWindowsInClient.get(window.getName())

        if openWindowCache is not None:
            openWindowCache.clear()


    def unregisterPaintable(self, p):
        """Called when communication manager stops listening for repaints
        for given component.
        """
        p.removeListener(self, IRepaintRequestListener)


    def handleVariables(self, request, response, callback, application2,
                window):
        """If this method returns false, something was submitted that we did
        not expect; this is probably due to the client being out-of-sync
        and sending variable changes for non-existing pids

        @return: true if successful, false if there was an inconsistency
        """
        success = True

        changes = self.getRequestPayload(request)
        if changes is not None:

            # Manage bursts one by one
            bursts = re.split(self.VAR_BURST_SEPARATOR, changes)
            # FIXME: remove trailing empty string using re
            if (len(bursts) > 0) & (bursts[-1] == ''):
                bursts = bursts[:-1]

            # Security: double cookie submission pattern unless disabled by
            # property
            if application2.getProperty(AbstractApplicationServlet.\
                        SERVLET_PARAMETER_DISABLE_XSRF_PROTECTION) != 'true':
                if len(bursts) == 1 and 'init' == bursts[0]:
                    # init request; don't handle any variables, key sent in
                    # response.
                    request.setAttribute(
                            self._WRITE_SECURITY_TOKEN_FLAG, True)
                    return True
                else:
                    # ApplicationServlet has stored the security token in the
                    # session; check that it matched the one sent in the UIDL
                    sessId = request.getSession().getAttribute(
                            ApplicationConnection.UIDL_SECURITY_TOKEN_ID, '')

                    if (sessId is None) or (sessId != bursts[0]):
                        msg = 'Security key mismatch'
                        raise InvalidUIDLSecurityKeyException(msg)

            for bi in range(1, len(bursts)):
                burst = bursts[bi]
                success = self.handleVariableBurst(request, application2,
                        success, burst)

                # In case that there were multiple bursts, we know that this
                # is a special synchronous case for closing window. Thus we
                # are not interested in sending any UIDL changes back to
                # client. Still we must clear component tree between bursts
                # to ensure that no removed components are updated. The
                # painting after the last burst is handled normally by the
                # calling method.
                if bi < (len(bursts) - 1):
                    # We will be discarding all changes
                    outWriter = cStringIO()
                    self.paintAfterVariableChanges(request, response,
                            callback, True, outWriter, window, False)

        # Note that we ignore inconsistencies while handling unload request.
        # The client can't remove invalid variable changes from the burst, and
        # we don't have the required logic implemented on the server side. E.g.
        # a component is removed in a previous burst.
        return success or (self._closingWindowName is not None)


    def handleVariableBurst(self, source, app, success, burst):
        # extract variables to two dim string array
        tmp = re.split(self._VAR_RECORD_SEPARATOR, burst)
        variableRecords = [None] * len(tmp)

        for i in range(len(tmp)):
            variableRecords[i] = re.split(self._VAR_FIELD_SEPARATOR, tmp[i])

        i = 0
        while i < len(variableRecords):
            variable = variableRecords[i]
            nextVariable = None
            if (i + 1) < len(variableRecords):
                nextVariable = variableRecords[i + 1]

            owner = self.getVariableOwner( variable[self._VAR_PID] )
            if (owner is not None) and owner.isEnabled():
                m = dict()
                if ((nextVariable is not None) and (variable[self._VAR_PID]
                            == nextVariable[self._VAR_PID])):
                    # we have more than one value changes in row for
                    # one variable owner, collect em in HashMap
                    m[variable[self._VAR_NAME]] = \
                        self.convertVariableValue(variable[self._VAR_TYPE][0],
                                                  variable[self._VAR_VALUE])
                else:
                    # use optimized single value map
                    m[variable[self._VAR_NAME]] = \
                        self.convertVariableValue(variable[self._VAR_TYPE][0],
                                                  variable[self._VAR_VALUE])

                # collect following variable changes for this owner
                while (nextVariable is not None and variable[self._VAR_PID] \
                        == nextVariable[self._VAR_PID]):
                    i += 1
                    variable = nextVariable
                    if (i + 1) < len(variableRecords):
                        nextVariable = variableRecords[i + 1]
                    else:
                        nextVariable = None

                    m[variable[self._VAR_NAME]] = \
                        self.convertVariableValue(variable[self._VAR_TYPE][0],
                                                  variable[self._VAR_VALUE])

                try:
                    self.changeVariables(source, owner, m)

                    # Special-case of closing browser-level windows:
                    # track browser-windows currently open in client
                    if isinstance(owner, Window) and owner.getParent() is None:
                        close = m.get('close')
                        if (close is not None) and bool(close):
                            self._closingWindowName = owner.getName()

                except Exception, e:
                    if isinstance(owner, IComponent):
                        self.handleChangeVariablesError(app, owner, e, m)
                    else:
                        # TODO DragDropService error handling
                        raise RuntimeError(e)
            else:
                # Handle special case where window-close is called
                # after the window has been removed from the
                # application or the application has closed
                if (variable[self._VAR_NAME] == 'close'
                        and variable[self._VAR_VALUE] == 'true'):
                    # Silently ignore this
                    i += 1
                    continue

                # Ignore variable change
                msg = 'Warning: Ignoring variable change for '
                if owner is not None:
                    msg += 'disabled component ' + str(owner.__class__)
                    caption = owner.getCaption()
                    if caption is not None:
                        msg += ', caption=' + caption
                else:
                    msg += ('non-existent component, VAR_PID='
                            + variable[self._VAR_PID])
                    success = False

                logger.warning(msg)

            i += 1

        return success


    def changeVariables(self, source, owner, m):
        owner.changeVariables(source, m)


    def getVariableOwner(self, string):
        owner = self._idPaintableMap.get(string)
        if (owner is None) and string.startswith('DD'):
            return self.getDragAndDropService()
        return owner


    def getDragAndDropService(self):
        if self._dragAndDropService is None:
            self._dragAndDropService = DragAndDropService(self)
        return self._dragAndDropService


    def getRequestPayload(self, request):
        """Reads the request data from the Request and returns it converted
        to an UTF-8 string.

        @raise IOException:
        """
        requestLength = request.getContentLength()
        if requestLength == 0:
            return None

        inputStream = request.getInputStream()
        if inputStream is not None:
            return inputStream.read()
        else:
            return None


    def handleChangeVariablesError(self, application, owner, e, m):
        """Handles an error (exception) that occurred when processing variable
        changes from the client or a failure of a file upload.

        For L{AbstractField} components, C{AbstractField.handleError()}
        is called. In all other cases (or if the field does not handle the
        error), L{ErrorListener.terminalError} for the application error
        handler is called.

        @param application:
        @param owner:
                   component that the error concerns
        @param e:
                   exception that occurred
        @param m:
                   map from variable names to values
        """
        handled = False
        errorEvent = ChangeVariablesErrorEvent(owner, e, m)

        if isinstance(owner, AbstractField):
            try:
                handled = owner.handleError(errorEvent)
            except Exception, handlerException:
                # If there is an error in the component error handler we pass
                # the that error to the application error handler and continue
                # processing the actual error
                application.getErrorHandler().terminalError(
                        ErrorHandlerErrorEvent(handlerException))
                handled = False

        if not handled:
            application.getErrorHandler().terminalError(errorEvent)


    def convertVariableValue(self, variableType, strValue):
        m = {
            self._VTYPE_ARRAY: lambda s: self.convertArray(s),
            self._VTYPE_MAP: lambda s: self.convertMap(s),
            self._VTYPE_STRINGARRAY: lambda s: self.convertStringArray(s),
            self._VTYPE_STRING: lambda s: self.decodeVariableValue(s),
            self._VTYPE_INTEGER: lambda s: int(s),
            self._VTYPE_LONG: lambda s: long(s),
            self._VTYPE_FLOAT: lambda s: float(s),
            self._VTYPE_DOUBLE: lambda s: float(s),
            self._VTYPE_BOOLEAN: lambda s: s.lower() == 'true',
            self._VTYPE_PAINTABLE: lambda s: self._idPaintableMap.get(s)
        }.get(variableType)

        if m is not None:
            return m(strValue)
        else:
            return None


    def convertMap(self, strValue):
        parts = strValue.split(self.VAR_ARRAYITEM_SEPARATOR)
        mapp = dict()
        i = 0
        while i < len(parts):
            key = parts[i]
            if len(key) > 0:
                variabletype = key[0]
                # decode encoded separators
                decodedValue = self.decodeVariableValue(parts[i + 1])
                decodedKey = self.decodeVariableValue(key[1:])
                value = self.convertVariableValue(variabletype, decodedValue)
                mapp[decodedKey] = value
            i += 2
        return mapp


    def convertStringArray(self, strValue):
        # need to return delimiters and filter them out; otherwise empty
        # strings are lost
        # an extra empty delimiter at the end is automatically eliminated
        arrayItemSeparator = self.VAR_ARRAYITEM_SEPARATOR
        splitter = re.compile('(\\' + arrayItemSeparator + '+)')

        tokens = list()
        prevToken = arrayItemSeparator
        for token in splitter.split(strValue):
            if arrayItemSeparator != token:
                # decode encoded separators
                tokens.append(self.decodeVariableValue(token))
            elif arrayItemSeparator == prevToken:
                tokens.append('')
            prevToken = token

        return tokens


    def convertArray(self, strValue):
        val = strValue.split(self.VAR_ARRAYITEM_SEPARATOR)

        if len(val) == 0 or (len(val) == 1 and len(val[0]) == 0):
            return []

        values = [None] * len(val)
        for i in range(len(values)):
            string = val[i]
            # first char of string is type
            variableType = string[0]
            values[i] = self.convertVariableValue(variableType, string[1:])

        return values


    def decodeVariableValue(self, encodedValue):
        """Decode encoded burst, record, field and array item separator
        characters in a variable value String received from the client.
        This protects from separator injection attacks.

        @param encodedValue: value to decode
        @return: decoded value
        """
        iterator = iter(encodedValue)

        try:
            character = iterator.next()
        except StopIteration:
            return ''

        result = StringIO()
        while True:
            try:
                if self.VAR_ESCAPE_CHARACTER == character:
                    character = iterator.next()
                    if character == chr(ord(self.VAR_ESCAPE_CHARACTER) + 0x30):
                        # escaped escape character
                        result.write(self.VAR_ESCAPE_CHARACTER)

                    elif character == chr(ord(self.VAR_BURST_SEPARATOR) + 0x30):
                        pass
                    elif character == chr(ord(self._VAR_RECORD_SEPARATOR)+0x30):
                        pass
                    elif character == chr(ord(self._VAR_FIELD_SEPARATOR) +0x30):
                        pass
                    elif (character ==
                            chr(ord(self.VAR_ARRAYITEM_SEPARATOR) + 0x30)):
                        # +0x30 makes these letters for easier reading
                        result.write( chr(ord(character) - 0x30) )
                    else:
                        # other escaped character - probably a client-server
                        # version mismatch
                        raise ValueError("Invalid escaped character from the "
                                "client - check that the widgetset and server "
                                "versions match")
                else:
                    # not a special character - add it to the result as is
                    result.write(character)

                character = iterator.next()

            except StopIteration:
                break

        r = result.getvalue()
        result.close()
        return r


    def printLocaleDeclarations(self, outWriter):
        """Prints the queued (pending) locale definitions to a PrintWriter
        in a (UIDL) format that can be sent to the client and used there in
        formatting dates, times etc.
        """
        # Send locale informations to client
        outWriter.write(', \"locales\":[')

        while self._pendingLocalesIndex < len(self._locales):
            l = self.generateLocale(self._locales[self._pendingLocalesIndex])

            # Locale name
            outWriter.write('{\"name\":\"' + str(l) + '\",')

            # Month names (both short and full)
            months = l.months['format']['wide'].values()
            short_months = l.months['format']['abbreviated'].values()

            outWriter.write(('\"smn\":[\"'
                    + short_months[0] + '\",\"' + short_months[1] + '\",\"'
                    + short_months[2] + '\",\"' + short_months[3] + '\",\"'
                    + short_months[4] + '\",\"' + short_months[5] + '\",\"'
                    + short_months[6] + '\",\"' + short_months[7] + '\",\"'
                    + short_months[8] + '\",\"' + short_months[9] + '\",\"'
                    + short_months[10] + '\",\"' + short_months[11] + '\"'
                    + '],').encode('utf-8'))
            outWriter.write(('\"mn\":[\"'
                    + months[0] + '\",\"' + months[1] + '\",\"'
                    + months[2] + '\",\"' + months[3] + '\",\"'
                    + months[4] + '\",\"' + months[5] + '\",\"'
                    + months[6] + '\",\"' + months[7] + '\",\"'
                    + months[8] + '\",\"' + months[9] + '\",\"'
                    + months[10] + '\",\"' + months[11] + '\"'
                    + '],').encode('utf-8'))

            # Weekday names (both short and full)
            days = l.days['format']['wide'].values()
            short_days = l.days['format']['abbreviated'].values()

            outWriter.write(('\"sdn\":[\"'
                    + short_days[0] + '\",\"' + short_days[1] + '\",\"'
                    + short_days[2] + '\",\"' + short_days[3] + '\",\"'
                    + short_days[4] + '\",\"' + short_days[5] + '\",\"'
                    + short_days[6] + '\"'
                    + '],').encode('utf-8'))
            outWriter.write(('\"dn\":[\"'
                    + days[0] + '\",\"' + days[1] + '\",\"'
                    + days[2] + '\",\"' + days[3] + '\",\"'
                    + days[4] + '\",\"' + days[5] + '\",\"'
                    + days[6] + '\"'
                    + '],').encode('utf-8'))

            # First day of week
            # (Babel: 6 = sunday, 0 = monday, Vaadin: 0 = sunday, 1 = monday)
            fdow = l.first_week_day
            if fdow == 6:
                fdow = 0
            else:
                fdow += 1
            outWriter.write('\"fdow\":' + str(fdow) + ',')

            # Date formatting (MM/DD/YYYY etc.)
            try:
                df = l.date_formats['short'].pattern
                df += ' '
                df += l.time_formats['short'].pattern
                df = df.encode('utf-8')  # convert unicode to string
            except KeyError:
                logger.warning('Unable to get default date '
                               'pattern for locale ' + str(l))
                #df = locale.nl_langinfo(locale.D_T_FMT)
                df = 'dd/MM/yy HH:mm'

            timeStart = df.find('H')
            if timeStart < 0:
                timeStart = df.find('h')
            ampm_first = df.find('a')
            # E.g. in Korean locale AM/PM is before h:mm
            # TODO should take that into consideration on client-side as well,
            # now always h:mm a
            if ampm_first > 0 and ampm_first < timeStart:
                timeStart = ampm_first
            # Hebrew locale has time before the date
            timeFirst = timeStart == 0
            if timeFirst:
                dateStart = df.find(' ')
                if ampm_first > dateStart:
                    dateStart = df.find(' ', ampm_first)
                dateformat = df[dateStart + 1:]
            else:
                dateformat = df[:timeStart - 1]

            outWriter.write('\"df\":\"' + dateformat.strip() + '\",')

            # Time formatting (24 or 12 hour clock and AM/PM suffixes)
            timeformat = df[timeStart:len(df)]

            # Doesn't return second or milliseconds.
            #
            # We use timeformat to determine 12/24-hour clock
            twelve_hour_clock = timeformat.find('a') > -1

            # TODO there are other possibilities as well, like 'h' in french
            # (ignore them, too complicated)
            hour_min_delimiter = '.' if timeformat.find('.') > -1 else ':'

            # outWriter.write("\"tf\":\"" + timeformat + "\",");
            outWriter.write('\"thc\":' + str(twelve_hour_clock).lower() + ',')
            outWriter.write('\"hmd\":\"' + hour_min_delimiter + '\"')
            if twelve_hour_clock:
                ampm = [( l.periods['am'] ).encode('utf-8'),
                        ( l.periods['pm'] ).encode('utf-8')]
                outWriter.write(',\"ampm\":[\"' + ampm[0] + '\",\"'
                                + ampm[1] + '\"]')
            outWriter.write('}')
            if self._pendingLocalesIndex < len(self._locales) - 1:
                outWriter.write(',')

            self._pendingLocalesIndex += 1

        outWriter.write(']')  # close locales


    def doGetApplicationWindow(self, request, callback, application,
                assumedWindow):

        window = None

        # If the client knows which window to use, use it if possible
        windowClientRequestedName = request.getParameter('windowName')

        if ((assumedWindow is not None)
                and (assumedWindow in application.getWindows())):
            windowClientRequestedName = assumedWindow.getName()

        if windowClientRequestedName is not None:
            window = application.getWindow(windowClientRequestedName)
            if window is not None:
                return window

        # If client does not know what window it wants
        if (window is None) and not request.isRunningInPortlet():
            # This is only supported if the application is running inside a
            # servlet

            # Get the path from URL
            path = callback.getRequestPathInfo(request)

            # If the path is specified, create name from it.
            #
            # An exception is if UIDL request have come this far. This happens
            # if main window is refreshed. In that case we always return main
            # window (infamous hacky support for refreshes if only main window
            # is used). However we are not returning with main window here (we
            # will later if things work right), because the code is so cryptic
            # that nobody really knows what it does.
            pathMayContainWindowName = (path is not None
                    and len(path) > 0 and not (path == '/'))

            if pathMayContainWindowName:
                uidlRequest = path.startswith('/UIDL')
                if not uidlRequest:
                    windowUrlName = None
                    if path[0] == '/':
                        path = path[1:]
                    index = path.find('/')
                    if index < 0:
                        windowUrlName = path
                        path = ''
                    else:
                        windowUrlName = path[:index]
                        path = path[index + 1:]
                    window = application.getWindow(windowUrlName)

        # By default, use mainwindow
        if window is None:
            window = application.getMainWindow()
            # Return null if no main window was found
            if window is None:
                return None

        # If the requested window is already open, resolve conflict
        if window.getName() in self._currentlyOpenWindowsInClient:
            newWindowName = window.getName()

            while newWindowName in self._currentlyOpenWindowsInClient:
                newWindowName = (window.getName() + '_' +
                        str(self._nextUnusedWindowSuffix))
                self._nextUnusedWindowSuffix += 1

            window = application.getWindow(newWindowName)

            # If everything else fails, use main window even in case of
            # conflicts
            if window is None:
                window = application.getMainWindow()

        return window


    def endApplication(self, request, response, application):
        """Ends the Application.

        The browser is redirected to the Application logout URL set with
        L{Application.setLogoutURL}, or to the application URL if no logout
        URL is given.

        @param request:
                   the request instance.
        @param response:
                   the response to write to.
        @param application:
                   the Application to end.
        @raise IOException:
                    if the writing failed due to input/output error.
        """
        logoutUrl = application.getLogoutURL()
        if logoutUrl is None:
            logoutUrl = application.getURL()

        # clients JS app is still running, send a special json file to tell
        # client that application has quit and where to point browser now
        # Set the response type
        outWriter = response.getOutputStream()
        self.openJsonMessage(outWriter, response)
        outWriter.write('\"redirect\":{')
        outWriter.write('\"url\":\"' + logoutUrl + '\"}')
        self.closeJsonMessage(outWriter)
        outWriter.flush()


    def closeJsonMessage(self, outWriter):
        outWriter.write('}]')


    def openJsonMessage(self, outWriter, response):
        """Writes the opening of JSON message to be sent to client.
        """
        # Sets the response type
        response.setContentType('application/json; charset=UTF-8')
        # some dirt to prevent cross site scripting
        outWriter.write('for(;;);[{')


    def getPaintableId(self, paintable):
        """Gets the IPaintable Id. If IPaintable has debug id set it will be
        used prefixed with "PID_S". Otherwise a sequenced ID is created.

        @param paintable:
        @return: the paintable Id.
        """
        idd = self._paintableIdMap.get(paintable)
        if idd is None:
            # use testing identifier as id if set
            idd = paintable.getDebugId()
            if idd is None:
                idd = 'PID' + str(self._idSequence)
                self._idSequence += 1  # post increment
            else:
                idd = 'PID_S' + idd

            old = self._idPaintableMap[idd] = paintable
            if (old is not None) and (old != paintable):
                # Two paintables have the same id. We still make sure the
                # old one is a component which is still attached to the
                # application. This is just a precaution and should not be
                # absolutely necessary.

                if (isinstance(old, IComponent)
                        and (old.getApplication() is not None)):
                    raise ValueError(('Two paintables ('
                            + paintable.__class__.__name__
                            + ',' + old.__class__.__name__
                            + ') have been assigned the same id: '
                            + paintable.getDebugId()))

            self._paintableIdMap[paintable] = idd

        return idd


    def hasPaintableId(self, paintable):
        return paintable in self._paintableIdMap


    def getDirtyVisibleComponents(self, w):
        """Returns dirty components which are in given window. Components
        in an invisible subtrees are omitted.

        @param w:
                   root window for which dirty components is to be fetched
        """
        resultset = list(self._dirtyPaintables)

        # The following algorithm removes any components that would be painted
        # as a direct descendant of other components from the dirty components
        # list. The result is that each component should be painted exactly
        # once and any unmodified components will be painted as "cached=true".

        for p in self._dirtyPaintables:
            if isinstance(p, IComponent):
                component = p
                if component.getApplication() is None:
                    # component is detached after requestRepaint is called
                    resultset.remove(p)
                    self._dirtyPaintables.remove(p)
                else:
                    componentsRoot = component.getWindow()
                    if componentsRoot is None:
                        # This should not happen unless somebody has overriden
                        # getApplication or getWindow in an illegal way.
                        raise ValueError('component.getWindow() returned null '
                                'for a component attached to the application')

                    if componentsRoot.getParent() is not None:
                        # this is a subwindow
                        componentsRoot = componentsRoot.getParent()

                    if componentsRoot != w:
                        resultset.remove(p)
                    elif ((component.getParent() is not None)
                            and not component.getParent().isVisible()):
                        # Do not return components in an invisible subtree.
                        #
                        # Components that are invisible in visible subree, must
                        # be rendered (to let client know that they need to be
                        # hidden).
                        resultset.remove(p)

        return resultset


    def repaintRequested(self, event):
        """@see: L{IRepaintRequestListener.repaintRequested}"""
        p = event.getPaintable()
        if p not in self._dirtyPaintables:
            self._dirtyPaintables.append(p)


    def paintablePainted(self, paintable):
        """Internally mark a L{IPaintable} as painted and start
        collecting new repaint requests for it.
        """
        if paintable in self._dirtyPaintables:
            self._dirtyPaintables.remove(paintable)
        paintable.requestRepaintRequests()


    def requireLocale(self, value):
        """Queues a locale to be sent to the client (browser) for date and
        time entry etc. All locale specific information is derived from
        server-side L{Locale} instances and sent to the client when
        needed, eliminating the need to use the L{Locale} class and all
        the framework behind it on the client.
        """
        if self._locales is None:
            self._locales = list()
            l = self._application.getLocale()
            self._locales.append(str(l))
            self._pendingLocalesIndex = 0

        if str(value) not in self._locales:
            self._locales.append(str(value))


    def generateLocale(self, value):
        """Constructs a L{Locale} instance to be sent to the client based on
        a short locale description string.

        @see: L{requireLocale}
        """
        temp = value.split('_')
        if len(temp) == 1:
            return Locale(temp[0], '')
        elif len(temp) == 2:
            return Locale(temp[0], temp[1])
        else:
            return Locale(temp[0], temp[1])#, temp[2])
        return value


    @classmethod
    def isChildOf(cls, parent, child):
        """Helper method to test if a component contains another.
        """
        p = child.getParent()
        while p is not None:
            if parent == p:
                return True
            p = p.getParent()
        return False


    def handleURI(self, window, request, response, callback):
        """Calls the Window URI handler for a request and returns the
        L{DownloadStream} returned by the handler.

        If the window is the main window of an application, the (deprecated)
        L{Application.handleURI} is called first
        to handle L{ApplicationResource}s, and the window handler is
        only called if it returns null.

        @param window:
                   the target window of the request
        @param request:
                   the request instance
        @param response:
                   the response to write to
        @return: DownloadStream if the request was handled and further
                    processing should be suppressed, null otherwise.
        @see: L{URIHandler}
        """
        warn("deprecated", DeprecationWarning)

        uri = callback.getRequestPathInfo(request)

        # If no URI is available
        if uri is None:
            uri = ''
        else:
            # Removes the leading /
            while uri.startswith('/') and len(uri) > 0:
                uri = uri[1:]

        # Handles the uri
        try:
            context = self._application.getURL()
            if window == self._application.getMainWindow():
                stream = None
                # Application.handleURI run first. Handles possible
                # ApplicationResources.
                stream = self._application.handleURI(context, uri)
                if stream is None:
                    stream = window.handleURI(context, uri)
                return stream
            else:
                # Resolve the prefix end index
                index = uri.find('/')
                if index > 0:
                    prefix = uri[:index]
                    windowContext = urljoin(context, prefix + '/')
                    if len(uri) > len(prefix) + 1:
                        windowUri = uri[len(prefix) + 1:]
                    else:
                        windowUri = ''
                    return window.handleURI(windowContext, windowUri)
                else:
                    return None
        except Exception, t:
            event = URIHandlerErrorImpl(self._application, t)
            self._application.getErrorHandler().terminalError(event)
            return None


    def getTagForType(self, class1):
        obj = self._typeToKey.get(class1)
        if obj is None:
            obj = self._nextTypeKey
            self._nextTypeKey += 1
            self._typeToKey[class1] = obj
        return str(obj)


    def getStreamVariableTargetUrl(self, owner, name, value):
        raise NotImplementedError


    def cleanStreamVariable(self, owner, name):
        raise NotImplementedError


class IRequest(object):
    """Generic interface of a (HTTP or Portlet) request to the application.

    This is a wrapper interface that allows
    L{AbstractCommunicationManager} to use a unified API.

    @author: peholmst
    """

    def getSession(self):
        """Gets a L{Session} wrapper implementation representing the
        session for which this request was sent.

        Multiple Muntjac applications can be associated with a single session.

        @return: Session
        """
        raise NotImplementedError


    def isRunningInPortlet(self):
        """Are the applications in this session running in a portlet or
        directly as servlets.

        @return: true if in a portlet
        """
        raise NotImplementedError


    def getParameter(self, name):
        """Get the named HTTP or portlet request parameter.
        """
        raise NotImplementedError


    def getContentLength(self):
        """Returns the length of the request content that can be read from the
        input stream returned by L{getInputStream}.

        @return: content length in bytes
        """
        raise NotImplementedError


    def getInputStream(self):
        """Returns an input stream from which the request content can be read.
        The request content length can be obtained with
        L{getContentLength} without reading the full stream contents.

        @raise IOException:
        """
        raise NotImplementedError


    def getRequestID(self):
        """Returns the request identifier that identifies the target Muntjac
        window for the request.

        @return: String identifier for the request target window
        """
        raise NotImplementedError


    def getAttribute(self, name):
        raise NotImplementedError


    def setAttribute(self, name, value):
        raise NotImplementedError


    def getWrappedRequest(self):
        """Gets the underlying request object. The request is typically either
        a L{ServletRequest} or a L{PortletRequest}.

        @return: wrapped request object
        """
        raise NotImplementedError


class IResponse(object):
    """Generic interface of a (HTTP or Portlet) response from the application.

    This is a wrapper interface that allows L{AbstractCommunicationManager} to
    use a unified API.

    @author: peholmst
    """

    def getOutputStream(self):
        """Gets the output stream to which the response can be written.

        @raise IOException:
        """
        raise NotImplementedError


    def setContentType(self, typ):
        """Sets the MIME content type for the response to be communicated
        to the browser.
        """
        raise NotImplementedError


    def getWrappedResponse(self):
        """Gets the wrapped response object, usually a class implementing
        either L{ServletResponse}.

        @return: wrapped request object
        """
        raise NotImplementedError


class ISession(object):
    """Generic wrapper interface for a (HTTP or Portlet) session.

    Several applications can be associated with a single session.

    @author: peholmst
    """

    def isNew(self):
        raise NotImplementedError


    def getAttribute(self, name):
        raise NotImplementedError


    def setAttribute(self, name, o):
        raise NotImplementedError


    def getMaxInactiveInterval(self):
        raise NotImplementedError


    def getWrappedSession(self):
        raise NotImplementedError


class ICallback(object):
    """@author: peholmst
    """

    def criticalNotification(self, request, response, cap, msg, details,
                outOfSyncURL):
        raise NotImplementedError


    def getRequestPathInfo(self, request):
        raise NotImplementedError


    def getThemeResourceAsStream(self, themeName, resource):
        raise NotImplementedError


class UploadInterruptedException(Exception):

    def __init__(self):
        msg = 'Upload interrupted by other thread'
        super(UploadInterruptedException, self).__init__(msg)


class ErrorHandlerErrorEvent(TerminalErrorEvent):

    def __init__(self, throwable):
        self._throwable = throwable


    def getThrowable(self):
        return self._throwable


class URIHandlerErrorImpl(URIHandlerErrorEvent):
    """Implementation of L{IErrorEvent} interface."""

    def __init__(self, owner, throwable):
        self._owner = owner
        self._throwable = throwable


    def getThrowable(self):
        """@see: L{IErrorEvent.getThrowable}"""
        return self._throwable


    def getURIHandler(self):
        """@see: L{IErrorEvent.getURIHandler}"""
        return self._owner


class InvalidUIDLSecurityKeyException(Exception):

    def __init__(self, message):
        super(InvalidUIDLSecurityKeyException, self).__init__(message)


class OpenWindowCache(object):
    """Helper class for terminal to keep track of data that client is
    expected to know.

    TODO: make customlayout templates (from theme) to be cached here.
    """

    def __init__(self):
        self._res = set()


    def cache(self, obj):
        """@return: true if the given class was added to cache
        """
        if obj in self._res:
            return False
        else:
            self._res.add(obj)
            return True


    def clear(self):
        self._res.clear()


class SimpleMultiPartInputStream(StringIO):  # FIXME InputStream
    """Stream that extracts content from another stream until the boundary
    string is encountered.

    Public only for unit tests, should be considered private for all other
    purposes.
    """

    def __init__(self, realInputStream, boundaryString, manager):
        super(SimpleMultiPartInputStream, self).__init__()

        # Counter of how many characters have been matched to boundary string
        # from the stream
        self._matchedCount = -1

        # Used as pointer when returning bytes after partly matched boundary
        # string.
        self._curBoundaryIndex = 0

        # The byte found after a "promising start for boundary"
        self._bufferedByte = -1

        self._atTheEnd = False

        self._boundary = manager.CRLF + manager.DASHDASH + boundaryString

        self._realInputStream = realInputStream


    def getvalue(self):
        if self._atTheEnd:

            # End boundary reached, nothing more to read
            return -1
        elif self._bufferedByte >= 0:

            # Purge partially matched boundary if there was such
            return self.getBuffered()
        elif self._matchedCount != -1:

            # Special case where last "failed" matching ended with first
            # character from boundary string
            return self.matchForBoundary()
        else:

            fromActualStream = self._realInputStream.read()
            if fromActualStream == -1:

                # unexpected end of stream
                raise IOError('The multipart stream ended unexpectedly')
            if self._boundary[0] == fromActualStream:

                # If matches the first character in boundary string, start
                # checking if the boundary is fetched.
                return self.matchForBoundary()

            return fromActualStream


    def matchForBoundary(self):
        """Reads the input to expect a boundary string. Expects that the first
        character has already been matched.

        @return: -1 if the boundary was matched, else returns the first byte
                from boundary
        @raise IOException:
        """
        self._matchedCount = 0

        # Going to "buffered mode". Read until full boundary match or a
        # different character.
        while True:
            self._matchedCount += 1
            if self._matchedCount == len(self._boundary):
                # The whole boundary matched so we have reached the end of
                # file
                self._atTheEnd = True
                return -1

            fromActualStream = self._realInputStream.read()

            if fromActualStream != self._boundary[self._matchedCount]:
                # Did not find full boundary, cache the mismatching byte
                # and start returning the partially matched boundary.
                self._bufferedByte = fromActualStream
                return self.getBuffered()


    def getBuffered(self):
        """Returns the partly matched boundary string and the byte following
        that.

        @raise IOException:
        """
        if self._matchedCount == 0:
            # The boundary has been returned, return the buffered byte.
            b = self._bufferedByte
            self._bufferedByte = -1
            self._matchedCount = -1
        else:
            b = self._boundary[self._curBoundaryIndex]
            self._curBoundaryIndex += 1
            if self._curBoundaryIndex == self._matchedCount:
                # The full boundary has been returned, remaining is the
                # char that did not match the boundary.
                self._curBoundaryIndex = 0
                if self._bufferedByte != self._boundary[0]:
                    # next call for getBuffered will return the
                    # bufferedByte that came after the partial boundary
                    # match
                    self._matchedCount = 0
                else:
                    # Special case where buffered byte again matches the
                    # boundaryString. This could be the start of the real
                    # end boundary.
                    self._matchedCount = 0
                    self._bufferedByte = -1

        if b == -1:
            raise IOError('The multipart stream ended unexpectedly')

        return b
