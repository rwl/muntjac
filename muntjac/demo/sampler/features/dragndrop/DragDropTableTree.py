# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.dragndrop.DragDropHtml5FromDesktop import (DragDropHtml5FromDesktop,)
from com.vaadin.demo.sampler.features.dragndrop.DragDropTreeSorting import (DragDropTreeSorting,)
from com.vaadin.demo.sampler.features.dragndrop.DragDropServerValidation import (DragDropServerValidation,)
from com.vaadin.demo.sampler.features.dragndrop.DragDropRearrangeComponents import (DragDropRearrangeComponents,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class DragDropTableTree(Feature):

    def getSinceVersion(self):
        return Version.V63

    def getDescription(self):
        return 'This example demonstrates how drag\'n\'drop can be used to move data between different components. ' + 'Try dragging hardware items or categories from the tree to the table or table rows onto categories in the tree. ' + 'Each component accepts data from the other one but not from itself, and the tree only accepts items dropped onto the correct category. ' + 'Validation of allowed drop targets is performed on the client side, without requests to the server.'

    def getName(self):
        return 'Drag items between tree and table'

    def getRelatedAPI(self):
        return [APIResource(Tree), APIResource(Table), APIResource(DropHandler), APIResource(ClientSideCriterion), APIResource(SourceIs), APIResource(TargetItemAllowsChildren)]

    def getRelatedFeatures(self):
        return [DragDropTreeSorting, DragDropServerValidation, DragDropRearrangeComponents, DragDropHtml5FromDesktop]

    def getRelatedResources(self):
        return None
