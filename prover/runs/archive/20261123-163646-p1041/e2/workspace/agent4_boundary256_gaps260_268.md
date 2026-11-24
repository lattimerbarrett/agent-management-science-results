# Boundary 256 classification and global gaps 260,264,268

This note uses ONLY the classical strictly-below-twice-minimum-distance
Kasami--Tokura theorem, the elementary Q identity already proved by agent1,
and exact finite binary linear algebra explicitly implemented in
`agent4_boundary256_orbits.py`. It does not prove the main 14->15 change.

## I. Standard quotient/lift and separator facts

A coorder7 support S has all degree<=6 moments zero. Under quotient by v,
its parity support T has the same property and weight |S|-2k, where k is
the number of double fibers. One of the two original slices has indicator
h; its support is contained in T union P, with P the k double fibers
outside T. The function h has all degree<=5 moments zero. Thus
sum nu5(P) lies in span nu5(T).

If T is contained in an affine subspace W and k<32, then h is supported
in W. Indeed for every affine hyperplane containing W, restriction of h
to the opposite halfspace has minimum nonzero weight32 (coorder drops
from6 to5); it has at most k points and so is empty. Therefore P lies in W.

If T is e-closed, meaning every outside point can be separated from T by
a polynomial of degree<=e vanishing on T, every nonempty outside collision
set P has size at least 2^(6-e). Multiply a separator by all monomials of
degree<=5-e and use minimum distance on the selected P. In particular:
cl2-closed => collision minimum16; cl3-closed => minimum8.

## II. Every coorder7 support of weight256 is 3-closed

Repeatedly take injective quotients until no such quotient remains.
The final support spans its ambient affine space. Pair count compresses
to dimension<=14 because C(256,2)=32640<32767.

If the irreducible dimension is n>8, averaging over all nonzero directions
provides a positive k<2^(15-n). By strict KT, k is a power of2, since the
quotient has weight256-2k<256. The KT two-flat type has intrinsic affine
span14-log2(k), which is >=n and cannot fit in quotient dimension n-1.
Therefore the quotient must be the KT quadratic type, whose intrinsic
span is9. If n>=11 this is a proper hyperplane support; the original S
has at most2k<=16 points outside its preimage, less than the restriction
minimum64. Hence S lies in that preimage, contradiction. (For n>=12,
the KT quadratic type actually cannot have the required rank at all.)
Thus irreducible n<=10.

For n=10, k<32. The only possible quadratic quotients are k=8 or16:
q of rank8 or6 respectively on F2^9. Their degree2 separator shows that
P is a degree<=3 even set, hence has size>=16. This excludes k8.
At k16, P is a minimum degree3-even set, so is an affine4-flat, entirely
in {q=0}. The quotient q has rank6 and positive type; write
q=x0*x1+x2*x3+x4*x5, with3 radical coordinates.

### Finite orbit reduction and exact linear algebra

The affine automorphism group preserving q is transitive on its zero
points. For completeness: the linear orthogonal group is transitive on
nonzero singular vectors, by extending each to a hyperbolic basis; and
on the first hyperbolic plane the affine map (x,y)->(1+x+y,y) preserves
xy and maps0 to(1,0). Thus move any point of P to0. P then becomes a
totally singular linear4-subspace. Its intersection with the3-dimensional
radical has dimension j=1,2,3. The orthogonal group on the active6-space,
GL on the radical, and radical shears are transitive for each j: project
P to a singular (4-j)-subspace of the active space, use a hyperbolic basis
to standardize it, and eliminate its radical graph by a shear.

It suffices to test the THREE representatives
P=span(e0,e2,...,e_(2t-2), first(4-t)radical vectors), t=1,2,3.
The checker additionally tests five affine presentations, redundantly.
For each P it solves the FULL linear system

    (1+q)h=1_P,   deg(h)<=3

on all512 points, using130 squarefree monomials. The t2/t3 systems are
inconsistent; t1 is solvable. The homogeneous solution space has
dimension10 and equals {q*l:l affine on9-space}. This is independently
verified by generating those10 independent polynomials. Consequently
all solutions for t1 give equivalent lifts, under z->z+l(x).
The resulting exceptional cubic support E has weight256 and spans10.

The checker computes rank nu5(E)=245 and affine-evaluation rank11.
Thus K=nu5(E)^perp has dimension11 and consists EXACTLY of affine
functions on E. It follows that E admits NO nonaffine graphlift: every
higher-dimensional realization injectively projecting to E remains in
an affine10-flat. This is the terminal exceptional class.

At n=9 the support is a balanced quadratic on9 variables. A balanced
quadratic has a radical direction on which its derivative is1; quotient
by that direction is injective. It compresses to dimension8, where256
points fill the entire cube.

Reversing the injective quotients therefore gives precisely two types:
(1) iterated graphlifts of F2^8; (2) the exceptional cubic E in an affine
10-flat. In type(1), every graph coordinate is a quadratic function of
the original8 coordinates: using only original-coordinate moments of
degree<=5 shows its truth vector belongs to RM(2,8). Hence quadratic
graph relations separate every outside point, i.e. type(1) is2-closed.
Type(2) is3-closed, since E has a cubic indicator in its10-flat and affine
linear equations detect points outside that flat. This proves the claim.

## III. Mixed-radical bounds for small KT quotients

For a symmetric difference T_s of two7-flats meeting in an s-flat,
write coordinates (x,y,r), x,y in F2^(7-s), r in F2^s. The mixed-moment
lemma of `agent4_mixed_moments_first_gap.md`, iterated over the s radical
coordinates, gives cross-part minimum

    B(5,s)=32-2^s.

Indeed an unequal pair of slices has difference minimum B(d,s-1),
while equal nonzero slices have twice minimum B(d-1,s-1).
A relation supported outside T_s with k<32 lies in span(T_s), by I.
If k>2^s but k<32-2^s, it cannot be supported in the common s-flat and
cannot have a nonempty cross part, so is impossible.

We will use:
T252 (s1): outside k=4,6,8 impossible.
T248 (s2): outside k=6,8,10 impossible.
T240 (s3): outside k=10,12,14 impossible.
T240 also has a KT quadratic type; it is2-closed and so forbids k<16.

## IV. Dimension reduction for weights260,264,268

For any of these weights, pair counting compresses to dimension15.
There Q is affine with Q(0)=0. If there is no injective direction and
Q=0, the pair count is >=65534. If Q is nonzero linear, the pair count
is >=16384+2*16383=49150. Both exceed C(268,2)=35778. Thus all these
weights compress to dimension14, where Q=0 and every k is even.
This evenness persists under further injective quotients, by embedding
back into14. Work henceforth in dimension<=14.

For260, quotient k2 has weight256 and is forbidden by II (minimum8).
The remaining small possibilities are k4->252, k6->248, k10->240,
all forbidden by III. Strict KT excludes every other positive k<18.
Therefore every positive difference multiplicity is >=18. Since
C(260,2)=33670<18*(2047), injective quotients continue to dimension10.
Every cubic on10 variables has weight divisible by8, excluding260.
This divisibility follows directly by expanding integer XOR weights:
a product of j cubic monomials contributes a multiple of
2^(j-1+max(10-3j,0)), always divisible by8.

For264, k2->260 is now excluded. The small possibilities
k4->256, k6->252, k8->248, k12->240 are forbidden by II/III.
Thus positive k>=20, and C(264,2)=34716<20*2047 compresses to10.
In dimension10 the quotient indicator q is quadratic on9 variables.
For k20 it has weight224. The outside indicator (1+q)h has degree<=5
on9 variables, and has weight20. This is impossible: such a nonzero
word has minimum16 and next weight24 by strict KT. All other positive
possibilities are now k>=36 (quadratic9 weights are0,128,192,224,240,
256,272,288,320,384,512). Since34716<36*1023, another injective
quotient reaches9. But no quadratic9 has weight264. Contradiction.

For268, use the preceding two absences. Small possibilities are
k6->256, k8->252, k10->248, k14->240, again impossible; k2->264
and k4->260 are absent. Thus positive k>=22 and
C(268,2)=35778<22*2047 compresses to10. There k22->224 would give
a degree<=5 word on9 variables of weight22, impossible between16
and24. All remaining positive k>=38; since35778<38*1023, compress
to9, where quadratic weight268 is impossible.

Hence260,264,268 are UNIVERSALLY absent at coorder7.

The orbit checker is an actual exact computation, not a claimed output:
it builds the130-column system, verifies every equation of its solution,
checks the10 kernel generators, performs all1023 difference-direction
tests for E, and verifies rank245 and affine rank11. Its assertions all
passed in under1second. Classical KT and elementary orbit arguments
are mathematical inputs and are not claimed to follow from enumeration.
