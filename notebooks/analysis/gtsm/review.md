Review:

In this dataset a tidal model (GTSM) is used to compute the long period
nodal tide, which has a 18.61 year period. The purpose of this
computation is tot correct yearly mean and monthly mean tide gauge
records for this tide constituent. For example Woodworth 2012 claims
that the small amplitude and presence of long period ocean signals in
the tide gauge data are more likely to make estimates of sealevel trends
worse than better. The computation here uses a full 19 year dynamic tide
computation, which Woodworth 2012 claims has not been done before.

Although possibly others have performed similar computations since then.
A consequence of this approach is that the estimates also contain
indirect non-linear effects, such as the nodal modulation on the
amplitude of M2 interacting with itself.

Thus the computation can potentially deviate from an equilibrium
approach. The tidal potential, corrections for solid earth tide and
its gravity effects, as well as selft attraction and loading are
present in both approaches.  This preliminary version of the dataset
has substantially lower nodal long period tide amplitudes. In fact the
amplitudes are about 50 percent smaller. It is not clear at present if
this is the result of an error in the implementation, poor perfomance
of GTSM in this respect, or a difference caused by the different
approach.

It would be very useful to perform additional checks that will result
either in finding the problem or lendig credibility to the
results. Woordworth claimed in 2012 that it is unlikely that the nodal
tide will deviate far from the self-consistent equilibruim tide. On
the other hand, no information from dynamic models were available at
that time. Note the non-linear effects will be strongest for large
tides in shallow water.

FB: run model with only nodal tide component. Discuss 50% deviation
with Arthur/Herman. Denote dataset as preliminary. Not for this version.



Some comments:
- In more detail the analysis would benefit from a more explicit use of
the nodal phase 'N'. In the least-squares approach, now the year 1970 is
used as a reference. A formula like in table 4.2 of the book "Sealevel
Science" by Pugh and Woodworth could align the phase with the driving
tidal potential. Also, then the component A would directly align with
the self-consistent amplitude including its sign.


FB: requires implementation in different parts of the sea-level
monitor code. T0 of this phase is not accurately/reproducible
described.  Do two approaches: relative to 1970 and relative to T0
(start of upgoing cycle, sin) of the nodal tide. 4.2 contains a -
sine.  Check for consistency with FM code. Check with Martin if this
can be implemented in v2. Add remark that this will be added in next
version.
FB: included


- Some locations have a mean that deviates substantially from zero. This
is most likely either an issue with stations that are locally influenced
by a local lack of resolution, or by non-linear effects. It would be
good to check for problems there.

FB: discuss top 5 psmsl stations.
psmsl-173: station in the river mound the St. Lawrence River in Quebec. Not enoguh resolotion
psmsl-1067: Anchorage in Alaska, in an inlet
psmsl-495: inlet
psmsl-1908: bathymetry/bridge
psmsl-2285: bathymetry resolution/bridge

General remark: resolution in narrow tidal inlets and stations up
rivers are not accurate. In an updated version we might be able to use
cells just outside the inlet. But tide in narrow inlets can be quite
different from outside.


It would be helpful to have a full spatial picture globally for
comparison with literature, but this can also be useful to check for
large local variability.

 Details:
 - I would change '`values`: mean sea surface level due to tidal waves
[m]' to '`values`: mean sea surface level due to tides [m]'
 - A,B and phase are all relative to Jan 1st 1970. Please make this
explicit, as tides are usually specified relative to the phase of the
tidal potential.

Groeten,
