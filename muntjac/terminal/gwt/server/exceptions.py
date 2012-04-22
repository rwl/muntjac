# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


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
