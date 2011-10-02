# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.trees.TreeSingleSelect import (TreeSingleSelect,)
from com.vaadin.demo.sampler.features.trees.TreeMultiSelect import (TreeMultiSelect,)
from com.vaadin.demo.sampler.features.trees.TreeActions import (TreeActions,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TreeMouseEvents(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Tree, mouse events'

    def getDescription(self):
        return 'In this example, selecting items from the tree' + ' is disabled. Instead, another method of selection' + ' is used. Using the ItemClickEvent, we can update the' + ' label showing the selection.' + '<br>Try to click your left, right and middle mouse' + ' buttons on the tree items. Any modifier keys will' + ' also be detected.'

    def getRelatedAPI(self):
        return [APIResource(Tree)]

    def getRelatedFeatures(self):
        return [TreeSingleSelect, TreeMultiSelect, TreeActions]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
