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

"""Defines a component for embedding external objects."""

from muntjac.ui.abstract_component import AbstractComponent
from muntjac.event.mouse_events import IClickListener, ClickEvent
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails

from muntjac.terminal.gwt.client.ui.v_embedded import VEmbedded


class Embedded(AbstractComponent):
    """Component for embedding external objects.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    CLIENT_WIDGET = None #ClientWidget(VEmbedded, LoadStyle.EAGER)

    _CLICK_EVENT = VEmbedded.CLICK_EVENT_IDENTIFIER

    #: General object type.
    TYPE_OBJECT = 0

    #: Image types.
    TYPE_IMAGE = 1

    #: Browser ("iframe") type.
    TYPE_BROWSER = 2

    def __init__(self, caption=None, source=None):
        """Creates a new Embedded object whose contents is loaded from
        given resource. The dimensions are assumed if possible. The
        type is guessed from resource.

        @param caption:
        @param source:
                   the Source of the embedded object.
        """
        super(Embedded, self).__init__()

        #: Type of the object.
        self._type = self.TYPE_OBJECT

        #: Source of the embedded object.
        self._source = None

        #: Generic object attributes.
        self._mimeType = None
        self._standby = None

        #: Hash of object parameters.
        self._parameters = dict()

        #: Applet or other client side runnable properties.
        self._codebase = None
        self._codetype = None
        self._classId = None
        self._archive = None

        if caption is not None:
            self.setCaption(caption)

        if source is not None:
            self.setSource(source)


    def paintContent(self, target):
        """Invoked when the component state should be painted."""

        if self._type == self.TYPE_IMAGE:
            target.addAttribute('type', 'image')
        elif self._type == self.TYPE_BROWSER:
            target.addAttribute('type', 'browser')


        if self.getSource() is not None:
            target.addAttribute('src', self.getSource())

        if self._mimeType is not None and not ('' == self._mimeType):
            target.addAttribute('mimetype', self._mimeType)

        if self._classId is not None and not ('' == self._classId):
            target.addAttribute('classid', self._classId)

        if self._codebase is not None and not ('' == self._codebase):
            target.addAttribute('codebase', self._codebase)

        if self._codetype is not None and not ('' == self._codetype):
            target.addAttribute('codetype', self._codetype)

        if self._standby is not None and not ('' == self._standby):
            target.addAttribute('standby', self._standby)

        if self._archive is not None and not ('' == self._archive):
            target.addAttribute('archive', self._archive)

        # Params
        for key in self.getParameterNames():
            target.startTag('embeddedparam')
            target.addAttribute('name', key)
            target.addAttribute('value', self.getParameter(key))
            target.endTag('embeddedparam')


    def setParameter(self, name, value):
        """Sets an object parameter. Parameters are optional information,
        and they are passed to the instantiated object. Parameters are are
        stored as name value pairs. This overrides the previous value
        assigned to this parameter.

        @param name: the name of the parameter.
        @param value: the value of the parameter.
        """
        self._parameters[name] = value
        self.requestRepaint()


    def getParameter(self, name):
        """Gets the value of an object parameter. Parameters are optional
        information, and they are passed to the instantiated object.
        Parameters are are stored as name value pairs.

        @return: the Value of parameter or null if not found.
        """
        return self._parameters.get(name)


    def removeParameter(self, name):
        """Removes an object parameter from the list.

        @param name:
                   the name of the parameter to remove.
        """
        if name in self._parameters:
            del self._parameters[name]
        self.requestRepaint()


    def getParameterNames(self):
        """Gets the embedded object parameter names.

        @return: the Iterator of parameters names.
        """
        return self._parameters.keys()


    def getCodebase(self):
        """This attribute specifies the base path used to resolve relative
        URIs specified by the classid, data, and archive attributes. When
        absent, its default value is the base URI of the current document.

        @return: the code base.
        """
        return self._codebase


    def getCodetype(self):
        """Gets the MIME-Type of the code.

        @return: the MIME-Type of the code.
        """
        return self._codetype


    def getMimeType(self):
        """Gets the MIME-Type of the object.

        @return: the MIME-Type of the object.
        """
        return self._mimeType


    def getStandby(self):
        """This attribute specifies a message that a user agent may render
        while loading the object's implementation and data.

        @return: The text displayed when loading
        """
        return self._standby


    def setCodebase(self, codebase):
        """This attribute specifies the base path used to resolve relative
        URIs specified by the classid, data, and archive attributes. When
        absent, its default value is the base URI of the current document.

        @param codebase:
                   The base path
        """
        if (codebase != self._codebase
                or (codebase is not None and codebase != self._codebase)):
            self._codebase = codebase
            self.requestRepaint()


    def setCodetype(self, codetype):
        """This attribute specifies the content type of data expected when
        downloading the object specified by classid. This attribute is
        optional but recommended when classid is specified since it allows
        the user agent to avoid loading information for unsupported content
        types. When absent, it defaults to the value of the type attribute.

        @param codetype:
                   the codetype to set.
        """
        if (codetype != self._codetype
                or (codetype is not None and codetype != self._codetype)):
            self._codetype = codetype
            self.requestRepaint()


    def setMimeType(self, mimeType):
        """Sets the mimeType, the MIME-Type of the object.

        @param mimeType: the mimeType to set.
        """
        if (mimeType != self._mimeType
                or (mimeType is not None and mimeType != self._mimeType)):
            self._mimeType = mimeType
            if 'application/x-shockwave-flash' == mimeType:
                # Automatically add wmode transparent as we use lots of
                # floating layers in Muntjac. If developers need better flash
                # performance, they can override this value programmatically
                # back to "window" (the defautl).
                if self.getParameter('wmode') is None:
                    self.setParameter('wmode', 'transparent')

            self.requestRepaint()


    def setStandby(self, standby):
        """This attribute specifies a message that a user agent may render
        while loading the object's implementation and data.

        @param standby: The text to display while loading
        """
        if (standby != self._standby
                or (standby is not None and standby != self._standby)):
            self._standby = standby
            self.requestRepaint()


    def getClassId(self):
        """This attribute may be used to specify the location of an object's
        implementation via a URI.

        @return: the classid.
        """
        return self._classId


    def setClassId(self, classId):
        """This attribute may be used to specify the location of an object's
        implementation via a URI.

        @param classId:
                   the classId to set.
        """
        if (classId != self._classId
                or (classId is not None and classId != self._classId)):
            self._classId = classId
            self.requestRepaint()


    def getSource(self):
        """Gets the resource contained in the embedded object.

        @return: the Resource
        """
        return self._source


    def getType(self):
        """Gets the type of the embedded object.

        This can be one of the following:

          - TYPE_OBJECT I{(This is the default)}
          - TYPE_IMAGE

        @return: the type.
        """
        return self._type


    def setSource(self, source):
        """Sets the object source resource. The dimensions are assumed
        if possible. The type is guessed from resource.

        @param source: the source to set.
        """
        if source is not None and source != self._source:
            self._source = source
            mt = source.getMIMEType()

            if self._mimeType is None:
                self._mimeType = mt

            if mt == 'image/svg+xml':
                self._type = self.TYPE_OBJECT
            elif mt[:mt.find('/')].lower() == 'image':
                self._type = self.TYPE_IMAGE
            else:
                pass  # Keep previous type

            self.requestRepaint()


    def setType(self, typ):
        """Sets the object type.

        This can be one of the following:

          - TYPE_OBJECT I{(This is the default)}
          - TYPE_IMAGE
          - TYPE_BROWSER

        @param typ: the type to set.
        """
        if (typ != self.TYPE_OBJECT and typ != self.TYPE_IMAGE
                and typ != self.TYPE_BROWSER):
            raise ValueError, 'Unsupported typ'

        if typ != self._type:
            self._type = typ
            self.requestRepaint()


    def getArchive(self):
        """This attribute may be used to specify a space-separated list of
        URIs for archives containing resources relevant to the object, which
        may include the resources specified by the classid and data
        attributes. Preloading archives will generally result in reduced load
        times for objects. Archives specified as relative URIs should be
        interpreted relative to the codebase attribute.

        @return: Space-separated list of URIs with resources relevant to the
                 object
        """
        return self._archive


    def setArchive(self, archive):
        """This attribute may be used to specify a space-separated list of
        URIs for archives containing resources relevant to the object, which
        may include the resources specified by the classid and data
        attributes. Preloading archives will generally result in reduced load
        times for objects. Archives specified as relative URIs should be
        interpreted relative to the codebase attribute.

        @param archive:
                   Space-separated list of URIs with resources relevant to
                   the object
        """
        if (archive != self._archive
                or (archive is not None and archive != self._archive)):
            self._archive = archive
            self.requestRepaint()


    def addListener(self, listener, iface=None):
        """Add a click listener to the component. The listener is called
        whenever the user clicks inside the component. Depending on the
        content the event may be blocked and in that case no event is fired.

        Use L{removeListener} to remove the listener.

        @param listener:
                   The listener to add
        """
        if (isinstance(listener, IClickListener) and
                (iface is None or issubclass(iface, IClickListener))):
            self.registerListener(self._CLICK_EVENT, ClickEvent,
                    listener, IClickListener.clickMethod)

        super(Embedded, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ClickEvent):
            self.registerCallback(ClickEvent, callback,
                    self._CLICK_EVENT, *args)
        else:
            super(Embedded, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        """Remove a click listener from the component. The listener should
        earlier have been added using L{addListener}.

        @param listener:
                   The listener to remove
        """
        if (isinstance(listener, IClickListener) and
                (iface is None or issubclass(iface, IClickListener))):
            self.withdrawListener(self._CLICK_EVENT, ClickEvent, listener)

        super(Embedded, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ClickEvent):
            self.withdrawCallback(ClickEvent, callback, self._CLICK_EVENT)
        else:
            super(Embedded, self).removeCallback(callback, eventType)


    def changeVariables(self, source, variables):
        super(Embedded, self).changeVariables(source, variables)

        if self._CLICK_EVENT in variables:
            self.fireClick(variables.get(self._CLICK_EVENT))


    def fireClick(self, parameters):
        """Notifies click-listeners that a mouse click event has occurred.
        """
        mouseDetails = \
                MouseEventDetails.deSerialize(parameters['mouseDetails'])
        self.fireEvent( ClickEvent(self, mouseDetails) )
