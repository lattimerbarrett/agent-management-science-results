# A quadratic-closure relative gap and the reduction excluding weight 292

## General relative-gap lemma

Let S⊂F2^n satisfy cl2(S)=S, and let P be disjoint from S with
sumν5(P)∈spanν5(S). If 0<|P|<24, then |P|=16.

For any polynomial L of degree≤2 vanishing on S, multiply the original
relation by L times each monomial of degree≤3. The selected subset
A_L={p∈P:L(p)=1} is 3-even. A nonzero 3-even set has minimum weight
16 and second weight 24. Since |P|<24, each A_L is empty or size 16.
For two distinct nonempty A_L,A_M, their symmetric difference is the
nonempty 3-even set A_(L+M), so it has at least 16 points. But two
16-subsets of a set of size less than 24 have symmetric difference
at most 2|P|−32<16, a contradiction. Thus all nonempty selected sets
are identical. Quadratic closure says that every p∈P is separated by
some such L, so their union is P. Hence P is that 16-point set.

In particular, no quadratic-graph weight-256 support has an outside
ν5 collision of size 18, 20, or 22. This is stronger than the usual
minimum-only separator bound 16.

## Exceptional weight-256 supports: divisibility of small collisions

For each exceptional E32⊂F2^7, all 10668 affine 5-flats were enumerated
by `agent3_E32_5flat_intersections.py`. For EACH of the three base
orbits, the COMPLETE intersection histogram is
  size 0:13; 4:764; 6:2624; 8:3930; 10:2592;
  12:636; 14:96; 16:13.
In particular every affine 5-flat has at least sixteen points outside
E32.

Consider P disjoint from E32×F2^3, with a ν5 relation, 0<|P|<32.
Its fibre-parity vector is a relative ν5 relation on the base. The
associated coorder-six word has size at most 32+|P|<64 and is zero.
So all fibres are even. Each first-free-coordinate moment has outside
support at most |P|/2≤15. Its relative ν4 relation gives a coorder-five
word h in seven variables of size at most 47; if nonzero it must be
a 32-point affine 5-flat. The histogram says h has at least sixteen
outside points, impossible. Therefore all first moments vanish.
The fibres are 1-even subsets of F2^3, with weights 0,4,8. Consequently
|P| is divisible by four. In particular P18 is impossible.

Combining this with the general lemma shows that EVERY weight-256
support forbids outside ν5 collisions of size eighteen.

## Weight-272 collision P10

The team's classification says every 272 support is terminal and is
one of the following, up to affine equivalence:
* a degree-two-closed quadratic support in dimension nine;
* B68×F2^2 in dimension ten, B68 a coorder-five word in eight
  variables of weight 68;
* B34×F2^3 in dimension eleven, B34 a coorder-four word in eight
  variables of weight 34.

For the first, P10 is below the relative minimum sixteen.
For B34×F2^3, fibre parity gives a coorder-six base word of size≤44,
hence zero. A first moment has outside size m≤5 and gives a coorder-five
word h of size≤39, hence h32. Then B34+h is a nonzero coorder-four
word of weight 2+2m≤12, below minimum sixteen. Thus first moments
vanish. Every fibre is 1-even in F2^3, so |P| is divisible by four,
not ten.

For B68×F2^2, fibre parity gives a coorder-six word h of size≤78,
hence h64 if nonzero. Then B68+h has coorder five and weight
4+2m≤24<32, impossible. A first moment has outside size m≤5 and
gives a coorder-five h with |h|≤73. If h32, then B68+h has weight
36+2m, between 38 and 46, excluded by strict KT. If |h|≥48, this
sum has weight at most 68−48+10=30<32. Thus all first moments vanish;
a 1-even fibre in F2^2 is empty or full, again making |P| divisible
by four. Therefore every weight-272 support forbids P10.

## Reduction for a hypothetical weight-292 support

This final step assumes the team's remaining quadratic-graph P16
checks have established that ALL weight-288 supports are degree-four
closed; that numerical branch must not be silently omitted.

First compress to dimension≤14 using pair counting and linear pair
parity at dimension fifteen, as for weight 284. All collision
multiplicities k are then even. For positive k<26:
* k2 gives weight288, forbidden by degree-four closure (relative
  minimum four).
* k4,6,8,12,14,16 give absent weights284,280,276,268,264,260.
* k10 gives weight272/P10, forbidden above.
* k18 gives weight256/P18, forbidden above.
* k20 gives weight252/P20, below cross minimum30 but beyond radical2.
* k22 gives weight248/P22, below cross minimum28 but beyond radical4.
* k24 gives weight244, excluded by strict KT.
Thus every positive k is at least 26. Now
  C(292,2)=42486, floor(42486/26)=1634<2047.
So repeated injective quotients compress the support to dimension ten.
But RM(3,10) weights are divisible by eight, whereas 292≡4 mod8.
This contradiction proves global absence of 292 once the stated
weight-288 closure input is certified. Complementary k1/Q arguments
then give global absence of 294. This note does not prove the main
no-fixed-list assertion.
