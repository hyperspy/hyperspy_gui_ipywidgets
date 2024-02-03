import matplotlib
matplotlib.use('agg')

import hyperspy.api as hs

hs.preferences.GUIs.enable_traitsui_gui = False
hs.preferences.GUIs.enable_ipywidgets_gui = True

# Use matplotlib fixture to clean up figure, setup backend, etc.
from matplotlib.testing.conftest import mpl_test_settings  # noqa: F401
