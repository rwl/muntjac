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

"""Interface for painting to the UIDL stream."""


class IPaintTarget(object):
    """This interface defines the methods for painting XML to the UIDL
    stream.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def addSection(self, sectionTagName, sectionData):
        """Prints single XMLsection.

        Prints full XML section. The section data is escaped from XML
        tags and surrounded by XML start and end-tags.

        @param sectionTagName:
                   the name of the tag.
        @param sectionData:
                   the scetion data.
        @raise PaintException:
                    if the paint operation failed.
        """
        raise NotImplementedError


    def startTag(self, paintable, tag=None):
        """Prints element start tag of a paintable section. Starts a paintable
        section using the given tag. The IPaintTarget may implement a caching
        scheme, that checks the paintable has actually changed or can a cached
        version be used instead. This method should call the startTag method.

        If the Paintable is found in cache and this function returns true it
        may omit the content and close the tag, in which case cached content
        should be used.

        @param paintable:
                   the paintable to start.
        @param tag:
                   the name of the start tag.
        @return: C{True} if paintable found in cache, C{False} otherwise.
        @raise PaintException:
                    if the paint operation failed.
        """
        raise NotImplementedError


    def paintReference(self, paintable, referenceName):
        """Paints a component reference as an attribute to current tag. This
        method is meant to enable component interactions on client side. With
        reference the client side component can communicate directly to other
        component.

        Note! This was experimental api and got replaced by L{addAttribute}.

        @param paintable:
                   the Paintable to reference
        @param referenceName:
        @raise PaintException

        @deprecated: use L{addAttribute} or L{addVariable} instead
        """
        raise NotImplementedError


    def endTag(self, tagName):
        """Prints element end tag.

        If the parent tag is closed before every child tag is closed an
        PaintException is raised.

        @param tagName:
                   the name of the end tag.
        @raise PaintException:
                    if the paint operation failed.
        """
        raise NotImplementedError


    def addAttribute(self, *args):
        """Adds a boolean attribute to component. Attributes must be added
        before any content is written.

        @raise PaintException:
                    if the paint operation failed.
        """
        raise NotImplementedError


    def addVariable(self, *args):
        """Adds details about L{StreamVariable} to the UIDL stream.
        Eg. in web terminals Receivers are typically rendered for the client
        side as URLs, where the client side implementation can do an http
        post request.

        The urls in UIDL message may use Muntjac specific protocol. Before
        actually using the urls on the client side, they should be passed via
        L{ApplicationConnection.translateMuntjacUri}.

        Note that in current terminal implementation StreamVariables are
        cleaned from the terminal only when:

          - a StreamVariable with same name replaces an old one
          - the variable owner is no more attached
          - the developer signals this by calling
            L{StreamingStartEvent.disposeStreamVariable}

        Most commonly a component developer can just ignore this issue, but
        with strict memory requirements and lots of StreamVariables
        implementations that reserve a lot of memory this may be a critical
        issue.

        @param args: tuple of the form
            - (owner, name, value)
              1. the ReceiverOwner that can track the progress of streaming
                 to the given StreamVariable
              2. an identifying name for the StreamVariable
              3. the StreamVariable to paint
        @raise PaintException:
                    if the paint operation failed.
        """
        raise NotImplementedError


    def addUploadStreamVariable(self, owner, name):
        """Adds a upload stream type variable.

        @param owner:
                   the Listener for variable changes.
        @param name:
                   the Variable name.

        @raise PaintException:
                    if the paint operation failed.
        """
        raise NotImplementedError


    def addXMLSection(self, sectionTagName, sectionData, namespace):
        """Prints single XML section.

        Prints full XML section. The section data must be XML and it is
        surrounded by XML start and end-tags.

        @param sectionTagName:
                   the tag name.
        @param sectionData:
                   the section data to be printed.
        @param namespace:
                   the namespace.
        @raise PaintException:
                    if the paint operation failed.
        """
        raise NotImplementedError


    def addUIDL(self, uidl):
        """Adds UIDL directly. The UIDL must be valid in accordance with
        the UIDL.dtd

        @param uidl:
                   the UIDL to be added.
        @raise PaintException:
                    if the paint operation failed.
        """
        raise NotImplementedError


    def addText(self, text):
        """Adds text node. All the contents of the text are XML-escaped.

        @param text:
                   the Text to add
        @raise PaintException:
                    if the paint operation failed.
        """
        raise NotImplementedError


    def addCharacterData(self, text):
        """Adds CDATA node to target UIDL-tree.

        @param text:
                   the Character data to add
        @raise PaintException:
                    if the paint operation failed.
        """
        raise NotImplementedError


    def getTag(self, paintable):
        """@return: the "tag" string used in communication to present given
                L{IPaintable} type. Terminal may define how to present
                paintable.
        """
        raise NotImplementedError


    def isFullRepaint(self):
        """@return true if a full repaint has been requested. E.g. refresh
        in a browser window or such.
        """
        raise NotImplementedError
