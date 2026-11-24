# Greedy triangle lemma for a >=1/9, and resulting mixed-model upper bound

Assume 1/9<=a<=1/4, b<(1-sqrt(a))², and the feasible mixed weighted
model from the team reduction. Red-loop vertices R form a pure-red clique,
of weight r<=a, blue-loop vertices B have weight s=1-r. Let c=1-b and
c0=2sqrt(a)-a, so c>c0>1/2. For i in B put q_i=int_R p_ix².
Symmetry and the red-loop norm caps imply int_B q_i<=T=r(a-r).

Choose v0 minimizing q_i in B, then v1 minimizing q_i in the red-support
neighborhood N(v0) within B. Set q0=q(v0),q1=q(v1), so q1>=q0.
Every blue-loop row i has transformed degree int(2p_ij-p_ij²)>=c.
Its red-support neighborhood within B therefore has mass at least c-r,
so N(v0) is nonempty. Since every vertex outside N(v0) has q>=q0,
we have (c0-r)q1+(1-c0)q0<=T. Consequently
 S=q0+q1<=T/min(c0-r,1-c0)<=r*a/(1-c0)=r*z,
where z=a/(1-c0)=[sqrt(a)/(1-sqrt(a))]²<=1.

For any selected blue-loop row i, its R transformed-degree contribution
is at most f(q_i)=2sqrt(r q_i)-q_i, by Cauchy. Hence its red-support
neighborhood inside B has mass at least c-f(q_i). The two selected vertices
have common B red-support neighborhood mass m bounded below by
 m >=2c-s-f(q0)-f(q1)
   >2c0-1+r-[2sqrt(2r S)-S]
   >=2c0-1+r[1-2sqrt(2z)+z].
Here S<=rz<=r<2r, where 2sqrt(2r S)-S is increasing in S.
If the bracket is nonnegative then m>0 immediately. Otherwise r<=a gives
 m> E(sigma)=2c0-1+a[1-2sqrt(2z)+z], sigma=sqrt(a).
For sigma in[1/3,1/2], using sqrt(2)<3/2 gives
 (1-sigma)² E(sigma) >=P(sigma)
 :=3sigma^4+3sigma^3-10sigma²+6sigma-1.
P is concave on this interval because P''<=-2, while
P(1/3)=1/27 and P(1/2)=1/16. Thus m>0, producing a red-support
triangle of blue-loop vertices.

But such a triangle is impossible. Put t=(a+c)/2. We have t>sqrt(a)>=1/3,
and each blue-loop row has ordinary red degree d_i>=1-sqrt(b)>t.
For any red clique of k=3 blue-loop rows choose lambda_i=1/(d_i-t),
L=sum lambda_i. Summing row norm and red pair caps gives
 ||sum lambda_i f_i||²<=aL²+2L.
Cauchy gives the lower bound (tL+3)². Therefore
 (t²-a)L²+(6t-2)L+9<=0,
impossible since every coefficient is positive.

This proves the full weighted mixed-model book frontier for a>=1/9.
In the requested Ramsey parametrization this covers alpha>=1/4,
provided the weighted-model regularity/counting reduction is supplied.
