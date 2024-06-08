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
from importlib.metadata import version
from pathlib import Path


__version__ = version("hyperspy_gui_ipywidgets")

# For development version, `setuptools_scm` will be used at build time
# to get the dev version, in case of missing vcs information (git archive,
# shallow repository), the fallback version defined in pyproject.toml will
# be used

# if we have a editable install from a git repository try to use
# `setuptools_scm` to find a more accurate version:
# `importlib.metadata` will provide the version at installation
# time and for editable version this may be different

# we only do that if we have enough git history, e.g. not shallow checkout
_root = Path(__file__).resolve().parents[1]
if (_root / ".git").exists() and not (_root / ".git/shallow").exists():
    try:
        # setuptools_scm may not be installed
        from setuptools_scm import get_version

        __version__ = get_version(_root)
    except ImportError:  # pragma: no cover
        # setuptools_scm not install, we keep the existing __version__
        pass


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
    # lazy loading of module: this is only call when the attribute "name" is not found
    # in the module
    # See https://peps.python.org/pep-0562/
    if name in __all__:
        return importlib.import_module(
            "." + name, 'hyperspy_gui_ipywidgets'
            )
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
