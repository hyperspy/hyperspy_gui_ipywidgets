import ipywidgets
import traits.api as t

from link_traits import link
from hyperspy.signal_tools import (SPIKES_REMOVAL_INSTRUCTIONS,
                                   IMAGE_CONTRAST_EDITOR_HELP_IPYWIDGETS)

from hyperspy_gui_ipywidgets.utils import (labelme, enum2dropdown,
        add_display_arg, set_title_container)
from hyperspy_gui_ipywidgets.custom_widgets import OddIntSlider
from hyperspy_gui_ipywidgets.axes import get_ipy_navigation_sliders


@add_display_arg
def interactive_range_ipy(obj, **kwargs):
    # Define widgets
    wdict = {}
    axis = obj.axis
    left = ipywidgets.FloatText(disabled=True)
    right = ipywidgets.FloatText(disabled=True)
    units = ipywidgets.Label()
    help_text = ipywidgets.HTML(
        "Click on the signal figure and drag to the right to select a signal "
        "range. Press `Apply` to perform the operation or `Close` to cancel.",)
    help = ipywidgets.Accordion(children=[help_text], selected_index=None)
    set_title_container(help, ["Help"])
    close = ipywidgets.Button(
        description="Close",
        tooltip="Close widget and remove span selector from the signal figure.")
    apply = ipywidgets.Button(
        description="Apply",
        tooltip="Perform the operation using the selected range.")
    wdict["left"] = left
    wdict["right"] = right
    wdict["units"] = units
    wdict["help_text"] = help_text
    wdict["close_button"] = close
    wdict["apply_button"] = apply

    # Connect
    link((obj, "ss_left_value"), (left, "value"))
    link((obj, "ss_right_value"), (right, "value"))
    link((axis, "units"), (units, "value"))

    def on_apply_clicked(b):
        if obj.ss_left_value != obj.ss_right_value:
            obj.span_selector_switch(False)
            for method, cls in obj.on_close:
                method(cls, obj.ss_left_value, obj.ss_right_value)
            obj.span_selector_switch(True)
    apply.on_click(on_apply_clicked)

    box = ipywidgets.VBox([
        ipywidgets.HBox([left, units, ipywidgets.Label("-"), right, units]),
        help,
        ipywidgets.HBox((apply, close))
    ])

    def on_close_clicked(b):
        obj.span_selector_switch(False)
        box.close()
    close.on_click(on_close_clicked)
    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def calibrate2d_ipy(obj, **kwargs):
    # Define widgets
    wdict = {}
    length = ipywidgets.FloatText(disabled=True, description="Current length")
    scale = ipywidgets.FloatText(disabled=True, description="Scale")
    new_length = ipywidgets.FloatText(disabled=False, description="New length")
    units = ipywidgets.Text(description="Units")
    unitsl = ipywidgets.Label(layout=ipywidgets.Layout(width="10%"))
    help_text = ipywidgets.HTML(
        "Click on the signal figure and drag line to some feature with a "
        "known size. Set the new length, then press `Apply` to update both "
        "the x- and y-dimensions in the signal, or press `Close` to cancel. "
        "The units can also be set with `Units`"
    )
    wdict["help_text"] = help_text
    help = ipywidgets.Accordion(children=[help_text], selected_index=None)
    set_title_container(help, ["Help"])
    close = ipywidgets.Button(
        description="Close",
        tooltip="Close widget and remove line from the signal figure.",
    )
    apply = ipywidgets.Button(
        description="Apply", tooltip="Set the x- and y-scaling with the `scale` value."
    )

    # Connect
    link((obj, "length"), (length, "value"))
    link((obj, "new_length"), (new_length, "value"))
    link((obj, "units"), (units, "value"))
    link((obj, "units"), (unitsl, "value"))
    link((obj, "scale"), (scale, "value"))

    def on_apply_clicked(b):
        obj.apply()
        obj.on = False
        box.close()

    apply.on_click(on_apply_clicked)

    box = ipywidgets.VBox(
        [
            ipywidgets.HBox([new_length, unitsl]),
            length,
            scale,
            units,
            help,
            ipywidgets.HBox((apply, close)),
        ]
    )

    def on_close_clicked(b):
        obj.on = False
        box.close()

    close.on_click(on_close_clicked)

    wdict["length"] = length
    wdict["scale"] = scale
    wdict["new_length"] = new_length
    wdict["units"] = units
    wdict["close_button"] = close
    wdict["apply_button"] = apply

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def calibrate_ipy(obj, **kwargs):
    # Define widgets
    wdict = {}
    left = ipywidgets.FloatText(disabled=True, description="Left")
    right = ipywidgets.FloatText(disabled=True, description="Right")
    offset = ipywidgets.FloatText(disabled=True, description="Offset")
    scale = ipywidgets.FloatText(disabled=True, description="Scale")
    new_left = ipywidgets.FloatText(disabled=False, description="New left")
    new_right = ipywidgets.FloatText(disabled=False, description="New right")
    units = ipywidgets.Text(description="Units")
    unitsl = ipywidgets.Label(layout=ipywidgets.Layout(width="10%"))
    help_text = ipywidgets.HTML(
        "Click on the signal figure and drag to the right to select a signal "
        "range. Set the new left and right values and press `Apply` to update "
        "the calibration of the axis with the new values or press "
        " `Close` to cancel.",)
    wdict["help_text"] = help_text
    help = ipywidgets.Accordion(children=[help_text], selected_index=None)
    set_title_container(help, ["Help"])
    close = ipywidgets.Button(
        description="Close",
        tooltip="Close widget and remove span selector from the signal figure.",
    )
    apply = ipywidgets.Button(
        description="Apply",
        tooltip="Set the axis calibration with the `offset` and `scale` values above.",
    )

    # Connect
    link((obj, "ss_left_value"), (left, "value"))
    link((obj, "ss_right_value"), (right, "value"))
    link((obj, "left_value"), (new_left, "value"))
    link((obj, "right_value"), (new_right, "value"))
    link((obj, "units"), (units, "value"))
    link((obj, "units"), (unitsl, "value"))
    link((obj, "offset"), (offset, "value"))
    link((obj, "scale"), (scale, "value"))

    def on_apply_clicked(b):
        if (new_left.value, new_right.value) != (0, 0):
            # traitlets does not support undefined, therefore we need to makes
            # sure that the values are updated in the obj if they make sense
            if new_left.value == 0 and obj.left_value is t.Undefined:
                obj.left_value = 0
            elif new_right.value == 0 and obj.right_value is t.Undefined:
                obj.right_value = 0
            # This is the default value, we need to update
        obj.apply()

    apply.on_click(on_apply_clicked)

    box = ipywidgets.VBox(
        [
            ipywidgets.HBox([new_left, unitsl]),
            ipywidgets.HBox([new_right, unitsl]),
            ipywidgets.HBox([left, unitsl]),
            ipywidgets.HBox([right, unitsl]),
            ipywidgets.HBox([offset, unitsl]),
            scale,
            units,
            help,
            ipywidgets.HBox((apply, close)),
        ]
    )

    def on_close_clicked(b):
        obj.span_selector_switch(False)
        box.close()

    close.on_click(on_close_clicked)

    wdict["left"] = left
    wdict["right"] = right
    wdict["offset"] = offset
    wdict["scale"] = scale
    wdict["new_left"] = new_left
    wdict["new_right"] = new_right
    wdict["units"] = units
    wdict["close_button"] = close
    wdict["apply_button"] = apply

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def print_edges_table_ipy(obj, **kwargs):
    # Define widgets
    wdict = {}
    axis = obj.axis
    style_d = {'description_width': 'initial'}
    layout_d = {'width': '50%'}
    left = ipywidgets.FloatText(disabled=True, layout={'width': '25%'})
    right = ipywidgets.FloatText(disabled=True, layout={'width': '25%'})
    units = ipywidgets.Label(style=style_d)
    major = ipywidgets.Checkbox(value=False, description='Only major edge',
                                indent=False, layout=layout_d)
    complmt = ipywidgets.Checkbox(value=False, description='Complementary edge',
                                 indent=False, layout=layout_d)
    order = ipywidgets.Dropdown(options=['closest', 'ascending', 'descending'],
                                value='closest',
                                description='Sort energy by: ',
                                disabled=False,
                                style=style_d
                                )
    update = ipywidgets.Button(description='Refresh table', layout={'width': 'initial'})
    gb = ipywidgets.GridBox(layout=ipywidgets.Layout(
            grid_template_columns="70px 125px 75px 250px"))
    help_text = ipywidgets.HTML(
        "Click on the signal figure and drag to the right to select a signal "
        "range. Drag the rectangle or change its border to display edges in "
        "different signal range. Select edges to show their positions "
        "on the signal.",)
    help = ipywidgets.Accordion(children=[help_text], selected_index=None)
    set_title_container(help, ["Help"])
    close = ipywidgets.Button(description="Close", tooltip="Close the widget.")
    reset = ipywidgets.Button(description="Reset",
                              tooltip="Reset the span selector.")

    header = ('<p style="padding-left: 1em; padding-right: 1em; '
              'text-align: center; vertical-align: top; '
              'font-weight:bold">{}</p>')
    entry = ('<p style="padding-left: 1em; padding-right: 1em; '
             'text-align: center; vertical-align: top">{}</p>')

    wdict["left"] = left
    wdict["right"] = right
    wdict["units"] = units
    wdict["help"] = help
    wdict["major"] = major
    wdict["update"] = update
    wdict["complmt"] = complmt
    wdict["order"] = order
    wdict["gb"] = gb
    wdict["reset"] = reset
    wdict["close"] = close

    # Connect
    link((obj, "ss_left_value"), (left, "value"))
    link((obj, "ss_right_value"), (right, "value"))
    link((axis, "units"), (units, "value"))
    link((obj, "only_major"), (major, "value"))
    link((obj, "complementary"), (complmt, "value"))
    link((obj, "order"), (order, "value"))

    def update_table(change):
        edges, energy, relevance, description = obj.update_table()

        # header
        items = [ipywidgets.HTML(header.format('edge')),
                 ipywidgets.HTML(header.format('onset energy (eV)')),
                 ipywidgets.HTML(header.format('relevance')),
                 ipywidgets.HTML(header.format('description'))]

        # rows
        obj.btns = []
        for k, edge in enumerate(edges):
            if edge in obj.active_edges or \
                edge in obj.active_complementary_edges:
                btn_state = True
            else:
                btn_state = False

            btn = ipywidgets.ToggleButton(value=btn_state,
                                          description=edge,
                                          layout=ipywidgets.Layout(width='70px'))
            btn.observe(obj.update_active_edge,  names='value')
            obj.btns.append(btn)

            wenergy = ipywidgets.HTML(entry.format(str(energy[k])))
            wrelv = ipywidgets.HTML(entry.format(str(relevance[k])))
            wdes = ipywidgets.HTML(entry.format(str(description[k])))
            items.extend([btn, wenergy, wrelv, wdes])

        gb.children = items
    update.on_click(update_table)
    major.observe(update_table)

    def on_complementary_toggled(change):
        obj.update_table()
        obj.check_btn_state()
    complmt.observe(on_complementary_toggled)

    def on_order_changed(change):
        obj._get_edges_info_within_energy_axis()
        update_table(change)
    order.observe(on_order_changed)

    def on_close_clicked(b):
        obj.span_selector_switch(False)
        box.close()
    close.on_click(on_close_clicked)

    def on_reset_clicked(b):
        # ss_left_value is linked with left.value, this can prevent cyclic
        # referencing
        obj._clear_markers()
        obj.span_selector_switch(False)
        left.value = 0
        right.value = 0
        obj.span_selector_switch(True)
        update_table(b)
    reset.on_click(on_reset_clicked)

    energy_box = ipywidgets.HBox([left, units, ipywidgets.Label("-"), right,
                                   units])
    check_box = ipywidgets.HBox([major, complmt])
    control_box = ipywidgets.VBox([energy_box, update, order, check_box])

    box = ipywidgets.VBox([
        ipywidgets.HBox([gb, control_box]),
        help,
        ipywidgets.HBox([reset, close]),
    ])

    return {
        "widget": box,
        "wdict": wdict,
    }

@add_display_arg
def smooth_savitzky_golay_ipy(obj, **kwargs):
    wdict = {}
    window_length = OddIntSlider(
        value=3, step=2, min=3, max=max(int(obj.axis.size * 0.25), 3))
    polynomial_order = ipywidgets.IntSlider(value=3, min=1,
                                            max=window_length.value - 1)
    # Polynomial order must be less than window length

    def update_bound(change):
        polynomial_order.max = change.new - 1
    window_length.observe(update_bound, "value")
    differential_order = ipywidgets.IntSlider(value=0, min=0, max=10)
    color = ipywidgets.ColorPicker()
    close = ipywidgets.Button(
        description="Close",
        tooltip="Close widget and remove the smoothed line from the signal figure.")
    apply = ipywidgets.Button(
        description="Apply",
        tooltip="Perform the operation using the selected range.")
    link((obj, "polynomial_order"), (polynomial_order, "value"))
    link((obj, "window_length"), (window_length, "value"))
    link((obj, "differential_order"),
         (differential_order, "value"))
    # Differential order must be less or equal to polynomial_order
    link((polynomial_order, "value"),
         (differential_order, "max"))
    link((obj, "line_color_ipy"), (color, "value"))
    box = ipywidgets.VBox([
        labelme("Window length", window_length),
        labelme("polynomial order", polynomial_order),
        labelme("Differential order", differential_order),
        labelme("Color", color),
        ipywidgets.HBox((apply, close))
    ])

    wdict["window_length"] = window_length
    wdict["polynomial_order"] = polynomial_order
    wdict["differential_order"] = differential_order
    wdict["color"] = color
    wdict["close_button"] = close
    wdict["apply_button"] = apply

    def on_apply_clicked(b):
        obj.apply()
    apply.on_click(on_apply_clicked)

    def on_close_clicked(b):
        obj.close()
        box.close()
    close.on_click(on_close_clicked)
    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def smooth_lowess_ipy(obj, **kwargs):
    wdict = {}
    smoothing_parameter = ipywidgets.FloatSlider(min=0, max=1)
    number_of_iterations = ipywidgets.IntText()
    color = ipywidgets.ColorPicker()
    close = ipywidgets.Button(
        description="Close",
        tooltip="Close widget and remove the smoothed line from the signal figure.")
    apply = ipywidgets.Button(
        description="Apply",
        tooltip="Perform the operation using the selected range.")
    link((obj, "smoothing_parameter"),
         (smoothing_parameter, "value"))
    link((obj, "number_of_iterations"),
         (number_of_iterations, "value"))
    link((obj, "line_color_ipy"), (color, "value"))
    box = ipywidgets.VBox([
        labelme("Smoothing parameter", smoothing_parameter),
        labelme("Number of iterations", number_of_iterations),
        labelme("Color", color),
        ipywidgets.HBox((apply, close))
    ])
    wdict["smoothing_parameter"] = smoothing_parameter
    wdict["number_of_iterations"] = number_of_iterations
    wdict["color"] = color
    wdict["close_button"] = close
    wdict["apply_button"] = apply

    def on_apply_clicked(b):
        obj.apply()
    apply.on_click(on_apply_clicked)

    def on_close_clicked(b):
        obj.close()
        box.close()
    close.on_click(on_close_clicked)
    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def smooth_tv_ipy(obj, **kwargs):
    wdict = {}
    smoothing_parameter = ipywidgets.FloatSlider(min=0.1, max=1000)
    smoothing_parameter_max = ipywidgets.FloatText(
        value=smoothing_parameter.max)
    color = ipywidgets.ColorPicker()
    close = ipywidgets.Button(
        description="Close",
        tooltip="Close widget and remove the smoothed line from the signal figure.")
    apply = ipywidgets.Button(
        description="Apply",
        tooltip="Perform the operation using the selected range.")
    link((obj, "smoothing_parameter"),
         (smoothing_parameter, "value"))
    link((smoothing_parameter_max, "value"),
         (smoothing_parameter, "max"))
    link((obj, "line_color_ipy"), (color, "value"))
    wdict["smoothing_parameter"] = smoothing_parameter
    wdict["smoothing_parameter_max"] = smoothing_parameter_max
    wdict["color"] = color
    wdict["close_button"] = close
    wdict["apply_button"] = apply
    box = ipywidgets.VBox([
        labelme("Weight", smoothing_parameter),
        labelme("Weight max", smoothing_parameter_max),
        labelme("Color", color),
        ipywidgets.HBox((apply, close))
    ])

    def on_apply_clicked(b):
        obj.apply()
    apply.on_click(on_apply_clicked)

    def on_close_clicked(b):
        obj.close()
        box.close()
    close.on_click(on_close_clicked)
    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def smooth_butterworth(obj, **kwargs):
    wdict = {}
    cutoff = ipywidgets.FloatSlider(min=0.01, max=1.)
    order = ipywidgets.IntText()
    type_ = ipywidgets.Dropdown(options=("low", "high"))
    color = ipywidgets.ColorPicker()
    close = ipywidgets.Button(
        description="Close",
        tooltip="Close widget and remove the smoothed line from the signal figure.")
    apply = ipywidgets.Button(
        description="Apply",
        tooltip="Perform the operation using the selected range.")
    link((obj, "cutoff_frequency_ratio"), (cutoff, "value"))
    link((obj, "type"), (type_, "value"))
    link((obj, "order"), (order, "value"))
    wdict["cutoff"] = cutoff
    wdict["order"] = order
    wdict["type"] = type_
    wdict["color"] = color
    wdict["close_button"] = close
    wdict["apply_button"] = apply
    box = ipywidgets.VBox([
        labelme("Cutoff frequency ration", cutoff),
        labelme("Type", type_),
        labelme("Order", order),
        ipywidgets.HBox((apply, close))
    ])

    def on_apply_clicked(b):
        obj.apply()
    apply.on_click(on_apply_clicked)

    def on_close_clicked(b):
        obj.close()
        box.close()
    close.on_click(on_close_clicked)
    return {
        "widget": box,
        "wdict": wdict,
    }

@add_display_arg
def image_constast_editor_ipy(obj, **kwargs):
    wdict = {}
    left = ipywidgets.FloatText(disabled=True, description="Vmin")
    right = ipywidgets.FloatText(disabled=True, description="Vmax")
    bins = ipywidgets.IntText(description="Bins")
    norm = ipywidgets.Dropdown(options=("Linear", "Power", "Log", "Symlog"),
                               description="Norm",
                               value=obj.norm)
    percentile = ipywidgets.FloatRangeSlider(value=[0.0, 100.0],
                                             min=0.0, max=100.0, step=0.1,
                                             description="Vmin/vmax percentile",
                                             readout_format='.1f')
    gamma = ipywidgets.FloatSlider(1.0, min=0.1, max=3.0, description="Gamma")
    linthresh = ipywidgets.FloatSlider(0.01, min=0.001, max=1.0, step=0.001,
                                       description="Linear threshold")
    linscale = ipywidgets.FloatSlider(0.1, min=0.001, max=10.0, step=0.001,
                                      description="Linear scale")
    auto = ipywidgets.Checkbox(True, description="Auto")
    help_text = ipywidgets.HTML(IMAGE_CONTRAST_EDITOR_HELP_IPYWIDGETS)
    wdict["help_text"] = help_text
    help = ipywidgets.Accordion(children=[help_text], selected_index=None)
    set_title_container(help, ["Help"])
    close = ipywidgets.Button(
        description="Close",
        tooltip="Close widget.")
    apply = ipywidgets.Button(
        description="Apply",
        tooltip="Use the selected range to re-calculate the histogram.")
    reset = ipywidgets.Button(
        description="Reset",
        tooltip="Reset the settings to their initial values.")
    wdict["left"] = left
    wdict["right"] = right
    wdict["bins"] = bins
    wdict["norm"] = norm
    wdict["percentile"] = percentile
    wdict["gamma"] = gamma
    wdict["linthresh"] = linthresh
    wdict["linscale"] = linscale
    wdict["auto"] = auto
    wdict["close_button"] = close
    wdict["apply_button"] = apply
    wdict["reset_button"] = reset

    def transform_vmin(value):
        return (value, percentile.upper)

    def transform_vmin_inv(value):
        return value[0]

    def transform_vmax(value):
        return (percentile.lower, value)

    def transform_vmax_inv(value):
        return value[1]

    # Connect
    link((obj, "ss_left_value"), (left, "value"))
    link((obj, "ss_right_value"), (right, "value"))
    link((obj, "bins"), (bins, "value"))
    link((obj, "norm"), (norm, "value"))
    link((obj, "vmin_percentile"), (percentile, "value"),
         (transform_vmin, transform_vmin_inv))
    link((obj, "vmax_percentile"), (percentile, "value"),
         (transform_vmax, transform_vmax_inv))
    link((obj, "gamma"), (gamma, "value"))
    link((obj, "linthresh"), (linthresh, "value"))
    link((obj, "linscale"), (linscale, "value"))
    link((obj, "auto"), (auto, "value"))

    def display_parameters(change):
        # Necessary for the initialisation
        v = change if isinstance(change, str) else change.new
        if v == "Symlog":
            linthresh.layout.display = ""
            linscale.layout.display = ""
        else:
            linthresh.layout.display = "none"
            linscale.layout.display = "none"
        if v == "Power":
            gamma.layout.display = ""
        else:
            gamma.layout.display = "none"
    display_parameters(obj.norm)
    norm.observe(display_parameters, "value")

    def disable_parameters(change):
        # Necessary for the initialisation
        v = change if isinstance(change, bool) else change.new
        percentile.disabled = not v

    disable_parameters(obj.auto)
    auto.observe(disable_parameters, "value")

    def on_apply_clicked(b):
        obj.apply()
    apply.on_click(on_apply_clicked)

    def on_reset_clicked(b):
        obj.reset()
    reset.on_click(on_reset_clicked)

    box = ipywidgets.VBox([left,
                           right,
                           auto,
                           percentile,
                           bins,
                           norm,
                           gamma,
                           linthresh,
                           linscale,
                           help,
                           ipywidgets.HBox((apply, reset, close)),
                           ])

    def on_close_clicked(b):
        obj.close()
        box.close()
    close.on_click(on_close_clicked)
    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def remove_background_ipy(obj, **kwargs):
    wdict = {}
    left = ipywidgets.FloatText(disabled=True, description="Left")
    right = ipywidgets.FloatText(disabled=True, description="Right")
    red_chisq = ipywidgets.FloatText(disabled=True, description="red-χ²")
    link((obj, "ss_left_value"), (left, "value"))
    link((obj, "ss_right_value"), (right, "value"))
    link((obj, "red_chisq"), (red_chisq, "value"))
    fast = ipywidgets.Checkbox(description="Fast")
    zero_fill = ipywidgets.Checkbox(description="Zero Fill")
    help_text = ipywidgets.HTML(
        "Click on the signal figure and drag to the right to select a "
        "range. Press `Apply` to remove the background in the whole dataset. "
        "If \"Fast\" is checked, the background parameters are estimated "
        "using a fast (analytical) method that can compromise accuracy. "
        "When unchecked, non-linear least squares is employed instead. "
        "If \"Zero Fill\" is checked, all the channels prior to the fitting "
        "region will be set to zero. "
        "Otherwise the background subtraction will be performed in the "
        "pre-fitting region as well.",)
    wdict["help_text"] = help_text
    help = ipywidgets.Accordion(children=[help_text], selected_index=None)
    set_title_container(help, ["Help"])
    close = ipywidgets.Button(
        description="Close",
        tooltip="Close widget and remove span selector from the signal figure.")
    apply = ipywidgets.Button(
        description="Apply",
        tooltip="Remove the background in the whole dataset.")

    polynomial_order = ipywidgets.IntText(description="Polynomial order")
    background_type = enum2dropdown(obj.traits()["background_type"])
    background_type.description = "Background type"

    def enable_poly_order(change):
        if change.new == "Polynomial":
            polynomial_order.layout.display = ""
        else:
            polynomial_order.layout.display = "none"
    background_type.observe(enable_poly_order, "value")
    link((obj, "background_type"), (background_type, "value"))
    # Trigger the function that controls the visibility of poly order as
    # setting the default value doesn't trigger it.

    class Dummy:
        new = background_type.value
    enable_poly_order(change=Dummy())
    link((obj, "polynomial_order"), (polynomial_order, "value"))
    link((obj, "fast"), (fast, "value"))
    link((obj, "zero_fill"), (zero_fill, "value"))
    wdict["left"] = left
    wdict["right"] = right
    wdict["red_chisq"] = red_chisq
    wdict["fast"] = fast
    wdict["zero_fill"] = zero_fill
    wdict["polynomial_order"] = polynomial_order
    wdict["background_type"] = background_type
    wdict["apply_button"] = apply
    box = ipywidgets.VBox([
        left, right, red_chisq,
        background_type,
        polynomial_order,
        fast,
        zero_fill,
        help,
        ipywidgets.HBox((apply, close)),
    ])

    def on_apply_clicked(b):
        obj.apply()
        obj.span_selector_switch(False)
        box.close()
    apply.on_click(on_apply_clicked)

    def on_close_clicked(b):
        obj.span_selector_switch(False)
        box.close()
    close.on_click(on_close_clicked)
    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def spikes_removal_ipy(obj, **kwargs):
    wdict = {}
    threshold = ipywidgets.FloatText()
    add_noise = ipywidgets.Checkbox()
    default_spike_width = ipywidgets.IntText()
    spline_order = ipywidgets.IntSlider(min=1, max=10)
    progress_bar = ipywidgets.IntProgress(max=len(obj.coordinates) - 1)
    help_text = ipywidgets.HTML(
        value=SPIKES_REMOVAL_INSTRUCTIONS.replace('\n', '<br/>'))
    help = ipywidgets.Accordion(children=[help_text], selected_index=None)
    set_title_container(help, ["Help"])

    show_diff = ipywidgets.Button(
        description="Show derivative histogram",
        tooltip="This figure is useful to estimate the threshold.",
        layout=ipywidgets.Layout(width="auto"))
    close = ipywidgets.Button(
        description="Close",
        tooltip="Close widget and remove span selector from the signal figure.")
    next = ipywidgets.Button(
        description="Find next",
        tooltip="Find next spike")
    previous = ipywidgets.Button(
        description="Find previous",
        tooltip="Find previous spike")
    remove = ipywidgets.Button(
        description="Remove spike",
        tooltip="Remove spike and find next one.")
    wdict["threshold"] = threshold
    wdict["add_noise"] = add_noise
    wdict["default_spike_width"] = default_spike_width
    wdict["spline_order"] = spline_order
    wdict["progress_bar"] = progress_bar
    wdict["show_diff_button"] = show_diff
    wdict["close_button"] = close
    wdict["next_button"] = next
    wdict["previous_button"] = previous
    wdict["remove_button"] = remove

    def on_show_diff_clicked(b):
        obj._show_derivative_histogram_fired()
    show_diff.on_click(on_show_diff_clicked)

    def on_next_clicked(b):
        obj.find()
    next.on_click(on_next_clicked)

    def on_previous_clicked(b):
        obj.find(back=True)
    previous.on_click(on_previous_clicked)

    def on_remove_clicked(b):
        obj.apply()
    remove.on_click(on_remove_clicked)
    labeled_spline_order = labelme("Spline order", spline_order)

    link((obj, "threshold"), (threshold, "value"))
    link((obj, "add_noise"), (add_noise, "value"))
    link((obj, "default_spike_width"),
         (default_spike_width, "value"))
    link((obj, "spline_order"), (spline_order, "value"))
    link((obj, "index"), (progress_bar, "value"))
    # Trigger the function that controls the visibility  as
    # setting the default value doesn't trigger it.

    advanced = ipywidgets.Accordion((
        ipywidgets.VBox([
            labelme("Add noise", add_noise),
            labelme("Default spike width", default_spike_width),
            labelme("Spline order", spline_order), ]),))

    set_title_container(advanced, ["Advanced settings"])

    box = ipywidgets.VBox([
        ipywidgets.VBox([
            show_diff,
            labelme("Threshold", threshold),
            labelme("Progress", progress_bar), ]),
        advanced,
        help,
        ipywidgets.HBox([previous, next, remove, close])
    ])

    def on_close_clicked(b):
        obj.span_selector_switch(False)
        box.close()
    close.on_click(on_close_clicked)
    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def find_peaks2D_ipy(obj, **kwargs):
    wdict = {}
    # Define widgets
    # For "local max" method
    local_max_distance = ipywidgets.IntSlider(min=1, max=20, value=3)
    local_max_threshold = ipywidgets.FloatSlider(min=0, max=20, value=10)
    # For "max" method
    max_alpha = ipywidgets.FloatSlider(min=0, max=6, value=3)
    max_distance = ipywidgets.IntSlider(min=1, max=20, value=10)
    # For "minmax" method
    minmax_distance = ipywidgets.FloatSlider(min=0, max=6, value=3)
    minmax_threshold = ipywidgets.FloatSlider(min=0, max=20, value=10)
    # For "Zaefferer" method
    zaefferer_grad_threshold = ipywidgets.FloatSlider(min=0, max=0.2,
                                                      value=0.1, step=0.2*1E-1)
    zaefferer_window_size = ipywidgets.IntSlider(min=2, max=80, value=40)
    zaefferer_distance_cutoff = ipywidgets.FloatSlider(min=0, max=100, value=50)
    # For "stat" method
    stat_alpha = ipywidgets.FloatSlider(min=0, max=2, value=1)
    stat_window_radius = ipywidgets.IntSlider(min=5, max=20, value=10)
    stat_convergence_ratio = ipywidgets.FloatSlider(min=0, max=0.1, value=0.05)
    # For "Laplacian of Gaussians" method
    log_min_sigma = ipywidgets.FloatSlider(min=0, max=2, value=1)
    log_max_sigma = ipywidgets.FloatSlider(min=0, max=100, value=50)
    log_num_sigma = ipywidgets.FloatSlider(min=0, max=20, value=10)
    log_threshold = ipywidgets.FloatSlider(min=0, max=0.4, value=0.2)
    log_overlap = ipywidgets.FloatSlider(min=0, max=1, value=0.5)
    log_log_scale = ipywidgets.Checkbox()
    # For "Difference of Gaussians" method
    dog_min_sigma = ipywidgets.FloatSlider(min=0, max=2, value=1)
    dog_max_sigma = ipywidgets.FloatSlider(min=0, max=100, value=50)
    dog_sigma_ratio = ipywidgets.FloatSlider(min=0, max=3.2, value=1.6)
    dog_threshold = ipywidgets.FloatSlider(min=0, max=0.4, value=0.2)
    dog_overlap = ipywidgets.FloatSlider(min=0, max=1, value=0.5)
    # For "Cross correlation" method
    xc_distance = ipywidgets.FloatSlider(min=0, max=10., value=5.)
    xc_threshold = ipywidgets.FloatSlider(min=0, max=2., value=0.5)

    wdict["local_max_distance"] = local_max_distance
    wdict["local_max_threshold"] = local_max_threshold
    wdict["max_alpha"] = max_alpha
    wdict["max_distance"] = max_distance
    wdict["minmax_distance"] = minmax_distance
    wdict["minmax_threshold"] = minmax_threshold
    wdict["zaefferer_grad_threshold"] = zaefferer_grad_threshold
    wdict["zaefferer_window_size"] = zaefferer_window_size
    wdict["zaefferer_distance_cutoff"] = zaefferer_distance_cutoff
    wdict["stat_alpha"] = stat_alpha
    wdict["stat_window_radius"] = stat_window_radius
    wdict["stat_convergence_ratio"] = stat_convergence_ratio
    wdict["log_min_sigma"] = log_min_sigma
    wdict["log_max_sigma"] = log_max_sigma
    wdict["log_num_sigma"] = log_num_sigma
    wdict["log_threshold"] = log_threshold
    wdict["log_overlap"] = log_overlap
    wdict["log_log_scale"] = log_log_scale
    wdict["dog_min_sigma"] = dog_min_sigma
    wdict["dog_max_sigma"] = dog_max_sigma
    wdict["dog_sigma_ratio"] = dog_sigma_ratio
    wdict["dog_threshold"] = dog_threshold
    wdict["dog_overlap"] = dog_overlap
    wdict["xc_distance"] = xc_distance
    wdict["xc_threshold"] = xc_threshold

    # Connect
    link((obj, "local_max_distance"), (local_max_distance, "value"))
    link((obj, "local_max_threshold"), (local_max_threshold, "value"))
    link((obj, "max_alpha"), (max_alpha, "value"))
    link((obj, "max_distance"), (max_distance, "value"))
    link((obj, "minmax_distance"), (minmax_distance, "value"))
    link((obj, "minmax_threshold"), (minmax_threshold, "value"))
    link((obj, "zaefferer_grad_threshold"), (zaefferer_grad_threshold, "value"))
    link((obj, "zaefferer_window_size"), (zaefferer_window_size, "value"))
    link((obj, "zaefferer_distance_cutoff"), (zaefferer_distance_cutoff, "value"))
    link((obj, "stat_alpha"), (stat_alpha, "value"))
    link((obj, "stat_window_radius"), (stat_window_radius, "value"))
    link((obj, "stat_convergence_ratio"), (stat_convergence_ratio, "value"))
    link((obj, "log_min_sigma"), (log_min_sigma, "value"))
    link((obj, "log_max_sigma"), (log_max_sigma, "value"))
    link((obj, "log_num_sigma"), (log_num_sigma, "value"))
    link((obj, "log_threshold"), (log_threshold, "value"))
    link((obj, "log_overlap"), (log_overlap, "value"))
    link((obj, "log_log_scale"), (log_log_scale, "value"))
    link((obj, "dog_min_sigma"), (dog_min_sigma, "value"))
    link((obj, "dog_max_sigma"), (dog_max_sigma, "value"))
    link((obj, "dog_sigma_ratio"), (dog_sigma_ratio, "value"))
    link((obj, "dog_threshold"), (dog_threshold, "value"))
    link((obj, "dog_overlap"), (dog_overlap, "value"))
    link((obj, "xc_distance"), (xc_distance, "value"))
    link((obj, "xc_threshold"), (xc_threshold, "value"))

    close = ipywidgets.Button(
        description="Close",
        tooltip="Close widget and close figure.")
    compute = ipywidgets.Button(
        description="Compute over navigation axes.",
        tooltip="Find the peaks by iterating over the navigation axes.")

    box_local_max = ipywidgets.VBox([
            labelme("Distance", local_max_distance),
            labelme("Threshold", local_max_threshold),
            ])
    box_max = ipywidgets.VBox([#max_alpha, max_distance
            labelme("Alpha", max_alpha),
            labelme("Distance", max_distance),
            ])
    box_minmax = ipywidgets.VBox([
            labelme("Distance", minmax_distance),
            labelme("Threshold", minmax_threshold),
            ])
    box_zaefferer = ipywidgets.VBox([
            labelme("Gradient threshold", zaefferer_grad_threshold),
            labelme("Window size", zaefferer_window_size),
            labelme("Distance cutoff", zaefferer_distance_cutoff),
            ])
    box_stat = ipywidgets.VBox([
            labelme("Alpha", stat_alpha),
            labelme("Radius", stat_window_radius),
            labelme("Convergence ratio", stat_convergence_ratio),
            ])
    box_log = ipywidgets.VBox([
            labelme("Min sigma", log_min_sigma),
            labelme("Max sigma",  log_max_sigma),
            labelme("Num sigma", log_num_sigma),
            labelme("Threshold", log_threshold),
            labelme("Overlap", log_overlap),
            labelme("Log scale", log_log_scale),
            ])
    box_dog = ipywidgets.VBox([
            labelme("Min sigma", dog_min_sigma),
            labelme("Max sigma", dog_max_sigma),
            labelme("Sigma ratio", dog_sigma_ratio),
            labelme("Threshold", dog_threshold),
            labelme("Overlap", dog_overlap),
            ])
    box_xc = ipywidgets.VBox([
            labelme("Distance", xc_distance),
            labelme("Threshold", xc_threshold),
            ])

    box_dict = {"Local Max": box_local_max,
                "Max": box_max,
                "Minmax": box_minmax,
                "Zaefferer": box_zaefferer,
                "Stat": box_stat,
                "Laplacian of Gaussians": box_log,
                "Difference of Gaussians": box_dog,
                "Template matching": box_xc}

    method = enum2dropdown(obj.traits()["method"])
    def update_method_parameters(change):
        # Remove all parameters vbox widgets
        for item, value in box_dict.items():
            value.layout.display = "none"
        if change.new == "Local max":
            box_local_max.layout.display = ""
        elif change.new == "Max":
            box_max.layout.display = ""
        elif change.new == "Minmax":
            box_minmax.layout.display = ""
        elif change.new == "Zaefferer":
            box_zaefferer.layout.display = ""
        elif change.new == "Stat":
            box_stat.layout.display = ""
        elif change.new == "Laplacian of Gaussians":
            box_log.layout.display = ""
        elif change.new == "Difference of Gaussians":
            box_dog.layout.display = ""
        elif change.new == "Template matching":
            box_xc.layout.display = ""

    method.observe(update_method_parameters, "value")
    link((obj, "method"), (method, "value"))

    # Trigger the function that controls the visibility  as
    # setting the default value doesn't trigger it.
    class Dummy:
        new = method.value
    update_method_parameters(change=Dummy())

    widgets_list = []

    if obj.show_navigation_sliders:
        nav_widget = get_ipy_navigation_sliders(
                obj.signal.axes_manager.navigation_axes,
                in_accordion=True,
                random_position_button=True)
        widgets_list.append(nav_widget['widget'])
        wdict.update(nav_widget['wdict'])

    l = [labelme("Method", method)]
    l.extend([value for item, value in box_dict.items()])
    method_parameters = ipywidgets.Accordion((ipywidgets.VBox(l), ))
    set_title_container(method_parameters, ["Method parameters"])

    widgets_list.extend([method_parameters,
                         ipywidgets.HBox([compute, close])])
    box = ipywidgets.VBox(widgets_list)

    def on_compute_clicked(b):
        obj.compute_navigation()
        obj.signal._plot.close()
        obj.close()
        box.close()
    compute.on_click(on_compute_clicked)

    def on_close_clicked(b):
        obj.signal._plot.close()
        obj.close()
        box.close()
    close.on_click(on_close_clicked)
    return {
        "widget": box,
        "wdict": wdict,
    }
