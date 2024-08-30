import numpy as np
import pytest

import hyperspy.api as hs
from hyperspy_gui_ipywidgets.tests.utils import KWARGS
from hyperspy.signal_tools import (
    Signal1DCalibration,
    Signal2DCalibration,
    ImageContrastEditor,
)


class TestTools:

    def setup_method(self, method):
        self.s = hs.signals.Signal1D(1 + np.arange(100)**2)
        self.s.change_dtype('float')
        self.s.axes_manager[0].offset = 10
        self.s.axes_manager[0].scale = 2
        self.s.axes_manager[0].units = "m"

    def test_calibrate(self):
        s = self.s
        cal = Signal1DCalibration(s)
        cal.ss_left_value = 10
        cal.ss_right_value = 30
        wd = cal.gui(**KWARGS)["ipywidgets"]["wdict"]
        wd["new_left"].value = 0
        wd["new_right"].value = 10
        wd["units"].value = "nm"
        wd["apply_button"]._click_handlers(wd["apply_button"])    # Trigger it
        assert s.axes_manager[0].scale == 1
        assert s.axes_manager[0].offset == 0
        assert s.axes_manager[0].units == "nm"

    def test_calibrate_from_s(self):
        s = self.s
        wd = s.calibrate(**KWARGS)["ipywidgets"]["wdict"]
        wd["left"].value = 10
        wd["right"].value = 30
        wd["new_left"].value = 1
        wd["new_right"].value = 11
        wd["units"].value = "nm"
        assert wd["offset"].value == 1
        assert wd["scale"].value == 1
        wd["apply_button"]._click_handlers(wd["apply_button"])    # Trigger it
        assert s.axes_manager[0].scale == 1
        assert s.axes_manager[0].offset == 1
        assert s.axes_manager[0].units == "nm"

    def test_smooth_sg(self):
        s = self.s
        s.add_gaussian_noise(0.1)
        s2 = s.deepcopy()
        wd = s.smooth_savitzky_golay(**KWARGS)["ipywidgets"]["wdict"]
        wd["window_length"].value = 11
        wd["polynomial_order"].value = 5
        wd["differential_order"].value = 1
        wd["color"].value = "red"
        wd["apply_button"]._click_handlers(wd["apply_button"])    # Trigger it
        s2.smooth_savitzky_golay(polynomial_order=5, window_length=11,
                                 differential_order=1)
        np.testing.assert_allclose(s.data, s2.data)

    def test_smooth_lowess(self):
        s = self.s
        s.add_gaussian_noise(0.1)
        s2 = s.deepcopy()
        wd = s.smooth_lowess(**KWARGS)["ipywidgets"]["wdict"]
        wd["smoothing_parameter"].value = 0.9
        wd["number_of_iterations"].value = 3
        wd["color"].value = "red"
        wd["apply_button"]._click_handlers(wd["apply_button"])    # Trigger it
        s2.smooth_lowess(smoothing_parameter=0.9, number_of_iterations=3)
        np.testing.assert_allclose(s.data, s2.data)

    def test_smooth_tv(self):
        s = self.s
        s.add_gaussian_noise(0.1)
        s2 = s.deepcopy()
        wd = s.smooth_tv(**KWARGS)["ipywidgets"]["wdict"]
        wd["smoothing_parameter"].value = 300
        wd["color"].value = "red"
        wd["apply_button"]._click_handlers(wd["apply_button"])    # Trigger it
        s2.smooth_tv(smoothing_parameter=300)
        np.testing.assert_allclose(s.data, s2.data)

    def test_filter_butterworth(self):
        s = self.s
        s.add_gaussian_noise(0.1)
        s2 = s.deepcopy()
        wd = s.filter_butterworth(**KWARGS)["ipywidgets"]["wdict"]
        wd["cutoff"].value = 0.5
        wd["order"].value = 3
        wd["type"].value = "high"
        wd["color"].value = "red"
        wd["apply_button"]._click_handlers(wd["apply_button"])    # Trigger it
        s2.filter_butterworth(
            cutoff_frequency_ratio=0.5,
            order=3,
            type="high")
        np.testing.assert_allclose(s.data, s2.data)

    def test_remove_background(self):
        s = self.s
        s.add_gaussian_noise(0.1)
        s2 = s.remove_background(
            signal_range=(15., 50.),
            background_type='Polynomial',
            polynomial_order=2,
            fast=False,
            zero_fill=True)
        wd = s.remove_background(**KWARGS)["ipywidgets"]["wdict"]
        assert wd["polynomial_order"].layout.display == "none"  # not visible
        wd["background_type"].value = "Polynomial"
        assert wd["polynomial_order"].layout.display == ""  # visible
        wd["polynomial_order"].value = 2
        wd["fast"].value = False
        wd["zero_fill"] = True
        wd["left"].value = 15.
        wd["right"].value = 50.
        wd["apply_button"]._click_handlers(wd["apply_button"])    # Trigger it
        np.testing.assert_allclose(s.data[2:], s2.data[2:], atol=1E-5)
        np.testing.assert_allclose(np.zeros(2), s2.data[:2])

    def test_constrast_editor(self):
        # To get this test to work, matplotlib backend needs to set to 'Agg'
        np.random.seed(1)
        im = hs.signals.Signal2D(np.random.random((32, 32)))
        im.plot()
        ceditor = ImageContrastEditor(im._plot.signal_plot)
        ceditor.ax.figure.canvas.draw_idle()
        wd = ceditor.gui(**KWARGS)["ipywidgets"]["wdict"]
        assert wd["linthresh"].layout.display == "none"  # not visible
        assert wd["linscale"].layout.display == "none"  # not visible
        assert wd["gamma"].layout.display == "none"  # not visible
        wd["bins"].value = 50
        assert ceditor.bins == 50
        wd["norm"].value = 'Log'
        assert ceditor.norm == 'Log'
        assert wd["linthresh"].layout.display == "none"  # not visible
        assert wd["linscale"].layout.display == "none"  # not visible
        wd["norm"].value = 'Symlog'
        assert ceditor.norm == 'Symlog'
        assert wd["linthresh"].layout.display == ""  # visible
        assert wd["linscale"].layout.display == ""  # visible
        assert wd["linthresh"].value == 0.01 # default value
        assert wd["linscale"].value == 0.1 # default value

        wd["linthresh"].value = 0.1
        assert ceditor.linthresh == 0.1
        wd["linscale"].value = 0.2
        assert ceditor.linscale == 0.2


        wd["norm"].value = 'Linear'
        percentile = [1.0, 99.0]
        wd["percentile"].value = percentile
        assert ceditor.vmin_percentile == percentile[0]
        assert ceditor.vmax_percentile == percentile[1]
        assert im._plot.signal_plot.vmin == f'{percentile[0]}th'
        assert im._plot.signal_plot.vmax == f'{percentile[1]}th'

        wd["norm"].value = 'Power'
        assert ceditor.norm == 'Power'
        assert wd["gamma"].layout.display == ""  # visible
        assert wd["gamma"].value == 1.0 # default value
        wd["gamma"].value = 0.1
        assert ceditor.gamma == 0.1

        assert wd["auto"].value is True # default value
        wd["auto"].value = False
        assert ceditor.auto is False

        wd["left"].value = 0.2
        assert ceditor.ss_left_value == 0.2
        wd["right"].value = 0.5
        assert ceditor.ss_right_value == 0.5
        # Setting the span selector programmatically from the widgets will
        # need to be implemented properly
        wd["apply_button"]._click_handlers(wd["apply_button"])    # Trigger it
        # assert im._plot.signal_plot.vmin == 0.2
        # assert im._plot.signal_plot.vmax == 0.5

        # Reset to default values
        wd["reset_button"]._click_handlers(wd["reset_button"])    # Trigger it
        assert im._plot.signal_plot.vmin == '0.0th'
        assert im._plot.signal_plot.vmax == '100.0th'

    def test_eels_table_tool(self):
        exspy = pytest.importorskip("exspy")
        s = exspy.data.EELS_MnFe(True)
        s.plot()
        try:
            # exspy API from 0.3
            # https://github.com/hyperspy/exspy/pull/59
            from exspy import _signal_tools 
        except ImportError:
            from exspy import signal_tools as _signal_tools

        er = _signal_tools.EdgesRange(s)

        er.ss_left_value = 500
        er.ss_right_value = 550

        wd = er.gui(**KWARGS)["ipywidgets"]["wdict"]
        wd["update"]._click_handlers(wd["update"])  # refresh the table
        assert wd["units"].value == 'eV'
        assert wd["left"].value == 500
        assert wd["right"].value == 550
        assert len(wd['gb'].children) == 44 # 9 edges displayed

        wd['major'].value = True
        wd["update"]._click_handlers(wd["update"])  # refresh the table
        assert len(wd['gb'].children) == 24 # 6 edges displayed
        assert wd['gb'].children[4].description == 'Sb_M4'

        wd['order'].value = 'ascending'
        wd["update"]._click_handlers(wd["update"])  # refresh the table
        assert wd['gb'].children[4].description == 'V_L3'

        wd["reset"]._click_handlers(wd["reset"])  # reset the selector
        assert len(wd['gb'].children) == 4 # only header displayed


def test_calibration_2d():
    s = hs.signals.Signal2D(np.zeros((100, 100)))
    cal2d = Signal2DCalibration(s)
    wd = cal2d.gui(**KWARGS)["ipywidgets"]["wdict"]
    cal2d.x0, cal2d.x1, cal2d.y0, cal2d.y1 = 50, 70, 80, 80
    wd["new_length"].value = 10
    wd["units"].value = "mm"
    wd["apply_button"]._click_handlers(wd["apply_button"])
    assert s.axes_manager[0].scale == 0.5
    assert s.axes_manager[1].scale == 0.5
    assert s.axes_manager[0].units == "mm"
    assert s.axes_manager[1].units == "mm"


def test_spikes_removal_tool():
    s = hs.signals.Signal1D(np.ones((2, 3, 30)))
    s.add_gaussian_noise(std=1, random_state=0)

    # The maximum value that we expect after removing a spikes
    max_value_after_spike_removal = 10

    # Add three spikes
    s.data[1, 0, 1] += 40
    s.data[0, 2, 29] += 20
    s.data[1, 2, 14] += 100
    wd = s.spikes_removal_tool(**KWARGS)["ipywidgets"]["wdict"]

    def next():
        wd["next_button"]._click_handlers(wd["next_button"])

    def previous():
        wd["previous_button"]._click_handlers(wd["previous_button"])

    def remove():
        wd["remove_button"]._click_handlers(wd["remove_button"])
    wd["threshold"].value = 25
    next()
    assert s.axes_manager.indices == (0, 1)
    wd["threshold"].value = 15
    assert s.axes_manager.indices == (0, 0)
    next()
    assert s.axes_manager.indices == (2, 0)
    next()
    assert s.axes_manager.indices == (0, 1)
    previous()
    assert s.axes_manager.indices == (2, 0)
    wd["add_noise"].value = False
    remove()
    assert s.data[0, 2, 29] < max_value_after_spike_removal
    assert s.axes_manager.indices == (0, 1)
    remove()
    assert s.data[1, 0, 1] < max_value_after_spike_removal
    assert s.axes_manager.indices == (2, 1)
    np.random.seed(1)
    wd["add_noise"].value = True
    wd["spline_order"].value = 1
    remove()
    assert s.data[1, 2, 14] < max_value_after_spike_removal
    # After going through the whole dataset, come back to (0, 0) position
    assert s.axes_manager.indices == (0, 0)
