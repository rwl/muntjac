# -*- coding: utf-8 -*-


class ImageEmbedExample(VerticalLayout):

    def __init__(self):
        e = Embedded('Image from a theme resource', ThemeResource('../runo/icons/64/document.png'))
        self.addComponent(e)
