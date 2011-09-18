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

from __pyjamas__ import (ARGERROR,)
# from java.io.IOException import (IOException,)
# from java.io.NotSerializableException import (NotSerializableException,)
# from java.io.Serializable import (Serializable,)
# from java.lang.reflect.Method import (Method,)
# from java.util.Arrays import (Arrays,)
# from java.util.EventListener import (EventListener,)
# from java.util.EventObject import (EventObject,)
# from java.util.logging.Level import (Level,)
# from java.util.logging.Logger import (Logger,)


class ListenerMethod(EventListener, Serializable):
    """<p>
    One registered event listener. This class contains the listener object
    reference, listened event type, the trigger method to call when the event
    fires, and the optional argument list to pass to the method and the index of
    the argument to replace with the event object.
    </p>

    <p>
    This Class provides several constructors that allow omission of the optional
    arguments, and giving the listener method directly, or having the constructor
    to reflect it using merely the name of the method.
    </p>

    <p>
    It should be pointed out that the method
    {@link #receiveEvent(EventObject event)} is the one that filters out the
    events that do not match with the given event type and thus do not result in
    calling of the trigger method.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Special serialization to handle method references
    _logger = Logger.getLogger(ListenerMethod.getName())
    # Type of the event that should trigger this listener. Also the subclasses
    # of this class are accepted to trigger the listener.

    _eventType = None
    # The object containing the trigger method.
    _target = None
    # The trigger method to call when an event passing the given criteria
    # fires.

    _method = None
    # Optional argument set to pass to the trigger method.
    _arguments = None
    # Optional index to <code>arguments</code> that point out which one should
    # be replaced with the triggering event object and thus be passed to the
    # trigger method.

    _eventArgumentIndex = None
    # Special serialization to handle method references

    def writeObject(self, out):
        try:
            out.defaultWriteObject()
            name = self._method.getName()
            paramTypes = self._method.getParameterTypes()
            out.writeObject(name)
            out.writeObject(paramTypes)
        except NotSerializableException, e:
            self._logger.warning('Error in serialization of the application: Class ' + self._target.getClass().getName() + ' must implement serialization.')
            raise e

    def readObject(self, in_):
        in_.defaultReadObject()
        try:
            name = in_.readObject()
            paramTypes = in_.readObject()
            # We can not use getMethod directly as we want to support anonymous
            # inner classes
            self._method = self.findHighestMethod(self._target.getClass(), name, paramTypes)
        except SecurityException, e:
            self._logger.log(Level.SEVERE, 'Internal deserialization error', e)

    @classmethod
    def findHighestMethod(cls, cls, method, paramTypes):
        ifaces = cls.getInterfaces()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(ifaces)):
                break
            ifaceMethod = cls.findHighestMethod(ifaces[i], method, paramTypes)
            if ifaceMethod is not None:
                return ifaceMethod
        if cls.getSuperclass() is not None:
            parentMethod = cls.findHighestMethod(cls.getSuperclass(), method, paramTypes)
            if parentMethod is not None:
                return parentMethod
        methods = cls.getMethods()
        _1 = True
        i = 0
        while True:
            if _1 is True:
                _1 = False
            else:
                i += 1
            if not (i < len(methods)):
                break
            # we ignore parameter types for now - you need to add this
            if methods[i].getName() == method:
                return methods[i]
        return None

    def __init__(self, *args):
        """<p>
        Constructs a new event listener from a trigger method, it's arguments and
        the argument index specifying which one is replaced with the event object
        when the trigger method is called.
        </p>

        <p>
        This constructor gets the trigger method as a parameter so it does not
        need to reflect to find it out.
        </p>

        @param eventType
                   the event type that is listener listens to. All events of this
                   kind (or its subclasses) result in calling the trigger method.
        @param target
                   the object instance that contains the trigger method
        @param method
                   the trigger method
        @param arguments
                   the arguments to be passed to the trigger method
        @param eventArgumentIndex
                   An index to the argument list. This index points out the
                   argument that is replaced with the event object before the
                   argument set is passed to the trigger method. If the
                   eventArgumentIndex is negative, the triggering event object
                   will not be passed to the trigger method, though it is still
                   called.
        @throws java.lang.IllegalArgumentException
                    if <code>method</code> is not a member of <code>target</code>
                    .
        ---
        <p>
        Constructs a new event listener from a trigger method name, it's
        arguments and the argument index specifying which one is replaced with
        the event object. The actual trigger method is reflected from
        <code>object</code>, and <code>java.lang.IllegalArgumentException</code>
        is thrown unless exactly one match is found.
        </p>

        @param eventType
                   the event type that is listener listens to. All events of this
                   kind (or its subclasses) result in calling the trigger method.
        @param target
                   the object instance that contains the trigger method.
        @param methodName
                   the name of the trigger method. If the object does not contain
                   the method or it contains more than one matching methods
                   <code>java.lang.IllegalArgumentException</code> is thrown.
        @param arguments
                   the arguments to be passed to the trigger method.
        @param eventArgumentIndex
                   An index to the argument list. This index points out the
                   argument that is replaced with the event object before the
                   argument set is passed to the trigger method. If the
                   eventArgumentIndex is negative, the triggering event object
                   will not be passed to the trigger method, though it is still
                   called.
        @throws java.lang.IllegalArgumentException
                    unless exactly one match <code>methodName</code> is found in
                    <code>target</code>.
        ---
        <p>
        Constructs a new event listener from the trigger method and it's
        arguments. Since the the index to the replaced parameter is not specified
        the event triggering this listener will not be passed to the trigger
        method.
        </p>

        <p>
        This constructor gets the trigger method as a parameter so it does not
        need to reflect to find it out.
        </p>

        @param eventType
                   the event type that is listener listens to. All events of this
                   kind (or its subclasses) result in calling the trigger method.
        @param target
                   the object instance that contains the trigger method.
        @param method
                   the trigger method.
        @param arguments
                   the arguments to be passed to the trigger method.
        @throws java.lang.IllegalArgumentException
                    if <code>method</code> is not a member of <code>target</code>
                    .
        ---
        <p>
        Constructs a new event listener from a trigger method name and it's
        arguments. Since the the index to the replaced parameter is not specified
        the event triggering this listener will not be passed to the trigger
        method.
        </p>

        <p>
        The actual trigger method is reflected from <code>target</code>, and
        <code>java.lang.IllegalArgumentException</code> is thrown unless exactly
        one match is found.
        </p>

        @param eventType
                   the event type that is listener listens to. All events of this
                   kind (or its subclasses) result in calling the trigger method.
        @param target
                   the object instance that contains the trigger method.
        @param methodName
                   the name of the trigger method. If the object does not contain
                   the method or it contains more than one matching methods
                   <code>java.lang.IllegalArgumentException</code> is thrown.
        @param arguments
                   the arguments to be passed to the trigger method.
        @throws java.lang.IllegalArgumentException
                    unless exactly one match <code>methodName</code> is found in
                    <code>object</code>.
        ---
        <p>
        Constructs a new event listener from a trigger method. Since the argument
        list is unspecified no parameters are passed to the trigger method when
        the listener is triggered.
        </p>

        <p>
        This constructor gets the trigger method as a parameter so it does not
        need to reflect to find it out.
        </p>

        @param eventType
                   the event type that is listener listens to. All events of this
                   kind (or its subclasses) result in calling the trigger method.
        @param target
                   the object instance that contains the trigger method.
        @param method
                   the trigger method.
        @throws java.lang.IllegalArgumentException
                    if <code>method</code> is not a member of <code>object</code>
                    .
        ---
        <p>
        Constructs a new event listener from a trigger method name. Since the
        argument list is unspecified no parameters are passed to the trigger
        method when the listener is triggered.
        </p>

        <p>
        The actual trigger method is reflected from <code>object</code>, and
        <code>java.lang.IllegalArgumentException</code> is thrown unless exactly
        one match is found.
        </p>

        @param eventType
                   the event type that is listener listens to. All events of this
                   kind (or its subclasses) result in calling the trigger method.
        @param target
                   the object instance that contains the trigger method.
        @param methodName
                   the name of the trigger method. If the object does not contain
                   the method or it contains more than one matching methods
                   <code>java.lang.IllegalArgumentException</code> is thrown.
        @throws java.lang.IllegalArgumentException
                    unless exactly one match <code>methodName</code> is found in
                    <code>target</code>.
        """
        # Checks that the object is of correct type
        _0 = args
        _1 = len(args)
        if _1 == 3:
            if isinstance(_0[2], Method):
                eventType, target, method = _0
                if not method.getDeclaringClass().isAssignableFrom(target.getClass()):
                    raise java.lang.IllegalArgumentException()
                self._eventType = eventType
                self._target = target
                self._method = method
                self._eventArgumentIndex = -1
                params = method.getParameterTypes()
                if len(params) == 0:
                    self._arguments = [None] * 0
                elif len(params) == 1 and params[0].isAssignableFrom(eventType):
                    self._arguments = [None]
                    self._eventArgumentIndex = 0
                else:
                    raise self.IllegalArgumentException()
            else:
                eventType, target, methodName = _0
                methods = target.getClass().getMethods()
                method = None
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(methods)):
                        break
                    if methods[i].getName() == methodName:
                        method = methods[i]
                if method is None:
                    raise self.IllegalArgumentException()
                self._eventType = eventType
                self._target = target
                self._method = method
                self._eventArgumentIndex = -1
                params = method.getParameterTypes()
                if len(params) == 0:
                    self._arguments = [None] * 0
                elif len(params) == 1 and params[0].isAssignableFrom(eventType):
                    self._arguments = [None]
                    self._eventArgumentIndex = 0
                else:
                    raise self.IllegalArgumentException()
        elif _1 == 4:
            if isinstance(_0[2], Method):
                eventType, target, method, arguments = _0
                if not method.getDeclaringClass().isAssignableFrom(target.getClass()):
                    raise java.lang.IllegalArgumentException()
                self._eventType = eventType
                self._target = target
                self._method = method
                self._arguments = arguments
                self._eventArgumentIndex = -1
            else:
                eventType, target, methodName, arguments = _0
                methods = target.getClass().getMethods()
                method = None
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(methods)):
                        break
                    if methods[i].getName() == methodName:
                        method = methods[i]
                if method is None:
                    raise self.IllegalArgumentException()
                self._eventType = eventType
                self._target = target
                self._method = method
                self._arguments = arguments
                self._eventArgumentIndex = -1
        elif _1 == 5:
            if isinstance(_0[2], Method):
                eventType, target, method, arguments, eventArgumentIndex = _0
                if not method.getDeclaringClass().isAssignableFrom(target.getClass()):
                    raise java.lang.IllegalArgumentException()
                # Checks that the event argument is null
                if eventArgumentIndex >= 0 and arguments[eventArgumentIndex] is not None:
                    raise java.lang.IllegalArgumentException()
                # Checks the event type is supported by the method
                if (
                    eventArgumentIndex >= 0 and not method.getParameterTypes()[eventArgumentIndex].isAssignableFrom(eventType)
                ):
                    raise java.lang.IllegalArgumentException()
                self._eventType = eventType
                self._target = target
                self._method = method
                self._arguments = arguments
                self._eventArgumentIndex = eventArgumentIndex
            else:
                eventType, target, methodName, arguments, eventArgumentIndex = _0
                methods = target.getClass().getMethods()
                method = None
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(methods)):
                        break
                    if methods[i].getName() == methodName:
                        method = methods[i]
                if method is None:
                    raise self.IllegalArgumentException()
                # Checks that the event argument is null
                if eventArgumentIndex >= 0 and arguments[eventArgumentIndex] is not None:
                    raise java.lang.IllegalArgumentException()
                # Checks the event type is supported by the method
                if (
                    eventArgumentIndex >= 0 and not method.getParameterTypes()[eventArgumentIndex].isAssignableFrom(eventType)
                ):
                    raise java.lang.IllegalArgumentException()
                self._eventType = eventType
                self._target = target
                self._method = method
                self._arguments = arguments
                self._eventArgumentIndex = eventArgumentIndex
        else:
            raise ARGERROR(3, 5)

    # Finds the correct method
    # Check that the object is of correct type
    # Find the correct method
    # Checks that the object is of correct type
    # Finds the correct method

    def receiveEvent(self, event):
        """Receives one event from the <code>EventRouter</code> and calls the
        trigger method if it matches with the criteria defined for the listener.
        Only the events of the same or subclass of the specified event class
        result in the trigger method to be called.

        @param event
                   the fired event. Unless the trigger method's argument list and
                   the index to the to be replaced argument is specified, this
                   event will not be passed to the trigger method.
        """
        # Only send events supported by the method
        if self._eventType.isAssignableFrom(event.getClass()):
            # This should never happen
            # An exception was thrown by the invocation target. Throw it
            # forwards.
            try:
                if self._eventArgumentIndex >= 0:
                    if self._eventArgumentIndex == 0 and len(self._arguments) == 1:
                        self._method.invoke(self._target, [event])
                    else:
                        arg = [None] * len(self._arguments)
                        _0 = True
                        i = 0
                        while True:
                            if _0 is True:
                                _0 = False
                            else:
                                i += 1
                            if not (i < len(arg)):
                                break
                            arg[i] = self._arguments[i]
                        arg[self._eventArgumentIndex] = event
                        self._method.invoke(self._target, arg)
                else:
                    self._method.invoke(self._target, self._arguments)
            except java.lang.IllegalAccessException, e:
                raise java.lang.RuntimeException('Internal error - please report', e)
            except java.lang.reflect.InvocationTargetException, e:
                raise self.MethodException('Invocation of method ' + self._method + ' failed.', e.getTargetException())

    def matches(self, *args):
        """Checks if the given object and event match with the ones stored in this
        listener.

        @param target
                   the object to be matched against the object stored by this
                   listener.
        @param eventType
                   the type to be tested for equality against the type stored by
                   this listener.
        @return <code>true</code> if <code>target</code> is the same object as
                the one stored in this object and <code>eventType</code> equals
                the event type stored in this object. *
        ---
        Checks if the given object, event and method match with the ones stored
        in this listener.

        @param target
                   the object to be matched against the object stored by this
                   listener.
        @param eventType
                   the type to be tested for equality against the type stored by
                   this listener.
        @param method
                   the method to be tested for equality against the method stored
                   by this listener.
        @return <code>true</code> if <code>target</code> is the same object as
                the one stored in this object, <code>eventType</code> equals with
                the event type stored in this object and <code>method</code>
                equals with the method stored in this object
        """
        _0 = args
        _1 = len(args)
        if _1 == 2:
            eventType, target = _0
            return self._target == target and eventType == self._eventType
        elif _1 == 3:
            eventType, target, method = _0
            return self._target == target and eventType == self._eventType and method == self._method
        else:
            raise ARGERROR(2, 3)

    def hashCode(self):
        hash = 7
        hash = (31 * hash) + self._eventArgumentIndex
        hash = (31 * hash) + (0 if self._eventType is None else self._eventType.hashCode())
        hash = (31 * hash) + (0 if self._target is None else self._target.hashCode())
        hash = (31 * hash) + (0 if self._method is None else self._method.hashCode())
        return hash

#    @Override
#    public boolean equals(Object obj) {
#
#        if (this == obj) {
#            return true;
#        }
#
#        // return false if obj is a subclass (do not use instanceof check)
#        if ((obj == null) || (obj.getClass() != getClass())) {
#            return false;
#        }
#
#        // obj is of same class, test it further
#        ListenerMethod t = (ListenerMethod) obj;
#
#        return eventArgumentIndex == t.eventArgumentIndex
#                && (eventType == t.eventType || (eventType != null && eventType
#                        .equals(t.eventType)))
#                && (target == t.target || (target != null && target
#                        .equals(t.target)))
#                && (method == t.method || (method != null && method
#                        .equals(t.method)))
#                && (arguments == t.arguments || (Arrays.equals(arguments,
#                        t.arguments)));
#    }

    class MethodException(RuntimeError, Serializable):
        """Exception that wraps an exception thrown by an invoked method. When
        <code>ListenerMethod</code> invokes the target method, it may throw
        arbitrary exception. The original exception is wrapped into
        MethodException instance and rethrown by the <code>ListenerMethod</code>.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        _cause = None
        _message = None

        def __init__(self, message, cause):
            super(MethodException, self)(message)
            self._cause = cause

        def getCause(self):
            """Retrieves the cause of this throwable or <code>null</code> if the
            cause does not exist or not known.

            @return the cause of this throwable or <code>null</code> if the cause
                    is nonexistent or unknown.
            @see java.lang.Throwable#getCause()
            """
            return self._cause

        def getMessage(self):
            """Returns the error message string of this throwable object.

            @return the error message.
            @see java.lang.Throwable#getMessage()
            """
            return self._message

        def toString(self):
            """@see java.lang.Throwable#toString()"""
            msg = str(super(MethodException, self))
            if self._cause is not None:
                msg += '\nCause: ' + str(self._cause)
            return msg

    def isType(self, eventType):
        """Compares the type of this ListenerMethod to the given type

        @param eventType
                   The type to compare with
        @return true if this type of this ListenerMethod matches the given type,
                false otherwise
        """
        return self._eventType == eventType

    def isOrExtendsType(self, eventType):
        """Compares the type of this ListenerMethod to the given type

        @param eventType
                   The type to compare with
        @return true if this event type can be assigned to the given type, false
                otherwise
        """
        return eventType.isAssignableFrom(self._eventType)

    def getTarget(self):
        """Returns the target object which contains the trigger method.

        @return The target object
        """
        return self._target
