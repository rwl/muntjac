# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.dragndrop.DragDropHtml5FromDesktop import (DragDropHtml5FromDesktop,)
from com.vaadin.demo.sampler.features.dragndrop.DragDropTreeSorting import (DragDropTreeSorting,)
from com.vaadin.demo.sampler.features.dragndrop.DragDropTableTree import (DragDropTableTree,)
from com.vaadin.demo.sampler.features.dragndrop.DragDropServerValidation import (DragDropServerValidation,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class DragDropRearrangeComponents(Feature):

    def getSinceVersion(self):
        return Version.V63

    def getDescription(self):
        return 'In addition to arbitrary data items, whole components can also be dragged. ' + 'Here, the order of various components in a layout can be rearranged by dragging the components.'

    def getName(self):
        return 'Drag components'

    def getRelatedAPI(self):
        return [APIResource(DragAndDropWrapper), APIResource(DropHandler)]

    def getRelatedFeatures(self):
        return [DragDropTreeSorting, DragDropTableTree, DragDropServerValidation, DragDropHtml5FromDesktop]

    def getRelatedResources(self):
        return None
