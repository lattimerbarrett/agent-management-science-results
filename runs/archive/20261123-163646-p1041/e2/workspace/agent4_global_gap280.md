# Exact elimination of weight280, coorder7 (agent4)

This supplements agent1/agent3's independent proof. It uses strict-below-2d
KT, not an unproved classification above2d. Its final orbit elimination
is independently executable in agent4_T280_q224_P28.py.

## Reductions

Previously established: 260,264,268,276 are globally absent; all272
supports are3-closed; every256 support is either a quadratic graph over
an8-flat or the terminal exceptional E256 in10-space. For the latter,
agent3's complete relative-code/fibre certificate proves every outside
nu5 collision of positive size<16 has size8, never12.

All0mod4 weights<=312 compress to14 by pair counting and Q-affinity.
There every pair multiplicity is even. For a280 support, k2->276,
k4->272, k6->268, k8->264, k10->260 are impossible. At k12->256,
a quadratic graph is2-closed (collision minimum16); exceptional E256
forbids P12 by the preceding relative-gap certificate. At k14->252,
k16->248, and k20->240, use mixed-axis minima30,28,24 respectively;
the quadratic240 type instead gives an outside degree5 word on9-space
of weight20, impossible between minimum16 and next24.

Thus all positive k>=28. Since C(280,2)=39060<28*2047, every280 support
compresses to10. (An unused direction exists in every dimension>=11.)
If it compresses to9, its indicator is quadratic; quadratic9 has no
weight280. Otherwise an irreducible cubic280 in10 exists.

For such a cubic, every quotient is quadratic on9 variables. The only
possible positive k below44 is28: k12 and20 were excluded, and quadratic
weights give k28->224, k44->192, k76->128, k140->0. Averaging
39060/1023<44 forces k28. Its quotient is q224, a positive rank6
quadratic on9-space. Set q=x0*x1+x2*x3+x4*x5 with radical coordinates
r0,r1,r2. The slice h is cubic. The outside support P of (1+q)h has
weight28 and degree<=5, i.e. coorder4 on9-space. Strict KT gives two
possible shapes for P:

 I. Positive nondegenerate rank6 quadric on its affine6-flat span W.
 II. Symmetric difference of two4-flats meeting in a line; its span W
     has dimension7. In coordinates X,Y in F2^3 and u in F2,
     P={(X,0,u):X!=0} union {(0,Y,u):Y!=0}.

We eliminate BOTH forms below.

## Type I

On the6-flat W, all quadratic polynomials vanishing on P form the
one-dimensional space <1+q_P>. The checker verifies this directly:
there are22 squarefree monomials through degree2; their evaluation on
these28 points has rank21. Thus q|W is0 or1+q_P.

The latter is a negative nondegenerate quadratic on6-space, impossible:
W-direction projects injectively to the active6-space of ambient q,
hence isomorphically. Any affine offset is absorbed into this bijective
projection. Consequently the restriction has the positive type of q,
with28 ones, not the36 ones of1+q_P.

If q|W=0, move W to a linear maximum singular6-flat via an affine
q-isometry. Such a W contains all3 radical directions and projects to
a maximal singular3-space in the active6-space, so is unique up to
q-isometry. Choose W=span(x0,x2,x4,r0,r1,r2).

To avoid classifying P within W, solve ALL cubic h vanishing on the
q-zero set outside W. This is a binary linear homogeneous system in130
coefficients. Its solution space has dimension17; its image on W has
dimension7. Exhausting the128 image words gives weight enumerator

    1 +28 z^16 +70 z^32 +28 z^48 +z^64.

In particular there is no weight28. The checker constructs the entire
kernel, verifies every constraint for every kernel basis vector, computes
the image basis and exhausts all128 images. This eliminates Type I.

## Type II: 164 complete embedding cases

Let the common line be U. The restriction q|W is quadratic and zero on
P. Because each X/Y punctured cube has3 variables and the allowed degree
is only2, its quadratic vanishing ideal consists exactly of the9 mixed
monomials X_i Y_j. (Pure terms would give a degree<=2 function supported
only at0 in F2^3, impossible.) In particular q is also zero on U.

Move a point of U to0 by an affine q-isometry; then W and both4-flats
are linear. By GL(X) times GL(Y), which preserves P, put

    q|W = X1*Y1 + ... + Xt*Yt,

for t=0,1,2,3. Let J=W intersect Rad(q_ambient), and j=dim J. The
projection of W onto the active symplectic6-space has dimension7-j
and polar rank2t. Elementary symplectic dimension restrictions give
exactly

    (t,j)=(3,1),(2,2),(2,3),(1,3).

Explanation: j>=1 because W has dimension7 and active dimension6.
For j1 its projection is all6-space and rank6; for j2 it is a5-space
whose restricted alternating form has rank4; for j3 it is a4-space
whose rank can4 or2. Rank0 would be a4-dimensional isotropic space
inside a symplectic6-space, impossible. The restricted quadratic is
positive since it is the displayed mixed bilinear form.

J is ANY j-dimensional subspace of the radical of that displayed form,
whose dimension is7-2t. We enumerate ALL such J, without quotienting by
P-automorphisms. Their counts are

    1,7,1,155, total164.

For each J, select a complementary radical subspace. Map J to j of the
3 global radical directions; map the complement to singular active
x-directions; map the t hyperbolic pairs to t standard active pairs.
This constructs an isometric embedding W->F2^9. The checker verifies
injectivity, dimension7, and preservation of q on ALL128 W-points.

These embeddings exhaust all possibilities up to ambient q-isometry:
first identify J with the actual global-radical intersection and match
its basis; pass to the active quotient, where Witt extension identifies
the two embedded nondegenerate-plus-singular subspaces; finally remove
any residual radical graph by a shear. No assumption about the
intersection of J with the distinguished common line is made: EVERY J
is explicitly enumerated.

For each embedded P, solve the FULL130-variable affine system

    h(x)=1_P(x) for EVERY x with q(x)=0, deg h<=3.

Every one of the164 systems is inconsistent. This is actual finite
Gaussian elimination, not a solver timeout. The script's output reports
1/7/1/155 cases with zero solutions. Thus Type II is impossible.

There is no irreducible cubic280 in10-space, and hence no coorder7
weight280 in any ambient dimension. Weight282 is then absent by the
standard Q=1/k1 forcing argument. The same relative gap of E256 excludes
P14; together with the preceding low-quotient exclusions this gives
minimum positive k>=30 for284, compresses it to10, and8-divisibility of
cubic10 weights excludes284. Weight286 follows by the same k1 forcing.

## Actual computational artifacts

- agent4_T280_q224_P28.py: ALL164 TypeII systems; TypeI rank21;
  complete TypeI image-code kernel and weight enumerator. Executed0.1s.
- agent1_T280_q224_P28.py: independent TypeII U/A/B-space enumeration.
- agent3_T280_P12_allorbits.py: independent exact fibre proof excluding
  ALL outside P12 (and P10/P14) for exceptional E256.
- agent4_T280_P12.py: redundant complete6SUM enumeration of P12 using
  affine automorphism direction/point orbits, no hits in8.4s.

These prove real low-weight absences, NOT the user's main no-fixed-list
claim. A genuine14->15 spectral change is still missing.
