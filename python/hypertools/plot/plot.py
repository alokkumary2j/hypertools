#!/usr/bin/env python

"""
Wrapper function that parses plot styling arguments and calls plotting functions

INPUTS:
-numpy array(s)
-list of numpy arrays

OUTPUTS:
-None
"""

##PACKAGES##
from __future__ import division
import sys
import warnings
import re
import itertools
import seaborn as sns
from .._shared.helpers import *
from .static import static_plot
from .animate import animated_plot

##MAIN FUNCTION##
def plot(x,*args,**kwargs):

    ##STYLING##

    # handle point_colors flag
    if 'point_colors' in kwargs:
        point_colors=kwargs['point_colors']
        del kwargs['point_colors']

        if 'color' in kwargs:
            warnings.warn("Using point_colors, color keyword will be ignored.")
            del kwargs['color']

        # if list of lists, unpack
        if any(isinstance(el, list) for el in point_colors):
            point_colors = list(itertools.chain(*point_colors))

        # if all of the elements are numbers, map them to colors
        if all(isinstance(el, int) or isinstance(el, float) for el in point_colors):
            point_colors = vals2bins(point_colors)
        elif all(isinstance(el, str) for el in point_colors):
            point_colors = group_by_category(point_colors)

        categories = list(set(np.sort(point_colors)))
        x_stacked = np.vstack(x)
        x_reshaped = [[] for i in categories]
        for idx,point in enumerate(point_colors):
            x_reshaped[categories.index(point)].append(x_stacked[idx])
        x = [np.vstack(i) for i in x_reshaped]

    if 'style' in kwargs:
        sns.set(style=kwargs['style'])
        del kwargs['style']
    else:
        sns.set(style="whitegrid")

    if 'palette' in kwargs:
        sns.set_palette(palette=kwargs['palette'], n_colors=len(x))
        palette = sns.color_palette(palette=kwargs['palette'], n_colors=len(x))
        del kwargs['palette']
    else:
        sns.set_palette(palette="hls", n_colors=len(x))
        palette=sns.color_palette(palette="hls", n_colors=len(x))

    if 'animate' in kwargs:
        animate=kwargs['animate']
        del kwargs['animate']

        # if animate mode, pass the color palette via kwargs so we can build a legend
        kwargs['color_palette']=palette
        
    else:
        animate=False

    # if x is not a list, make it one
    if type(x) is not list:
        x = [x]

    if animate:
        animated_plot(x,*args,**kwargs)
    else:
        static_plot(x,*args,**kwargs)