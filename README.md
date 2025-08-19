# LULUCF SOMERS Shell (LUSOS)
[![PyPI version](https://img.shields.io/pypi/v/lusos.svg)](https://pypi.org/project/lusos)
[![License: MIT](https://img.shields.io/pypi/l/imod)](https://choosealicense.com/licenses/mit)
[![Lifecycle: experimental](https://lifecycle.r-lib.org/articles/figures/lifecycle-experimental.svg)](https://lifecycle.r-lib.org/articles/stages.html)
[![Build: status](https://img.shields.io/github/actions/workflow/status/deltares-research/lulucf-somers/ci.yml)](https://github.com/Deltares-research/lulucf-somers/actions)
[![codecov](https://codecov.io/gh/Deltares-research/lulucf-somers/graph/badge.svg?token=HCNGLWTQ2H)](https://codecov.io/gh/Deltares-research/lulucf-somers)
[![Formatting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)

Python package to calculate spatial greenhouse gas (GHG) emissions based on [PeatParcel2d-AAP](https://github.com/Deltares-research/PeatParcel2d-AAP) data, topographic data ([BGT](https://www.pdok.nl/introductie/-/article/basisregistratie-grootschalige-topografie-bgt-)) and the [BRO Bodemkaart](https://www.pdok.nl/-/de-services-voor-de-bro-datasets-bodemkaart-en-geomorfologische-kaart-zijn-vernieuwd).


# How to install
Currently, `lusos` needs be installed in a Python 3.12 environment or higher, install the latest stable release using pip:

```powershell
pip install lusos
```

Or the latest (experimental) version of the main branch directly from GitHub using:

```powershell
pip install git+https://github.com/Deltares-research/lusos.git
```


## Installation (developer)
We use [Pixi](https://github.com/prefix-dev/pixi) for package management and workflows.

With pixi installed, navigate to the folder of the cloned repository and run the following 
to install all GeoST dependencies:

```powershell
pixi install
```

This installs the package in editable mode, so you can make changes to the code and test them immediately.


# How to use
TODO: Add usage instructions