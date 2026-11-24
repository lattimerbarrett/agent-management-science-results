# Rigorous upper-bound reduction
Write Q=[W]_{A_p}, B=W^{1/p}. Constants below depend only on p and dimension 2.

Classical lemmas used (state explicitly):
1. Scalar quantitative reverse Holder: if [v]_{A_t}<=K, then for 0<delta<=c_t/K,
   (<v^{1+delta}>_I)^{1/(1+delta)}<=2<v>_I, for every interval I.
2. Convex-body sparse domination for the componentwise Hilbert transform: for compactly supported vector u,v there are finitely many eta-sparse interval families S such that
   |int <Hu,v>| <= C sum_S sum_{I in S}|I| sup{|<a,b>|:a in <<u>>_I,b in <<v>>_I}.
   Here <<u>>_I={average_I phi u: phi measurable scalar, |phi|<=1}; allow complex phi.
   This is the standard local weak-(1,1)/grand-maximal recursion applied after John-normalizing each vector-average convex body. Its constants depend only on dimension. Degenerate bodies are handled on their spans.
3. Finite-dimensional reducing matrices: for any norm N on C^2 invariant under scalar phases, there is positive Hermitian A with c|Ae|<=N(e)<=C|Ae|. This is John's ellipsoid on real dimension 4; phase invariance makes the ellipsoid complex Hermitian.

For each I choose positive A,D reducing
 N(e)=(<|Be|^p>_I)^{1/p}, Nd(e)=(<|B^{-1}e|^q>_I)^{1/q}.
These norms are finite: local integrability of W gives the first; finiteness of Q, by choosing one invertible B(x0) with finite inner integral, gives local L^q integrability of B^{-1}.

The reducing-product bound is ||AD||<=C Q^{1/p}. Indeed
 ||AD||<=C (<||B(x)D||^p>_x)^{1/p},
 ||B(x)D||=||D B(x)||<=C (<||B(y)^{-1}B(x)||^q>_y)^{1/q}.
The last kernel norm equals ||B(x)B(y)^{-1}|| by taking adjoints.

Directional scalarization: v_e=|Be|^p has [v_e]_{A_p}<=Q because
 |B(x)e|/|B(y)e|<=||B(x)B(y)^{-1}||.
For u_e=|B^{-1}e|^q, Cauchy gives
 |B(x)^{-1}e| |B(x)v|>=|<e,v>|.
Choose v=A^{-2}e. Then
 (<|B^{-1}e|^{-p}>)^{1/p}<=C/|A^{-1}e|,
 while Nd(e)<=C|De|<=C||DA|| |A^{-1}e|.
Consequently [u_e]_{A_q}<=C Q^{q/p} uniformly in e.

Set delta_w=c_p/Q and delta_d=c_p/Q^{q/p}, reducing c_p to put both in (0,1]. Scalar RH, applied to the fixed directions A^{-1}e_j and D^{-1}e_j, followed by a finite-basis operator-norm bound, yields
 (<||A^{-1}B||^{p(1+delta_w)}>)^{1/[p(1+delta_w)]}<=C_p,
 (<||D^{-1}B^{-1}||^{q(1+delta_d)}>)^{1/[q(1+delta_d)]}<=C_p.
Use adjoints to put A^{-1},D^{-1} on the right inside each directional norm.

Conjugate the Hilbert transform, T=B H B^{-1}. For unweighted F,G, sparse domination of u=B^{-1}F and v=BG gives, for each sparse family,
 |<TF,G>|<=C Q^{1/p} sum_I |I| <|D^{-1}B^{-1}F|>_I <|A^{-1}BG|>_I.
Indeed factor D and A out of the respective convex averages and use ||DA||=||AD||.
Holder and the normalized RH bounds reduce this to
 C Q^{1/p} sum_I|I| <|F|^r>_I^{1/r}<|G|^s>_I^{1/s},
 r=(q(1+delta_d))'<p, s=(p(1+delta_w))'<q.
By disjoint sparse sets this sum is <=C||M_r F||_p||M_sG||_q.

An explicit maximal estimate adequate here is
 ||M_r F||_p <= C_p [p/(p-r)]^{1/p}||F||_p.
To prove it, weak-(1,1) applied to h 1_{|h|>lambda/2} yields
 ||Mh||_t^t<=C t 2^{t-1}/(t-1)||h||_t^t, 1<t<=p,
 and take h=|F|^r,t=p/r. Thus this norm costs delta_d^{-1/p}; the other costs delta_w^{-1/q}.

Altogether
 ||H||_{L^p(W)}<=C_p Q^{1/p} delta_d^{-1/p}delta_w^{-1/q}
 <=C_p Q^{1/p+q/p^2+1/q}=C_p Q^{1+1/[p(p-1)]}.
The exact exponent identity and the normalized Holder-gap identities are checked in agent4_upper_checks.py.
