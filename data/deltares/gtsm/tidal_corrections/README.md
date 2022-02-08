# Nodal tide components for the PSMSL annual and monthly dataset (preliminary)
This preliminary dataset contains the tidal component for the mean sea
level for the tide gauges in the Permanent Service for Mean Sealevel
dataset. These files can be used to subtract the long term tide of the
mean sea level.


# Authors and contact
This dataset is created by Jelmer Veenstra, Martin Verlaan, Fedor
Baart, and Willem Stolte. You can contact Jelmer Veenstra or Fedor
Baart for more information.


# Files
You can find the following files in this dataset.

- `monthlymean_gtsm_psmsl-{id}.csv`: monthly tidal corrections for mean sea level.
- `yearlymean_gtsm_psmsl-{id}.csv`: annual tidal corrections for the mean sea level.
- `yearlymeanOLS_gtsm_psmsl-{id}.csv`: annual tidal corrections based
  on a harmonic analysis through the reanalysis data (see details
  below).
  - `df_OLSmodelstats_year.csv`: an overview of the phase and amplitude
  of the harmonic analysis of all the stations, also includes the
  equilibrium tidal amplitude.

All files are stored in `.csv` files, using a `,` as field separator and
`.` as decimal separator. Time is stored as `YYYY` for the annual
series and as `YYYY-MM` for the monthly series.

The file `df_OLSmodelstats_year.csv` also contains the list of all
stations for which we provide information. More information on these
stations can be found at [1].


# Data specific information

The file `monthlymean_gtsm_psmsl-{id}.csv` contains the following columns:
- `time [year-month]` : year-month for which the mean tidal level is determined
- `sea_surface_height_due_to_tide [m]`: mean sea surface level due to tidal waves [m]

The file `yearlymean_gtsm_psmsl-{id}.csv` contains the following columns:
- `time [year]`: year for which the mean tidal level is determined
- `sea_surface_height_due_to_tide [m]`: mean sea surface level due to tidal waves [m]

The file `yearlymeanOLS_gtsm_psmsl-{id}.csv` contains the following columns:
- `time [year]`: year for which the mean tidal level is determined
- `sea_surface_height_due_to_tide_fitted [m]`: mean sea surface level due to tidal waves, harmonic fit [m]

The file `df_OLSmodelstats_year.csv` contains the following columns:

- `longitude [degrees east]`: longitude of the station
- `latitude [degrees north]`: latitude of the station
- `station_name`: station name
- `nodal tide U [m]`: linearized fit of the nodal cycle (A/U/cos term) (relative to 1970) [m]
- `nodal tide V [m]`: linearized fit of the nodal cycle (B/V/sin term) (relative to 1970) [m]
- `nodal amplitude [m]`: amplitude of the fitted nodal cycle, sqrt(A**2 + B**2) [m]
- `nodal phase [radians since 1970-01-01]`: phase of the fitted nodal cycle arctan2(B, A) [rad, epoch 1970]
- `mean sea surface height of nodal fit [m]`: mean tidal level over the fitted time window [m]
- `nodal amplitude fitted with nodal epoch [m]`: amplitude of the fitted nodal tide with epoch at the start of the phase of the nodal tide. Note that the amplitude here can be negative. [m]
- `nodal amplitude of equilibrium tide [m]`: equilibrium amplitude of the nodal tide [m]


# Methods
To generate this dataset we have run a tidal model (GTSM v4.0) for 19
years. This multi-decadal reanalysis of tides allows separating the
tidal component from other sea-level fluctuations. The purpose of this
computation is to correct yearly mean and monthly mean tide gauge
records for this tide constituent.  See [1, 2] for a discussion on
this topic.

The equilibrium ampltiude is computed as:
``` python
abs(0.69 * 20 * (3 * sin(deg2rad(lat))**2 - 1)) / 1000
```
This assumes an all water, elastic earth, and no self attraction.

In this simulation, all tidal forcings (~400) are active. Thus the
estimates also contain indirect non-linear effects, such as the nodal
modulation on the amplitude of M2 interacting with itself. This allows
the computation to deviate from the equilibrium tide. The tidal
potential, corrections for solid earth tide (through Love numbers), and
self attraction and loading are included.

Using this dataset we fit, using an ordinary least squares approach,
the nodal tidal amplitude, and phase. Details of this analysis can be
found in the corresponding notebook [3].

The results have not been validated or published, so please use this
dataset with caution. See the details in the section preliminary
results.


## Preliminary results
These are preliminary results, intended for evaluation with other
scientists. Make sure you take into account the following:

- These results are based on GTSM 4.0, we expect to create an updated
  version based on 4.1. Version 4.1 should have a better internal tide
  model, which should improve reanalysis results in general.

- The following regions are not reliable:
  - Black Sea, due to a limited topological relation with the rest of
    the grid. These stations are excluded.
  - Regions in inlets have not been validated

- The reanalysis amplitude is lower than expected from equilibrium
  tide (about a factor 2 lower). Research into the cause of this is
  pending (love numbers, self attraction can be considered).

- The phase of the nodal tide is not yet validated.

- Some stations have deviating mean sea levels. A few examples:

* psmsl-173: station in the river mound the St. Lawrence River in
  Quebec. Not enough resolution
* psmsl-1067: Anchorage in Alaska, in an inlet
* psmsl-495: inlet
* psmsl-1908: bathymetry/bridge
* psmsl-2285: bathymetry resolution/bridge

General remark: resolution in narrow tidal inlets and stations up
rivers are not accurate. In an updated version we might be able to use
cells just outside the inlet. Tide in narrow inlets can be quite
different from outside.




# Sharing and Access information
This dataset is available under a CC-BY-SA license [3]. See the link below for details.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

Please make sure you refer to the preliminary status of this dataset if you use it.


[0] https://www.psmsl.org
[1] https://doi.org/10.2112/JCOASTRES-D-11-00169.1
[2] https://doi.org/10.2112/JCOASTRES-D-11A-00023.1
[3] http://creativecommons.org/licenses/by-sa/4.0/
