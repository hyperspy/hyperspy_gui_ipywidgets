import numpy as np
import pytest

import hyperspy.api as hs
from hyperspy_gui_ipywidgets.tests.utils import KWARGS


def check_axis_attributes(axes_manager, widgets_dict, index, attributes):
    for attribute in attributes:
        assert (widgets_dict["axis{}".format(index)][attribute].value ==
                getattr(axes_manager[index], attribute))


class TestAxes:

    def setup_method(self, method):
        self.s = hs.signals.Signal1D(np.empty((2, 3, 4)))
        am = self.s.axes_manager
        am[0].scale = 0.5
        am[0].name = "a"
        am[0].units = "eV"
        am[1].scale = 1000
        am[1].name = "b"
        am[1].units = "meters"
        am[2].scale = 5
        am[2].name = "c"
        am[2].units = "e"
        am.indices = (2, 1)

    def test_navigation_sliders(self):
        s = self.s
        am = self.s.axes_manager
        wd = s.axes_manager.gui_navigation_sliders(
            **KWARGS)["ipywidgets"]["wdict"]
        check_axis_attributes(axes_manager=am, widgets_dict=wd, index=0,
                              attributes=("value", "index", "units"))
        check_axis_attributes(axes_manager=am, widgets_dict=wd, index=1,
                              attributes=("value", "index", "units"))
        wd["axis0"]["value"].value = 1.5
        am[0].units = "cm"
        check_axis_attributes(axes_manager=am, widgets_dict=wd, index=0,
                              attributes=("value", "index", "units"))

    def test_axes_manager_gui(self):
        s = self.s
        am = self.s.axes_manager
        wd = s.axes_manager.gui(**KWARGS)["ipywidgets"]["wdict"]
        check_axis_attributes(axes_manager=am, widgets_dict=wd, index=0,
                              attributes=("value", "index", "units",
                                          "index_in_array", "name",
                                          "size", "scale", "offset"))
        check_axis_attributes(axes_manager=am, widgets_dict=wd, index=1,
                              attributes=("value", "index", "units",
                                          "index_in_array", "name", "size",
                                          "scale", "offset"))
        check_axis_attributes(axes_manager=am, widgets_dict=wd, index=2,
                              attributes=("units", "index_in_array",
                                          "name", "size", "scale",
                                          "offset"))
        wd["axis0"]["value"].value = 1.5
        wd["axis0"]["name"].name = "parrot"
        wd["axis0"]["offset"].name = -1
        wd["axis0"]["scale"].name = 1e-10
        wd["axis0"]["units"].value = "cm"
        check_axis_attributes(axes_manager=am, widgets_dict=wd, index=0,
                              attributes=("value", "index", "units",
                                          "index_in_array", "name",
                                          "size", "scale", "offset"))

def test_non_uniform_axes():
    try:
        from hyperspy.axes import UniformDataAxis
    except ImportError:
        pytest.skip("HyperSpy version doesn't support non-uniform axis")

    dict0 = {'scale': 1.0, 'size': 2, }
    dict1 = {'expression': 'a / (x+b)', 'a': 1240, 'b': 1, 'size': 3,
             'name': 'plumage', 'units': 'beautiful'}
    dict2 = {'axis': np.arange(4), 'name': 'norwegianblue', 'units': 'ex'}
    dict3 = {'expression': 'a / (x+b)', 'a': 1240, 'b': 1, 'x': dict2,
             'name': 'pushing up', 'units': 'the daisies'}
    s = hs.signals.Signal1D(np.empty((3, 2, 4, 4)), axes=[dict0, dict1, dict2, dict3])
    s.axes_manager[0].navigate = False

    am = s.axes_manager
    wd = s.axes_manager.gui(**KWARGS)["ipywidgets"]["wdict"]
    check_axis_attributes(axes_manager=am, widgets_dict=wd, index=0,
                          attributes=("name", "units", "size", "index",
                                      "value", "index_in_array",))
    check_axis_attributes(axes_manager=am, widgets_dict=wd, index=2,
                          attributes=("name", "units", "size",
                                      "index_in_array"))
    check_axis_attributes(axes_manager=am, widgets_dict=wd, index=3,
                          attributes=("name", "units", "size",
                                      "index_in_array"))
    wd2 = s.axes_manager.gui_navigation_sliders(
            **KWARGS)["ipywidgets"]["wdict"]
    check_axis_attributes(axes_manager=am, widgets_dict=wd, index=0,
                          attributes=("name", "units", "size", "index",
                                      "value", "index_in_array",))
    check_axis_attributes(axes_manager=am, widgets_dict=wd, index=2,
                          attributes=("name", "units", "size",
                                      "index_in_array"))
    check_axis_attributes(axes_manager=am, widgets_dict=wd, index=3,
                          attributes=("name", "units", "size",
                                      "index_in_array"))
