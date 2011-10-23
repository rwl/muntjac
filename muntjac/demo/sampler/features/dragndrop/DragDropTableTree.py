
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.api import Tree, Table
from muntjac.event.dd.drop_handler import IDropHandler
from muntjac.event.dd.acceptcriteria.source_is import SourceIs
from muntjac.ui.tree import TargetItemAllowsChildren

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class DragDropTableTree(Feature):

    def getSinceVersion(self):
        return Version.V63


    def getDescription(self):
        return ('This example demonstrates how drag\'n\'drop can be used to '
            'move data between different components. Try dragging hardware '
            'items or categories from the tree to the table or table rows '
            'onto categories in the tree. Each component accepts data from '
            'the other one but not from itself, and the tree only accepts '
            'items dropped onto the correct category. Validation of allowed '
            'drop targets is performed on the client side, without requests '
            'to the server.')


    def getName(self):
        return 'Drag items between tree and table'


    def getRelatedAPI(self):
        return [
            APIResource(Tree),
            APIResource(Table),
            APIResource(IDropHandler),
            APIResource(ClientSideCriterion),
            APIResource(SourceIs),
            APIResource(TargetItemAllowsChildren)
        ]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.dragndrop.DragDropHtml5FromDesktop import \
            DragDropHtml5FromDesktop

        from muntjac.demo.sampler.features.dragndrop.DragDropTreeSorting import \
            DragDropTreeSorting

        from muntjac.demo.sampler.features.dragndrop.DragDropServerValidation import \
            DragDropServerValidation

        from muntjac.demo.sampler.features.dragndrop.DragDropRearrangeComponents \
            import DragDropRearrangeComponents

        return [
            DragDropTreeSorting,
            DragDropServerValidation,
            DragDropRearrangeComponents,
            DragDropHtml5FromDesktop
        ]


    def getRelatedResources(self):
        return None
