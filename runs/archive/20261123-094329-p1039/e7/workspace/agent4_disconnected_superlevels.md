# Negative control: rank-two entire maps can have disconnected superlevels
Take an attracting quadratic Henon basin B, with a Fatou--Bieberbach parametrization (h,g): C^2 -> B. The standard escape cone implies B lies in the horn |g|<=max(|h|,R0), with R0>=1.
Define G=(exp(h^2), exp(h^2)g). Its Jacobian is 2h exp(2h^2) times the nonvanishing Jacobian of (h,g), hence G is nondegenerate.
On Re h=0, writing h=iy, the squared norm is at most exp(-2y^2)(1+max(y^2,R0^2)) <=1+R0^2. For y^2<=R0^2 this is immediate; for y^2>=R0^2 use exp(-2s)(1+s)<=1 (its derivative is negative).
The nonconstant entire scalar function h takes every complex value except possibly one, by restricting to a complex line where it is nonconstant and applying Picard. Thus for arbitrarily large T, both h=T and h=-T occur. At those points ||G||>=exp(T^2).
For L>sqrt(1+R0^2), G^{-1}({||z||>L}) consequently has nonempty portions in Re h>0 and Re h<0 but no point with Re h=0. It is disconnected.
This refutes the proposed universal connectivity lemma. It is NOT a target Oka counterexample.

## Stronger negative control: finite source curves / psh hulls
Let C=sqrt(1+R0^2), L=4C, and f(h)=(exp(-h^2)-exp(-2h^2))/h^2, extended by f(0)=1. This f is entire.
If ||G||>L then |h|>1, since for |h|<=1 the horn gives ||G||<=e*C<4C. Put r=|h|>1 and a=exp(-Re h^2). The horn gives ||G||<=exp(Re h^2)*C*r, hence a<C*r/L=r/4. Consequently |f(h)|<=a*(1+a)/r^2<1/(4r)+1/16<5/16.
At h=iy with y nonzero, f(iy)=exp(y^2)*(exp(y^2)-1)/y^2>1. Thus v=max(log|2f(h)|,-1) is a global continuous psh function, positive at separator points h=iy (where G has full rank), but negative on {||G||>L}.
Therefore the psh hull of the outside-ball preimage need not contain such a regular point. Also no compact bordered source curve through such a point can have its whole boundary in that outside-ball preimage, by the maximum principle for v restricted to the curve. This refutes the proposed generic finite-source-curve selection lemma as well.
