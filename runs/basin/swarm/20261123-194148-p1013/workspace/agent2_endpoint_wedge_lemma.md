# Endpoint wedge tuning for r=4, k=8

This note proves the analytic endpoint comparison for the programmed
star/path phases, using the cycle-contraction expansion. It does not prove
the separate global-template theorem or the forbidden-graph realization.

Let q=(r-1)/r. For a fixed graph F write w(F)=sum_v binom(d_F(v),2).
For a graph F let p_F(z)=sum_P 2^{comp(P)}z^{e(P)}, summing over edge
subsets P whose nontrivial components are paths (including the empty set).
Then, by inspecting one- and two-edge subsets,

log p_F(z)=2e(F)z-2(e(F)+w(F))z^2+O_F(z^3).                 (1)

Indeed the two-edge coefficient of p is
4*binom(e,2)-2w. Formula (1) is exact to the stated degree, even when F
contains triangles or vertices of large (but fixed) degree.

## Finite replacement lemma

Suppose two almost balanced complete r-partite graphs, r>=3, have the
same part sizes and the same repeated bounded internal components, and
on a fixed reserved set in one part they respectively carry F and F'.
Assume e(F)=e(F'). Then

log(c(G_F)/c(G_F')) = -2(w(F)-w(F'))/(q^2 n^2)+O_{F,F'}(n^-3). (2)

This remains true if the repeated-component counts differ from their
linear limiting values by an arbitrary fixed amount.

Proof: contract the selected internal path forests. The common
contraction coefficient for j edges is (qn)^(-j)*(1+O(j^C/n)); the
Hamiltonian version depends only on j, while for all cycles its bounded
omission corrections also depend polynomially on the number of used
vertices. In the ratio, (1) says that the finite replacement first differs
by -2 Delta w z^2. Multiplication by the bulk path-forest polynomial and
summation over j evaluates this difference at z=1/(qn), to leading order.
The bulk factor cancels on dividing. Errors in this evaluation gain one
power of n^-1. Any finite three-edge cluster also costs n^-3. For all
cycles, omitted vertices have a factorially decreasing tail; the chance
of omitting a specified finite vertex is O(1/n). Thus omission corrections
to the finite wedge term start at n^-3. Corrections to finite edge terms
are identical because the two finite graphs have equal edge counts.
The logarithmic expansion follows because the relative difference is
O(n^-2). The factorial domination in agent2_tree_cycle_expansion.md
justifies all these termwise operations (and one further Taylor order).

## Dependence on the marker length

Let T_S=K_{1,k-1}, T_P=P_k. Fix a residue U mod k. Put n=rm and
m-U=kt. Compare

S_U: active part m,        t*T_S + C_U;
P_U: active part m+1,      t*T_P + P_2 + C_{U-1};

all other parts as equal as possible (for P_U one other part has size
m-1). Both have EXACTLY the same number of internal edges

t(k-1)+U.

Let A(r,k) be the first-order advantage computed in
agent2_phase_bound_proof.md. At A(r,k)=0, there are constants b0,b1,
independent of U in its fixed residue class, such that

n^2 log(c(P_U)/c(S_U)) -> b0+b1*U.                         (3)

Only existence, not values, of b0,b1 is needed. Here is the power-counting
justification, to avoid assuming their independence of U. In the
logarithmic path-forest/contraction expansion through order n^-2:
* zeroth order is 2*e_internal/(qn), plus the common complete-partite term;
  it is LINEAR in the edge count;
* connected two-edge clusters enter as -2w/(q^2 n^2);
* three-edge and higher connected clusters of the fixed marker enter only
  at n^-3 or smaller;
* the O(n) repeated three-edge cluster counts contribute at n^-2 only
  through their limiting densities, which do not depend on U;
* global contraction/omission corrections are analytic functions of
  limiting edge/wedge densities. Their first-order n^-1 coefficient
  gains only a LINEAR correction from the O(U) finite edge/count shifts.
For cycle markers e=w=U (and U-1), all remaining finite contributions
are linear in U; the repeated count t=m/k-U/k has only a linear offset.
Disconnected finite clusters cancel in the logarithm. These statements
also follow directly by applying the contraction functional to
p_T(z)^t*p_F(z), expanding (1) and the bulk logarithm one further order.
Thus the n^-2 coefficient is affine in U. The complete-partite part
sizes differ by a fixed vector, independent of U.

## High-wedge marker

Replace S_U's cycle by X_U, the graph formed by a triangle plus U-3
pendant vertices attached to one triangle vertex. Then

v(X_U)=e(X_U)=U,
w(X_U)=binom(U-1,2)+2.

By (2) and (3),

lim n^2 log(c(P_U)/c(S_XU))
 = b0+b1*U + 2*(binom(U-1,2)+2-U)/q^2
 = U^2/q^2 + O(U).

It is therefore strictly positive for every sufficiently large fixed U
in the chosen residue class. In particular this proves the desired
cycle separation at r=4,k=8, where A(4,8)=0.

## Edge maximality is not lost by deleting pendant vertices

At the selected n, S's active bulk has size m-U=kt. A proper subgraph
of X_U on U-p retained vertices has at most U-p edges. If p>0, combining
it with any k-tree forest on the other m-U+p vertices gives at most

m-ceil((m-U+p)/k) < m-(m-U)/k,

strictly below the full-marker edge count. If p=0 but an edge is deleted,
the edge count also falls. Thus among the edge-extremal star phase at
this n the ENTIRE high-wedge marker is forced; its pendant vertices
cannot be traded for bulk vertices at zero edge cost.

## Inactive-pattern chromatic number

For the hereditary component class generated by stars, paths, a cycle,
and X_U, every minimal forbidden connected graph has chromatic number
at most three. Otherwise it contains an edge-minimal 4-chromatic subgraph
J, of minimum degree at least three. For each edge e, J-e is connected
and has minimum degree at least two. It cannot be a subgraph of a
star/path; a connected minimum-degree-two subgraph of X_U is just its
triangle, and of a cycle is the cycle itself. Neither can contain J-e
(which has at least four vertices and is not a cycle). Hence J-e would
already be a forbidden proper subgraph, contradicting minimality.
This verifies the profile realizer's inactive proper-coloring hypothesis.


# Stronger version: no second-order expansion is required

The affine-limit argument above can be replaced by a simpler uniform
error bound, so no uncomputed second-order local-CLT coefficient is used.

The already proved first-order expansion in
`agent2_tree_cycle_expansion.md` is UNIFORM for internal maximum degree
at most a fixed D; its O_D(n^-2) constant does not depend on internal
component orders. This follows directly from the path-forest estimate:
connected three-edge configurations number O_D(n), pairs of wedges
number O_D(n^2), and the remaining selected edges are arbitrary. Thus

S_j=2^j binom(M,j)-2^(j-1)w binom(M-2,j-2)
    +O(C_D^j n^(j-2)/(j-4)!),

with the evident separate interpretations for j<4. Closed triangles
are among the O_D(n) three-edge errors; longer cycles cause smaller
errors. The contraction coefficient's uniform polynomial-j Taylor
error, followed by the factorial tail bound, gives an O_D(n^-2)
remainder. None of these estimates uses a bound on component order.

Write K=r/(r-2), DeltaW=w(T_S)-w(T_P)=(k-2)(k-3)/2. For the two CYCLE
marker graphs S_U,P_U, their maximum degrees are at most k-1 independent
of U, and their internal edge counts are exactly equal:

M=rho*m+U/k,   lambda=2M/(qn),   t=(m-U)/k.

Their active deviations differ by one and Q differs by two. Consequently

log(c(P_U)/c(S_U))
 =[-2K+2K*lambda]/n + [2t*DeltaW+2]/(q^2*n^2)
   + O_{r,k}(n^-2).

At A(r,k)=0 the coefficient of n^-1 vanishes, leaving

n^2 log(c(P_U)/c(S_U))
 = U*[4K/(kq)-2DeltaW/(kq^2)] + 2/q^2 + O_{r,k}(1).       (4)

Crucially the last O(1) constant is independent of U. The statement is
read as a uniform limsup/liminf bound for each fixed U, not as the
existence of a second-order limit.

Now use the finite replacement lemma (2), which only requires the
first-order O(1/n) error in the contraction coefficient: the finite
wedge difference already carries n^-2, so that error becomes n^-3.
It follows from (4) that

liminf_{n->infty} n^2 log(c(P_U)/c(S_XU))
 >= 2*(binom(U-1,2)+2-U)/q^2 - C_{r,k}(1+U).

This is positive for a sufficiently large fixed U. Therefore endpoint
inclusion follows from the EXISTING first-order expansion with a uniform
maximum-degree remainder, and the finite-replacement lemma. No unknown
second-order coefficient or numerical extrapolation is needed.

At r=4,k=8, q=3/4,K=2,DeltaW=15, the explicit linear coefficient in (4)
is -16/3. The high-wedge correction has leading coefficient 16/9 times
U^2, so the domination is immediate.


## Fully explicit uniform forest-error bound

Here is a direct proof of the uniformity claim, avoiding any appeal to
an unspecified cluster-expansion constant. Let M=e(G), Delta(G)<=D,
w=sum_v binom(d(v),2). For a j-edge subset A let w_A be its number of
adjacent edge pairs. Its actual path-forest weight W_A is 2^(j-w_A)
if A is a linear forest, and zero otherwise. If w_A is 0 or 1, then
W_A=2^j*(1-w_A/2). If w_A>=2, then

|W_A-2^j*(1-w_A/2)| <= 2^j*binom(w_A,2).

Indeed W_A/2^j lies in [0,1], so its distance from 1-w_A/2 is at most
w_A/2 <= binom(w_A,2).

Sum over A. Every pair of distinct adjacent-edge-pairs has a union of
three or four edges. Let N3,N4 count these two possibilities. Then

|S_j-2^j binom(M,j)+2^(j-1)w binom(M-2,j-2)|
 <= 2^j*[N3 binom(M-3,j-3)+N4 binom(M-4,j-4)].

A three-edge union has a uniquely shared edge, and that edge has at
most 2D-2 neighboring edges. Therefore

N3 <= M*binom(2D-2,2),
N4 <= binom(w,2),   w <= (D-1)M.

These are exactly the degree-only estimates required above. Interpret
binomial coefficients with an invalid lower index as zero.

`agent2_uniform_forest_error_checks.py` exhaustively checked the
per-subset weight inequality and the summed bound for ALL 145253 edge
subsets of ALL 209 unlabeled graphs on at most six vertices; every
assertion passed. Its JSON file records the actual counts.
