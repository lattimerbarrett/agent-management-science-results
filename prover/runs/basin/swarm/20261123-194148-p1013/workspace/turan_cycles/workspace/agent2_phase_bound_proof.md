# Exact lattice bound within finite-template tree phases (r>=3)

This is a proved optimization lemma, **not** a proof that every graph extremizer
has the requisite finite-template form.

Fix r>=3, k>=2, rho=(k-1)/k, q=(r-1)/r,
L=r/((r-1)(r-2)), B=2r/(r-1)^2. A phase consists of:
* an active part of size a, other r-1 parts as equal as possible;
* a fixed bounded exceptional gadget occupying u active vertices;
* remaining vertices packed into allowed trees of maximum order k.
Each order 1,...,k is realizable as a subtree of one allowed k-tree. Thus
maximal internal edges in the phase have the exact form
m_u(a)=a-ceil((a-u)/k)+d, where d is an integer constant.
Missing cross edges and other finite edge corrections can be included in d.

Write Q=sum_i(a_i-n/r)^2 and delta=a-n/r. Edge count, after a common
constant, is E=-Q/2+m_u(a). Our rigorously derived first-order cycle score is

S=(2/q)E-L Q+4L rho delta-B omega,

where omega=(sum_v binom(deg_T(v),2))/k for a repeated k-tree T.
For mixtures, omega is the vertex-weighted average. Stars maximize omega,
paths minimize it, with gap D_k=(k-2)(k-3)/(2k).

## 1. Only three active sizes need consideration

Put n=rm+s, 0<=s<r. A move increasing a by one takes a vertex from a largest
other part, of size b. Its cross-edge change is b-a-1. The internal-edge
change is 0 or 1. Hence
Delta S <= 2(1/q+L)(b-a)+2L(2rho-1).
If a>b this is strictly negative. If a is smaller than every other part,
the reverse consideration shows increasing a strictly improves both the
edge count and the cycle score. Consequently a maximizer lies among
m,m+1,m+2. The last is possible only when s>=2; for s=0 or 1 its preceding
move already starts with a>b.

## 2. Within a phase, a cycle-score maximizer is edge maximizing

For s=0, compare a=m and m+1. The larger has cross loss one and internal
gain j in {0,1}, while its extra part score is
P=2L(2rho-1)>=0. If j=1 it is edge tied and cycle favored; if j=0 its
score loss is 2/q-P>0, since
P < 2L <= 2/q (equality in the last inequality only at r=3).

For s=1, sizes m,m+1 are both balanced; the latter's internal increment
is j in {0,1} and its part-score increment is 4Lrho>0. Thus m+1 is
edge maximizing and cycle favored.

For s>=2, sizes m,m+1 are balanced, while m+2 has cross loss one versus
m+1. The first move has nonnegative internal gain and strictly positive
part-score gain. The second has exactly the same alternatives as s=0.
Thus the cycle-optimal edge maximizer is m+2 if the last internal increment
is 1, otherwise m+1. This is also a cycle-score maximizer over all a.

## 3. Comparing phases one edge apart

For fixed n, the part scores of the selected cycle-optimal edge maxima
of any two phases differ by at most P=2L(2rho-1). Indeed for s=0 there
are only m,m+1; for s=1 there is only m+1; for s>=2 there are only m+1,m+2.
Both nontrivial differences have Delta Q=2 and Delta delta=1.
The difference P is attained by choosing the residue u to make the
internal increment respectively 0 or 1 across that last move.

Therefore if a phase G has maximum edge count at least one below a
phase F, then comparing its best possible path shape against F's worst
possible star shape gives

S_G-S_F <= A(r,k) = -2/q + 2L(2rho-1) + B D_k.

This upper bound is attained in the abstract phase model: set the two
phase intercepts d to make the edge maxima differ by exactly one, take
F a repeated k-star and G a repeated k-path, and choose the residues
as above. It remains a separate GRAPH-REALIZATION problem whether these
phases can be forced by one forbidden graph.

Algebra gives

A(r,k)>0 iff
(r-2)k^2+(-2r^2+3r+4)k+2r-8>0.

For r=3 the first strict-positive integer k is 6.
For r=4 k=8 is an exact zero, and k=9 is first strict positive.
For r>=5 the first strict-positive integer k is 2r+1.
Proof of the last assertion: the polynomial is convex in k and increasing
on k>=2r; its value at 2r is -2(r-1)(r-4)<0 and its value at 2r+1 is
6(r-1)>0. Values on 2<=k<=2r are negative by convexity and the value
at k=2 is -4(r-1)(r-2)<0.

At A<0, the abstract phase comparison strictly favors an edge maximum.
At A=0 (r=4,k=8), this lemma is SILENT about the next-order sign.

## Computation

`agent2_phase_bound_check.py` computes all exact rational phase scores,
all residue pairs and all active sizes -2r..2r for r=3..10 and
k=2..2r+4. It asserts the numerical maximum equals A(r,k), and saves
actual maximizing witnesses in `agent2_phase_bound_check.json`.
