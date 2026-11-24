# Conditional closest-cluster exclusion (agent_2)

Assume a scale-uniform local Pohozaev nonnegativity theorem for isolated
boundary blowups, including sequences viewed in domains converging smoothly to
halfspace on compact sets. For interior blowups in a flat chart the required
sign is automatic from the exact interior Pohozaev identity. Also assume the
standard bubble-selection output below; its proof by point picking and CGS
classification is not supplied in this file.

SELECTION OUTPUT NEEDED. There are selected local maxima q_i1,...,q_iNi such that
(a) u_i(x) dist(x,{q_ij})^a<=C uniformly;
(b) each peak has its standard bubble profile in its own scale;
(c) different selected centers are separated by a sufficiently large fixed
    multiple R of BOTH bubble scales;
(d) maxima with bounded height may be ignored away from a fixed compact set;
(e) the selection/classification includes boundary and interior peaks; rescaled
    boundary conditions converge to Neumann and rescaled metrics to Euclidean.
Here a=(n-2)/2. The mixed interior/boundary cases need to be included explicitly
in a final selection proof; a boundary-only selection can miss interior peaks.

Suppose the minimum selected-center separation d_i tends to zero. Rescale by
d_i about one endpoint of a closest pair:

                W_i(y)=d_i^a u_i(q_i1+d_i y).

The selected centers now have mutual distance >=1, and at least two of them
remain in a fixed bounded set. Every compact set contains uniformly finitely
many centers by packing. After subsequence their limits form a locally finite
set S in the limiting domain, which is either R^n or a halfspace. Away from S,
selection gives uniform boundedness and local linear Harnack/elliptic estimates.
Each center is isolated on a ball of radius <1/3, uniformly in i. By the
second-critical-radius reduction, the assumed sign makes every divergent
rescaled peak isolated simple. Consequently the conditional sharp estimate
applies on a fixed ball about each divergent center.

## Case 1: all rescaled selected heights stay locally bounded

Compactness across the finitely many centers in each compact set gives a smooth
positive global critical solution W on the limiting whole space or halfspace,
with homogeneous Neumann data in the latter case. (Local boundedness near a
center follows from its selected bubble profile and bounded rescaled height.)
CGS classification, after even reflection in the halfspace case, says W is a
single bubble. But the two closest-pair selected local maxima survive at two
distinct points, whereas a bubble has exactly one local maximum. Contradiction.
For a halfspace, its bubble maximum lies on the boundary; this also excludes
an interior limiting critical point. Interior poles approaching the boundary
are handled in Case 2 by their reflected Green contribution.

## Case 2: at least one rescaled selected height diverges

The sharp simple estimate makes W_i tend to zero on a fixed annulus around that
center. Harnack chains propagate this convergence to every compact subset away
from S. No other selected height can stay bounded: its positive finite-height
bubble profile on a fixed-radius core would contradict convergence to zero on
punctured neighborhoods. In particular both closest-pair heights diverge.
Choose the endpoint with larger height as center zero, and let N_i=W_i(0).
The sharp estimate gives upper bounds for N_i W_i on a fixed punctured ball
about zero; normalized bubble flux gives a positive lower bound on an annulus.
Harnack chains and elliptic estimates give a subsequential positive harmonic
limit h on the limiting domain minus S. In the halfspace case it has Neumann
data away from S. At zero it has fundamental coefficient A_1>0.

The fundamental coefficient at the other closest-pair point is a positive
constant times lim N_i/W_i(q_i2). The ratio is >=1 by choice of endpoint, while
Harnack boundedness on an annulus about q_i2 bounds the ratio above. Hence that
coefficient A_2 is finite and strictly positive. This assertion can also be
seen directly by integrating the equation over the core bubble ball; the
normalized source mass is a fixed positive constant times the peakheight ratio.

Any nonnegative harmonic function on the whole space or halfspace minus a
locally finite set of poles dominates the sum of any finite collection of its
fundamental pole functions. Indeed compare on a radius-L ball using the
Dirichlet Green function (Neumann data on the flat disk in the halfspace), then
send L to infinity. Thus near zero the regular harmonic part satisfies

                         B_1>=c A_2>0.

If zero is an interior pole at finite distance from a limiting plane boundary,
the Neumann reflection image itself already contributes a strictly positive
regular part, so the same conclusion holds.

The harmonic Pohozaev limit at zero is therefore

             -(n-2)^2 |S^(n-1)| A_1 B_1/4<0

for a boundary pole (twice this for an interior pole). This contradicts the
assumed local nonnegative sign, or the exact interior Pohozaev identity.
Therefore selected-center separation is uniformly positive.

SCOPE. This is a conditional logical reduction. It does not prove the boundary
selection lemma or the nonlinear local sign theorem; the latter is the crucial
missing bridge. It explains why those two inputs, plus the already written
conditional sharp estimate, suffice for simplicity and cluster exclusion.
