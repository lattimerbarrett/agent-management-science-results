# Boundary-supported compact dual: geometric verification

Let g=25. Write j: M_25 -> Mbar_25. Let xi_irr: Mbar_24,2 -> Mbar_25 denote the ordered-branch nonseparating gluing map, and xi_1: Mbar_24,1 x Mbar_1,1 -> Mbar_25 the separating gluing map. Set Lambda=lambda_24 lambda_23. On Mbar_24,2 let D be the rational-tail boundary with markings1,2, let L=psi1+psi2, and on Mbar_24,1 write K=psi1.

Suppose beta is symmetric of degree12, every term has a psi marking factor, and rho has degree11 on Mbar_24,1. It suffices to establish the following identities after multiplication by Lambda:

(1) L beta + D Q = 0, where Q is a degree12 class on Mbar_24,1 and DQ denotes its pushforward along D;
(2) Q=K rho.

All equalities may be proved using Pixton relations, since their other graph terms are killed by Lambda (nonseparating/positive-genus splitting), or by the marking psi multiplier (rational tail).

Restriction to D gives K Q=0: indeed D beta=0, D^2=-K D, and both psi markings restrict to0 on D. Thus Lambda K^2 rho=0.

Define
 c0=(1/2) xi_irr,*(Lambda beta),
 c1=xi_1,*(Lambda (lambda_1-K)rho),
 c=c0+c1 in CH^60(Mbar_25).

Then c restricts to zero on every normalized boundary divisor:
* At Delta_irr, self-intersection of c0 is -Lambda L beta = D Lambda Q. The factor1/2 cancels the degree2 ordered-branch normalization. The intersection of c1 with Delta_irr on the rational-tail stratum contributes -D Lambda K rho, cancelling it.
* At Delta_1, c0 restricts to0 because beta|D=0. The self-normal line for xi_1 has first Chern class -(K+psi_ell), with psi_ell=lambda_1 and lambda_1^2=0. Thus c1 self-restriction is Lambda K^2rho=0.
* Every other boundary pullback has a nonseparating or positive-genus splitting in the genus24 core. Lambda restricts to0 in either case.
These statements include higher-codimension intersections, because the restrictions of Lambda to every relevant core boundary are zero as Chow classes.

Consequently f -> integral_Mbar25 f_tilde c factors through CH^12(M_25), by Chow localization and the projection formula. No independence/conjecture about tautological rings is used here.

For a target degree12 polynomial f in kappa, nonseparating gluing gives f(kappa_mark2). Separating gluing gives f(kappa_mark1 + lambda_1*[i=1]); on Mbar_1,1, kappa1=psi1=lambda1, all kappa_i withi>=2 vanish, and integral lambda1=1/24. Hence the functional equals
 (1/2) integral_Mbar24,2 Lambda beta f(kappa_mark2)
 +(1/24) integral_Mbar24,1 Lambda rho [f(kappa_mark1)-K partial_{kappa1}f(kappa_mark1)].
Thus the normalized exact numerical detector is12A+B.

WARNING: This note proves sufficiency of the stated identities. It does not assert that suitable beta,rho have been found, nor that12A+B is nonzero on the FZ radical. Those are the computational tasks still pending.


## Surviving rational-tail term of the 3-spin relation
Write A(T)=sum(6n)!/((3n)!(2n)!)T^n and B(T)=sum A_n(6n+1)/(6n-1)T^n. For smooth source relation P_r=[T^r] E_48 F_sigma C_a(psi1T)C_b(psi2T), let m be the multiplicity of1 in sigma. Then the surviving full-Pixton graph term is D Q_r, with
 Q_r=(-1)^(a+b) sum_(k=0)^m binom(m,k) k! [T^(r-1)] E_47 F_(sigma minus1^k) H_(a+b+k)(K,T),
 H_even=(1-A(KT))/(KT), H_odd=(1+B(KT))/(KT).
Here core kappa0=47 and rational-tail kappa0=1. All sigma parts other than1 force positive codimension on Mbar0,3 and hence cannot live on the tail. The parity k counts the tail zeta factor from those1-insertions.

The standard 3-spin edge factor at the tail psi=0 is
 [ zeta_tail(1-A(zeta_main KT)) + zeta_main(1+B(zeta_main KT)) ]/(KT).
Multiplying tail vertex zeta_tail and marked factors(-zeta_tail)^(a+b), then selecting the required parity, gives the displayed propagators. No graph automorphism factor occurs for this one-tail graph. Relations in the Chow ring (not merely cohomology) are provided by Janda's Chow-theoretic proof of Pixton's 3-spin relations.
