# Audited dynamical countercheck
Let H(z,w)=(w,16w^2-z/4). It is a polynomial automorphism, inverse
H^{-1}(z,w)=(64z^2-4w,z), with det DH=1/4. Eigenvalues at 0
are +/- i/2; after linear conjugation (z,w)->(z,2w), the linear
part has Euclidean operator norm 1/2. Thus 0 has an attracting basin D.
The classical attracting-basin theorem makes D biholomorphic to C^2.
Choose a sufficiently small polynomially convex forward-invariant
ellipsoid E at 0. Then D=union H^{-j}(E), an increasing union of
polynomially convex domains, hence D is Runge.

For |t|=1 the first three iterates are
(0,-t/4), (-t/4,t^2), (t^2,16t^4+t/16).
The third has |w|>=255/16 and |z|=1. The open cone
|w|>max(|z|,1) is forward invariant and escaping, since
|w_new|>=16|w|^2-|z|/4 > 16|w|^2-|w|/4 > |w|.
Consequently D avoids the unit circle K={(t,0):|t|=1}, but contains 0,
which lies in its polynomial hull. This disproves the proposed
assertion that a Runge Fatou-Bieberbach domain avoiding K cannot meet
its hull. This is a countercheck, NOT a proof of the user's theorem.

All algebraic steps checked by agent4_basin_hull_check.py.
Uniform escape and compactness also imply D avoids a sufficiently thin
smooth strictly-pseudoconvex tube around that circle. For example use
(|z|^2-1)^2+|w|^2<=epsilon with sufficiently small epsilon>0; near that
tube the Levi eigenvalues are 4|z|^2-2 and 1, both positive.
