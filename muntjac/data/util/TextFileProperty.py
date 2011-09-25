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

from muntjac.data.util.AbstractProperty import AbstractProperty


class TextFileProperty(AbstractProperty):
    """Property implementation for wrapping a text file.

    Supports reading and writing of a File from/to String.

    {@link ValueChangeListener}s are supported, but only fire when
    setValue(Object) is explicitly called. {@link ReadOnlyStatusChangeListener}s
    are supported but only fire when setReadOnly(boolean) is explicitly called.
    """
    _file = None
    _charset = None

    def __init__(self, *args):
        """Wrap given file with property interface.

        Setting the file to null works, but getValue() will return null.

        @param file
                   File to be wrapped.
        ---
        Wrap the given file with the property interface and specify character
        set.

        Setting the file to null works, but getValue() will return null.

        @param file
                   File to be wrapped.
        @param charset
                   Charset to be used for reading and writing the file.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            fd, = _0
            self._file = fd
        elif _1 == 2:
            fd, charset = _0
            self._file = fd
            self._charset = charset
        else:
            raise ValueError


    def getType(self):
        return str


    def getValue(self):
        if self._file is None:
            return None
#        try:
#            fis = FileInputStream(self._file)
#            isr = InputStreamReader(fis) if self._charset is None else InputStreamReader(fis, self._charset)
#            r = StringIO(isr)
#            b = self.StringBuilder()
#            buf = [None] * 8 * 1024
#            while len = r.read(buf) != -1:
#                b.append(buf, 0, len)
#            r.close()
#            isr.close()
#            fis.close()
#            return str(b)
#        except FileNotFoundException, e:
#            return None
#        except IOException, e:
#            raise RuntimeError(e)


    def isReadOnly(self):
        return ((self._file is None) or super(TextFileProperty, self).isReadOnly()) or (not self._file.canWrite())


    def setValue(self, newValue):
        if self.isReadOnly():
            raise self.ReadOnlyException()
        if self._file is None:
            return
#        try:
#            fos = FileOutputStream(self._file)
#            osw = OutputStreamWriter(fos) if self._charset is None else OutputStreamWriter(fos, self._charset)
#            w = BufferedWriter(osw)
#            w.append(str(newValue))
#            w.flush()
#            w.close()
#            osw.close()
#            fos.close()
#            self.fireValueChange()
#        except IOException, e:
#            raise RuntimeError(e)
