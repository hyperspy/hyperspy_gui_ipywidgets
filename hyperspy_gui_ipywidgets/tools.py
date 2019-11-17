import ipywidgets
import traits.api as t

from hyperspy_gui_ipywidgets.utils import (labelme, enum2dropdown, 
        add_display_arg)
from link_traits import link
from hyperspy_gui_ipywidgets.custom_widgets import OddIntSlider
from hyperspy.signal_tools import (SPIKES_REMOVAL_INSTRUCTIONS,
                                   IMAGE_CONTRAST_EDITOR_HELP)


@add_display_arg
def interactive_range_ipy(obj, **kwargs):
    # Define widgets
    wdict = {}
    axis = obj.axis
    left = ipywidgets.FloatText(disabled=True)
    right = ipywidgets.FloatText(disabled=True)
    units = ipywidgets.Label()
    help = ipywidgets.HTML(
        "Click on the signal figure and drag to the right to select a signal "
        "range. Press `Apply` to perform the operation or `Close` to cancel.",)
    help = ipywidgets.Accordion(children=[help])
    help.set_title(0, "Help")
    close = ipywidgets.Button(
        description="Close",
        tooltip="Close widget and remove span selector from the signal figure.")
    apply = ipywidgets.Button(
        description="Apply",
        tooltip="Perform the operation using the selected range.")
    wdict["left"] = left
    wdict["right"] = right
    wdict["units"] = units
    wdict["help"] = help
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
def calibrate_ipy(obj, **kwargs):
    # Define widgets
    wdict = {}
    axis = obj.axis
    left = ipywidgets.FloatText(disabled=True, description="Left")
    right = ipywidgets.FloatText(disabled=True, description="Right")
    offset = ipywidgets.FloatText(disabled=True, description="Offset")
    scale = ipywidgets.FloatText(disabled=True, description="Scale")
    new_left = ipywidgets.FloatText(disabled=False, description="New left")
    new_right = ipywidgets.FloatText(disabled=False, description="New right")
    units = ipywidgets.Text(description="Units", )
    unitsl = ipywidgets.Label(layout=ipywidgets.Layout(width="10%"))
    help = ipywidgets.HTML(
        "Click on the signal figure and drag to the right to select a signal "
        "range. Set the new left and right values and press `Apply` to update "
        "the calibration of the axis with the new values or press "
        " `Close` to cancel.",)
    wdict["help"] = help
    help = ipywidgets.Accordion(children=[help])
    help.set_title(0, "Help")
    close = ipywidgets.Button(
        description="Close",
        tooltip="Close widget and remove span selector from the signal figure.")
    apply = ipywidgets.Button(
        description="Apply",
        tooltip="Set the axis calibration with the `offset` and `scale` values "
        "above.")

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

    box = ipywidgets.VBox([
        ipywidgets.HBox([new_left, unitsl]),
        ipywidgets.HBox([new_right, unitsl]),
        ipywidgets.HBox([left, unitsl]),
        ipywidgets.HBox([right, unitsl]),
        ipywidgets.HBox([offset, unitsl]),
        scale,
        units,
        help,
        ipywidgets.HBox((apply, close))
    ])

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
    left = ipywidgets.FloatText(disabled=True, description="Min")
    right = ipywidgets.FloatText(disabled=True, description="Max")
    bins = ipywidgets.IntText(description="Bins")
    norm = ipywidgets.Dropdown(options=("Linear", "Power", "Log", "Symlog"),
                               description="Norm",
                               value=obj.norm)
    saturated_pixels = ipywidgets.FloatSlider(0.05, min=0.0, max=5.0,
                                              description="Saturated pixels")
    gamma = ipywidgets.FloatSlider(1.0, min=0.1, max=3.0, description="Gamma")
    linthresh = ipywidgets.FloatSlider(0.01, min=0.001, max=1.0, step=0.001,
                                       description="Linear threshold")
    linscale = ipywidgets.FloatSlider(0.1, min=0.001, max=10.0, step=0.001,
                                      description="Linear scale")
    auto = ipywidgets.Checkbox(True, description="Auto")
    help = ipywidgets.HTML(IMAGE_CONTRAST_EDITOR_HELP)
    wdict["help"] = help
    help = ipywidgets.Accordion(children=[help], selected_index=None)
    help.set_title(0, "Help")
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
    wdict["saturated_pixels"] = saturated_pixels
    wdict["gamma"] = gamma
    wdict["linthresh"] = linthresh
    wdict["linscale"] = linscale
    wdict["auto"] = auto
    wdict["close_button"] = close
    wdict["apply_button"] = apply
    wdict["reset_button"] = reset

    # Connect
    link((obj, "ss_left_value"), (left, "value"))
    link((obj, "ss_right_value"), (right, "value"))
    link((obj, "bins"), (bins, "value"))
    link((obj, "norm"), (norm, "value"))
    link((obj, "saturated_pixels"), (saturated_pixels, "value"))
    link((obj, "gamma"), (gamma, "value"))
    link((obj, "linthresh"), (linthresh, "value"))
    link((obj, "linscale"), (linscale, "value"))
    link((obj, "auto"), (auto, "value"))

    def enable_parameters(change):
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
    enable_parameters(obj.norm)
    norm.observe(enable_parameters, "value")

    def on_apply_clicked(b):
        obj.apply()
    apply.on_click(on_apply_clicked)

    def on_reset_clicked(b):
        obj.reset()
    reset.on_click(on_reset_clicked)

    box = ipywidgets.VBox([left,
                           right,
                           bins,
                           norm,
                           saturated_pixels,
                           gamma,
                           linthresh,
                           linscale,
                           auto,
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
    link((obj, "ss_left_value"), (left, "value"))
    link((obj, "ss_right_value"), (right, "value"))
    fast = ipywidgets.Checkbox(description="Fast")
    zero_fill = ipywidgets.Checkbox(description="Zero Fill")
    help = ipywidgets.HTML(
        "Click on the signal figure and drag to the right to select a "
        "range. Press `Apply` to remove the background in the whole dataset. "
        "If \"Fast\" is checked, the background parameters are estimated "
        "using a fast (analytical) method that can compromise accuracy. "
        "When unchecked, non-linear least squares is employed instead. "
        "If \"Zero Fill\" is checked, all the channels prior to the fitting "
        "region will be set to zero. "
        "Otherwise the background subtraction will be performed in the "
        "pre-fitting region as well.",)
    wdict["help"] = help
    help = ipywidgets.Accordion(children=[help])
    help.set_title(0, "Help")
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
    wdict["fast"] = fast
    wdict["zero_fill"] = zero_fill
    wdict["polynomial_order"] = polynomial_order
    wdict["background_type"] = background_type
    wdict["apply_button"] = apply
    box = ipywidgets.VBox([
        left, right,
        background_type,
        polynomial_order,
        fast,
        zero_fill,
        help,
        ipywidgets.HBox((apply, close)),
    ])

    def on_apply_clicked(b):
        obj.apply()
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
    interpolator_kind = enum2dropdown(obj.traits()["interpolator_kind"])
    spline_order = ipywidgets.IntSlider(min=1, max=10)
    progress_bar = ipywidgets.IntProgress(max=len(obj.coordinates) - 1)
    help = ipywidgets.HTML(
        value=SPIKES_REMOVAL_INSTRUCTIONS.replace('\n', '<br/>'))
    help = ipywidgets.Accordion(children=[help])
    help.set_title(0, "Help")

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
    wdict["interpolator_kind"] = interpolator_kind
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

    def enable_interpolator_kind(change):
        if change.new == "Spline":
            for child in labeled_spline_order.children:
                child.layout.display = ""
        else:
            for child in labeled_spline_order.children:
                child.layout.display = "none"
    interpolator_kind.observe(enable_interpolator_kind, "value")
    link((obj, "interpolator_kind"),
         (interpolator_kind, "value"))
    link((obj, "threshold"), (threshold, "value"))
    link((obj, "add_noise"), (add_noise, "value"))
    link((obj, "default_spike_width"),
         (default_spike_width, "value"))
    link((obj, "spline_order"), (spline_order, "value"))
    link((obj, "index"), (progress_bar, "value"))
    # Trigger the function that controls the visibility  as
    # setting the default value doesn't trigger it.

    class Dummy:
        new = interpolator_kind.value
    enable_interpolator_kind(change=Dummy())
    advanced = ipywidgets.Accordion((
        ipywidgets.VBox([
            labelme("Add noise", add_noise),
            labelme("Interpolator kind", interpolator_kind),
            labelme("Default spike width", default_spike_width),
            labelme("Spline order", spline_order), ]),))

    advanced.set_title(0, "Advanced settings")
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
