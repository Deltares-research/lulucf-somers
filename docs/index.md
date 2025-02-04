---
html_theme.sidebar_secondary.remove:
---

# LULUCF SOMERS Shell (LUSOS)

This page is a work in progress. 


# How to install
Currently, `lusos` needs be installed in a Python 3.12 environment, install the latest stable release using pip:

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


```{toctree}
---
hidden:
---

Home <self>
About <about>
User guide <user_guide>
API Reference <api_reference>
```