# Explicit open rational-hull pocket for the explicit KB tube
This uses the explicit defining function and Levi verification in agent1_rudin_explicit_candidate.md.

Let epsilon=2^-14, delta=2^-12, and K={R<=epsilon}. In square-root coordinates z=s²,w=sq put r=|s|, c=r-2, x=Re q,y=Im q, F1=c²+x²-1,F2=y-2cx,R=F1²+F2². On M, |s|>=1, |c|<=1, |x|<=1 and |q|<=5/4, because |q|²=(1-c²)(1+4c²)=25/16-4(c²-3/8)².

For an ambient translation a=(a_z,a_w) with ||a||<=delta, continue the square root along z+ta_z,0<=t<=1. Since |z+ta_z|>=1-delta>=1/2, the derivative bound gives |Delta s|<=delta/sqrt2<delta. Also |s'|>=1/sqrt2, so |Delta q|<=sqrt2(1+5/4)delta<4delta. Therefore |Delta c|<=delta, |Delta x|,|Delta y|<4delta. Since F1=F2=0 on M,
|F1'|<=10delta+17delta²<11delta,
|F2'|<=14delta+8delta²<15delta.
Hence R<=346delta²<epsilon on M+a. Thus every M+a with ||a||<=delta lies inside K.

Rational hull is monotone and translation equivariant. Since p=(4,0) belongs to the rational hull of M, p+a belongs to the rational hull of M+a and hence to the rational hull of K. Thus B(p,delta) is contained in the interior rational hull of K.

This entire ball is disjoint from K. For |z-4|,|w|<=delta, the square root near2 satisfies |s-2|<=delta, |s|>1; hence |q|<=delta, |c|<=delta and c²+x²<=2delta²<1/2. Thus R>=F1²>1/4>epsilon. Consequently B(p,2^-12) is an explicit open rational-hull pocket disjoint from K.

All scalar inequalities are checked exactly in agent2_rudin_pocket_checks.py. NO non-Oka consequence has yet been proved.
