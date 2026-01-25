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


import matplotlib
matplotlib.use('agg')

import hyperspy.api as hs

hs.preferences.GUIs.enable_traitsui_gui = False
hs.preferences.GUIs.enable_ipywidgets_gui = True

# Use matplotlib fixture to clean up figure, setup backend, etc.
from matplotlib.testing.conftest import mpl_test_settings  # noqa: F401
