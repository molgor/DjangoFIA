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


import scipy.stats as st


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