# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.table.TableMainFeaturesExample import (TableMainFeaturesExample,)
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TableColumnCollapsing(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Table, column collapsing'

    def getExample(self):
        return TableMainFeaturesExample()

    def getDescription(self):
        return 'Columns can be \'collapsed\', which means that it\'s not shown,' + ' but the user can make the column re-appear by using the' + ' menu in the upper right of the table.<br/>' + ' Columns can also be made invisible, in which case they can' + ' not be brought back by the user.'

    def getRelatedAPI(self):
        return [APIResource(Table)]

    def getRelatedFeatures(self):
        return [FeatureSet.Tables]

    def getRelatedResources(self):
        return None
