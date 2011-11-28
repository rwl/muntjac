# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.


class VConsole(object):
    """A helper class to do some client side logging.

    This class replaces previously used login style:
    ApplicationConnection.getConsole().log("foo").

    The default widgetset provides three modes for debugging:

      * NullConsole (Default, displays no errors at all)
      * VDebugConsole ( Enabled by appending ?debug to url. Displays a floating
        console in the browser and also prints to browsers internal console
        (builtin or Firebug) and GWT's development mode console if available.)
      * VDebugConsole in quiet mode (Enabled by appending ?debug=quiet. Same as
        previous but without the console floating over application).

    Implementations can be customized with GWT deferred binding by overriding
    NullConsole.class or VDebugConsole.class. This way developer can for
    example build mechanism to send client side logging data to a server.

    Note that logging in client side is not fully optimized away even in
    production mode. Use logging moderately in production code to keep the size
    of client side engine small. An exception is {@link GWT#log(String)} style
    logging, which is available only in GWT development mode, but optimized
    away when compiled to web mode.
    """

    _impl = None

    @classmethod
    def setImplementation(cls, console):
        """Used by ApplicationConfiguration to initialize VConsole.
        """
        cls._impl = console


    @classmethod
    def getImplementation(cls):
        """Used by ApplicationConnection to support deprecated getConsole()
        api."""
        return cls._impl


    @classmethod
    def log(cls, e_or_msg):
        if isinstance(e_or_msg, BaseException):
            e = e_or_msg
            cls._impl.log(e)
        else:
            msg = e_or_msg
            cls._impl.log(msg)


    @classmethod
    def error(cls, e_or_msg):
        if isinstance(e_or_msg, BaseException):
            e = e_or_msg
            cls._impl.error(e)
        else:
            msg = e_or_msg
            cls._impl.error(msg)


    @classmethod
    def printObject(cls, msg):
        cls._impl.printObject(msg)


    @classmethod
    def dirUIDL(cls, u, cnf):
        cls._impl.dirUIDL(u, cnf)


    @classmethod
    def printLayoutProblems(cls, meta, applicationConnection,
            zeroHeightComponents, zeroWidthComponents):
        cls._impl.printLayoutProblems(meta, applicationConnection,
                zeroHeightComponents, zeroWidthComponents)
