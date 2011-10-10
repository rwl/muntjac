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

import inspect
import logging

from muntjac.util import IEventListener
from muntjac.util import getSuperClass


logger = logging.getLogger(__name__)


class ListenerMethod(IEventListener):
    """One registered event listener. This class contains the listener object
    reference, listened event type, the trigger method to call when the event
    fires, and the optional argument list to pass to the method and the index of
    the argument to replace with the event object.

    This Class provides several constructors that allow omission of the optional
    arguments, and giving the listener method directly, or having the constructor
    to reflect it using merely the name of the method.

    It should be pointed out that the method
    {@link #receiveEvent(EventObject event)} is the one that filters out the
    events that do not match with the given event type and thus do not result in
    calling of the trigger method.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def writeObject(self, out):
        raise NotImplementedError

        # Special serialization to handle method references
        try:
            out.defaultWriteObject()
            name = self._method.__name__
            paramTypes = self._method.getParameterTypes()
            out.writeObject(name)
            out.writeObject(paramTypes)
        except Exception, e:  # FIXME: NotSerializableException
            logger.warning(('Error in serialization of the application: Class '
                    + self._target.__class__.__name__
                    + ' must implement serialization.'))
            raise e


    def readObject(self, in_):
        raise NotImplementedError

        # Special serialization to handle method references
        in_.defaultReadObject()
        try:
            name = in_.readObject()
            paramTypes = in_.readObject()
            # We can not use getMethod directly as we want to support anonymous
            # inner classes
            self._method = self.findHighestMethod(self._target.__class__,
                    name, paramTypes)
        except Exception:  # FIXME: SecurityException
            logger.critical('Internal deserialization error')


    @classmethod
    def findHighestMethod(cls, klass, method, paramTypes):
        ifaces = klass.getInterfaces()
        for i in range(len(ifaces)):
            ifaceMethod = cls.findHighestMethod(ifaces[i], method, paramTypes)
            if ifaceMethod is not None:
                return ifaceMethod

        if getSuperClass(klass) is not None:
            parentMethod = cls.findHighestMethod(getSuperClass(klass), method, paramTypes)
            if parentMethod is not None:
                return parentMethod

        methods = klass.getMethods()
        for i in range(len(methods)):
            # we ignore parameter types for now - you need to add this
            if methods[i].getName() == method:
                return methods[i]

        return None


    def __init__(self, eventType, target, method, arguments=None,
                 eventArgumentIndex=None):
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
        # Type of the event that should trigger this listener. Also the subclasses
        # of this class are accepted to trigger the listener.
        self._eventType = None

        # The object containing the trigger method.
        self._target = None

        # The trigger method to call when an event passing the given criteria
        # fires.
        self._method = None

        # Optional argument set to pass to the trigger method.
        self._arguments = None

        # Optional index to <code>arguments</code> that point out which one
        # should be replaced with the triggering event object and thus be
        # passed to the trigger method.
        self._eventArgumentIndex = None


        # Checks that the object is of correct type
        if arguments is None:
            if isinstance(method, basestring):
                methodName = method
                methods = target.__class__.getMethods()  # FIXME: getMethods
                for i in range(len(methods)):
                    if methods[i].getName() == methodName:
                        method = methods[i]

                if method is None:
                    raise ValueError

                self._eventType = eventType
                self._target = target
                self._method = method
                self._eventArgumentIndex = -1

                params = method.getParameterTypes()

                if len(params) == 0:
                    self._arguments = [None] * 0
                elif len(params) == 1 and issubclass(eventType, params[0]):
                    self._arguments = [None]
                    self._eventArgumentIndex = 0
                else:
                    raise ValueError
            else:
                if not issubclass(target.__class__, method.im_class):
                    raise ValueError

                self._eventType = eventType
                self._target = target

                self._method = method.im_func.func_name  # can't pickle unbound method

                self._eventArgumentIndex = -1

                params, _, _, _ = inspect.getargspec(method)
                if len(params) == 1:
                    self._arguments = []
                elif len(params) == 2:# and issubclass(eventType, params[1]):
                    self._arguments = [None]
                    self._eventArgumentIndex = 0
                else:
                    raise ValueError
        elif eventArgumentIndex is None:
            if isinstance(method, basestring):
                methodName = method
                methods = target.__class__.getMethods()  # FIXME: getMethods
                for i in range(len(methods)):
                    if methods[i].getName() == methodName:
                        method = methods[i]
                if method is None:
                    raise ValueError

                self._eventType = eventType
                self._target = target
                self._method = method
                self._arguments = arguments
                self._eventArgumentIndex = -1
            else:
                if not issubclass(target.__class__, method.im_class):
                    raise ValueError

                self._eventType = eventType
                self._target = target
                self._method = method
                self._arguments = arguments
                self._eventArgumentIndex = -1
        else:
            if isinstance(method, basestring):
                methodName = method
                methods = target.__class__.getMethods()  # FIXME: getMethods
                for i in range(len(methods)):
                    if methods[i].getName() == methodName:
                        method = methods[i]

                if method is None:
                    raise ValueError

                # Checks that the event argument is null
                if (eventArgumentIndex >= 0
                        and arguments[eventArgumentIndex] is not None):
                    raise ValueError

                # Checks the event type is supported by the method
                if (eventArgumentIndex >= 0
                        and not issubclass(eventType,
                            method.getParameterTypes()[eventArgumentIndex])):
                    raise ValueError

                self._eventType = eventType
                self._target = target
                self._method = method
                self._arguments = arguments
                self._eventArgumentIndex = eventArgumentIndex
            else:
                if not issubclass(target.__class__, method.im_class):
                    raise ValueError

                # Checks that the event argument is null
                if (eventArgumentIndex >= 0
                        and arguments[eventArgumentIndex] is not None):
                    raise ValueError

                # Checks the event type is supported by the method
                if (eventArgumentIndex >= 0
                        and not issubclass(eventType,
                            method.getParameterTypes()[eventArgumentIndex])):
                    raise ValueError

                self._eventType = eventType
                self._target = target
                self._method = method
                self._arguments = arguments
                self._eventArgumentIndex = eventArgumentIndex


    def receiveEvent(self, event):
        """Receives one event from the <code>EventRouter</code> and calls
        the trigger method if it matches with the criteria defined for the
        listener. Only the events of the same or subclass of the specified
        event class result in the trigger method to be called.

        @param event
                   the fired event. Unless the trigger method's argument list
                   and the index to the to be replaced argument is specified,
                   this event will not be passed to the trigger method.
        """
        # Only send events supported by the method
        if issubclass(event.__class__, self._eventType):
            try:
                m_name = self._method#.im_func.func_name
                m = getattr(self._target, m_name)

                if self._eventArgumentIndex >= 0:
                    if (self._eventArgumentIndex == 0
                            and len(self._arguments) == 1):
                        m(event)
                    else:
                        arg = [None] * len(self._arguments)
                        for i in range(len(arg)):
                            arg[i] = self._arguments[i]

                        arg[self._eventArgumentIndex] = event
                        m(*arg)
                else:
                    m()
#            except Exception:  # IllegalAccessException
#                raise RuntimeError, 'Internal error - please report'
            except AttributeError:  # FIXME: InvocationTargetException
                raise MethodException, ('Invocation of method '
                        + self._method + ' failed.')


    def matches(self, eventType, target, method=None):
        """Checks if the given object and event match with the ones stored in
        this listener.

        @param target
                   the object to be matched against the object stored by this
                   listener.
        @param eventType
                   the type to be tested for equality against the type stored
                   by this listener.
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
                   the type to be tested for equality against the type stored
                   by this listener.
        @param method
                   the method to be tested for equality against the method
                   stored by this listener.
        @return <code>true</code> if <code>target</code> is the same object as
                the one stored in this object, <code>eventType</code> equals
                with the event type stored in this object and
                <code>method</code> equals with the method stored in this
                object
        """
        if method is None:
            return self._target == target and eventType == self._eventType
        else:
            return (self._target == target and eventType == self._eventType
                    and method == self._method)


    def __hash__(self):
        hsh = 7
        hsh = (31 * hsh) + self._eventArgumentIndex
        hsh = (31 * hsh) + (0 if self._eventType is None else hash(self._eventType))
        hsh = (31 * hsh) + (0 if self._target is None else hash(self._target))
        hsh = (31 * hsh) + (0 if self._method is None else hash(self._method))
        return hsh


    def __eq__(self, obj):

        # return false if obj is a subclass (do not use instanceof check)
        if (obj is None) or (obj.__class__ != self.__class__):
            return False

        # obj is of same class, test it further
        t = obj

        return (self._eventArgumentIndex == t._eventArgumentIndex
                and (self._eventType == t._eventType
                        or (self._eventType != None
                                and self._eventType == t._eventType))
                and (self._target == t._target
                        or (self._target != None
                                and self._target == t._target))
                and (self._method == t._method
                        or (self._method != None
                                and self._method == t._method))
                and (self._arguments == t._arguments
                        or (self._arguments == t._arguments)))  # FIXME: Arrays.equals


    def isType(self, eventType):
        """Compares the type of this ListenerMethod to the given type

        @param eventType
                   The type to compare with
        @return true if this type of this ListenerMethod matches the given
                type, false otherwise
        """
        return self._eventType == eventType


    def isOrExtendsType(self, eventType):
        """Compares the type of this ListenerMethod to the given type

        @param eventType
                   The type to compare with
        @return true if this event type can be assigned to the given type,
                false otherwise
        """
        return issubclass(self._eventType, eventType)


    def getTarget(self):
        """Returns the target object which contains the trigger method.

        @return The target object
        """
        return self._target


class MethodException(RuntimeError):
    """Exception that wraps an exception thrown by an invoked method. When
    <code>ListenerMethod</code> invokes the target method, it may throw
    arbitrary exception. The original exception is wrapped into
    MethodException instance and rethrown by the <code>ListenerMethod</code>.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, message, cause):
        super(MethodException, self).__init__(message)
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


    def __str__(self):
        """@see java.lang.Throwable#toString()"""
        msg = str(super(MethodException, self))

        if self._cause is not None:
            msg += '\nCause: ' + str(self._cause)

        return msg
