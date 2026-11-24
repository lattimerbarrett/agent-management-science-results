# Convergence for s=2 and at most four distinct active eigenvalues

Cases with at most two active eigenvalues terminate, and with exactly three the normalized residual map squares to the identity (Vandermonde formula). Consider four nodes lambda_1<...<lambda_4 and P(z)=prod(z-lambda_i). We use the globally proved fact that q_{2k}->q and q_{2k+1}->r, with q r=P+H whenever the union of limiting supports has four nodes. If that union has at most three, fixed q-orthogonality and total mass determine its weights uniquely (Vandermonde), so the even weights converge already.

Assume therefore that q r=P+H, H>0. Let M_k=P sum_i w_{k,i}/(z-lambda_i), a monic cubic. Divide
 q_k M_k=(z-eta_k)P+h_k(z-zeta_k).
The restart identity is M_{k+1}=q_k(z-zeta_k), and h_k is the monic quadratic norm. Polynomial orthogonality proves these identities, as in the general Stieltjes checker. All quantities are rational smooth functions of weights while the two-degree moment Gram matrix is invertible; near the limiting polytope it remains uniformly invertible.

Write q=q_k, h=h_k, eta=eta_k,zeta=zeta_k and put primes on the next-step quantities, K=h'-h>=0 and R=zeta-eta. Eliminating M and P from the two division identities yields
 h'(z-zeta')(z-eta)-h(z-eta')(z-zeta)=K q(z).
Consequently, when R!=0,
 zeta'-zeta=-K q(zeta)/(h' R),
 eta'-eta=-K q(eta)/(h R).
A second elimination gives
 K[h q(zeta)+q(eta)P(zeta)]=-h R^2 P(zeta).

Here is the limiting geometry. Every cluster measure w satisfies M=r(z-zeta) on an even step (or M=q(z-zeta) on an odd step), so eta=zeta. The roots of q and r lie in the first and third spectral gaps, one in each, since q r=P+H. The remaining Stieltjes zero zeta lies in the closed middle gap [lambda_2,lambda_3]. Throughout this compact interval q(zeta),r(zeta)<0, and neither vanishes. Thus the denominator in the last display tends uniformly, on an even step, to q(zeta)^2 r(zeta), and on an odd step to r(zeta)^2 q(zeta); both are bounded away from zero. It follows that K=R^2 C for a uniformly bounded smooth function C near the whole limiting polytope.

Subtracting the two scalar increment formulas gives
 R'-R=(K/R)[q(eta)/h-q(zeta)/h'].
The bracket equals O(R)+O(K)=O(R), hence R'=R(1+O(R)), uniformly. Also R_k->0, since all cluster points satisfy eta=zeta. Therefore R_k has eventually constant sign unless it vanishes. If R=0, the division identity gives q M=(z-zeta)(P+h); since q(zeta)!=0 near the polytope, q divides P+h and the residual weight dynamics is exactly a two-cycle, so convergence is immediate.

Otherwise q_k(zeta_k)<0 eventually on both parities, h'>0, and K>=0. The formula for zeta'-zeta shows that all sufficiently late increments of zeta have the same sign. Since zeta is bounded, it converges. Finally M_{2k}=q_{2k-1}(z-zeta_{2k-1}) converges coefficientwise, and the weights w_{2k,i}=M_{2k}(lambda_i)/P'(lambda_i) converge. The standard eventual-sign argument for the normalized residual then gives convergence of y_{2k}.

Important scope: this proof is exact for four-node dynamics. It does not yet justify discarding summable external modes from a higher-dimensional orbit.
