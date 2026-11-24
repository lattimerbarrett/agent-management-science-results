# Cycle comparison reduction (conditional asymptotic derivation)
Let r>=3, n_i=n/r+s_i with bounded s_i and sum s_i=0, and insert a bounded-degree forest F in class1. Write rho=lim e(F)/n_1, e(F)=rho*n_1+delta, W=sum_v binom(d_F(v),2). Up to quantities common to all compared hosts having the same rho and n, the order 1/n part of log total cycles is

(2*r/((r-2)*n))*[-sum_i s_i^2/2 + r*rho*s_1/(r-1)+(r-2)*delta/(r-1)-r*(r-2)*W/((r-1)^2*n)].

This statement still requires a uniform saddle-point proof; do NOT present it as established solely by finite checks.

Derivation of quadratic term: proper r-color cyclic words have stationary transition matrix with diagonal0, offdiagonal1/(r-1). Contrast covariance per step is (r-2)/r^2. Combining Gaussian counts of words with prod n_i! gives log Hamilton count imbalance term -r*sum_i s_i^2/((r-2)*n).

Internal linear-forest contraction: each selected path component has two orientations, and each selected internal edge reduces first-class size by1. If R=r/((r-1)*n), first-order internal-edge contribution is 2*R*e. Adjacent pairs contribute weight2 R^2 instead of the weight4 R^2 for independent edge pairs; hence shape correction -2*R^2*W. Derivative of R under first-class shift supplies the stated linear term.

## Sharp candidate comparison
Let u=k*q and compare
 A parts (u+3,u+3,u+2,...,u+2), internal (q-1)K_{1,k-1} disjoint union K_{1,k+2};
 B parts (u+4,u+2,...,u+2), internal q P_k disjoint union P_4.
Both have internal edges q*(k-1)+3. A has exactly1 more total edge. Difference of limiting W/n is (k-2)*(k-3)/(2*k*r). Thus normalized cycle advantage of B is
 G_r(k)=-1+2*(k-1)/(k*(r-1))+(r-2)*(k-2)*(k-3)/(2*k*(r-1)^2).

G_3(6)=1/12; G_4(8)=0;
G_r(2r)=-(r-4)/(2r*(r-1));
G_r(2r+1)=3/((r-1)*(2r+1)).
Hence strict cycle gain for r3,k6 and r>=5,k2r+1, conditional on asymptotic formula. Exact integer cycle checks support these comparisons (see agent4_sharp_checks.py). For r4 k8, exact checks support positive SECOND-order difference with the large-star gadget, but no analytic second-order proof has yet been obtained.

Most importantly, no fixed forbidden graph H realizing these competing regimes has yet been proved. Candidate host graphs alone do not establish the desired S_r inclusion.
