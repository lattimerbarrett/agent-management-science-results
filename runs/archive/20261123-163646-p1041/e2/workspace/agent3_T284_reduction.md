# The weight-284 reduction and its final 16-case certificate

This note records the reduction using the team's previously checked inputs:
weights 260,264,268,276,280 are globally absent; all weight-272 supports
are degree-three closed; all weight-256 supports are either iterated
quadratic graph lifts of an 8-flat or one of the exceptional terminal
256 supports; and strict-below-twice-minimum Kasami–Tokura forms are
available. The exceptional relative-gap input is independently proved
in `agent3_exceptional256_relative_gap.md`.

## Compression to dimension ten

At dimensions at least 16, C(284,2)=40186<65535 gives an injective
quotient direction. At dimension 15, the pair-parity Q is linear with
Q(0)=0. If every direction were a difference, Q=0 would require at
least 65534 pairs; a nonzero Q would require at least 49150 pairs.
Both exceed 40186. Hence any weight-284 support compresses to dimension
at most 14. There Q=0, so every collision multiplicity k is even.

For a positive k<30, the parity quotient has weight 284−2k.
The following list exhausts the possibilities:

* k=2,4,8,10,12 give weights 280,276,268,264,260, already absent.
* k=6 gives weight 272; degree-three closure and the separator lemma
  forbid an outside ν5 collision of size less than eight.
* k=14 gives weight 256. Quadratic graph classes are degree-two closed
  and forbid outside collisions of size less than sixteen. For an
  exceptional terminal class, its span is ten. Any collision word
  leaving that span would have at least 32 points outside it, so P14
  stays inside; the exceptional relative-gap theorem forbids P14.
* k=16 gives weight 252, whose cross-point minimum is 30 and whose
  omitted common radical has only two points; k=18 gives weight 248,
  with cross minimum 28 and common radical four. Both are impossible.
* k=22 gives weight 240. Its Type-II form has cross minimum 24 and
  common radical eight. Its quadratic Type-I form lives in dimension
  nine; P22 must stay there (outside minimum 32), and then
  P=(1+q)h has degree at most five, so is a coorder-four word. Weight
  22 lies strictly between its minimum 16 and second weight 24.
* k=20,24,26,28 give 244,236,232,228, excluded by strict KT.

Thus every positive k is at least 30. The number of represented
nonzero directions is at most floor(40186/30)=1339<2047. Therefore
injective quotients compress any such support to dimension ten.

If it is irreducible there, some direction has k≤39, by averaging
40186 over 1023 nonzero directions. The quotient is a quadratic
function in nine variables. Its possible weights below 284 are
0,128,192,224,240,256,272. The preceding exclusions and k≤39 leave
only k=30, quotient weight 224. This quadratic has the canonical form
q=x0x1+x2x3+x4x5, with three radical variables.

## Reduction of the remaining P30 forms

Write the two slices of a cubic lift as h and h+q. The collision set is
P=(1+q)h, degree at most five in nine variables, weight 30.
Strict KT for coorder four says P=A4△B4, two affine 4-flats meeting
in one point p. The quadratic q vanishes on A4\{p} and B4\{p}; a
quadratic on a 4-flat cannot be supported on only one point, so it
vanishes on both entire flats, including p.

Move p to zero by the q-preserving affine map
phi_p(x)=x+(B(p,x)+1)p, since q(p)=0. The 8-dimensional span W=A+B
is then a hyperplane, and q|W is purely bilinear between the two
4-dimensional axes. Write its mixed matrix rank as t, so its polar
rank is 2t. Put j=dim(W∩Rad(q)). Restricting a rank-six quadratic
with 3-dimensional radical to a hyperplane gives exactly:

* t=3,j=2: W does not contain the full radical;
* t=2,j=3: W contains the full radical.

In the abstract source coordinates (a∈F2^4,b∈F2^4), put
q_W=sum_{i<t}a_i b_i. Its radical has dimension 8−2t. The subspace
J mapped to the ambient radical has dimension j. Every J is enumerated:
for t=3 it is the unique full two-space; for t=2 it is any of the
15 three-subspaces of a four-space. Once J is specified, choose a
complement and use the standard hyperbolic/radical embedding. Witt
basis extension, radical shears, and ambient radical changes show that
these 16 embeddings cover all possible placements of W (with possible
redundancy). No orbit is discarded by a numerical heuristic.

## Exact finite certificate

The standalone file `agent3_T284_q224_P30.py` enumerates all 16 J,
constructs an injective 8-to-9 coordinate map, verifies q on ALL 256
source points, and forms P=A4△B4. For each P it solves the FULL
linear system for all 130 squarefree monomials of degree ≤3 in h:
  h(x)=1_P(x) for every x with q(x)=0.
Every one of the 16 systems is inconsistent. The coefficient and
right-hand-side elimination is exact binary integer arithmetic.
`agent3_T284_q224_P30.json` saves every J, P and outcome.

Consequently this last branch is impossible, and under the explicitly
listed earlier team inputs, weight 284 is globally absent. This does
not establish the requested no-fixed-list theorem; that main theorem
still requires an actual spectral change between dimensions 14 and 15.
