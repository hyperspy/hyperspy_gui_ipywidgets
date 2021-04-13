"""ipywidgets GUI elements for HyperSpy.

"""
# setup.py adapted from https://github.com/pypa/sampleproject/blob/master/setup.py
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


version = {}
with open(path.join(here, "hyperspy_gui_ipywidgets", "version.py")) as fp:
    exec(fp.read(), version)

PROJECT_URLS = {
    'Bug Tracker': 'https://github.com/hyperspy/hyperspy_gui_ipywidgets/issues',
    'Documentation': 'https://hyperspy.org/hyperspy-doc/current/index.html',
    'Source Code': 'https://github.com/hyperspy_gui_ipywidgets/hyperspy',
    'Support' : 'https://gitter.im/hyperspy/hyperspy'
}


setup(
    name='hyperspy_gui_ipywidgets',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version['__version__'],

    description=('ipywidgets GUI elements for HyperSpy.'),
    long_description=long_description,
    long_description_content_type="text/markdown",

    # The project's main homepage.
    url='https://github.com/hyperspy/hyperspy_gui_ipywidgets',
    project_urls=PROJECT_URLS,

    # Author details
    author='The HyperSpy Developers',

    # Choose your license
    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],

    # What does your project relate to?
    keywords='hyperspy ipywidgets',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['hyperspy>=1.6.2', 'ipywidgets>=7.0', 'link_traits'],


    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'tests': ['pytest'],
        'coverage':["pytest-cov", "codecov"]},
    entry_points={'hyperspy.extensions': 'hyperspy-gui-ipywidgets = hyperspy_gui_ipywidgets'},
    package_data={  # Optional
        'hyperspy_gui_ipywidgets': ['hyperspy_extension.yaml'],
},
)
