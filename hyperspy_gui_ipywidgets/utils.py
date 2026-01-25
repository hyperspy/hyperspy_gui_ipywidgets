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


import functools

import ipywidgets
from traits.api import Undefined
import IPython.display




FORM_ITEM_LAYOUT = ipywidgets.Layout(
    display='flex',
    flex_flow='row',
    justify_content='space-between',
)


def labelme(label, widget):
    if label is Undefined:
        label = ""
    if not isinstance(label, ipywidgets.Label):
        label = ipywidgets.Label(label,
                                 layout=ipywidgets.Layout(width="auto"))
    return ipywidgets.HBox(
        [label, widget],
        layout=FORM_ITEM_LAYOUT,
    )


def labelme_sandwich(label1, widget, label2):
    if label1 is Undefined:
        label1 = ""
    if label2 is Undefined:
        label2 = ""
    if not isinstance(label1, ipywidgets.Label):
        label1 = ipywidgets.Label(label1)
    if not isinstance(label2, ipywidgets.Label):
        label2 = ipywidgets.Label(label2)
    return ipywidgets.HBox(
        [label1, widget, label2],
        layout=FORM_ITEM_LAYOUT)


def get_label(trait, label):
    label = (label.replace("_", " ").capitalize()
             if not trait.label else trait.label)
    return label


def enum2dropdown(trait, description=None, **kwargs):
    widget = ipywidgets.Dropdown(
        options=trait.trait_type.values, **kwargs)
    if description is not None:
        description_tooltip = trait.desc if trait.desc else ""
        widget.description = description
        widget.description_tooltip = description_tooltip
    return widget


def float2floattext(trait, label):
    description_tooltip = trait.desc if trait.desc else ""
    widget = ipywidgets.FloatText()
    widget.description_tooltip = description_tooltip
    return labelme(widget=widget, label=label)


def str2text(trait, label):
    description = trait.desc if trait.desc else ""
    widget = ipywidgets.Text()
    widget.description_tooltip = description
    return labelme(widget=widget, label=label)


def add_display_arg(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        display = kwargs.pop("display", True)
        wdict = f(*args, **kwargs)
        if display:
            IPython.display.display(wdict["widget"])
        else:
            return wdict
    return wrapper


def set_title_container(container, titles):
    """Convenience function to set the title of a container widget, following
    API changes in ipywidget 8.0.

    Parameters
    ----------
    container : ipywidgets accordion, tab or nested tab
        The container onto which the title is added
    titles : list of string
        The list of string to add to the container.

    Returns
    -------
    None.

    """
    try:
        for index, title in enumerate(titles):
            container.set_title(index, title)
    except AttributeError:
        container.titles = tuple(titles)
