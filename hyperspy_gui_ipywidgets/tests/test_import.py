
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
