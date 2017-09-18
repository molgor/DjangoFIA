#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Forest Inventory Analysis Program Sampling scenarios
========================================
.. This module creates several DataFrames using the FIA database. 

"""

from __future__ import unicode_literals
from external_plugins.DjangoFIA.models import BiomassGroups, Spplist, SppNProduct, TreesPerYear
from external_plugins.DjangoFIA.models import USGrid100km as grid
from django_pandas.io import read_frame
import pandas as pd
import logging

logger = logging.getLogger('biospytial.gbif')


import scipy.stats as st
import numpy as np

def ObtainRandomUniformCellSampling(grid_model,sample_size=100):
    """
    Select random uniform sample of cells given a grid_model.
    The grid cells has an id (pk) and I'm selecting a the index of this.
    """
    N = grid_model.objects.count()
    f = st.randint(0,N)
    sample_ids = f.rvs(sample_size)
    sample_cells = grid_model.objects.filter(pk__in=sample_ids)
    return sample_cells


def TreesOnCellsSelection(list_of_sampled_cells,filter_empty=True):
    """
    Returns a QuerySet of type: TreeLevel corresponding to the objects that intersect to the geometry attribute of Cell
    """
    trees_sample = map(lambda c : TreesPerYear.objects.filter(geom__intersects=c.geom),list_of_sampled_cells)
    if filter_empty:
        trees_sample = filter(lambda sample : sample.count() != 0 , trees_sample)
    return trees_sample


def getRandomSelectionOfTrees(list_of_treesqueryset,N=3):
    """
    selects a set of trees (records TreeLevel) for a queryset defined by the intersection of a cell with the TRee year table.
    """
    trees = list_of_treesqueryset
    samples = map(lambda l : np.random.choice(l,N),trees)
    return samples
    



def sampleScenario1pre(number_of_points=100,buffer_size_km=10):
    """
    Sample scenario according to the 1st. Task.
    """
    cells = ObtainRandomUniformCellSampling(grid,number_of_points)
    trees_sample = TreesOnCellsSelection(cells) 
    points = getRandomSelectionOfTrees(trees_sample)
    ## Reduce selection (choice) into a single list
    points = reduce(lambda a,b : list(a)+list(b) , points)
    return points


def selectFromBuffer(list_of_points,buffer_size_km=10):
    """
    First create the buffer then selects Points within that buffer.
    """
    buffers = map(lambda p : p.alberts102003.buffer(buffer_size_km),list_of_points)
    trees_sample = map(lambda polygon : TreesPerYear.objects.filter(alberts102003__intersects=polygon),buffers)
    return trees_sample
    
def sampleScenario(number_of_points=100,buffer_size_km=10,feature_names=["statenm","statecd","stateab","subp","n_inventor","elev","invyr","tree","spcd","family","ht_m","ba_m2","biomass_kg"]):
    points = sampleScenario1pre(number_of_points=number_of_points,buffer_size_km=buffer_size_km)
    selections = selectFromBuffer(points,buffer_size_km)
    dfsels = map(lambda q : read_frame(q, fieldnames=feature_names),selections)
    ## compent if prefer custom feature selection
    dfsels = getSummaryStatistics(dfsels)
    return dfsels



def getSummaryStatistics(list_samples):
    getSummaryStats = lambda df : [df.ba_m2.describe()['mean'],df.ba_m2.describe()['std'],df.biomass_kg.describe()['mean'],df.biomass_kg.describe()['std']]
    samps = map(getSummaryStats,list_samples)
    samples = pd.DataFrame(samps)
    richness = pd.DataFrame(map(lambda df : len(df.spcd.unique()),list_samples))
    samples = pd.concat([richness,samples],axis=1)
    samples.columns = ["Sp_Richness","Ba_m2-mean","Ba_m2_std","Biomass-mean","Biomass-std"]
    return samples

