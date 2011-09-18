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



class CSSRule(object):
    """Utility class for fetching CSS properties from DOM StyleSheets JS object."""
    _selector = None
    _rules = None

    def __init__(self, selector, deep):
        """@param selector
                   the CSS selector to search for in the stylesheets
        @param deep
                   should the search follow any @import statements?
        """
        # TODO how to find the right LINK-element? We should probably give the
        # stylesheet a name.
        self._selector = selector
        self.fetchRule(selector, deep)

    def fetchRule(self, selector, deep):
        # -{
        #     var sheets = $doc.styleSheets;
        #     for(var i = 0; i < sheets.length; i++) {
        #     var sheet = sheets[i];
        #     if(sheet.href && sheet.href.indexOf("VAADIN/themes")>-1) {
        #     this.@com.vaadin.terminal.gwt.client.CSSRule::rules = @com.vaadin.terminal.gwt.client.CSSRule::searchForRule(Lcom/google/gwt/core/client/JavaScriptObject;Ljava/lang/String;Z)(sheet, selector, deep);
        #     return;
        #     }
        #     }
        #     this.@com.vaadin.terminal.gwt.client.CSSRule::rules = [];
        #     }-

        # Loops through all current style rules and collects all matching to
        # 'rules' array. The array is reverse ordered (last one found is first).

        pass

    @classmethod
    def searchForRule(cls, sheet, selector, deep):
        # -{
        #     if(!$doc.styleSheets)
        #     return null;
        # 
        #     selector = selector.toLowerCase();
        # 
        #     var allMatches = [];
        # 
        #     // IE handles imported sheet differently
        #     if(deep && sheet.imports && sheet.imports.length > 0) {
        #     for(var i=0; i < sheet.imports.length; i++) {
        #     var imports = @com.vaadin.terminal.gwt.client.CSSRule::searchForRule(Lcom/google/gwt/core/client/JavaScriptObject;Ljava/lang/String;Z)(sheet.imports[i], selector, deep);
        #     allMatches.concat(imports);
        #     }
        #     }
        # 
        #     var theRules = new Array();
        #     if (sheet.cssRules)
        #     theRules = sheet.cssRules
        #     else if (sheet.rules)
        #     theRules = sheet.rules
        # 
        #     var j = theRules.length;
        #     for(var i=0; i<j; i++) {
        #     var r = theRules[i];
        #     if(r.type == 1 || sheet.imports) {
        #     var selectors = r.selectorText.toLowerCase().split(",");
        #     var n = selectors.length;
        #     for(var m=0; m<n; m++) {
        #     if(selectors[m].replace(/^\s+|\s+$/g, "") == selector) {
        #     allMatches.unshift(r);
        #     break; // No need to loop other selectors for this rule
        #     }
        #     }
        #     } else if(deep && r.type == 3) {
        #     // Search @import stylesheet
        #     var imports = @com.vaadin.terminal.gwt.client.CSSRule::searchForRule(Lcom/google/gwt/core/client/JavaScriptObject;Ljava/lang/String;Z)(r.styleSheet, selector, deep);
        #     allMatches = allMatches.concat(imports);
        #     }
        #     }
        # 
        #     return allMatches;
        #     }-

        pass

    def getPropertyValue(self, propertyName):
        """Returns a specific property value from this CSS rule.

        @param propertyName
                   camelCase CSS property name
        @return the value of the property as a String
        """
        # -{
        #     var j = this.@com.vaadin.terminal.gwt.client.CSSRule::rules.length;
        #     for(var i=0; i<j; i++) {
        #     var value = this.@com.vaadin.terminal.gwt.client.CSSRule::rules[i].style[propertyName];
        #     if(value)
        #     return value;
        #     }
        #     return null;
        #     }-

        pass

    def getSelector(self):
        return self._selector
