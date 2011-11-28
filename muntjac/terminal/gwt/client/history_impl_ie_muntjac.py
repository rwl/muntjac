# Copyright (C) 2008 Google Inc.
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

from __pyjamas__ import JS

from pyjamas import DOM


class HistoryImplIEVaadin(HistoryImpl):
    """A slightly modified version of GWT's HistoryImplIE6 to bypass bug #2931.
    Also combined with HistoryImplFrame.

    This class should be removed if GWT issue 3890 gets resolved. (Also
    remember to removed deferred binding rule from .gwt.xml file).
    """

    def __init__(self):
        super(HistoryImplIEVaadin, self).__init__()
        self.historyFrame = None


    @classmethod
    def findHistoryFrame(cls):
        JS("""
            return $doc.getElementById('__gwt_historyFrame');
        """)
        pass


    @classmethod
    def getTokenElement(cls, historyFrame):
        JS("""
           // Initialize the history iframe.  If '__gwt_historyToken' already exists, then
           // we're probably backing into the app, so _don't_ set the iframe's location.
           if (@{{historyFrame}}.contentWindow) {
               var doc = @{{historyFrame}}.contentWindow.document;
               return doc.getElementById('__gwt_historyToken');
           }
        """)
        pass


    def nativeUpdate(self, historyToken):
        # Must update the location hash since it isn't already correct.
        self.updateHash(historyToken)
        self.navigateFrame(historyToken)


    def nativeUpdateOnEvent(self, historyToken):
        self.updateHash(historyToken)


    @classmethod
    def escapeHtml(cls, maybeHtml):
        """Sanitizes an untrusted string to be used in an HTML context.
        NOTE: This method of escaping strings should only be used on Internet
        Explorer.

        @param maybeHtml:
                   untrusted string that may contain html
        @return: sanitized string
        """
        div = DOM.createDiv()
        DOM.setInnerText(div, maybeHtml)
        return DOM.getInnerHTML(div)


    @classmethod
    def getLocationHash(cls):
        """For IE6, reading from $wnd.location.hash drops part of the fragment
        if the fragment contains a '?'. To avoid this bug, we use location.href
        instead.
        """
        JS("""
           var href = $wnd.location.href;
           var hashLoc = href.lastIndexOf("#");
           return (hashLoc > 0) ? href.substring(hashLoc) : "";
        """)
        pass


    def init(self):
        self.historyFrame = self.findHistoryFrame()
        if self.historyFrame is None:
            return False

        self.initHistoryToken()

        # Initialize the history iframe. If a token element already exists,
        # then
        # we're probably backing into the app, so _don't_ create a new item.
        tokenElement = self.getTokenElement(self.historyFrame)
        if tokenElement is not None:
            self.setToken(self.getTokenElementContent(tokenElement))
        else:
            self.navigateFrame(self.getToken())

        self.injectGlobalHandler()

        self.initUrlCheckTimer()
        return True


    def getTokenElementContent(self, tokenElement):
        JS("""
            return @{{tokenElement}}.innerText;
        """)
        pass

    def initHistoryToken(self):
        JS("""
          // Assume an empty token.
          var token = '';
          // Get the initial token from the url's hash component.
          var hash = @com.vaadin.terminal.gwt.client.HistoryImplIEVaadin::getLocationHash()();
          if (hash.length > 0) {
            try {
              token = @{{self}}.@com.google.gwt.user.client.impl.HistoryImpl::decodeFragment(Ljava/lang/String;)(hash.substring(1));
            } catch (e) {
              // Clear the bad hash (@{{self}} can't have been a valid token).
              $wnd.location.hash = '';
            }
          }
          @com.google.gwt.user.client.impl.HistoryImpl::setToken(Ljava/lang/String;)(token);
        """)
        pass


    def injectGlobalHandler(self):
        JS("""
          var historyImplRef = @{{self}};

          $wnd.__gwt_onHistoryLoad = function(token) {
            historyImplRef.@com.google.gwt.user.client.impl.HistoryImpl::newItemOnEvent(Ljava/lang/String;)(token);
          };
        """)
        pass


    def navigateFrame(self, token):
        JS("""
          var escaped = @com.vaadin.terminal.gwt.client.HistoryImplIEVaadin::escapeHtml(Ljava/lang/String;)(@{{token}});
          var doc = @{{self}}.@com.vaadin.terminal.gwt.client.HistoryImplIEVaadin::historyFrame.contentWindow.document;
          doc.open();
          doc.write('<html><body onload="if(parent.__gwt_onHistoryLoad)parent.__gwt_onHistoryLoad(__gwt_historyToken.innerText)"><div id="__gwt_historyToken">' + escaped + '</div></body></html>');
          doc.close();
        """)
        pass


    def updateHash(self, token):
        JS("""
           $wnd.location.hash = @{{self}}.@com.google.gwt.user.client.impl.HistoryImpl::encodeFragment(Ljava/lang/String;)(@{{token}});
         """)
        pass


    def initUrlCheckTimer(self):
        JS("""
          // This is the URL check timer.  It detects when an unexpected change
          // occurs in the document's URL (e.g. when the user enters one manually
          // or selects a 'favorite', but only the #hash part changes).  When @{{self}}
          // occurs, we _must_ reload the page.  This is because IE has a really
          // nasty bug that totally mangles its history stack and causes the location
          // bar in the UI to stop working under these circumstances.
          var historyImplRef = @{{self}};
          var urlChecker = function() {
            $wnd.setTimeout(urlChecker, 250);
            var hash = @com.vaadin.terminal.gwt.client.HistoryImplIEVaadin::getLocationHash()();
            if (hash.length > 0) {
              var token = '';
              try {
                token = historyImplRef.@com.google.gwt.user.client.impl.HistoryImpl::decodeFragment(Ljava/lang/String;)(hash.substring(1));
              } catch (e) {
                // If there's a bad hash, always reload. This could only happen if
                // if someone entered or linked to a bad url.
                $wnd.location.reload();
              }

              var historyToken = @com.google.gwt.user.client.impl.HistoryImpl::getToken()();
              if (token != historyToken) {
                $wnd.location.reload();
              }
            }
          };
          urlChecker();
        """)
        pass
