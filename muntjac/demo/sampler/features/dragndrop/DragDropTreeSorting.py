
from muntjac.demo.sampler.features.dragndrop.DragDropHtml5FromDesktop import \
    DragDropHtml5FromDesktop

from muntjac.demo.sampler.features.dragndrop.DragDropTableTree import \
    DragDropTableTree

from muntjac.demo.sampler.features.dragndrop.DragDropServerValidation import \
    DragDropServerValidation
from muntjac.ui.tree import Tree
from muntjac.event.dd.drop_handler import IDropHandler

from muntjac.demo.sampler.features.dragndrop.DragDropRearrangeComponents \
    import DragDropRearrangeComponents

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class DragDropTreeSorting(Feature):

    def getSinceVersion(self):
        return Version.V63


    def getName(self):
        return 'Tree sorting using drag\'n\'drop'


    def getDescription(self):
        return ('This example demonstrates how drag\'n\'drop can be used to '
            'allow a user to sort a tree. The sort is not restricted, the '
            'tree can be freely sorted in any way the user likes. Try '
            'dragging an item and dropping it on another node.')


    def getRelatedAPI(self):
        return [APIResource(Tree), APIResource(IDropHandler)]


    def getRelatedFeatures(self):
        return [
            DragDropTableTree,
            DragDropServerValidation,
            DragDropRearrangeComponents,
            DragDropHtml5FromDesktop
        ]


    def getRelatedResources(self):
        return None
