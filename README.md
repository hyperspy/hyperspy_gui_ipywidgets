# link_traits
[![Build Status](https://travis-ci.org/hyperspy/link_traits.svg?branch=master)](https://travis-ci.org/hyperspy/link_traits)



**link_traits** is a fork of [traitlets'](https://github.com/ipython/traitlets)
**link** and **dlink** functions to add the ability to link
[traits](https://github.com/enthought/traits) in addition to traitlets.


## Installation

Make sure you have
[pip installed](https://pip.pypa.io/en/stable/installing/) and run:

```bash
pip install link_traits
```

**link_traits** depends on **traits** which is not a pure Python package. In
[Anaconda](http://continuum.io/anaconda) you can install traits from
conda forge before install **link_traits** as above:

```bash
conda install traits -c conda-forge

```

## Running the tests

py.test is required to run the tests.

```bash
pip install "link_traits[test]"
py.test traitlets
```

## Usage

```python

import traits.api as t
import traitlets
from link_traits import link

class A(t.HasTraits):
    a = t.Int()

class B(traitlets.HasTraits):
    b = t.Int()
a = A()
b = B()
l = link((a, "a"), (b, "b"))
```

```python
>>> a.a = 3
>>> b.b
3
```

## Development

Contributions through pull requests are welcome. The intention is to keep the
syntax and features in sync with the original traitlets' **link** and **dlink**
functions. Therefore, before contributing a new feature here,
please contribute it to [traitlets](https://github.com/ipython/traitlets/)
first.
