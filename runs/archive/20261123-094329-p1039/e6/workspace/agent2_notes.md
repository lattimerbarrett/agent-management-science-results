# Audited necessity reductions and obstructions

## No bounded complementary component
If a bounded component U of Y were present, choose p in U and a nonzero vector a with |a|<dist(p,C^n\\U)/4, so p+az is in U for |z|<2. CAP on the closed unit disk, with error <|a|/2, would give an entire F:C->Y. Its connected image lies in U since F(0) is in U, hence it is constant by Liouville. But |F(1)-F(-1)| >= 2|a|-2 epsilon >0. Contradiction.

## A smooth nonpseudoconvex obstacle with a PSH-Liouville exterior
Write z=(t,w) in C x C^(n-1), n>=3. Put
K={ |w|^2+|t|^4-|t|^2 <=1 }.
The defining function is proper. Its only critical levels are -1 and -5/4, so its zero level is smooth. K is connected: each nonempty w-fiber is a ball, the allowed t values form a disk, and each point joins to (t,0), then (0,0), inside K.
At t=0, |w|=1, the t direction is complex tangential and its Levi value is -1. Thus K fails the required pseudoconvexity.
Every t-fiber of Y is C^(n-1) minus a closed ball, minus the origin, or all C^(n-1). Each is connected and Oka by the standard polynomially convex complement theorem (or C^d\{0}, d>=2). Any bounded-above PSH function u on Y is therefore constant on each t-fiber. Denote this constant h(t). For each t0, choose a single large w0 that stays in Y over a neighborhood of t0. Then h(t)=u(t,w0) there, proving h is subharmonic. It is bounded above on C, so h is constant. Therefore u is constant.

## Explicit arbitrarily fast entire curves in the offending tangent direction
For p=(sqrt(17)/4,0,0,...), in ordering (w1,t,w2,...), define
g_L(s)=(sqrt(17)/4,L s,2 L^2 s^2,0,...), L>0.
Then rho(g_L(s))=5 L^4(|s|^2-1/(10L^2))^2+1/80>0.
Thus g_L maps C into Y and g_L'(0)=L e_t. The scalar Kobayashi metric vanishes in this direction despite the negative Levi value of K.

## What these do NOT prove
None of the above proves Oka implies Levi pseudoconvexity in n>=3. PSH-Liouville and scalar/rank metrics are insufficient shortcuts. A valid proof must use more than these pointwise necessary conditions.
