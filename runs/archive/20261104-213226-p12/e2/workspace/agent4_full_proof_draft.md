# Proof architecture for dim R^12(M_25)=44

STATUS: COMPLETE. The exact rational coupled certificate has been reconstructed and every one of its1908 polynomial constraints independently verified by both Sage rational arithmetic and a separate GMP implementation. Its new functional has nonzero normalized value448507 modulo1000003 on delta. Thus both bounds44 are proved, using the established Chow-theoretic 3-spin relations and Hodge intersection theorem.

## Established geometric theorems used

1. Faber--Zagier relations vanish in the rational Chow ring of M_g. More generally the full 3-spin/Pixton relations vanish in CH(Mbar_g,n;Q), including their graph terms. The Chow statement is essential, not merely the cohomological statement. One may use Janda's Chow-theoretic proof, "Relations on Mbar_{g,n} via equivariant Gromov--Witten theory of P1" (Algebraic Geometry4, 2017), together with the explicit PPZ formula.

2. The Hodge intersection theorem: put l_g(f)=integral_Mbar_g f lambda_g lambda_(g-1). This descends to CH(M_g), since lambda_g lambda_(g-1) restricts to0 on every boundary divisor. Moreover l_g(kappa_(g-2)) is nonzero (its standard Bernoulli formula is |B_(2g)|/[2g*2^(2g-1)*(2g-1)!!]). If sum a_i=g-2, then
 integral_Mbar_g,n prod psi_i^(a_i+1) lambda_g lambda_(g-1) / l_g(kappa_(g-2))
 = (2g-3+n)! (2g-1)!! /[(2g-1)! prod(2a_i+1)!!].
This is Faber's intersection-number formula. The known psi pushforward identity sums permutations by their cycles; inversion gives the set-partition formula below. No Gorenstein conjecture is assumed.

## The upper bound

Index the77 degree12 monomials by increasing lexicographic partitions of12, writing kappa_mu=prod kappa_(mu_i). Define
 A(T)=sum_(n>=0) (6n)!/[(3n)!(2n)!] T^n,
 B(T)=sum_(n>=0) A_n*(6n+1)/(6n-1) T^n,
 Psi=A+sum_(j>=1,j!=2 mod3) p_j T^floor(j/3) * (A if j=0 mod3 else B).
Let K act coefficientwise by T^n -> kappa_n, with kappa0=48, and put gamma=K(log Psi). FZ says [T^r p^sigma] exp(-gamma)=0 if |sigma|<=3r-26 and |sigma|=r mod2.

Take r9,10,11,12 and multiply all such relations by all kappa monomials ofdegree12-r. There are59 labelled rows. Their coefficients are computed in workspace/agent2_fz.py by a multiset set-partition recurrence (not an assumed rank table). A33by33 minor, using the first33 monomial columns and row labels in workspace/agent2_upper_certificate.json, has determinant368438425 modulo1000000007. All denominator factors are invertible at this prime. Therefore these33 relations are independent overQ and eliminate the first33 monomials. The remaining44 span R^12(M25), proving the upper bound44.

## The old pairing and its exact radical

For mu a partition of g-2, the normalized value l_g(kappa_mu)/l_g(kappa_(g-2)) equals
 sum_(set partitions P of indices(mu)) (-1)^(len(mu)-|P|)
 * (2g-3+|P|)! (2g-1)!!
 /[(2g-1)! prod_(blocks C in P)(2 sum_(i in C)mu_i+1)!!].
There is NO factorial per block in the inversion coefficient.

Use g25, and pair partitions of12 against partitions of11. Exact arithmetic in workspace/agent3_lower.py gives rank43. A43by43 minor has determinant111661844 modulo1000000007; its selected partitions are in workspace/agent1_lower43_minor.json. On the44 upper-bound survivor monomials the kernel is one-dimensional. Its vector delta is given overQ in workspace/agent3_radical.json, normalized to first coordinate1. workspace/agent3_radical_check.py verifies it annihilates every complementary degree11 monomial exactly. Deleting that first survivor leaves43 classes independent under the old pairing.

We must show delta is NONZERO in actual Chow, not merely nonzero in the formal FZ quotient.

## The additional compact-support functional

Let xi_irr:Mbar24,2 -> Mbar25 be ordered nonseparating gluing, xi_1:Mbar24,1 x Mbar1,1 -> Mbar25 separating gluing. Write Lambda=lambda24 lambda23. On Mbar24,2 write L=psi1+psi2 and D=the rational-tail divisor containing both markings; D is isomorphic to Mbar24,1. On this latter space write K=psi1.

The desired exact coupled certificate consists of a symmetric degree12 polynomial beta, all of whose terms contain at least one of psi1,psi2, and a degree11 polynomial rho on Mbar24,1, with the following identities after multiplication by Lambda:
 L beta + D Q=0, Q=K rho, K^2rho=0.
The last identity follows from the first two, but can also be checked explicitly from n1 Pixton relations. These are established by polynomial identities expressing L beta as a rational linear combination of smooth source Pixton rows and tracking their FULL rational-tail graph terms; Q-Krho and K^2rho are combinations of n1 Pixton rows. See the next section for the precise tail formula.

Assuming that certificate, set
 c=(1/2) xi_irr,*(Lambda beta)+xi_1,*(Lambda(lambda1-K)rho) in CH^60(Mbar25).
This c restricts to zero on every boundary normalization. At Delta_irr its two contributions are +D Lambda Q and -D Lambda K rho. At Delta_1, beta restricts to0 on D, and the remaining self-intersection equals Lambda K^2rho=0, because the normal line is -(K+lambda1) and lambda1^2=0. All other boundary restrictions vanish by the restriction of Lambda to nonseparating/positive-genus splitting of the core. See workspace/agent4_boundary_geometry.md for the detailed independent geometry and stack factors.

By localization and projection formula, f -> integral_Mbar25 f_tilde c is a well-defined functional on CH^12(M25), independent of its extension. For a degree12 kappa polynomial f, its value is
 (1/2) A(f)+(1/24) B(f),
 A(f)=integral_Mbar24,2 Lambda beta f(kappa_mark2),
 B(f)=integral_Mbar24,1 Lambda rho [f(kappa_mark1)-K partial_(kappa1)f(kappa_mark1)].
Here kappa_target glues to the sum of pointed kappa on the vertices; on Mbar1,1, kappa1=lambda1, higher kappa_i=0, and integral lambda1=1/24.

Thus, using the common nonzero Faber normalization, the numerical test is12A(delta)+B(delta). Its normalized value is448507 modulo1000003, after all rational denominators have been verified invertible at this prime. The underlying polynomial identities are verified EXACTLY overQ, not merely modulo this prime. Therefore this rational functional is nonzero, and delta is a nonzero Chow class. The43 old independent classes together with delta are independent: the old pairings first kill all43 coefficients in any dependence, and the new functional kills the remaining delta coefficient. This proves the lower bound44 and finishes.

## Explicit tail correction used by the certificate

For a smooth source relation P_r=[T^r] E48 F_sigma C_a(psi1T) C_b(psi2T), where a,b in{0,1}, let m be the number of1-parts in sigma. After multiplication by Lambda every other graph term vanishes except DQ_r. Its polynomial is
 Q_r=(-1)^(a+b) sum_(k=0)^m binom(m,k) k! [T^(r-1)] E47 F_(sigma minus1^k) H_(a+b+k)(K,T),
 H_even=(1-A(KT))/(KT), H_odd=(1+B(KT))/(KT).
Core kappa0=47, tail kappa0=1. This formula is verified by the standard edge factor at tail psi=0, which is
 [zeta_tail(1-A(zeta_main KT))+zeta_main(1+B(zeta_main KT))]/(KT).
The vertex and marked-leg zeta factors select the indicated parity. Only1-parts can land on Mbar0,3; selecting k of them contributes binom(m,k)k!. There is no automorphism factor for this graph.

The exact generators and all498 eligible source-row compatibility identities are verified overQQ in workspace/agent3_exact_pointed.py and workspace/agent3_tail_consistency.py. For a row multiplied by a monomial involving a marked psi, its D term iszero; for a kappa-only multiplier, restrict that multiplier to D, using the n1 pointed kappa coordinates. This is exactly the coupled matrix bookkeeping.

## Completed exact certificate

workspace/agent3_exact_dual_witness.pkl and .json contain the rational row-combination witness, with1553 nonzero row coefficients (max2289 decimal digits). The exact matrix rows are in workspace/agent3_coupled_exact_sparse.pkl; their generation is reproducible from the stated smooth and tail formulas in workspace/agent3_coupled_exact.py. The witness selects beta with312 symmetrized terms and rho with195 terms; their exact coefficients are in workspace/agent3_exact_beta_rho.json.

workspace/agent3_lift.py reconstructs the exact witness using a1552by1552 rational constraint minor, then verifies ALL1908 coefficient identities exactly. An independent implementation workspace/agent4_exact_witness_check.py uses gmpy2.mpq to sum the1553 selected exact rows; every one of the1908 resulting rational entries is exactly zero. It verifies all witness denominators are units modulo1000003 and the normalized value12A(delta)+B(delta) is448507 at that prime.

Independently, the resulting new functional annihilates all59 genus25 FZ rows (a cross-check of normalizations, gluing factors and tail signs), and evaluates delta to448507 modulo1000003. Thus the44th independent Chow class is certified. Together with the33 independent relations among77 generators, this establishes dim_Q R^12(M25)=44.
