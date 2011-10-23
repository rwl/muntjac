
from muntjac.ui.tree import Tree

from muntjac.demo.sampler.features.trees.TreeSingleSelectExample import TreeSingleSelectExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TreeActions(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Tree, context menu'


    def getDescription(self):
        return ('In this example, actions have been attached to the tree '
            'component. Try clicking the secondary mouse button on an item '
            'in the tree.')


    def getRelatedAPI(self):
        return [APIResource(Tree)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.trees.TreeMouseEvents import TreeMouseEvents
        from muntjac.demo.sampler.features.trees.TreeSingleSelect import TreeSingleSelect
        from muntjac.demo.sampler.features.trees.TreeMultiSelect import TreeMultiSelect

        return [TreeSingleSelect, TreeMultiSelect, TreeMouseEvents]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None


    def getExample(self):
        return TreeSingleSelectExample()
