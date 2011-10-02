# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.features.table.TableClickListenersExample import (TableClickListenersExample,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TableClickListeners(Feature):

    def getDescription(self):
        return 'You can assign a click listener to the column headers and footers to handle user mouse clicks.'

    def getName(self):
        return 'Table, click listeners'

    def getRelatedAPI(self):
        return [APIResource(Table)]

    def getRelatedFeatures(self):
        return [FeatureSet.Tables]

    def getRelatedResources(self):
        return None

    def getSinceVersion(self):
        return Version.V64

    def getExample(self):
        return TableClickListenersExample()
