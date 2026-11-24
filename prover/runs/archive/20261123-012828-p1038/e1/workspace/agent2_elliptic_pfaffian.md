# A proved elliptic Schur–Pfaffian identity

Fix r,R,d>0, r<R. Let E be the smooth compactification of
r(x-x^{-1})-R(y-y^{-1})=2d,
and put q=r/R, z(P)=y(P)/x(P), σ(x,y)=(-1/x,-1/y).
For points P_i=(x_i,y_i) define the skew kernel
K_ij=(y_j-y_i)/(1+x_i x_j).

## Theorem
For 2n generic points of E,

Pf(K_ij) = q^{-n(n-1)} [∏_{i=1}^{2n} z_i^{-(n-1)}] ∏_{i<j} K_ij.

By rational continuation this holds whenever both sides are defined.
In particular, for distinct positive points ordered by increasing x (equivalently
y), every even principal Pfaffian is strictly positive.

## Geometry used in the proof
The birational coordinates z=y/x,
η=[r(x+x^{-1})-R(y+y^{-1})]/2 satisfy
η²=d²+r²+R²-rR(z+z^{-1}).
The double cover has four distinct branch points 0,t,1/t,∞, where
0<t=2rR/(d²+r²+R²+sqrt((d²+r²+R²)²-4r²R²))<1.
Thus E has genus one. The original bidegree-(2,2) compactification is smooth,
since its arithmetic genus is also one.

Let A=(∞,0), B=(∞,∞), C=(0,0), D=(0,∞). Then
 div x=C+D-A-B, div y=C+A-D-B, div z=2A-2D.
For fixed generic P, as a function of Q,
 div_Q K(P,Q)=P-σP+A-D.
Indeed Y-y(P) vanishes at P and ι_xP and has poles D,B;
1+x(P)X vanishes at σP and ι_xP and has poles A,B.
The common point ι_xP cancels.

Subtracting the curve equations at P and Q gives
 (y_Q-y_P)(1+y_P y_Q)/[(x_Q-x_P)(1+x_P x_Q)]
 =q y_P y_Q/(x_P x_Q).
Consequently
 K(P,Q) K(P,σQ)=-q z(P).                                      (1)

## Induction proof
The case n=1 is tautological. Fix P_1,…,P_{2n-1} generically and let Q=P_{2n}
vary. Call the Pfaffian F(Q) and the asserted product G(Q).
Both have possible simple poles at σP_j. Their residues there agree:
expand the Pfaffian along its last column; its j-term has sign (-1)^{j+1}.
In the product, pair K_ij with K_iQ and use (1). The i<j factors give
-q z_i and the i>j factors give +q z_i, yielding sign (-1)^{j-1}
and q^{2n-2}∏_{i≠j}z_i. Since z(Q)=1/z_j at Q=σP_j, the remaining prefactor is
 q^{-n(n-1)+2n-2}∏_{i≠j}z_i^{-(n-2)}
 =q^{-(n-1)(n-2)}∏_{i≠j}z_i^{-(n-2)},
exactly the induction prefactor for the smaller Pfaffian.

The only remaining possible pole of F-G is a simple pole at D. For G this
follows from
 (2n-1)(A-D)-(n-1)div z=A-D;
for F it is immediate term by term. Both vanish at A.
A meromorphic function on a genus-one compact curve cannot have a single
simple pole: multiply by a nowhere-vanishing holomorphic differential and use
the residue theorem. Hence F-G is holomorphic and constant. It vanishes at A,
so it is zero. This proves the identity for every n.

## Exact computational checks
`agent2_elliptic_pfaffian.py` clears denominators in the four-point identity
and reduces it *formally*, with free q,t,x_0,…,x_3, modulo
 y_i²=[q(x_i-x_i^{-1})-t]y_i+1.
All15 potentially nonzero remainder coefficients are exactly zero.
It also checks50 examples through ten points at150 digits; the analytic
induction, not those numerical examples, proves arbitrary size.

## Remaining gap
No identity between the original normalized Atiyah determinant / its cyclic
blocks and a (possibly confluent) Pfaffian or Pfaffian-Hafnian built from this
kernel has been established. This is a new proved positive kernel identity,
NOT yet a solution of the requested eventual nonvanishing theorem.
