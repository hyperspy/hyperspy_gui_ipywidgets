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

from hyperspy_gui_ipywidgets.utils import (
    add_display_arg, float2floattext, get_label)

from link_traits import link


def _set_microscope_parameters(obj, **kwargs):
    traits = obj.traits()
    widgets = []
    wdict = {}
    for trait_name in obj.editable_traits():
        if trait_name in ("mapping", "signal"):
            continue
        trait = traits[trait_name]
        widget = float2floattext(
            trait, get_label(trait, trait_name))
        widgets.append(widget)
        wdict[trait_name] = widget.children[1]
        link((obj, trait_name),
             (widget.children[1], "value"))
    store_button = ipywidgets.Button(
        description="Store",
        tooltip="Store the values in metadata")
    store_button.on_click(obj.store)
    wdict["store_button"] = store_button
    container = ipywidgets.VBox([ipywidgets.VBox(widgets), store_button])
    return {
        "widget": container,
        "wdict": wdict}


@add_display_arg
def eels_microscope_parameter_ipy(obj, **kwargs):
    return(_set_microscope_parameters(obj=obj, **kwargs))


@add_display_arg
def eds_sem_microscope_parameter_ipy(obj, **kwargs):
    return(_set_microscope_parameters(obj=obj, **kwargs))


@add_display_arg
def eds_tem_microscope_parameter_ipy(obj, **kwargs):
    return(_set_microscope_parameters(obj=obj, **kwargs))
