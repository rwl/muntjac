# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.dragndrop.DragDropHtml5FromDesktop import (DragDropHtml5FromDesktop,)
from com.vaadin.demo.sampler.features.dragndrop.DragDropTableTree import (DragDropTableTree,)
from com.vaadin.demo.sampler.features.dragndrop.DragDropServerValidation import (DragDropServerValidation,)
from com.vaadin.demo.sampler.features.dragndrop.DragDropRearrangeComponents import (DragDropRearrangeComponents,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class DragDropTreeSorting(Feature):

    def getSinceVersion(self):
        return Version.V63

    def getName(self):
        return 'Tree sorting using drag\'n\'drop'

    def getDescription(self):
        return 'This example demonstrates how drag\'n\'drop can be used to allow a user to sort a tree.' + ' The sort is not restricted, the tree can be freely sorted in any way the user likes.' + ' Try dragging an item and dropping it on another node.'

    def getRelatedAPI(self):
        return [APIResource(Tree), APIResource(DropHandler)]

    def getRelatedFeatures(self):
        return [DragDropTableTree, DragDropServerValidation, DragDropRearrangeComponents, DragDropHtml5FromDesktop]

    def getRelatedResources(self):
        return None
