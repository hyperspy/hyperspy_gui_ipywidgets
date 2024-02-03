import traits
import ipywidgets

from link_traits import link
from hyperspy_gui_ipywidgets.utils import (
    labelme, add_display_arg, float2floattext, get_label, str2text,
    set_title_container
    )


def bool2checkbox(trait, label):
    description_tooltip = trait.desc if trait.desc else ""
    widget = ipywidgets.Checkbox()
    widget.description_tooltip = description_tooltip
    return labelme(widget=widget, label=label)


def directory2unicode(trait, label):
    description_tooltip = trait.desc if trait.desc else ""
    widget = ipywidgets.Text()
    widget.description_tooltip = description_tooltip
    return labelme(widget=widget, label=label)


def enum2dropdown(trait, label):
    widget = ipywidgets.Dropdown(
        options=trait.trait_type.values)
    return labelme(widget=widget, label=label)


def range2floatrangeslider(trait, label):
    description_tooltip = trait.desc if trait.desc else ""
    widget = ipywidgets.FloatSlider(
        min=trait.trait_type._low,
        max=trait.trait_type._high,
        description_tooltip=description_tooltip,)
    return labelme(widget=widget, label=label)


# Trait types must be converted to the appropriate ipywidget
TRAITS2IPYWIDGETS = {
    traits.trait_types.CBool: bool2checkbox,
    traits.trait_types.Bool: bool2checkbox,
    traits.trait_types.CFloat: float2floattext,
    traits.trait_types.Directory: directory2unicode,
    traits.trait_types.File: directory2unicode,
    traits.trait_types.Range: range2floatrangeslider,
    traits.trait_types.Enum: enum2dropdown,
    traits.trait_types.Str: str2text,
}


@add_display_arg
def show_preferences_widget(obj, **kwargs):
    ipytabs = {}
    wdict = {}
    for tab in obj.editable_traits():
        tabdict = {}
        wdict["tab_{}".format(tab)] = tabdict
        ipytab = []
        tabtraits = getattr(obj, tab).traits()
        for trait_name in getattr(obj, tab).editable_traits():
            trait = tabtraits[trait_name]
            widget = TRAITS2IPYWIDGETS[type(trait.trait_type)](
                trait, get_label(trait, trait_name))
            ipytab.append(widget)
            tabdict[trait_name] = widget.children[1]
            link((getattr(obj, tab), trait_name),
                 (widget.children[1], "value"))
        ipytabs[tab] = ipywidgets.VBox(ipytab)
    # This defines the order of the tab in the widget
    titles = ["General", "GUIs", "Plot"]
    ipytabs_ = ipywidgets.Tab(
        children=[ipytabs[title] for title in titles])
    set_title_container(ipytabs_, titles)
    save_button = ipywidgets.Button(
        description="Save",
        tooltip="Make changes permanent")
    wdict["save_button"] = save_button

    def on_button_clicked(b):
        obj.save()

    save_button.on_click(on_button_clicked)

    container = ipywidgets.VBox([ipytabs_, save_button])
    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def show_exspy_preferences_widget(obj, **kwargs):
    ipytabs = {}
    wdict = {}
    for tab in obj.editable_traits():
        tabdict = {}
        wdict["tab_{}".format(tab)] = tabdict
        ipytab = []
        tabtraits = getattr(obj, tab).traits()
        for trait_name in getattr(obj, tab).editable_traits():
            trait = tabtraits[trait_name]
            widget = TRAITS2IPYWIDGETS[type(trait.trait_type)](
                trait, get_label(trait, trait_name))
            ipytab.append(widget)
            tabdict[trait_name] = widget.children[1]
            link((getattr(obj, tab), trait_name),
                 (widget.children[1], "value"))
        ipytabs[tab] = ipywidgets.VBox(ipytab)
    # This defines the order of the tab in the widget
    titles = ["EELS", "EDS"]
    ipytabs_ = ipywidgets.Tab(
        children=[ipytabs[title] for title in titles])
    set_title_container(ipytabs_, titles)
    save_button = ipywidgets.Button(
        description="Save",
        tooltip="Make changes permanent")
    wdict["save_button"] = save_button

    def on_button_clicked(b):
        obj.save()

    save_button.on_click(on_button_clicked)

    container = ipywidgets.VBox([ipytabs_, save_button])
    return {
        "widget": container,
        "wdict": wdict,
    }
