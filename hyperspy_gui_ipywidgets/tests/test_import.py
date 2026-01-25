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


def test_import_version():
    from hyperspy_gui_ipywidgets import __version__


def test_import():
    import hyperspy_gui_ipywidgets
    for obj_name in hyperspy_gui_ipywidgets.__all__:
        getattr(hyperspy_gui_ipywidgets, obj_name)


def test_import_import_error():
    import hyperspy_gui_ipywidgets
    try:
        hyperspy_gui_ipywidgets.inexisting_module
    except AttributeError:
        pass


def test_dir():
    import hyperspy_gui_ipywidgets
    d = dir(hyperspy_gui_ipywidgets)
    assert d == ['__version__',
                 'axes',
                 'microscope_parameters',
                 'model',
                 'preferences',
                 'roi',
                 'tools'
                 ]
