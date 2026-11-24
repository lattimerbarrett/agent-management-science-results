# Arithmetic proof of universal nonvanishing, all n>=3 and c>=3

This document states precisely the classical number-theoretic inputs and proves the reduction/application. It does NOT assume any presentation for IA_n, and it does not use an unjustified rank stabilization map.

## Classical inputs

(1) For a field F and d>=3, the Steinberg group St_d(F) maps onto SL_d(F) with central kernel K_2(F), identified with Milnor symbols {a,b} (Matsumoto). If F is a nonarchimedean local field containing mu_p, the p-th Hilbert symbol gives K_2(F)->mu_p. Pushing out gives the p-fold metaplectic cover of SL_d(F). Root unipotents have canonical lifts; for roots alpha,beta, commuting torus lifts satisfy
 [h_alpha(a),h_beta(b)] = (a,b)_p^{(alpha,beta)}.
For type A, the coroots e_i-e_k and e_i-e_0 have inner product 1 when i,k,0 are distinct.

(2) Let F/Q_p have ramification e, contain mu_p, and have residue field F_p. Put C=pe/(p-1). The Hilbert symbol satisfies
 (U^a,U^b)_p=1 if a+b>C,
 U^{C+1} subset F^{*p},
and, if p does not divide a, its boundary pairing
 U^a/U^{a+1} x U^{C-a}/U^{C-a+1} -> mu_p
is perfect. We use only a=1. Since residue degree is one, any two units with nonzero respective leading coefficients pair nontrivially.

(3) For a number field K, integral K_2(O_K) is unramified (all tame symbols vanish). Away from p the p-th Hilbert symbol factors through the tame symbol. The global Hilbert reciprocity product is 1. Consequently, if K is totally imaginary and has a UNIQUE prime v over p, then
 K_2(O_K) -> K_2(K_v) -> mu_p
is zero.

These are standard Matsumoto/local-symbol/localization/reciprocity theorems, not an Andreadakis theorem.

## Local congruence lemma (proved using the Steinberg relations)

Write Gamma_r={g in SL_d(O_F): g=I mod pi^r}. Let C=pe/(p-1) be integral. In the metaplectic cover choose the Gauss section sigma near I: lift lower unipotent, diagonal, upper unipotent factors in a fixed order.

Claim: if a+b>C then sigma(g)sigma(h)=sigma(gh) for g in Gamma_a,h in Gamma_b.

Indeed, converting the product of their Gauss decompositions to Gauss normal form requires only the elementary root/torus Steinberg relations. The possible central factors are torus symbols with unit arguments in U^a,U^b, or opposite-root symbols (x,1+xy)_p where v(x)>=a,v(y)>=b. The first vanish by (2); for the second, 1+xy belongs to U^{a+b} subset U^{C+1} subset F^{*p}. All other root relations have no central error. The operations preserve the relevant valuations, so induction through Gaussian elimination proves the claim.

It follows that sigma(Gamma_{C+1}) is a subgroup. It is normal in the full preimage E_1 of Gamma_1 and meets the central mu_p trivially. More generally, if a+b>C, then
 [preimage(Gamma_a),preimage(Gamma_b)] subset sigma(Gamma_{a+b}).
To see the commutator statement from the product statement, use gh=[g,h]hg: the extra factor [g,h] has level a+b, and its multiplication with hg has no central error. Central choices of lifts do not affect commutators.

Thus N=E_1/sigma(Gamma_{C+1}) is nilpotent of class at most C. Indeed, ordinary congruence commutators give gamma_C(E_1) subset preimage(Gamma_C), and commuting once more with E_1 lands in sigma(Gamma_{C+1}). The central mu_p embeds in N.

## Global integral lift

Suppose K is as in (3), v is its unique p-prime, F=K_v, and d>=3. The map St_d(O_K)->St_d(F)->metaplectic cover kills ker(St_d(O_K)->E_d(O_K)). For any element of this kernel maps, after stabilization, to integral K_2(O_K), which is killed by (3). Thus there is an ACTUAL GROUP HOMOMORPHISM
 E_d(O_K) -> metaplectic cover of SL_d(F)
lifting the ordinary local matrix homomorphism. No assumed lift of IA or matrix Lie algebra is involved.

## Fields and units for every C=c>=3

If c has an odd prime divisor p, put h=c/p, K0=Q(zeta_p), alpha=zeta_p-1. If c is a power of two, then c>=4: put p=2,h=c/4,K0=Q(i),alpha=i-1.

If h=1, take K=K0, pi=alpha, u=1+pi (a root of unity).
If h>=2, take pi a root of
 P(X)=X^h+alpha X+alpha
and K=K0(pi). This is Eisenstein at the unique prime (alpha) above p. Hence K has a unique p-prime, pi is a local uniformizer, and the residue field is F_p. K is totally imaginary because K0 is. Furthermore
 Norm_{K/K0}(1+pi)=(-1)^h P(-1)=1,
so u=1+pi is a GLOBAL integral unit.

For odd p, the local absolute ramification is e=(p-1)h and pe/(p-1)=ph=c. For p=2, it is e=2h, so 2e=4h=c. Thus the local congruence lemma has C=c in all cases.

## Actual Fox homomorphism in every rank

Fix the three distinct basis indices j=2,i=1,k=3 (additional indices are harmless). Specialize the abelianized Fox Jacobian at t_j=u, all other t_l=1. The fundamental Fox identity implies that the row module spanned by e_l, l!=j, is invariant: J(phi)*(0,...,u-1,...,0)^t equals the same vector, and O_K is a domain. Its restriction is invertible. Since row Fox Jacobians are antihomomorphisms under usual right-to-left composition, take their inverse to obtain a genuine homomorphism
 rho:IA_n -> GL_{n-1}(O_K).

Its Magnus generator images are diagonal u^{-1} on coordinate i for C_ij, and elementary matrices with parameter +/-(u-1) for M_a;jb; all other generators have identity image. In particular its image is generated by these elementary matrices and coordinate unit diagonals.

Embed GL_{n-1} into SL_n by A -> diag(A,det A^{-1}), using an auxiliary coordinate 0. The unit diagonal diag(u^{-1},u) is elementary via the standard root formula h_{i0}(u^{-1}), and all offdiagonal elementary matrices remain elementary. Therefore the Fox homomorphism lands in E_n(O_K), allowing the global integral lift above. It also lands in Gamma_1, so it composes to the class-at-most-c group N constructed above.

## Uniform witness

Use the left Magnus generators
 D=C_12,
 A=M_1;23: x1->[x2,x3]x1,
 B=M_3;12: x3->[x1,x2]x3.
For c>=3 set X=ad_D^{c-3}(A), L=[X,B], W_c=[L,D], with ad_D(X)=[D,X]. Then W_c belongs to gamma_c IA_n.

Its degree-c Johnson derivation is zero. Indeed all three degree-one derivations fix x2 and act linearly on x1,x3 over the polynomial operator t=ad(x2). Their matrices are t times a diagonal matrix and the two opposite matrix units (up to signs). Hence ad_D^{c-3}(A) is +/−t^{c-2} times one matrix unit, L is +/−t^{c-1} times diag(1,-1), and [L,D]=0. Since gamma_c IA_n subset A_c, this gives W_c in A_{c+1}.

Under the Fox homomorphism, D is the unit diagonal u^{-1} on coordinate i, A=x_ik(-pi), B=x_ki(pi). Therefore X is EXACTLY x_ik(r), where
 r=(-pi)(u^{-1}-1)^{c-3}
   =(-1)^{c-2} pi^{c-2} u^{-(c-3)}.
The commutator of x_ik(r),x_ki(pi) has its two-by-two block
 [[1+r*pi+r^2*pi^2, -r^2*pi], [r*pi^2,1-r*pi]].
Put v=1+r*pi+r^2*pi^2. Its Gauss decomposition equals h_ik(v) modulo Gamma_c, because the offdiagonal parameters have valuations at least c. Also
 v=1+epsilon*pi^{c-1} mod pi^c,
where epsilon has residue +1 or -1.

Consequently the image of W_c in N is the central torus commutator
 (v,u^{-1})_p^{(e_i-e_k,e_i-e_0)}=(v,u^{-1})_p.
The discarded root errors lie in Gamma_c, whose commutators with D lie in sigma(Gamma_{c+1}). Since u^{-1}=1-pi mod pi^2, the two leading coefficients are nonzero. The boundary Hilbert pairing of (2), with levels c-1 and1, says this symbol is NONTRIVIAL.

N has class at most c. Thus W_c does NOT belong to gamma_{c+1} IA_n. We have explicitly exhibited
 W_c in gamma_c IA_n intersection A_{c+1} minus gamma_{c+1} IA_n
for every n>=3,c>=3.

Combined with the already established exclusions n=2 or c=1,2, this gives exactly D={(n,c):n>=3,c>=3}.
