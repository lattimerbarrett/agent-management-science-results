# Universal periodic obstructions for coorder-seven supports

This note proves only obstructions to proposed constructors. It does NOT prove
that the full RM spectrum stabilizes or changes, and does NOT finish the user problem.

Notation: K_d(T) is the space of binary functions supported on T whose moments
against all squarefree monomials of degree at most d vanish. Thus a coorder-c
support has indicator in K_(c-1). A d-closure point p outside T means
nu_d(p) lies in the span of nu_d(T). Equivalently, there exists a function h
supported on T union {p}, with h(p)=1, whose moments through d vanish.

We use the already established minimum distance and strict-below-twice-minimum
KT weight theorem. For coorder six, the only possible nonzero weights below112
are64 and96. The machine-checkable arithmetic is in agent4_periodic_obstructions.py
and its JSON. The list used there is an overestimate of the KT spectrum; this
is harmless for excluding decompositions.

## 1. Product/graph identities

Write a periodic support as S=T x F2 with free coordinate r. A function supported
on S is h(x,r)=u(x)+r v(x). Summing over r shows

    h in K_d(S) iff u in K_(d-1)(T), v in K_d(T).

Here identifying u,v with their zero extensions outside T is understood.
The graph of a label h on a coorder-seven support S is again coorder seven iff
h belongs to K_5(S). This is immediate by splitting moments according to whether
they contain the new coordinate.

The degree-d closure of T x F2 is exactly cl_d(T) x F2. Indeed its Veronese
column at (p,r) is (nu_d(p), r nu_(d-1)(p)); the span of product columns is the
direct sum of the spans of nu_d(T) and nu_(d-1)(T).

## 2. Weights308,324,328,332,336: universal closure and preserved periods

Let n be154,162,164,166,168, and let T be ANY coorder-six support of weight n,
in ANY ambient space. A nonzero proper member of K_5(T) would partition T into
two nonzero coorder-six supports of weights a,b with a+b=n. Both sides are at
least64 and at most104, hence each must be64 or96. None of these n is128,160,192.
Consequently K_5(T)=<1_T>.

If p were an outside5-closure point, the witnessing h and h+1_T would be nonzero
coorder-six supports with weights summing n+2 (the point p is in both). Each side
is at least64 and at most106, so again each is64 or96, whose sums are128,160,192.
None equals n+2. Hence cl_5(T)=T.

Now S=T x F2 has weight2n. Every valid graph label is u(x)+c r, where c is
constant, by the tensor identity and K_5(T)=<1_T>. Its graph therefore retains
the period (0,1,c). For ANY number of simultaneous graph coordinates, each label
is still in the original K_5(S), so the common period is (0,1,c1,c2,...).
Thus arbitrary iterated graph lifts of ANY periodic support of weight
308,324,328,332,336 remain periodic. Every periodic support of any of these
weights is5-closed, by the quotient/product closure identity above. In particular
no member of these graph families admits a one-double-fiber lift producing
310,326,330,334, respectively.

Also a periodic support of weight divisible by4 has even unordered difference
multiplicities in every direction: translation by its period pairs up pairs,
except in the period direction itself, whose multiplicity is half the weight
and hence even. Therefore no periodic336 support has a k=1 quotient of weight334.

## 3. Weight320: all periodic graph families are stably5-closed

Let T be coorder six of weight160. The same outside-point argument uses a+b=162,
so cl_5(T)=T. Every nonzero proper v in K_5(T) has weights64 and96 on its two
parts, by KT. Write the64 part F and96 part Q. F is an affine6-flat; Q is the
second-weight quadratic support on its affine8-span. There exists a degree2
polynomial L which is1 on F and0 on Q. To see this, the quadratic indicator q
of Q is0 on F intersect aff(Q), since F and Q are disjoint; glue q on aff(Q)
with0 on F, extend the resulting quadratic to the ambient affine space, then
put L=1+q_extension. Quadratic gluing on two affine spaces is elementary: if
intersecting, use coordinates for their common subspace and private complements;
if disjoint, choose a separating affine linear coordinate and extend first on
their affine hull. In the disjoint case the degree2 extension of a quadratic
on one component and0 on the other need not always exist without a condition;
HERE F is disjoint from aff(Q), so an affine linear separator already gives L.

For any u in K_4(T), <u,v>=<u,1_F>=<u,L>=0; if v is the96 part use also
<u,1_T>=0. Constants cause no exception. Thus K_4(T) is orthogonal to K_5(T).
For S=T x F2, writing two K_5 labels as u+r v and u'+r v', their inner product
is <u,v'>+<v,u'>+<v,v'>. The first two terms vanish by the orthogonality just
proved, and the last does too because K_5(T) is contained in K_4(T).
Hence K_5(S) is self-orthogonal, while S is5-closed.

General inheritance: if S is5-closed and K_5(S) is self-orthogonal, every legal
graph lift remains5-closed and has self-orthogonal K_5. A closure point above
an old point p but in the wrong new fiber would require a relation a in K_5(S)
with <a,label>=1, impossible. Any new K_5 relation projects to an old one, so
self-orthogonality is inherited. Induct on the number of graph lifts.

Thus EVERY periodic320 support and EVERY iterated legal graph lift is5-closed.
This blocks the entire periodic320-to-new322 route, not just tested samples.

## 4. The288-K14 quadratic-extension route

The explicit ALL288-K14 classification checker is
agent4_T288_K14_periods.py/.json. Every source has a four-dimensional period
space and is B18 x F2^4, where B18 is coorder three. Strict KT/minimum distance
give K_2(B18)=<1> and K_3(B18)=0. Consequently every K_5 label on the product
has the form h(base)+a linear function of the four free coordinates, with
constant coefficients. Two such labels have common-one set of size divisible
by8: independent free linear parts give18*4=72; rank1 gives8 times a base count;
rank0 gives16 times a base count. Therefore a quadratic extension adding twice
that intersection to288 always has weight divisible by16. It cannot yield
324,328,332. If it yields320, at least two periods survive, so Section3 blocks
all subsequent322 graph-lift routes. These are universal consequences of the
checked source classification, not conclusions from random unsuccessful searches.
