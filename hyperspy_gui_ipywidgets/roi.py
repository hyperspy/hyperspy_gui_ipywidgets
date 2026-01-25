# -*- coding: utf-8 -*-
# Copyright 2007-2026 The HyperSpy developers
#
# This file is part of  HyperSpy.
#
# HyperSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HyperSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with  HyperSpy.  If not, see <http://www.gnu.org/licenses/#GPL>.


import ipywidgets
import traitlets

from hyperspy_gui_ipywidgets.utils import (
    labelme, labelme_sandwich, enum2dropdown, add_display_arg, )
from link_traits import link


@add_display_arg
def span_roi_ipy(obj, **kwargs):
    wdict = {}
    left = ipywidgets.FloatText(description="Left")
    right = ipywidgets.FloatText(description="Right")
    link((obj, "left"), (left, "value"))
    link((obj, "right"), (right, "value"))
    wdict["left"] = left
    wdict["right"] = right
    container = ipywidgets.HBox([left, right])
    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def point1d_roi_ipy(obj, **kwargs):
    wdict = {}
    value = ipywidgets.FloatText(description="value")
    wdict["value"] = value
    link((obj, "value"), (value, "value"))
    return {
        "widget": value,
        "wdict": wdict,
    }


@add_display_arg
def point_2d_ipy(obj, **kwargs):
    wdict = {}
    x = ipywidgets.FloatText(description="x")
    y = ipywidgets.FloatText(description="y")
    wdict["x"] = x
    wdict["y"] = y
    link((obj, "x"), (x, "value"))
    link((obj, "y"), (y, "value"))
    container = ipywidgets.HBox([x, y])
    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def rectangular_roi_ipy(obj, **kwargs):
    wdict = {}
    left = ipywidgets.FloatText(description="left")
    right = ipywidgets.FloatText(description="right")
    link((obj, "left"), (left, "value"))
    link((obj, "right"), (right, "value"))
    container1 = ipywidgets.HBox([left, right])
    top = ipywidgets.FloatText(description="top")
    bottom = ipywidgets.FloatText(description="bottom")
    link((obj, "top"), (top, "value"))
    link((obj, "bottom"), (bottom, "value"))
    container2 = ipywidgets.HBox([top, bottom])
    container = ipywidgets.VBox([container1, container2])
    wdict["left"] = left
    wdict["right"] = right
    wdict["top"] = top
    wdict["bottom"] = bottom
    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def circle_roi_ipy(obj, **kwargs):
    wdict = {}
    x = ipywidgets.FloatText(description="x")
    y = ipywidgets.FloatText(description="y")
    link((obj, "cx"), (x, "value"))
    link((obj, "cy"), (y, "value"))
    container1 = ipywidgets.HBox([x, y])
    radius = ipywidgets.FloatText(description="radius")
    inner_radius = ipywidgets.FloatText(description="inner_radius")
    link((obj, "r"), (radius, "value"))
    link((obj, "r_inner"), (inner_radius, "value"))
    container2 = ipywidgets.HBox([radius, inner_radius])
    container = ipywidgets.VBox([container1, container2])
    wdict["cx"] = x
    wdict["cy"] = y
    wdict["radius"] = radius
    wdict["inner_radius"] = inner_radius
    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def line2d_roi_ipy(obj, **kwargs):
    wdict = {}
    x1 = ipywidgets.FloatText(description="x1")
    y1 = ipywidgets.FloatText(description="x2")
    link((obj, "x1"), (x1, "value"))
    link((obj, "y1"), (y1, "value"))
    container1 = ipywidgets.HBox([x1, y1])
    x2 = ipywidgets.FloatText(description="x2")
    y2 = ipywidgets.FloatText(description="y2")
    link((obj, "x2"), (x2, "value"))
    link((obj, "y2"), (y2, "value"))
    container2 = ipywidgets.HBox([x2, y2])
    linewidth = ipywidgets.FloatText(description="linewidth")
    link((obj, "linewidth"), (linewidth, "value"))
    container = ipywidgets.VBox([container1, container2, linewidth])
    wdict["x1"] = x1
    wdict["x2"] = x2
    wdict["y1"] = y1
    wdict["y2"] = y2
    wdict["linewidth"] = linewidth
    return {
        "widget": container,
        "wdict": wdict,
    }
