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


from numpy.random import random
import pytest

import hyperspy.api as hs
from hyperspy_gui_ipywidgets.tests.utils import KWARGS


exspy = pytest.importorskip("exspy")


class TestSetMicroscopeParameters:

    def setup_method(self, method):
        self.s = hs.signals.Signal1D((2, 3, 4))

    def _perform_t(self, signal_type):
        s = self.s
        s.set_signal_type(signal_type)
        md = s.metadata
        wd = s.set_microscope_parameters(**KWARGS)["ipywidgets"]["wdict"]
        if signal_type == "EELS":
            mapping = exspy.signals.eels.EELSTEMParametersUI.mapping
        elif signal_type == "EDS_SEM":
            mapping = exspy.signals.eds_sem.EDSSEMParametersUI.mapping
        elif signal_type == "EDS_TEM":
            mapping = exspy.signals.eds_tem.EDSTEMParametersUI.mapping
        for key, widget in wd.items():
            if "button" not in key:
                widget.value = random()
        button = wd["store_button"]
        button._click_handlers(button)    # Trigger it
        for item, name in mapping.items():
            assert md.get_item(item) == wd[name].value

    def test_eels(self):
        self._perform_t(signal_type="EELS")

    def test_eds_tem(self):
        self._perform_t(signal_type="EDS_TEM")

    def test_eds_sem(self):
        self._perform_t(signal_type="EDS_SEM")
