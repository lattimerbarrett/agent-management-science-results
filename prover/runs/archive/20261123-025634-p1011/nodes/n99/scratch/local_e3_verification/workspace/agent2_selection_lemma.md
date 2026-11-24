# Bubble-selection lemma in a fixed smooth flat boundary chart (agent_2)

Fix R>>1 and a small C2 profile tolerance. Define a good center q to be either
an interior local maximum, or a local maximum of the boundary restriction, with
height m=u(q), scale eps=m^(-2/(n-2)), such that on scale 2R the normalized
solution is within the prescribed tolerance of a standard bubble. Interior
centers must have distance to boundary >=2R eps; boundary centers use flattened
half-ball coordinates. For any sequence of smooth positive critical solutions
on a fixed compact smooth manifold (with smooth conformal-Laplacian and Robin
coefficients), one can choose finitely many good centers S_i so that

  dist(q,q')>=R max(eps(q),eps(q')) for q!=q',
  u_i(x) dist(x,S_i)^((n-2)/2)<=C_R.

This invokes only positive entire-solution classification (CGS), after even
reflection for the limiting homogeneous Neumann halfspace, plus standard local
elliptic estimates. The argument below explains the selection and uniform bound.
It does not invoke Pohozaev positivity, isolated simplicity, or an energy bound.

For each i take a maximal separated family of good centers. Such a family is
finite, since eps(q)>=max(u_i)^(-2/(n-2))>0. It can be obtained by adding centers
until none can be added; compactness bounds the number for this fixed i. If no
uniform bound on u_i(x) dist(x,S_i)^a held, where a=(n-2)/2, choose witnesses x_i
with d_i^a u_i(x_i)->infinity, d_i=dist(x_i,S_i). When S_i is initially empty,
use any fixed small chart radius in place of d_i. Work in a ball of radius d_i/2
about x_i, shrinking by a fixed chart-radius cap if necessary.

Point picking: maximize [distance to the artificial spherical boundary]^a u_i
in that ball. At a maximizing q_i, with artificial-boundary distance rho_i,

   rho_i^a u_i(q_i)>=c d_i^a u_i(x_i)->infinity,
   u_i(z)<=2^a u_i(q_i) for d(z,q_i)<=rho_i/2.

The chosen ball lies distance >=d_i/2 from S_i, and u_i(q_i)>=u_i(x_i), so also

       dist(q_i,S_i)^a u_i(q_i)->infinity.

Set eps_i=u_i(q_i)^(-1/a). The local upper bound holds on radii rho_i/eps_i->infinity.
Rescaled elliptic estimates give a positive limiting solution on R^n, or on a
halfspace with homogeneous Neumann boundary (smooth metric/Robin coefficients
converge to their Euclidean values). The normalization and weighted-maximality
make its gradient vanish at the origin whenever the origin is interior; the
tangential gradient vanishes in the boundary case. CGS classification, after
even reflection in the halfspace case, identifies a standard bubble. A finite
positive limiting distance from the rescaled origin to the boundary is impossible:
the only halfspace bubble has its unique critical point on the boundary. Thus
one obtains either an interior good maximum or a boundary good tangential
maximum q_i' at distance O(eps_i) from q_i, with comparable height and eps_i'.
The C2 approximation on scale 2R follows for every fixed R. In the whole-space
case a nearby genuine maximum is obtained by maximizing in a fixed small
rescaled ball; in the halfspace case maximize the boundary restriction. Smooth
Robin data need not make the full maximum occur exactly on the boundary, which
is why the boundary-restriction maximum is used.

Since dist(q_i',S_i)/eps_i'->infinity, this new center is at least R eps_i' from
all old centers. If it lay within R eps_j of an old center q_j, that old center's
2R bubble profile would give u_i(q_i')<=C u_i(q_j), and therefore

  dist(q_i',S_i)^a u_i(q_i')<=C(R eps_j)^a u_i(q_j)=C R^a,

contradicting the divergent weighted product. Thus it is also at least R eps_j
from every old center. It can be added to the maximal family, contradiction.
This proves the uniform selection bound.

For a general fixed compact LCF manifold, cover by finitely many flat boundary
and interior charts, with uniformly controlled conformal factors. The argument
is local at the witnesses, so the same proof works globally with one constant.
Potential artificial chart edges are avoided by point picking in a smaller ball.

DEPENDENCIES: standard CGS classification and standard interior/boundary elliptic
compactness. This file supplies selection only. Cluster exclusion still uses
the scale-uniform local Pohozaev sign as described in agent2_cluster_reduction.md.
