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


class SystemMessageException(RuntimeError):

    def __init__(self, *args):
        """Constructs a new C{SystemMessageException} with
        the specified detail message and/or cause.
        """
        nargs = len(args)
        if nargs == 1:
            if isinstance(args[0], Exception):
                super(SystemMessageException, self).__init__()
                self._cause = args[0]
            else:
                msg = args[0]
                super(SystemMessageException, self).__init__(msg)
        elif nargs == 2:
            msg, cause = args
            super(SystemMessageException, self).__init__(msg)
            self._cause = cause
        else:
            raise ValueError, 'too many arguments'


    def getCause(self):
        return self._cause


class UploadException(Exception):

    def __init__(self, arg):
        if isinstance(arg, Exception):
            e = arg
            super(UploadException, self).__init__('Upload failed', e)
        else:
            msg = arg
            super(UploadException, self).__init__(msg)


class NoInputStreamException(Exception):
    pass


class NoOutputStreamException(Exception):
    pass


class ServletException(Exception):
    pass


class SessionExpiredException(Exception):
    pass
