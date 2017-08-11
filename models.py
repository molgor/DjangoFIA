#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Forest Inventory Analysis Program Models
========================================
.. This is a model description of the US FIA database
Here it is defined the Object Relational Mapping between

"""

from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
# Create your models here.

class Richness(models.Model):
    """
    .. 
    The model for the Richness CSV
    Attributes
    ----------
    id : int
        Identification value of each occurrence. Unique to any element of the GBIF dataset.
    
    geom : Geometric Point
        Geometric Value in WKB
    objects : spystats.GeoManager()
        Wrapper for GeoDjango
    
    """
    stateab = models.CharField(max_length=254,db_index=True)
    statenm = models.CharField(max_length=254,db_index=True)
    countynm = models.CharField(max_length=254,db_index=True)
    plot_idn = models.BigIntegerField(db_index=True)
    lat = models.FloatField()
    lon = models.FloatField()
    elev = models.FloatField(db_index=True)
    invyr = models.BigIntegerField()
    area = models.BigIntegerField()
    s = models.BigIntegerField()
    tree_dens = models.BigIntegerField()
    plot_agb = models.FloatField(db_index=True)
    geom = models.PointField(srid=4326,db_index=True)

# Auto-generated `LayerMapping` dictionary for Richness model
richness_mapping = {
    'stateab' : 'STATEAB',
    'statenm' : 'STATENM',
    'countynm' : 'COUNTYNM',
    'plot_idn' : 'PLOT_IDn',
    'lat' : 'LAT',
    'lon' : 'LON',
    'elev' : 'ELEV',
    'invyr' : 'INVYR',
    'area' : 'Area',
    's' : 'S',
    'tree_dens' : 'TREE_DENS',
    'plot_agb' : 'plot_AGB',
    'geom' : 'POINT',
}

class Spplist(models.Model):
    stateab = models.CharField(max_length=254,db_index=True)
    statenm = models.CharField(max_length=254,db_index=True)
    countynm = models.CharField(max_length=254,db_index=True)
    plot_idn = models.FloatField(db_index=True)
    lat = models.FloatField()
    lon = models.FloatField()
    elev = models.FloatField(db_index=True)
    spcd = models.BigIntegerField()
    genus = models.CharField(max_length=254,db_index=True)
    species = models.CharField(max_length=254,db_index=True)
    variety = models.CharField(max_length=254,db_index=True)
    subspecies = models.CharField(max_length=254,db_index=True)
    geom = models.PointField(srid=4326,db_index=True)

# Auto-generated `LayerMapping` dictionary for Spplist model
spplist_mapping = {
    'stateab' : 'STATEAB',
    'statenm' : 'STATENM',
    'countynm' : 'COUNTYNM',
    'plot_idn' : 'PLOT_IDn',
    'lat' : 'LAT',
    'lon' : 'LON',
    'elev' : 'ELEV',
    'spcd' : 'SPCD',
    'genus' : 'GENUS',
    'species' : 'SPECIES',
    'variety' : 'VARIETY',
    'subspecies' : 'SUBSPECIES',
    'geom' : 'POINT',
}

class TreeLevel(models.Model):
    study = models.CharField(max_length=254,db_index=True)
    lat = models.FloatField()
    long = models.FloatField()
    plot_id = models.BigIntegerField(db_index=True)
    plotarea_m = models.BigIntegerField()
    year = models.BigIntegerField(db_index=True)
    full_speci = models.CharField(max_length=254,db_index=True)
    tree_id = models.FloatField(db_index=True)
    dbhcm = models.FloatField()
    abundance = models.BigIntegerField(db_index=True)
    geom = models.PointField(srid=4326,db_index=True)

# Auto-generated `LayerMapping` dictionary for TreeLevel model
treelevel_mapping = {
    'study' : 'Study',
    'lat' : 'Lat',
    'long' : 'Long',
    'plot_id' : 'Plot_ID',
    'plotarea_m' : 'PlotArea_m',
    'year' : 'Year',
    'full_speci' : 'Full_speci',
    'tree_id' : 'Tree_ID',
    'dbhcm' : 'DBHcm',
    'abundance' : 'Abundance',
    'geom' : 'POINT',
}

class USGrid100km(models.Model):
    id = models.BigIntegerField(primary_key=True)
    xmini = models.FloatField()
    xmaxi = models.FloatField()
    ymini = models.FloatField()
    ymaxi = models.FloatField()
    geom = models.PolygonField(srid=4326,db_index=True)

# Auto-generated `LayerMapping` dictionary for USGrid100km model
usgrid100km_mapping = {
    'id' : 'ID',
    'xmini' : 'XMINI',
    'xmaxi' : 'XMAX',
    'ymini' : 'YMIN',
    'ymaxi' : 'YMAX',
    'geom' : 'POLYGON',
}

