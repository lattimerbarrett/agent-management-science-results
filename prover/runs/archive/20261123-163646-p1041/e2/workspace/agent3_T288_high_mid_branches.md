# Two high-dimensional branches of weight 288

This note proves the numerical/classification pieces claimed by agent3,
not the main no-fixed-interval-list theorem.

## Inputs from the preceding team classification

Every weight-272 support compresses to dimension eleven. Its irreducible
dimension-eleven forms are the 48 explicitly constructed products
B34×F2^3, with B34⊂F2^8, |B34|=34. They are terminal: their ν5 kernel
is exactly the affine evaluation space. Its irreducible dimension-ten
forms are the 896 products B68×F2^2, B68⊂F2^8, |B68|=68, also terminal.
The remaining irreducible form lives in dimension nine, is quadratic,
and is degree-two closed.

For weight 288, all positive collision multiplicities below eight are
forbidden by the preceding global gaps. Thus any support compresses
to dimension at most twelve. An irreducible dimension-twelve support
has some k≤10 by averaging C(288,2)=41328 over 4095 directions, and
only k=8 survives; its quotient is one of the dimension-eleven 272
products. An irreducible dimension-eleven support has k≤20 and only
k=8 or k=16 survives. The k=16 branch is NOT handled in this note.

## Dimension twelve, k=8

Let T=B34×F2^3 be the quotient and P8 the outside collision set.
Write its fibres over B34 coordinates. Their parity vector is a
relative ν5 relation against B34. Such a relation gives a coorder-six
word in eight variables, of support at most 34+8<64, so it is zero.
Every fibre is even. Each first-free-coordinate moment is supported
on at most four base points and is a relative ν4 relation against B34.
It would give a coorder-five word h of support at most 38. Thus h is
a 32-point affine 5-flat. If this had any outside base points m≤4,
then h+B34 would have weight 34−32+2m≤10<16, impossible for coorder
four. Thus all first moments vanish. A 1-even subset of F2^3 has
weight 0,4,8. Therefore P8 is either one full fibre or two affine
4-point planes in distinct fibres.

Because |P|<16, the degree-two separator lemma also puts all base
points in E=cl2(B34)\B34. In EACH of the 48 cases the exact checker
`agent3_T288_highdim_P8_bases.py` finds |E|=6. The six reduced ν3
syndromes are nonzero and pairwise distinct. The second free moments
of a 4-point plane in F2^3 form a nonzero normal vector. For two such
planes, any nonzero coordinate would force either a single zero
syndrome or an equality of two syndromes. Both are impossible.
Hence P8 is a single full fibre, at one of the six extra points.

All 48×6=288 lifts are constructed by exact ν2 relations in the base.
`agent3_T288_highdim_actual.py` verifies every resulting 288 support
has affine rank twelve, ν5 kernel dimension thirteen (affine only),
and degree-four closure equal to itself. The full supports are
B36×F2^3 with B36⊂F2^9; base lists are in the JSON certificate.
Consequently every one of these high-dimensional classes is terminal
and degree-four closed.

## Dimension eleven, k=8

The quotient is B68×F2^2. Let P8 be the outside set. Its fibre parity
vector gives a relative ν5 relation against B68, and hence a coorder-six
quadratic word h in eight variables. Since its support has size≤76,
a nonzero h has weight 64. If its outside size is m≤8, then h+B68
is a nonzero coorder-five word of weight 68−64+2m≤20<32, impossible.
Thus fibres are even.

A first-free-coordinate moment has outside support m≤4, and gives a
coorder-five word h with |h|≤72. If |h|≥48, then h+B68 has weight
68−|h|+2m≤28<32, impossible. Otherwise nonzero h has weight 32;
then h+B68 has weight 36+2m, one of 38,40,42,44. Strict KT excludes
all these weights between 32 and 48. So all first moments vanish.
A 1-even subset of F2^2 is empty or the full four-point square.
Therefore P8 consists of two full fibres at distinct base points p,q.
The original ν5 relation is equivalent to
ν3(p)+ν3(q)∈span ν3(B68).

The original agent1 P24 cap enumeration checked all 896 quotient
forms but stored only twenty sample supports. To avoid an accidental
sample-only claim, `agent3_T272_q224_P24_allseeds.py` repeats that full
finite cap enumeration and retains EVERY one of the 896 supports.
`agent3_T288_mid_P8_bases.py` straightens the two free periods in each
support (checking both possible top-coordinate tilts explicitly),
extracts its 68-point base, and checks ALL 188 outside points. In each
case exactly fifteen pairs have equal nonzero ν3 syndromes.

`agent3_T288_mid_actual.py` constructs ALL 896×15=13440 lifts in the
base. For EVERY resulting B72⊂F2^9 it directly verifies:

* affine rank nine;
* dim ker ν3(B72)=10;
* dim ker ν4(B72)=1;
* dim ker ν5(B72)=0.

The full lift is B72×F2^2. The tensor-kernel dimension identity gives
  dim ker ν5(B72×F2^2)=0+2·1+10=12.
Its affine evaluation space has dimension twelve, so it is terminal.
It has a quartic indicator and is therefore degree-four closed.
All base lists and exact kernel dimensions are saved in the JSON.

## What remains for global degree-four closure of weight 288

The irreducible dimension-eleven k=16 branch must still be handled.
Once that branch is terminal/degree-four closed, every irreducible
weight-288 class of dimension eleven or twelve has the same property.
Classes that compress to dimension≤10 have degree≤4 graph-label
representations over their original base, so every iterated graph lift
is degree-four closed automatically. This would prove all weight-288
supports degree-four closed and exclude the weight-292 k=2 branch.
No assertion is made here about that remaining k=16 branch.
