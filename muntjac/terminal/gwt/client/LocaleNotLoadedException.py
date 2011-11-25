# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class LocaleNotLoadedException(Exception):

    def __init__(self, locale):
        super(LocaleNotLoadedException, self)(locale)
