# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class ComputedStyle(object):
    computedStyle = None
    _elem = None

    def __init__(self, elem):
        """Gets this element's computed style object which can be used to gather
        information about the current state of the rendered node.
        <p>
        Note that this method is expensive. Wherever possible, reuse the returned
        object.

        @param elem
                   the element
        @return the computed style
        """
        self.computedStyle = self.getComputedStyle(elem)
        self._elem = elem

    @classmethod
    def getComputedStyle(cls, elem):
        JS("""
      if(@{{elem}}.nodeType != 1) {
          return {};
      }
      
      if($wnd.document.defaultView && $wnd.document.defaultView.getComputedStyle) {
          return $wnd.document.defaultView.getComputedStyle(@{{elem}}, null);
      }
      
      if(@{{elem}}.currentStyle) {
          return @{{elem}}.currentStyle;
      }
    """)
        pass

    def getProperty(self, name):
        """@param name
                   name of the CSS property in camelCase
        @return the value of the property, normalized for across browsers (each
                browser returns pixel values whenever possible).
        """
        JS("""
        var cs = @{{self}}.@com.vaadin.terminal.gwt.client.ComputedStyle::computedStyle;
        var elem = @{{self}}.@com.vaadin.terminal.gwt.client.ComputedStyle::elem;
        
        // Border values need to be checked separately. The width might have a 
        // meaningful value even if the border style is "none". In that case the 
        // value should be 0.
        if(@{{name}}.indexOf("border") > -1 && @{{name}}.indexOf("Width") > -1) {
            var borderStyleProp = @{{name}}.substring(0,@{{name}}.length-5) + "Style";
            if(cs.getPropertyValue)
                var borderStyle = cs.getPropertyValue(borderStyleProp);
            else // IE
                var borderStyle = cs[borderStyleProp];
            if(borderStyle == "none")
                return "0px";
        }

        if(cs.getPropertyValue) {
        
            // Convert @{{name}} to dashed format
            @{{name}} = @{{name}}.replace(/([A-Z])/g, "-$1").toLowerCase();
            var ret = cs.getPropertyValue(@{{name}});
            
        } else {
        
            var ret = cs[@{{name}}];
            var style = elem.style;

            // From the awesome hack by Dean Edwards
            // http://erik.eae.net/archives/2007/07/27/18.54.15/#comment-102291

            // If we're not dealing with a regular pixel number
            // but a number that has a weird ending, we need to convert it to pixels
            if ( !/^\d+(px)?$/i.test( ret ) && /^\d/.test( ret ) ) {
                // Remember the original values
                var left = style.left, rsLeft = elem.runtimeStyle.left;

                // Put in the new values to get a computed value out
                elem.runtimeStyle.left = @{{self}}.left;
                style.left = ret || 0;
                ret = style.pixelLeft + "px";

                // Revert the changed values
                style.left = left;
                elem.runtimeStyle.left = rsLeft;
            }
            
        }
        
        // Normalize margin values. This is not totally valid, but in most cases 
        // it is what the user wants to know.
        if(@{{name}}.indexOf("margin") > -1 && ret == "auto") {
            return "0px";
        }
        
        // Some browsers return undefined width and height values as "auto", so
        // we need to retrieve those ourselves.
        if (@{{name}} == "width" && ret == "auto") {
            ret = elem.clientWidth + "px";
        } else if (@{{name}} == "height" && ret == "auto") {
            ret = elem.clientHeight + "px";
        }

        return ret;
        
    """)
        pass

    def getIntProperty(self, name):
        parsed = self.parseInt(self.getProperty(name))
        if parsed is not None:
            return parsed.intValue()
        return 0

    def getMargin(self):
        """Get current margin values from the DOM. The array order is the default
        CSS order: top, right, bottom, left.
        """
        margin = [0, 0, 0, 0]
        margin[0] = self.getIntProperty('marginTop')
        margin[1] = self.getIntProperty('marginRight')
        margin[2] = self.getIntProperty('marginBottom')
        margin[3] = self.getIntProperty('marginLeft')
        return margin

    def getPadding(self):
        """Get current padding values from the DOM. The array order is the default
        CSS order: top, right, bottom, left.
        """
        padding = [0, 0, 0, 0]
        padding[0] = self.getIntProperty('paddingTop')
        padding[1] = self.getIntProperty('paddingRight')
        padding[2] = self.getIntProperty('paddingBottom')
        padding[3] = self.getIntProperty('paddingLeft')
        return padding

    def getBorder(self):
        """Get current border values from the DOM. The array order is the default
        CSS order: top, right, bottom, left.
        """
        border = [0, 0, 0, 0]
        border[0] = self.getIntProperty('borderTopWidth')
        border[1] = self.getIntProperty('borderRightWidth')
        border[2] = self.getIntProperty('borderBottomWidth')
        border[3] = self.getIntProperty('borderLeftWidth')
        return border

    @classmethod
    def parseInt(cls, value):
        """Takes a String value e.g. "12px" and parses that to int 12.

        @param String
                   a value starting with a number
        @return int the value from the string before any non-numeric characters.
                If the value cannot be parsed to a number, returns
                <code>null</code>.
        """
        JS("""
        var number = parseInt(@{{value}}, 10);
        if (isNaN(number))
            return null;
        else
            return @java.lang.Integer::valueOf(I)(number);
    """)
        pass
