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


richness_shp = os.path.abspath(
    os.path.join("external_plugins/iDivSS2017_Group_Project_2/maps/FIA","FIA_Richness_19042017.shp"))

spplist_shp = os.path.abspath(
    os.path.join("external_plugins/iDivSS2017_Group_Project_2/maps/FIA","FIA_SPPLIST_18042017.shp"))

treelevel_shp = os.path.abspath(
    os.path.join("external_plugins/iDivSS2017_Group_Project_2/maps/FIA","FIA_Tree_Level.shp"))

usgrid_shp = os.path.abspath(
    os.path.join("external_plugins/iDivSS2017_Group_Project_2/maps/Basemap/wgs84","USGrid1km.shp"))


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
    
    