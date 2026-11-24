UPPER BOUND (agent_2)
Let K=[W]Ap and S=W^{-1/(p-1)}, A=W^{1/p}, B=A^{-1}. Constants depend only on p and dimension.

1. Reducing matrices. For each I choose positive U_I,V_I such that
 |U_I e| <= (avg_I|A e|^p)^{1/p} <=2|U_I e|,
 |V_I e| <= (avg_I|B e|^q)^{1/q} <=2|V_I e|.
John's ellipsoid theorem on the real four-dimensional, complex-balanced norm balls supplies these; its uniqueness makes the ellipsoid complex/Hermitian. Endpoint choices of inequalities do not matter.
Finite-dimensional column comparisons and self-adjointness give
 K_I^{1/p} ~= (avg_x||A(x)V_I||^p)^{1/p} ~= ||U_I V_I||.
Indeed for fixed x, the Lq_y norm of ||A(x)B(y)|| equals up to dimension-dependent constants the ell^q sum of the N_B(A(x)e_j), hence ||V_I A(x)||=||A(x)V_I||. This also proves [S]Aq^{1/q} ~= K^{1/p}.

2. Directional scalar Ap and RHI. If w_e=|A e|^p, the pointwise scalar ratio |A(x)e|/|A(y)e| is at most ||A(x)B(y)||. Integrating exactly in the order in the question gives [w_e]Ap<=K. For sigma_e=|B e|^q, the dual version gives [sigma_e]Aq<=C K^{1/(p-1)}=:L.
An elementary scalar lemma: if [w]Ar<=D, then for every interval I,
 avg_I w^{1+delta} <=2(avg_I w)^{1+delta}, delta=c_r/D.
Proof: scalar Ar implies w(E)/w(J)>=(|E|/|J|)^r/D. Let M_I be dyadic local maximal and lambda0=avg_I w. For lambda>=lambda0, maximal dyadic components J of {M_I w>lambda} have avg_Jw<=2lambda. Thus |{M_Iw>4lambda} intersect J|<=|J|/2, so
 w({M_Iw>4lambda})<=(1-t)w({M_Iw>lambda}), t=2^{-r}/D.
Layer cake and iteration give, writing z=4^delta,
 integral_I (M_Iw)^delta w <= lambda0^delta w(I) [1+(z-1)/(1-(1-t)z)].
Choose z=1+t/4. The bracket is (4+t)/(3+t)<2; delta=log(1+t/4)/log4 >= c_r/D. Lebesgue differentiation and monotonicity of normalized Lr norms give the asserted RHI for smaller delta as well.
Consequently r_W=1+c_p/K and r_S=1+c_p/L are valid uniform reverse-Holder exponents.

3. Convex body sparse domination input. The standard finite-dimensional convex-body sparse domination theorem for the Hilbert transform gives a universal finite number of sparse families and bounds
 |<Hf,g>| <= C sum_{I in S}|I| sup_{u in C_I(f),v in C_I(g)} |<u,v>|,
where C_I(f)={avg_I phi f: measurable complex phi, |phi|<=1}. Multiple grids/families alter only C. Each family has disjoint E_I subset I with |E_I|>=eta|I|. For real convex-body versions apply to real and imaginary parts (dimension at most four), a fixed-factor change.
This is the only substantial harmonic-analysis theorem used as a black box in this upper proof. It follows from weak-(1,1) Hilbert/grand-maximal bounds and the usual stopping-time recursion, using John's ellipsoid to normalize all vector components simultaneously.

4. Sparse estimate. Put f=BF, g=AG. For u in C_I(BF), v in C_I(AG),
 |<u,v>| <= ||V_I U_I|| (avg_I |V_I^{-1}BF|)(avg_I |U_I^{-1}AG|).
Column estimates, reducing matrices and step 2 show
 (avg_I ||V_I^{-1}B||^{q r_S})^{1/(q r_S)}<=C,
 (avg_I ||U_I^{-1}A||^{p r_W})^{1/(p r_W)}<=C.
Thus with a=(q r_S)'<p and b=(p r_W)'<q the sparse form is bounded by
 C K^{1/p} sum_I |I| (avg_I |F|^a)^{1/a}(avg_I |G|^b)^{1/b}.
Disjoint E_I and Holder yield <= C K^{1/p}||M_a F||p ||M_bG||q.
The elementary unweighted maximal inequality ||M||L^t<=C t/(t-1) gives
 ||M_a||Lp <= C_p (p/(p-a))^{1/a} <= C_p L^{1/p},
 ||M_b||Lq <= C_p (q/(q-b))^{1/b} <= C_p K^{1/q}.
The apparent powers 1/a and 1/b cause no loss, since 1/a-1/p=O(1/L), 1/b-1/q=O(1/K), and sup_{x>=1}x^{c/x}<infinity.
The final upper exponent is 1/p+1/[p(p-1)]+1/q=1+1/(p-1)-1/p.

5. Domain issues. First apply the sparse theorem to bounded compactly supported vector inputs and test functions for which weighted norms are finite, and use truncation/density. If a smooth compactly supported f has infinite Lp(W) norm there is nothing to prove. For finite norm, approximate with functions truncated in size, support, and spectral values of W; usual unweighted locally integrable convergence plus boundedness identifies the extension with the componentwise distributional Hilbert transform. Weighted duality then produces the stated norm estimate.

Exact exponent/maximal-gap/reverse-Holder geometric-series identities are verified with SymPy in agent2_upper_checks.py. This does NOT verify the black-box sparse domination theorem, nor does finite computation prove an analytic universal statement.


APPENDIX: CLOSING THE CONVEX-BODY SPARSE INPUT
For compact f,g choose I0 with supp(g) subset I0 and supp(f) subset 3I0. Define K_J(f)={avg_J phi f: |phi|<=1}. Normalize K_{3I}(f) by its John ellipsoid A_I(unit ball), and set h=A_I^{-1}f. Degenerate convex bodies are handled in their linear span. Then avg_{3I}|h|<=C_dim. The scalar Hilbert transform and its local grand maximal operator are weak-(1,1), with constants unchanged under taking the four real coordinates of h. Hence a large fixed threshold C makes the bad set
 Omega={x in I: |H(h1_{3I})(x)|>C or G_{H,I}h(x)>C}
have measure at most |I|/8. Here
 G_{H,I}h(x)=sup_{Q subset I, Q contains x} esssup_{xi in Q}|H(h1_{3I\3Q})(xi)|.
Take maximal dyadic P subset I having avg_P1_Omega>1/4. Their total measure is at most |I|/2; maximality ensures each P has Omega-density at most1/2, so contains a point outside Omega. At such a point the grand-maximal condition gives the bound for H(h1_{3I\3P}) everywhere on P. Outside children the direct H condition gives the bound. Thus
 H(f1_{3I})=h_I+sum_P H(f1_{3P})1_P,
where h_I(x) lies in C K_{3I}(f) pointwise and is supported on I. Iterate. The depth-N union has measure <=2^{-N}|I0|, so for almost every x recursion terminates and gives the pointwise Minkowski convex-body sparse domination.

Pair against g. If E=A(unit ball) is the John ellipsoid of K=K_{3I}(f), then
 integral_I sup_{u in K}|<u,g(x)>| dx
 <=C integral_{3I}|A g| dx
 <=C sum_{j=1}^2 integral_{3I}|<Ae_j,g>| dx
 <=C |3I| sup_{u in K,v in K_{3I}(g)}|<u,v>|.
In the last step choose the measurable scalar complex phase that realizes the absolute scalar inner product; this is allowed in K(g). The intervals 3I are1/6-sparse because the original disjoint sets E_I subset I have measure at least |I|/2=|3I|/6. This proves the sparse bilinear statement used above.

CLASSICAL SCALAR WEAK-(1,1) PREREQUISITES
For H: perform dyadic Calderon-Zygmund decomposition at height lambda, write h=g+sum_J b_J with mean-zero b_J; ||g||infinity<=2lambda, ||g||1<=||h||1. Fourier multiplier -i sign gives ||Hg||2<=||g||2. Outside triple bad intervals, cancellation and the kernel derivative estimate imply integral |Hb_J|<=C||b_J||1. Chebyshev plus total bad-interval length gives weak-(1,1).
For global grand maximal G_H, fix Q containing x and xi in Q. Kernel smoothness gives
 |H(h1_{R\3Q})(xi)-H(h1_{R\3Q})(z)|<=C Mh(x), z in Q.
Choose z in Q simultaneously satisfying |Hh(z)|<=C(avg_Q|Hh|^delta)^{1/delta} and |H(h1_{3Q})(z)|<=C avg_{3Q}|h| (the latter uses weak-(1,1), the former Chebyshev, with constants making each exceptional set smaller than |Q|/2). Hence
 G_Hh(x)<=C[M_delta(Hh)(x)+Mh(x)], 0<delta<1.
The Hardy-Littlewood maximal operator maps weak-L^{1/delta} to itself since 1/delta>1; therefore M_delta maps weak-L1 to weak-L1. The preceding weak H estimate proves weak-(1,1) for G_H and therefore for the local version by applying to h1_{3I}.
All statements here are classical scalar facts with their standard proofs indicated; unlike the sharp lower construction, they do not require a recent matrix result.
