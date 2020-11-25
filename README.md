# Sea-level monitor
Tools and applications used to monitor sea-level rise. The notebooks under `notebooks` contain analysis used for the Dutch sea-level monitor. The directory `data` contains scripts that are used to process common sources of sea-level data. The directory `app` contains the public sea-level rise website.

# Notebooks
You can view the notebooks using the [nbviewer](https://nbviewer.ipython.org/github/openearth/sealevel/tree/master/notebooks/) website. You can try out the notebooks by going to the [binder](https://mybinder.org/v2/gh/openearth/sealevel/master?filepath=notebooks) website or using github codespaces. You need to follow a few steps to get an environment that can run the notebooks. The following steps will help you through it.

# Download data
For windows systems:
Install chocolatey from https://chocolatey.org/install
``` shell
choco install make
choco install wget
```

For all systems, also do:
```
cd data
make
```
Note that for the main sea-level monitor you only need to download the data from the directories: `psmsl` and `noaa`. So you can go into those directories and run make there. This will download all the tide gauge information and information needed to correct for wind effects.

# Packages
You can install the packages in the file `requirements.txt` using pip or anaconda. For pip this is done using `pip install -r requirements.txt`. Windows users might want to prefer installing these packages through anaconda.

# Running the notebook
You can run the notebook in either jupyter notebook or jupyterlab. To start jupyter notebook. From the main level of the repository start `jupyter notebook` and browse through the notebooks folders. The main notebook is `dutch-sea-level-monitor.ipynb`.


# Tags
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/openearth/sealevel/master?filepath=notebooks)
[![DOI](https://zenodo.org/badge/90898262.svg)](https://zenodo.org/badge/latestdoi/90898262)

# Corrections
In 2016 the [MSL](https://www.psmsl.org/about_us/news/2016/mtl_msl_correction.php) record changed . In December 2019 these figures were entered [incorrectly](https://github.com/openearth/sealevel/issues/5). This was fixed in July 2020. The new figures are based on the RLR - NAP distance directly.
