# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.trees.TreeMouseEvents import (TreeMouseEvents,)
from com.vaadin.demo.sampler.features.trees.TreeSingleSelectExample import (TreeSingleSelectExample,)
from com.vaadin.demo.sampler.features.trees.TreeSingleSelect import (TreeSingleSelect,)
from com.vaadin.demo.sampler.features.trees.TreeMultiSelect import (TreeMultiSelect,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TreeActions(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Tree, context menu'

    def getDescription(self):
        return 'In this example, actions have been attached to' + ' the tree component. Try clicking the secondary mouse' + ' button on an item in the tree.'

    def getRelatedAPI(self):
        return [APIResource(Tree)]

    def getRelatedFeatures(self):
        return [TreeSingleSelect, TreeMultiSelect, TreeMouseEvents]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None

    def getExample(self):
        return TreeSingleSelectExample()
