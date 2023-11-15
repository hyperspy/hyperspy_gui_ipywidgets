# -*- coding: utf-8 -*-
# Copyright 2007-2021 The HyperSpy developers
#
# This file is part of  HyperSpy.
#
#  HyperSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#  HyperSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with  HyperSpy.  If not, see <http://www.gnu.org/licenses/>.


import importlib
from pathlib import Path


if Path(__file__).parent.parent.name == "site-packages":  # pragma: no cover
    # Tested in the "Package & Test" workflow on GitHub CI
    from importlib.metadata import version

    __version__ = version("hyperspy_gui_ipywidgets")
else:
    # Editable install
    from setuptools_scm import get_version

    __version__ = get_version(Path(__file__).parent.parent)


__all__ = [
    'axes',
    'microscope_parameters',
    'model',
    'preferences',
    'roi',
    'tools',
    '__version__',
    ]


def __dir__():
    return sorted(__all__)


def __getattr__(name):
    if name in __all__:
        if name == "__version__":
            return __version__
        else:
            return importlib.import_module(
                "." + name, 'hyperspy_gui_ipywidgets'
                )
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
