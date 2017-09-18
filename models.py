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
from adaptor.model import CsvModel
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
    id = models.AutoField(primary_key=True, db_column="gid")
    id_original = models.IntegerField(blank=True, db_column="id")
    xmini = models.FloatField(db_column="__xmin")
    xmaxi = models.FloatField(db_column="__xmax")
    ymini = models.FloatField(db_column="ymin")
    ymaxi = models.FloatField(db_column="ymax")
    geom = models.MultiPolygonField(srid=4326,db_index=True,geography=True)
    class Meta:
        managed = False
        
        # remote server table name
        db_table = 'mesh\".\"us100km'    

# Auto-generated `LayerMapping` dictionary for USGrid100km model
usgrid100km_mapping = {
    'id_original' : 'ID',
    'xmini' : 'XMIN',
    'xmaxi' : 'XMAX',
    'ymini' : 'YMIN',
    'ymaxi' : 'YMAX',
    'geom' : 'POLYGON',
}


# This is an auto-generated Django model module created by ogrinspect.


class SppNProduct(models.Model):
    statecd = models.BigIntegerField(db_index=True)
    stateab = models.CharField(max_length=254,db_index=True)
    statenm = models.CharField(max_length=254,db_index=True)
    countycd = models.BigIntegerField(db_index=True)
    lat = models.FloatField(db_index=True)
    lon = models.FloatField(db_index=True)
    elev = models.FloatField(db_index=True)
    plot = models.BigIntegerField(db_index=True)
    plot_id = models.CharField(max_length=254,db_index=True)
    plotidn = models.BigIntegerField(db_index=True)
    period = models.BigIntegerField(db_index=True)
    n_inventor = models.BigIntegerField(db_index=True)
    sppn = models.BigIntegerField()
    mean_treed = models.FloatField()
    mai_basala = models.FloatField()
    mai_biomas = models.FloatField()
    geom = models.PointField(srid=4326,db_index=True)


    def __unicode__(self):
            """
            ..
            String representation of Occurrence
            Returns
            -------
            info : string
                Name
            """
            return u'<SppNProduct: %s  : %s , %s , %s , %s >' %(self.pk,self.sppn,self.plotidn,self.mai_basala,self.mai_biomas) #,self.geom)
    
    def __repr__(self):
            """
            ..
            String representation of Occurrence
            Returns
            -------
            info : string
                Name
            """
            return u'<SppNProduct: %s, SppN  : %s , PlotIdn: %s , mBas: %s ,mBiomas: %s >' %(self.pk,self.sppn,self.plotidn,self.mai_basala,self.mai_biomas) #,self.geom)
    
          

# Auto-generated `LayerMapping` dictionary for SppNProduct model
sppnproduct_mapping = {
    'statecd' : 'STATECD',
    'stateab' : 'STATEAB',
    'statenm' : 'STATENM',
    'countycd' : 'COUNTYCD',
    'lat' : 'LAT',
    'lon' : 'LON',
    'elev' : 'ELEV',
    'plot' : 'PLOT',
    'plot_id' : 'PLOT_ID',
    'plotidn' : 'PlotIDn',
    'period' : 'Period',
    'n_inventor' : 'N_Inventor',
    'sppn' : 'SppN',
    'mean_treed' : 'mean_TreeD',
    'mai_basala' : 'MAI_basala',
    'mai_biomas' : 'MAI_biomas',
    'geom' : 'POINT',
}

class TreesPerYear(models.Model):
    statenm = models.CharField(max_length=254)
    statecd = models.BigIntegerField()
    stateab = models.CharField(max_length=254)
    countycd = models.BigIntegerField()
    plot = models.BigIntegerField()
    plot_id = models.CharField(max_length=254,db_index=True)
    plotidn = models.BigIntegerField(db_index=True)
    subp = models.BigIntegerField(db_index=True)
    n_inventor = models.BigIntegerField(db_index=True)
    lat = models.FloatField(db_index=True)
    lon = models.FloatField(db_index=True)
    elev = models.FloatField(db_index=True)
    invyr = models.BigIntegerField(db_index=True)
    tree = models.FloatField(db_index=True)
    spcd = models.BigIntegerField(db_index=True)
    accepted_n = models.CharField(max_length=254,db_index=True)
    family = models.CharField(max_length=254,db_index=True)
    dia = models.FloatField(db_index=True)
    ht_m = models.CharField(max_length=254,db_index=True)
    ba_m2 = models.FloatField(db_index=True)
    biomass_kg = models.FloatField(db_index=True)
    geom = models.PointField(srid=4326,db_index=True)
    alberts102003 = models.PointField(srid=102003,db_index=True)





    def __repr__(self):
        """
        ..
        String representation of Tree
        Returns
        -------
        info : string
        Name
        """
        return u'<Tree_yr: %s, Name  : %s , PlotIdn: %s , SubPlot: %s , Dia : %s, ht_m: %s, ba_m2: %s,biomass_kg : %s >' %(self.pk,self.accepted_n,self.plotidn,self.subp,self.dia,self.ht_m,self.ba_m2,self.biomass_kg) #,self.geom)
    

# Auto-generated `LayerMapping` dictionary for TreesPerYear model
treesperyear_mapping = {
    'statenm' : 'STATENM',
    'statecd' : 'STATECD',
    'stateab' : 'STATEAB',
    'countycd' : 'COUNTYCD',
    'plot' : 'PLOT',
    'plot_id' : 'PLOT_ID',
    'plotidn' : 'PlotIDn',
    'subp' : 'SUBP',
    'n_inventor' : 'N_Inventor',
    'lat' : 'LAT',
    'lon' : 'LON',
    'elev' : 'ELEV',
    'invyr' : 'INVYR',
    'tree' : 'TREE',
    'spcd' : 'SPCD',
    'accepted_n' : 'Accepted_n',
    'family' : 'Family',
    'dia' : 'DIA',
    'ht_m' : 'HT_m',
    'ba_m2' : 'BA_m2',
    'biomass_kg' : 'Biomass_kg',
    'geom' : 'POINT',
}

class BiomassGroups(models.Model):
    spp_group = models.CharField(max_length=254,db_index=True)
    spcd = models.CharField(max_length=254,db_index=True)
    family = models.CharField(max_length=254,db_index=True)
    newgenus = models.CharField(max_length=254,db_index=True)
    newspecies = models.CharField(max_length=254,db_index=True)
    usfs_wd = models.CharField(max_length=254,db_index=True)
    chave_wd = models.CharField(max_length=254,db_index=True)
    chavewd_level = models.CharField(max_length=254,db_index=True)
    code = models.CharField(max_length=254,db_index=True)
    group = models.CharField(max_length=254,db_index=True)
    taxa = models.CharField(max_length=254,db_index=True)
    b_0 = models.CharField(max_length=254,db_index=True)
    b_1 = models.CharField(max_length=254,db_index=True)
    mindbh = models.CharField(max_length=254,db_index=True)
    maxdbh = models.CharField(max_length=254,db_index=True)




def loadThisLine(line,delimiter=","):
    """
    Loads a line, splits it and insert it into the database
    """
    loadline = lambda line : BiomassGroups.objects.create(spp_group=line[0],
                                                          spcd=line[1],
                                                          family=line[2],
                                                          newgenus=line[3],
                                                          newspecies=line[4],
                                                          usfs_wd=line[5],
                                                          chave_wd=line[6],
                                                          chavewd_level=line[7],
                                                          code=line[8],
                                                          group=line[9],
                                                          taxa=line[10],
                                                          b_0=line[11],
                                                          b_1=line[12],
                                                          mindbh=line[13],
                                                          maxdbh=line[14])
    l = line.split(delimiter)
    return loadline(l)

# Auto-generated `LayerMapping` dictionary for BiomassGroups model
biomassgroups_mapping = {
    'spp_group' : 'SPP_GROUP',
    'spcd' : 'SPCD',
    'family' : 'Family',
    'newgenus' : 'New.Genus',
    'newspecies' : 'New.Species',
    'usfs_wd' : 'USFS_WD',
    'chave_wd' : 'Chave_WD',
    'chavewd_level' : 'ChaveWD_level',
    'code' : 'Code',
    'group' : 'Group',
    'taxa' : 'Taxa',
    'b_0' : 'B_0',
    'b_1' : 'B_1',
    'mindbh' : 'minDBH',
    'maxdbh' : 'maxDBH',
}


"""
I've changed the names in the columns (editted directly the csv to map the names in biomassgroups_mapping (lowercase)).
The file is called biomass.csv
"""
def dataframeRowToModel(pandas_row):
    i,data = pandas_row
    model_i = BiomassGroups.objects.create(**dict(data))
    return model_i



