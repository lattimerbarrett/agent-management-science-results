# Certified nondegenerate scale extrema for the quartic graph in every n>=32

This proves a finite-dimensional scale-sector statement only. It is NOT a nonlinear Yamabe noncompactness theorem.

Set d=(n-2)/2>3. In the common normalization where harmless positive angular constants are suppressed, put
g0=[Gamma(3/2)/Gamma(d+1/2)]^2, g1=[Gamma(2)/Gamma(d+1)]^2.
The exact mixed spectral moments are
A=(g0+g1)/(d-1),
B=[g0 p0+g1 p1]/[(d-2)(d-1)(2d+1)],
C=[g0 q0+g1 q1]/[(d-3)(d-2)(d-1)(2d+1)^2],
where p0=2d^2+d+8, p1=6d^2+3d+2,
q0=4d^4+165d^2-41d+114,
q1=36d^4+181d^2+19d+6.

These follow by telescoping the positive spectral sum. In detail x=(j+3)/2, R(x)=8(x-1)(x+d)/(2d+1)-1; for k=0,1,2 solve the polynomial identity
Q_k(x)(x+d-1)^2-Q_k(x+1)x^2=(2x+d-1)R(x)^k.
The script computes these Q_k symbolically and checks the identities identically in x,d. Sum separately over x=3/2,5/2,... and x=2,3,... . Multiplication by [Gamma(x)/Gamma(x+d)]^2 makes the right side telescope. The tails vanish when d>k+1. The displayed A,B,C are the endpoint evaluations at x=3/2 and 2, as checked by exact symbolic simplification.

Let t=g1/g0=(4/pi)[Gamma(d+1/2)/Gamma(d+1)]^2. For all d>0,
(d+1/4)t(d) < 4/pi.
Indeed the ratio at d+1 versus d is greater than one because
(d+5/4)(d+1/2)^2-(d+1/4)(d+1)^2=1/16>0,
and Stirling's formula gives the limit 4/pi along each unit-spaced sequence. The elementary bound pi>333/106 follows, for example, from the Machin identity pi=16 atan(1/5)-4 atan(1/239) and four terms of the alternating series lower bound for atan(1/5), with atan(1/239)<1/239. The script checks these rational inequalities and the tangent identity underlying Machin's formula.

Consequently 0<t<U=1696/[333(4d+1)]. Define
D(d,t)=4(d-3)(p0+t p1)^2-3(d-2)(1+t)(q0+t q1).
Then B^2/(AC)>3/4 iff D(d,t)>0. For d=15+e, e>=0, direct exact expansion gives:
(1) The coefficient of t^2 in D has strictly positive coefficients as a polynomial in e.
(2) The numerator of partial_t D(d,U) has strictly negative coefficients in e; its denominator is positive.
(3) The numerator of D(d,U) has strictly positive coefficients in e; its denominator is positive.
All three coefficient-sign assertions are checked with exact integers by the script. Since partial_t D is increasing in t but negative at U, D decreases throughout [0,U]. Hence D(d,t)>D(d,U)>0 for every d>=15, proving B^2/(AC)>3/4 for every real n>=32.

For b>0, the reduced scale polynomial E(z)=-Az+2bBz^2-b^2Cz^3, z=lambda^2, has the two distinct positive critical points z_plus/minus=(2B plus/minus sqrt(4B^2-3AC))/(3bC). The smaller is a nondegenerate local minimum, the larger a nondegenerate local maximum. No assertion about tangential translations, nonlinear error estimates, or infinite gluing is made here.
