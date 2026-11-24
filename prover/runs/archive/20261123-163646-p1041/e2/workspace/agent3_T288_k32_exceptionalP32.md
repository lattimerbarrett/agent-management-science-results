# Cubic weight-288 k32 branch: exceptional coorder-four P32 excluded

The parity quotient is T224={q=1}⊂F2^9, q=x0x1+x2x3+x4x5,
with radical F2^3. A cubic lift has collision support
P=(1+q)h of weight 32. It is a coorder-four word. This note handles
ONLY the exceptional boundary32 class, not all quadratic-graph32
classes. The latter remain a separate piece.

The coorder-four exceptional class is one of the three explicit
32-point bases B in `agent3_T280_P12_allorbits.json`; their affine
equivalence need not be assumed. They have affine span seven and
quadratic vanishing ideal of dimension five. Translate a chosen base
point to zero. For any embedding P in q=0, move its corresponding
point to zero by the q-preserving affine map
phi_p(x)=x+(B(p,x)+1)p. Thus the placement is a linear injective map
of the seven-dimensional source span. The restricted quadratic q_W
vanishes on the translated base B.

`agent3_P32_E32_quadrics.py` computes the ENTIRE degree-two vanishing
ideal at all 32 points. It enumerates all 31 nonzero quadratic forms
for each of the three bases, and computes their polar radicals and
Arf invariants by evaluating all 128 source vectors. In each case:
* eighteen forms have polar rank four, radical dimension three,
  vanish on the radical, and positive Arf invariant;
* thirteen forms have polar rank two, radical dimension five,
  vanish on the radical, and positive Arf invariant.
There are no other forms. The zero form cannot be the restriction:
a totally q-singular subspace in the ambient space has dimension at
most Witt index three plus radical dimension three, namely six.

Let rank(q_W)=2t and let R be its radical. Put
J=R∩(preimage of the ambient radical), dimJ=j. The nonsingular source
core is a positive 2t-space, consuming t ambient hyperbolic pairs.
R/J must embed totally singularly in the remaining 3−t hyperbolic
pairs, so r−j≤3−t, and j≤3. Consequently:
* t2,r3: j2 or j3; enumerate all 7 two-subspaces and the full three-space;
* t1,r5: j3; enumerate all 155 three-subspaces.
These conditions are also sufficient. Ambient orthogonal isometries
are transitive on the positive nonsingular core and on the remaining
totally singular subspace. Radical GL maps and radical shears cover
all choices of lifts. Thus enumerating J gives a complete list of
placements up to ambient q-isometry (with permitted redundancy).

`agent3_T288_k32_exceptionalP32.py` explicitly finds hyperbolic source
pairs of q-value zero by finite enumeration, constructs a radical
basis, enumerates every J by RREF, and complements J in R. It maps
the hyperbolic pairs to the first t standard ambient pairs, J to the
ambient radical, and the remaining radical basis to isotropic vectors
from the unused ambient pairs. For EVERY embedding it checks linear
injectivity and q-preservation on ALL 128 source points.

There are 18·8+13·155=2159 embeddings per base and 6477 overall.
For each image P32 it solves the FULL linear system for all 130 cubic
coefficients of h in nine variables:
  h(x)=1_P(x) for every x with q(x)=0.
EVERY ONE of the 6477 systems is inconsistent. No h exists, so no
lift arises from this exceptional P32 class. The source T224 has ν5
kernel dimension ten (affine-only), also directly checked; no hidden
nonaffine solution parameter is being discarded. In fact all systems
are inconsistent, so solution-space completeness is immaterial here.

The code performs exact binary elimination and contains no SAT timeout,
random search, or unproved numerical membership assertion.
This is a classification subbranch, NOT the requested main theorem.
