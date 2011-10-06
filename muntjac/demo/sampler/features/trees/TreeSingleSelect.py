
from muntjac.ui.tree import Tree

from muntjac.demo.sampler.features.trees.TreeMultiSelect import TreeMultiSelect
from muntjac.demo.sampler.features.trees.TreeActions import TreeActions
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TreeSingleSelect(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Tree, single selection'


    def getDescription(self):
        return ('In this example, you can select any single tree node and '
            'modify its \'name\' property. Click again to de-select.')


    def getRelatedAPI(self):
        return [APIResource(Tree)]


    def getRelatedFeatures(self):
        return [TreeMultiSelect, TreeActions]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
