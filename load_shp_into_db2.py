#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
# This script is for importing the shapefiles into the Biospytial GU container.
## Usage: First make migrations and migrate
## In the shell (outside Biospytial do:)
1. (Biospytial)$ python manage.py makemigrations
2. (Biospytial)$ python manage.py migrate
3. (Biospytial)$ python manage.py shell
-- Now inside the shell
from external_plugins.DjangoFIA import load_shp_into_db
load_shp_into_db.run()
"""
import os
from django.contrib.gis.utils import LayerMapping
from .models import Richness,richness_mapping,Spplist,spplist_mapping,TreeLevel,treelevel_mapping,USGrid100km,usgrid100km_mapping
from .models import TreesPerYear, treesperyear_mapping, SppNProduct, sppnproduct_mapping,BiomassGroups,biomassgroups_mapping, dataframeRowToModel



old_maps ="external_plugins/iDivSS2017_Group_Project_2/maps/FIA"
new_maps = "/inputs/FIA/newData"
base_map = "/apps/external_plugins/iDivStuff/maps/Basemap/wgs84"

richness_shp = os.path.abspath(
    os.path.join(old_maps,"FIA_Richness_19042017.shp"))

spplist_shp = os.path.abspath(
    os.path.join(old_maps,"FIA_SPPLIST_18042017.shp"))

treelevel_shp = os.path.abspath(
    os.path.join(old_maps,"FIA_Tree_Level.shp"))

usgrid_shp = os.path.abspath(
    os.path.join(base_map,"USGrid1km.shp"))

treesperyear_shp = os.path.abspath(
    os.path.join(new_maps,"FIA_Trees_perYear_CLEAN.shp"))

sppnprod_shp = os.path.abspath(
    os.path.join(new_maps,"FIA_SppN_Productivity_CLEAN.shp"))

biomassgroups_csv = os.path.abspath(
    os.path.join(new_maps,"biomass.csv"))



def run(verbose=True):
    richness = LayerMapping(
        Richness, richness_shp, richness_mapping,
        transform=False,
    )
    richness.save(strict=True, verbose=verbose)
    
    spplist = LayerMapping(
        Spplist, spplist_shp, spplist_mapping,
        transform=False,
    )
    spplist.save(strict=True, verbose=verbose)
    
    treelevel = LayerMapping(
        TreeLevel, treelevel_shp, treelevel_mapping,
        transform=False,
    )
    treelevel.save(strict=True, verbose=verbose)
    

def run_mesh(verbose=True):
    mesh = LayerMapping(
        USGrid100km, usgrid_shp ,usgrid100km_mapping,
        transform=False,
        )
    mesh.save(strict=True, verbose=verbose)
    
def run_new_data(verbose=True):
    spplist = LayerMapping(
        SppNProduct, sppnprod_shp, sppnproduct_mapping,
        transform=False,
    )
    spplist.save(strict=True, verbose=verbose)
    
    treelevel = LayerMapping(
        TreesPerYear, treesperyear_shp ,treesperyear_mapping,
        transform=False,
    )
    treelevel.save(strict=True, verbose=verbose)
 
def run_biomassgroup(verbose=True):
    import pandas as pd
    data = pd.read_csv(biomassgroups_csv)
    iterdat = data.iterrows()
    objects = map(lambda row :  dataframeRowToModel(row), iterdat)
    return objects
