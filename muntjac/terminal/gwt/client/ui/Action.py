# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.Util import (Util,)


class Action(Command):
    owner = None
    iconUrl = None
    caption = ''

    def __init__(self, owner):
        self.owner = owner

    def execute(self):
        """Executed when action fired"""
        pass

    def getHTML(self):
        sb = str()
        sb.__add__('<div>')
        if self.getIconUrl() is not None:
            sb.__add__('<img src=\"' + Util.escapeAttribute(self.getIconUrl()) + '\" alt=\"icon\" />')
        sb.__add__(self.getCaption())
        sb.__add__('</div>')
        return str(sb)

    def getCaption(self):
        return self.caption

    def setCaption(self, caption):
        self.caption = caption

    def getIconUrl(self):
        return self.iconUrl

    def setIconUrl(self, url):
        self.iconUrl = url
