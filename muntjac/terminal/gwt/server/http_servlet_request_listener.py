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
