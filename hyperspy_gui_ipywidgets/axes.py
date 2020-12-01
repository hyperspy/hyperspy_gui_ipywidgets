import ipywidgets
import numpy as np

from hyperspy_gui_ipywidgets.utils import (
    labelme, add_display_arg)
from link_traits import link


@add_display_arg
def ipy_navigation_sliders(obj, **kwargs):
    return get_ipy_navigation_sliders(obj, **kwargs)


def get_ipy_navigation_sliders(obj, in_accordion=False,
                               random_position_button=False,
                               **kwargs):
    continuous_update = ipywidgets.Checkbox(True,
                                            description="Continous update")
    wdict = {}
    wdict["continuous_update"] = continuous_update
    widgets = []
    for i, axis in enumerate(obj):
        axis_dict = {}
        wdict["axis{}".format(i)] = axis_dict
        iwidget = ipywidgets.IntSlider(
            min=0,
            max=axis.size - 1,
            readout=True,
            description="index"
        )
        link((continuous_update, "value"),
             (iwidget, "continuous_update"))
        link((axis, "index"), (iwidget, "value"))
        vwidget = ipywidgets.BoundedFloatText(
            min=axis.low_value,
            max=axis.high_value,
            step=axis.scale,
            description="value"
            # readout_format=".lf"
        )
        link((continuous_update, "value"),
             (vwidget, "continuous_update"))
        link((axis, "value"), (vwidget, "value"))
        link((axis, "high_value"), (vwidget, "max"))
        link((axis, "low_value"), (vwidget, "min"))
        link((axis, "scale"), (vwidget, "step"))
        name = ipywidgets.Label(str(axis),
                                layout=ipywidgets.Layout(width="15%"))
        units = ipywidgets.Label(layout=ipywidgets.Layout(width="5%"))
        link((axis, "name"), (name, "value"))
        link((axis, "units"), (units, "value"))
        bothw = ipywidgets.HBox([name, iwidget, vwidget, units])
        # labeled_widget = labelme(str(axis), bothw)
        widgets.append(bothw)
        axis_dict["value"] = vwidget
        axis_dict["index"] = iwidget
        axis_dict["units"] = units

    if random_position_button:
        random_nav_position = ipywidgets.Button(
            description="Set random navigation position.",
            tooltip="Set random navigation position, useful to check the "
                     "method paramters.",
            layout=ipywidgets.Layout(width="auto"))

        def _random_navigation_position_fired(b):
            am = obj[0].axes_manager
            index = np.random.randint(0, am._max_index)
            am.indices = np.unravel_index(index, 
                tuple(am._navigation_shape_in_array))[::-1]
        random_nav_position.on_click(_random_navigation_position_fired)

        wdict["random_nav_position_button"] = random_nav_position
        widgets.append(random_nav_position)

    widgets.append(continuous_update)
    box = ipywidgets.VBox(widgets)
    if in_accordion:
        box = ipywidgets.Accordion((box,))
        box.set_title(0, "Navigation sliders")
    return {"widget": box, "wdict": wdict}


@add_display_arg
def _get_axis_widgets(obj):
    widgets = []
    wd = {}
    name = ipywidgets.Text()
    widgets.append(labelme(ipywidgets.Label("Name"), name))
    link((obj, "name"), (name, "value"))
    wd["name"] = name

    size = ipywidgets.IntText(disabled=True)
    widgets.append(labelme("Size", size))
    link((obj, "size"), (size, "value"))
    wd["size"] = size

    index_in_array = ipywidgets.IntText(disabled=True)
    widgets.append(labelme("Index in array", index_in_array))
    link((obj, "index_in_array"), (index_in_array, "value"))
    wd["index_in_array"] = index_in_array
    if obj.navigate:
        index = ipywidgets.IntSlider(min=0, max=obj.size - 1)
        widgets.append(labelme("Index", index))
        link((obj, "index"), (index, "value"))
        wd["index"] = index

        value = ipywidgets.FloatSlider(
            min=obj.low_value,
            max=obj.high_value,
        )
        wd["value"] = value
        widgets.append(labelme("Value", value))
        link((obj, "value"), (value, "value"))
        link((obj, "high_value"), (value, "max"))
        link((obj, "low_value"), (value, "min"))
        link((obj, "scale"), (value, "step"))

    units = ipywidgets.Text()
    widgets.append(labelme("Units", units))
    link((obj, "units"), (units, "value"))
    wd["units"] = units

    if hasattr(obj, "scale"):
        scale = ipywidgets.FloatText()
        widgets.append(labelme("Scale", scale))
        link((obj, "scale"), (scale, "value"))
        wd["scale"] = scale

    if hasattr(obj, "offset"):
        offset = ipywidgets.FloatText()
        widgets.append(labelme("Offset", offset))
        link((obj, "offset"), (offset, "value"))
        wd["offset"] = offset
        
    if "_expression" in obj.__dict__.keys():
        expression = ipywidgets.Text(disabled=True)
        widgets.append(labelme("Expression", expression))
        link((obj, "_expression"), (expression, "value"))
        wd["expression"] = expression

    return {
        "widget": ipywidgets.VBox(widgets),
        "wdict": wd
    }


@add_display_arg
def ipy_axes_gui(obj, **kwargs):
    wdict = {}
    nav_widgets = []
    sig_widgets = []
    i = 0
    for axis in obj.navigation_axes:
        wd = _get_axis_widgets(axis, display=False)
        nav_widgets.append(wd["widget"])
        wdict["axis{}".format(i)] = wd["wdict"]
        i += 1
    for j, axis in enumerate(obj.signal_axes):
        wd = _get_axis_widgets(axis, display=False)
        sig_widgets.append(wd["widget"])
        wdict["axis{}".format(i + j)] = wd["wdict"]
    nav_accordion = ipywidgets.Accordion(nav_widgets)
    sig_accordion = ipywidgets.Accordion(sig_widgets)
    i = 0  # For when there is not navigation axes
    for i in range(obj.navigation_dimension):
        nav_accordion.set_title(i, "Axis %i" % i)
    for j in range(obj.signal_dimension):
        sig_accordion.set_title(j, "Axis %i" % (i + j + 1))
    tabs = ipywidgets.HBox([nav_accordion, sig_accordion])
    return {
        "widget": tabs,
        "wdict": wdict,
    }
