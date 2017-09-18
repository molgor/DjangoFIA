#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Forest Inventory Analysis Program Sampling scenarios
====================================================
.. This module creates several DataFrames using the FIA database. 

"""

from __future__ import unicode_literals
from external_plugins.DjangoFIA.models import BiomassGroups, Spplist, SppNProduct, TreesPerYear
from external_plugins.DjangoFIA.models import USGrid100km as grid
from django_pandas.io import read_frame
import pandas as pd
import logging

logger = logging.getLogger('biospytial.gbif.taxonomy')


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
    logger.info("GridCells Sample obtained ")
    return sample_cells

def TreesOnCellsSelection(list_of_sampled_cells,filter_empty=True):
    """
    Returns a QuerySet of type: TreeLevel corresponding to the objects that intersect to the geometry attribute of Cell
    """
    trees_sample = map(lambda c : TreesPerYear.objects.filter(geom__intersects=c.geom),list_of_sampled_cells)
    logger.info("Intersecting TreeLevel data with chosen cells")
    if filter_empty:
        trees_sample = filter(lambda sample : sample.count() != 0 , trees_sample)
    return trees_sample


def getRandomSelectionOfTrees(list_of_treesqueryset,N=3):
    """
    selects a set of trees (records TreeLevel) for a queryset defined by the intersection of a cell with the TRee year table.
    """
    trees = list_of_treesqueryset
    samples = map(lambda l : np.random.choice(l,N),trees)
    logger.info("Random selection of Trees obtained")
    return samples
    
def getRandomSelectionOfPlots(list_of_treesqueryset,N=3):
    """
    selects a set of trees (records TreeLevel) for a queryset defined by the intersection of a cell with the TRee year table.
    """
    trees = list_of_treesqueryset
    ## Select only distinct
    plots = map(lambda qs : qs.distinct('plot_id'),trees)
    samples = map(lambda l : np.random.choice(l,N),plots)
    logger.info("Random selection of plots obtained")
    return samples


def sampleScenario1pre(number_of_points=100):
    """
    Sample scenario according to the 1st. Task.
    """
    cells = ObtainRandomUniformCellSampling(grid,number_of_points)
    trees_sample = TreesOnCellsSelection(cells) 
    #points = getRandomSelectionOfTrees(trees_sample)
    points = getRandomSelectionOfPlots(trees_sample)

    ## Reduce selection (choice) into a single list
    points = reduce(lambda a,b : list(a)+list(b) , points)
    return points


def selectFromBuffer(list_of_points,buffer_size_km=10):
    """
    First create the buffer then selects Points within that buffer.
    """
    logger.info("Creating newbuffers")
    buffers = map(lambda p : p.alberts102003.buffer(buffer_size_km),list_of_points)
    trees_sample = map(lambda polygon : TreesPerYear.objects.filter(alberts102003__intersects=polygon),buffers)
    return trees_sample

def selectFromBufferRandom(list_of_points,buffer_start_km,buffer_end_km,list_cutoffs=[]):
    """
    First create the buffer then selects Points within that buffer.
    This function selects a random uniform integer between  buffer start and buffer end.
    
        Buffer start in inclusive
        Buffer end is exclusive
     
    Returns:
    tuple :  QuerySet, list_buffer_weights    
    """
    # The buffer needs to be in kilometers
    def selectRandomCutoff(list_cutoffs):
        idcut = np.random.randint(1,len(list_cutoffs) + 1)
        #import ipdb; ipdb.set_trace()
        cut = list_cutoffs[idcut - 1 ]
        return cut
    
    logger.info("Selecting CutOff threshold")
    ks = map(lambda p : np.random.randint(buffer_start_km,buffer_end_km)*1000,list_of_points)
    logger.info("Creating Random Buffers")
    buffers = map(lambda (p,k) : p.alberts102003.buffer(k),zip(list_of_points,ks))
    trees_sample = map(lambda polygon : TreesPerYear.objects.filter(alberts102003__intersects=polygon),buffers)
    if not list_cutoffs:
        logger.info("No CutOff selected")
        nas = map(lambda n : np.nan, range(len(trees_sample)))
        return (trees_sample,ks,nas)
    else:
        logger.info("Selecting with Cutoffs")
        cuts = map(lambda qs : selectRandomCutoff(list_cutoffs),range(len(trees_sample)))
        trees_sample = map(lambda (qs,cut) : qs.filter(dia__gte=cut),zip(trees_sample,cuts))
        #trees_sample=[]
        return (trees_sample,ks,cuts)




def aggregateQuerySet(queryset_treelevel,study_id,buffer_size,cutoff):
    """
    Receive a TreeLevel query set
    
    Output: DataFrame with columns:
    Scenario, Study, Plotid, SpeciesRich, Productivity, Spec-Turnover, Buffer_size, LatLon
    """
    def calculateProductivityAndTurnOver(data_frame_by_plot_id):
        """
        Calculates the productivity based on the year inventory
        """
        by_yr = data_frame_by_plot_id.groupby('invyr')
        yrs = by_yr.groups.keys()
        aggr_yrs = by_yr.sum()
        minyr_biomass = aggr_yrs.loc[min(yrs)].biomass_kg
        maxyr_biomass = aggr_yrs.loc[max(yrs)].biomass_kg        
        ## Acording to the formula:
        ## Sum(biomas_max(yr)) - sum(biomass_min(yr))
        productivity = maxyr_biomass - minyr_biomass / (float(max(yrs)) - float(min(yrs)))
        
        ## Now for turnover
        d = data_frame_by_plot_id
        minyr_sp_rich = len(d[d['invyr'] == min(yrs)].spcd.unique())
        maxyr_sp_rich = len(d[d['invyr'] == max(yrs)].spcd.unique())
        
        turnoversp = maxyr_sp_rich - minyr_sp_rich / (float(max(yrs)) - float(min(yrs)))
        
        return productivity,turnoversp
    

    from django_pandas.io import read_frame
    qs = queryset_treelevel
    plot_ids = map(lambda v : v.values().pop(), list(qs.values('plot_id').distinct()))
    plots_pool = map(lambda pid : qs.filter(plot_id=pid),plot_ids)
    ## Convert to dataframes
    coords_wgs = map(lambda v : v.values().pop(), list(qs.values('geom').distinct()))
    coords_alberts = map(lambda v : v.values().pop(), list(qs.values('alberts102003').distinct()))

    ds =map(lambda q : read_frame(q),plots_pool)
    ## Remember to reduce everything to a number
    sp_richness = map(lambda d : len(d.spcd.unique()),ds)
    ## 
    #import ipdb; ipdb.set_trace()
    productivity_turnover = map(calculateProductivityAndTurnOver,ds)
    
    prod , turn = zip(*productivity_turnover)
    
    study_ids = list(np.ones(len(plot_ids)) * study_id)
    buffer_size = list(np.ones(len(plot_ids)) * buffer_size)
    cutoffs = list(np.ones(len(plot_ids)) * cutoff)
    
    
    lon,lat = zip(*coords_wgs)
    x,y = zip(*coords_alberts)
    
    
    l = [sp_richness,list(prod),list(turn),plot_ids,study_ids,buffer_size,cutoffs,list(lon),list(lat),list(x),list(y)]
    l = pd.DataFrame(l).transpose()
    l.columns = ["Sp_rich","Productivity","Sp_TurnOver","Plot_id","Study_id","Buffer_m","Cutoff","Lon","Lat","X(102003)","Y(102003)"]
    #l = reduce(lambda a,b : a + b , [sp_richness,list(prod),list(turn)])
    return l
    



    
def getSummaryStatistics(list_samples,ks=[]):
    getSummaryStats = lambda df : [df.ba_m2.describe()['mean'],df.ba_m2.describe()['std'],df.biomass_kg.describe()['mean'],df.biomass_kg.describe()['std']]
    samps = map(getSummaryStats,list_samples)
    samples = pd.DataFrame(samps)
    richness = pd.DataFrame(map(lambda df : len(df.spcd.unique()),list_samples))
    #geom = pd.DataFrame(map(lambda df : df.alberts102003.long, df.alberts102003.lat,list_samples))
    if ks :
        logger.info("Using Random buffers ")
        pks = pd.DataFrame(ks)
        samples = pd.concat([richness,samples,pks],axis=1)
        samples.columns = ["Sp_Richness","Ba_m2-mean","Ba_m2_std","Biomass-mean","Biomass-std","Buff_sizekm"]
        return samples
    else:
        logger.info("Using constant buffers ")
        samples = pd.concat([richness,samples],axis=1)
        samples.columns = ["Sp_Richness","Ba_m2-mean","Ba_m2_std","Biomass-mean","Biomass-std"]
        return samples




def sampleScenario(number_of_points=100,buffer_size_km=10,feature_names=["statenm","statecd","stateab","subp","n_inventor","elev","invyr","tree","spcd","family","ht_m","ba_m2","biomass_kg"]):
    points = sampleScenario1pre(number_of_points=number_of_points)
    selections = selectFromBuffer(points,buffer_size_km)
    dfsels = map(lambda q : read_frame(q, fieldnames=feature_names),selections)
    ## compent if prefer custom feature selection
    dfsels = getSummaryStatistics(dfsels)
    return dfsels


def sampleRandomBufferScenario(buffer_start_km,buffer_end_km,number_of_points=100,to_dataframe=True,using_cutoffs=[],scenario_id='sc-0',feature_names=["statenm","statecd","stateab","subp","n_inventor","elev","invyr","tree","spcd","family","ht_m","ba_m2","biomass_kg","alberts102003"]):
    points = sampleScenario1pre(number_of_points=number_of_points)
    selections,ks,cuts = selectFromBufferRandom(points,buffer_start_km,buffer_end_km,using_cutoffs)

    if to_dataframe:
        #dfsels = map(lambda q : read_frame(q, fieldnames=feature_names),selections)
        #import ipdb; ipdb.set_trace()
        dfsels = map(lambda (study_id,t_qbc) : aggregateQuerySet(t_qbc[0],study_id,t_qbc[1],t_qbc[2]),enumerate(zip(selections,ks,cuts)))
        ## compent if prefer custom feature selection
        #dfsels = getSummaryStatistics(dfsels,ks)
        dfsels = pd.concat(dfsels)
        #import ipdb; ipdb.set_trace()
        #new = pd.concat([scenario_col,dfsels],axis=1)
        return dfsels.assign(Scenario = lambda x : scenario_id)
    else:
        return (selections,ks,cuts)





    
