# Mixed-loop elimination when the maximal blue-loop red clique has >=4 vertices

Assume 1/12 <= a <=1/4. Let R be the pure-red-loop clique of mass r,
s=1-r, and suppose the blue-loop rows satisfy ||1-f_i||²<=b; put c=1-b.
Choose a blue-loop vertex v minimizing q_R(v)=int_R f_v². The red-loop
norm conditions and symmetry imply q_R(v)<=r(a-r)/s.
Extend v to any maximal red-support clique S of BLUE-loop vertices,
with k>=4. Let F=sum_{i in S}f_i, X=int_B F,Y=int_R F. Put
m(x)=min_{i in S}f_i(x) on R, and m=0 on B, and u=int_R m.
Then u<=r t, t=sqrt((a-r)/s).

On every column in B at least one of the k entries vanishes.
On R, subtracting m makes at least one vanish. Pointwise Cauchy yields
||F-m||²+(k-1)||m||² <=(k-1)sum ||f_i||².
Using partitioned Cauchy, ||m||²>=u²/r and row blue-book caps gives
 c <= c1 := [2(X+Y)-u²/r-(X²/s+(Y-u)²/r)/(k-1)]/k.
Summing all pairwise red-book caps also gives
 c <= c2 := [2(X+Y)+k(k-1)a-X²/s-Y²/r]/k.
(The r=0 case is already the pure-blue lemma.)

Write K=k-1, A=sqrt((k-2)/(k K² a)), d=(1-A)/(k-2), lambda=K d.
We have 0<=lambda<=1: A<=1 since (k-2)/(k K²)<=1/18<1/12<=a,
and A>=1/K since a<=(k-2)/k. Put B0=k-K²d=k-K lambda>=1.
A direct complete-square identity is
 lambda*c1+(1-lambda)*c2
 = g_k(a)+d/(kA)*(2u-B0*u²/r)
   - A/k*[(X-s/A)²/s+(Y-(r+d*u)/A)²/r],
where g_k(a)=2K sqrt(a)/sqrt(k(k-2))-K*a/(k-2).
Consequently c<=g_k(a)+2r*d*t/(kA).

Put x=1/(k-2)<=1/2, sigma=sqrt(a). Algebra gives
 d/(kA) <= x*sigma*(1+x)/sqrt(1+2x) <=3*x*sigma/(2sqrt(2)).
Also r*sigma*t <=a²/2. To see the latter set t=sigma*z, 0<=z<=1.
The assertion is equivalent to 2z(1-z²)<=1-a z².
If z²<=1/2, the left side is <=4/(3sqrt(3))<7/8<=the right side;
if z²>=1/2, the left side is <=1/sqrt(2)<3/4<=the right side.
Thus
 c<=g_k(a)+3a²*x/(2sqrt(2)).
The right side is convex in x on [0,1/2], since g_k''(x)
=2sigma(1-x)/(1+2x)^(5/2)>=0. Therefore
 c<=max{g_infty(a),g_4(a)+3a²/(4sqrt(2))}.

Let sigma0=4/sqrt(3)-2. For sigma<=sigma0<31/100,
 g_3-g_4-3a²/(4sqrt(2))
 =sigma[4/sqrt(3)-3/sqrt(2)-sigma/2-3sigma³/(4sqrt(2))]>0.
Indeed even replacing the last coefficient by twice its value gives a
positive bracket, using 4/sqrt(3)>2309/1000, 3/sqrt(2)<2122/1000,
3/(2sqrt(2))<1061/1000 and sigma<=31/100.
For sigma>=sigma0>3/10,
 g_infty-g_4-3a²/(4sqrt(2))
 =sigma[2-3/sqrt(2)+sigma/2-3sigma³/(4sqrt(2))]>0:
the bracket is increasing on [3/10,1/2] and positive at 3/10.
Hence ALWAYS c<=max{g_3(a),g_infty(a)}.

For a<=1/12 enlarge a to1/12; the same hypotheses hold and the conclusion
is c<=1/2. This eliminates every mixed model for which this chosen maximal
blue-loop red clique has k>=4. Only the k<=3 cases remain.
