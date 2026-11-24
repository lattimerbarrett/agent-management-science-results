# Explicit totally real Klein bottle and rational-hull annulus

This file proves geometry and a curve obstruction only, NOT non-Oka of a complement.

Put g(phi)=2+cos(phi), h(phi)=sin(phi)+i sin(2phi), and
j(theta,phi)=(exp(2i theta)g(phi)^2, exp(i theta)g(phi)h(phi)).
The free involution (theta,phi)->(theta+pi,-phi) leaves j invariant and reverses orientation. Its quotient is a Klein bottle. The complex determinant of the two real tangent vectors is
2i exp(3i theta) g(phi)^3 h'(phi),
which is nonzero: h'=cos(phi)+2i cos(2phi), and cos(phi)=0 forces cos(2phi)=-1. Thus j is a totally real immersion.

To prove the induced map on the quotient injective, note w²/z=h(phi)². With c=cos(phi), its real and imaginary parts are R(c)=1-5c²+4c⁴ and I(c)=4c-4c³. If c!=d and R(c)=R(d), I(c)=I(d), then either c+d=0 and c²=1, or c²+d²=5/4, cd=-1/4. The latter forces max(|c|,|d|)=(sqrt7+sqrt3)/4>1 and is impossible. In the endpoint case c=1,d=-1, |z| is respectively 9 and 1, so images differ. Otherwise cos(phi)=cos(psi), hence psi=phi or -phi. The z coordinate determines theta modulo pi, and the w coordinate selects exactly the stated involution (including h=0 at endpoints). Therefore the quotient map is an embedding. Compactness makes its image K0 a smooth compact totally real Klein bottle.

Let A={(z,0):1<=|z|<=9}. If P is any entire function nonzero on K0, then P(z,0) is not identically zero and is nonzero on both boundary circles of A. The loops theta->P(j(theta,phi)), 0<=theta<=2pi, are all nonzero and homotopic as phi runs from 0 to pi. At phi=0 and phi=pi their winding numbers are respectively twice the number of zeros of P(z,0) inside |z|<9 and inside |z|<1, counted with multiplicity. Equality of winding numbers proves there are no zeros in 1<|z|<9. Thus no entire function can vanish at any p in A and stay nonzero on K0. In particular A is contained in the rational hull of K0.

Every ambient closed analytic curve through p in A meets K0, since a closed analytic curve in C² is the zero set of a global entire function (Cartan divisor theorem on C²).

A small squared-distance tube K_delta={dist(.,K0)²<=delta} is smoothly bounded and strongly pseudoconvex: squared distance to a smooth totally real submanifold is strictly plurisubharmonic on a sufficiently small tubular neighborhood; its gradient is nonzero on positive small levels. It is bounded, connected, and excludes p=(4,0) for small delta. The closed-analytic-curve obstruction persists because K0 is contained in K_delta.

The missing analytic step is an exterior-specific non-Oka obstruction (possibly via rational hulls). Generic entire-image closed-curve selection was subsequently REFUTED by the Hénon-basin negative control. This file DOES NOT assert any such step or conclude non-Oka.
