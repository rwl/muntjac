# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Request start and end listener"""


class IHttpServletRequestListener(object):
    """L{Application} that implements this interface gets notified
    of request start and end by terminal.

    Interface can be used for several helper tasks including:

      - Opening and closing database connections
      - Implementing L{ThreadLocal}
      - Setting/Getting L{Cookie}

    Alternatives for implementing similar features are are Servlet
    L{Filter}s and L{TransactionListener}s in Muntjac.
    """

    def onRequestStart(self, request, response):
        """This method is called before L{Terminal} applies the
        request to Application.
        """
        raise NotImplementedError


    def onRequestEnd(self, request, response):
        """This method is called at the end of each request.
        """
        raise NotImplementedError
