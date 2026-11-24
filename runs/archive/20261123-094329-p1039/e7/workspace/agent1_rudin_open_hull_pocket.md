# Verified strengthening of the Rudin-Klein-bottle candidate

Let M be Rudin's totally real Klein bottle, and p=(4,0). Agent2's winding argument establishes p in the rational hull r(M). Agent1's exact Sturm calculation proves dist(p,M)>sqrt(3).

For a sufficiently small delta>0, K_delta={x:dist(x,M)<=delta} is a smooth strongly pseudoconvex compact domain: squared distance to a compact smooth totally real submanifold is strictly plurisubharmonic on a sufficiently small tubular neighborhood. Its interior is connected, and K_delta is its closure. We may require delta<1/2.

For every translation a with ||a||<delta, M+a is a subset of K_delta. Rational hulls are translation-equivariant and monotone. Therefore

    p+a in r(M+a) subset r(K_delta).

Consequently B(p,delta) is contained in r(K_delta). Moreover, for x in B(p,delta),

    dist(x,M) >= dist(p,M)-||x-p|| > sqrt(3)-delta > delta,

so B(p,delta) is disjoint from K_delta. Thus this candidate has a genuine OPEN rational-hull pocket outside the compact domain:

    B(p,delta) subset int(r(K_delta)) minus K_delta.

This is a geometric/rational-convexity conclusion ONLY. No theorem connecting this pocket to non-Oka behavior has been proved or verified in our work.
