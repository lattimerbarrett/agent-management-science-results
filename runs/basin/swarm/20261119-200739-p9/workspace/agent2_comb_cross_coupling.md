# Explicit audit of the direct-Hilbert cross-limit coupling

Use agent4's orientation: positive h on the left rotation and negative h on the right. Let z=rc, and signs sigma_j be independent fair +/-1. Set
D_G(sigma)=(3-sigma)/2 in{1,2}, D_B(sigma)=3(1-sigma)/2 in{0,3}.
For exitage N=n and an independent U uniform[0,1],
X_n=sum_{j=0}^{n-1}D_G(sigma_j)4^(-j-1)+(D_B(sigma_n)+U)4^(-n-1),
H_n(z)=sum_{j=0}^n sigma_j z^(-j).
For a horizon-L survivor use
X_surv=sum_{j=0}^{L-1}D_G(sigma_j)4^(-j-1)+U4^(-L),
H_surv=sum_{j=0}^{L-1}sigma_j z^(-j).
Under measure a_L dx, N is geometric with exit probability la/2, truncated atL. Under c_L dx it is geometric with exit probability lc/2. These formulas follow by multiplying branch interval lengths by their constant density: each active signed branch has mass ra/4 (respectivelyrc/4), each absorbing signed branch la/4 (respectivelylc/4). The signs remain fair and independent conditional on exitage.

For FIXED Q let L tend to infinity. Couple using one finite geometric N, all signs and U. Eventually L>N almost surely, so (X,H) stabilizes exactly. The resulting measure is absolutely continuous, being a countable mixture of uniform terminal bad intervals; hence no atoms occur at any quarter boundary or fixed separation distance.

For Q tending to infinity, construct geometric N_Q explicitly from E exponential(1):
N_Q=floor(E/[-log(1-d_Q)]), where d_Q=la/2 orlc/2.
Then N_Q tends to infinity almost surely. Since z_Q tends to2 and z_Q>=3/2,
X_NQ tends to X_infinity=sum_{j>=0}D_G(sigma_j)4^(-j-1),
H_NQ(z_Q) tends to H_infinity=sum_{j>=0}sigma_j2^(-j)
almost surely. This is elementary finite-prefix convergence plus tails bounded by4^(-m) and3(2/3)^m. Also |H|<=3 uniformly. Apply this coupling independently to the two measures a dx and c dy.

Let C_L/k be the cross-top-quarter integral of (H(x)-H(y))/(pi(x-y)). Off the set |x-y|<1/16 its integrand is bounded by96/pi. Both fixed-Q/horizon and Q/infinite-horizon couplings therefore permit dominated convergence away from that set. The top-quarter indicator has no limiting boundary mass. In the Q-limit the two different surviving quarter supports have separation>=1/6, so no limiting separation-cutoff issue arises either.

For the omitted near-boundary set, both points must lie in the constant strips of width1/16 flanking one of the three quarter boundaries. For every L>=2 those strips have ALREADY ABSORBED and satisfy a<=2la,c<=2lc,|H|<=3. Therefore the absolute near contribution is at most
C la lc sum_boundaries int_0^(1/16)int_0^(1/16)(u+v)^(-1)dudv
<=C' la lc.
For fixed Q the entire near contribution is independent of L>=2, so C_L has a limit C_Q. As Q tends to infinity the near contribution tends to zero. This rigorously justifies both limiting operations used by agent4, without an unjustified interchange of Q and L.

The limit Cantor law has half its mass in each active top quarter. On the left H=1+H'/2 in[0,2], with mean1; on the right H=-1+H'/2 in[-2,0], with mean-1. Across those quarters H(x)-H(y) and x-y have opposite signs. Since |x-y|<=1/2, each ordered cross integral is at most -1, before the factor1/pi. Thus C_Q/k tends to a constant<=-2/pi.

Finally, with theta=ra/2<1, the exact finite recursion is
B_L=sum_{j=1}^L theta^(L-j) C_j.
Uniform |C_j|<=Ck and dominated convergence for the convergent geometric series give B_L -> C_Q/(1-theta)=2Q C_Q. For Q large enough C_Q<=-k/pi, some FINITE horizonL(Q) therefore satisfies |B_L|>=Qk/pi. No infinite terminal weight is needed in the final counterexample.
