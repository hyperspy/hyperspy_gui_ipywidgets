
import ipywidgets
from numpy.random import random, uniform
import pytest

import hyperspy.api as hs
from hyperspy_gui_ipywidgets.tests.utils import KWARGS


module_list = [hs]
try:
    import exspy
    module_list.append(exspy)
except Exception:
    # exspy is not installed
    pass


@pytest.mark.parametrize("module", module_list)
def test_preferences(module):
    wd = module.preferences.gui(**KWARGS)["ipywidgets"]["wdict"]
    for tabkey, tabvalue in wd.items():
        if tabkey.startswith("tab_"):
            for key, value in tabvalue.items():
                assert getattr(
                    getattr(module.preferences, tabkey[4:]), key) == value.value
                value_bk = value.value
                if isinstance(value, ipywidgets.Checkbox):
                    value.value = not value
                elif isinstance(value, ipywidgets.FloatText):
                    value.value = random()
                elif isinstance(value, ipywidgets.Text):
                    value.value = "qwerty"
                elif isinstance(value, ipywidgets.FloatSlider):
                    value.value = uniform(low=value.min, high=value.max)
                elif isinstance(value, ipywidgets.Dropdown):
                    options = set(value.options) - set(value.value)
                    value.value = options.pop()
                assert getattr(
                    getattr(module.preferences, tabkey[4:]), key) == value.value
                value.value = value_bk
