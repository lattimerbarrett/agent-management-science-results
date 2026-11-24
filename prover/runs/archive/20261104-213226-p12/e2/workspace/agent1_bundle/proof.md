# Exact computation of dim_Q R^12(M_25)

## Result and verification

The dimension is **44**. The upper bound and the lower bound below are independent: the upper bound uses33 Chow relations among77 kappa monomials; the lower bound uses a nonzero44by44 intersection determinant.

Run `python verify.py` in this directory. Only the Python standard library is used. The verifier regenerates all relations from their defining series, checks the rational certificate exactly, and computes both determinants. No cached relation matrix, numerical approximation, Sage installation, or asserted dimension is used as evidence. The supplied `certificate.json` is an explicit finite rational row-combination certificate, not a rank assumption. Its1553 rational coefficients define the auxiliary classes used below.

On independent execution the verifier prints:

```
Exact rational Pixton certificate: all 1908 identities verified.
Witness rows: 1553  beta terms: 312  rho terms: 195
Upper 33 by 33 minor mod 1000000007 : 368438425
Lower 44 by 44 minor mod 1000003 : 540716
All 59 known target FZ relations annihilated by the new functional.
VERIFIED: dimension <= 44 and dimension >= 44; hence dimension = 44.
```

## Geometric theorems used

We use two established theorems, not either Gorenstein conjecture or a completeness conjecture for tautological relations.

**Chow-theoretic 3-spin relations.** The full Pixton/3-spin stable-graph relations vanish in CH^*(Mbar_g,n;Q). Their restriction to M_g gives the Faber--Zagier relations. The Chow version is important here: one can use Felix Janda, *Relations on Mbar_g,n via equivariant Gromov--Witten theory of P1*, Algebraic Geometry4(3) (2017), together with the explicit 3-spin formula of Pandharipande--Pixton--Zvonkine, *Relations on Mbar_g,n via3-spin structures*, JAMS28 (2015).

**Hodge intersection formula.** Put
 l_g(f)=integral_Mbar_g f lambda_g lambda_(g-1).
The class lambda_g lambda_(g-1) restricts to zero on every boundary divisor; hence l_g descends to the Chow ring of M_g. Its value on kappa_(g-2) is nonzero; explicitly
 l_g(kappa_(g-2))=|B_(2g)|/[2g*2^(2g-1)*(2g-1)!!].
Faber's intersection-number theorem states, for sum d_i=g-2,
 integral_Mbar_g,n prod psi_i^(d_i+1) lambda_g lambda_(g-1) / l_g(kappa_(g-2))
 = (2g-3+n)!(2g-1)!!/[(2g-1)! prod(2d_i+1)!!].
Together with the standard psi pushforward and string identities, this computes all the Hodge integrals below. These theorems provide genuine rational-equivalence relations and genuine intersection functionals, respectively.

Throughout, kappa on a pointed compactification means the usual **log-pointed** kappa class. Its kappa0 is2g-2+n. Gluing pulls a target kappa class back to the sum of these classes over the vertices. All these compactified classes restrict to the classes specified in the question.

## 1. The upper bound44

Let
 A(T)=sum_(n>=0) (6n)!/[(3n)!(2n)!] T^n,
 B(T)=sum_(n>=0) A_n (6n+1)/(6n-1) T^n,
 Psi=A+sum_(j>=1,j!=2 mod3) p_j T^floor(j/3) (A if j=0 mod3 else B).
Let K act on series coefficients by T^m -> kappa_m and set gamma=K(log Psi), with kappa0=48. The genus25 FZ relation is
 [T^r p^sigma] exp(-gamma)=0
when |sigma|<=3r-26, |sigma|=r mod2, and no part of sigma is2 modulo3. These inequalities are the usual3r>g-1+|sigma| and parity condition, specialized to genus25.

For r9,10,11,12, multiply every eligible relation by every kappa monomial of degree12-r. There are59 resulting labelled rows in the77 monomials indexed by partitions of12. The functions in `fz_engine.py` compute them directly from A,B. In particular they do not import any table of tautological dimensions.

For clarity, the coefficient recurrence used there is this. Write E=exp(-K(log A)) and define F_sigma by
 E F_sigma=aut(sigma)[p^sigma] exp(-K(log Psi)).
Then F_empty=1, and, with the entries of sigma regarded as labelled,
 F_sigma=sum_(blocks C containing the first entry)
 (-1)^|C|(|C|-1)! K(T^sum floor(j/3) (B/A)^(number of j=1 mod3 in C)) F_(sigma minus C).
The code groups equal entries and inserts the binomial multiplicities. Thus it computes exactly the indicated coefficients.

The verifier row-reduces these59 rows modulo1000000007. A33by33 minor has determinant368438425, which is nonzero at that prime. All coefficient denominators are prime to this prime, so this certifies independence overQ. Its pivot columns are precisely the first33 lexicographic partitions of12. Let S be the remaining44 partitions; the classes kappa_mu, mu in S, span R^12(M25). This proves dim<=44.

## 2. An additional intersection functional on the open moduli space

Ordinary complementary kappa/Hodge pairings alone have rank43 here. The following additional compact-support functional supplies the missing test. Its rational coefficients are explicitly defined by `certificate.json`, and their required identities are checked exactly, not inferred from modular ranks.

Write Lambda=lambda24 lambda23. Let
 xi_irr:Mbar24,2 -> Mbar25
be gluing of the two ordered branches of a nonseparating node, and
 xi_1:Mbar24,1 x Mbar1,1 -> Mbar25
be separating gluing. On Mbar24,2 let L=psi1+psi2 and let D be the rational-tail boundary containing both markings. Thus D is isomorphic to Mbar24,1. On the latter space write K=psi1. Write DQ for pushforward of a class Q along this boundary inclusion.

### The certificate and the identities it proves

Each entry of `certificate.json` is a rational coefficient c with one of four label types. The files `pointed.py` and `certificate_rows.py` regenerate the corresponding row exactly overQ:

* `rel`: a degree13 smooth-pointed genus24 3-spin relation P_j, together with its surviving rational-tail term Q_j. After multiplication by Lambda, its full compactified relation is P_j+DQ_j=0.
* `beta`: the row -L times a degree12 symmetric monomial, with at least one marking psi. When the exponents are unequal, the label represents the sum of both exchanges of the marking labels.
* `gamma`: the pair of rows (-K times a degree11 monomial, K^2 times that monomial).
* `single`: a genus24 one-pointed relation of degree12 or13, including its monomial multiplier.

The beta-labelled coefficients define a symmetric polynomial beta of degree12 with312 symmetrized terms. The gamma-labelled coefficients define rho of degree11 with195 terms. In particular every term of beta contains psi1 or psi2.

The certificate is organized in three coefficient blocks, of dimensions1263,272,373 respectively. The exact zero row combination says
 sum u_j P_j-L beta=0,
 sum u_j Q_j-K rho+sum v_j R_j=0,
 K^2 rho+sum w_j S_j=0.                    (1)
Here R_j,S_j are valid one-pointed Pixton relations. The verifier checks all1908 rational coefficients of (1) by direct addition. No modular dependence is substituted for these equalities.

Multiplication by Lambda kills every boundary graph in a one-pointed genus24 relation: nonseparating degeneration kills lambda24, and a positive-genus separating degeneration kills lambda24 lambda23. There is no stable rational tail with only one marked point. Consequently (1), and the full two-pointed relations, give the actual compactified Chow identities
 Lambda(L beta+DK rho)=0,
 Lambda K^2 rho=0.                         (2)

### Why Q_j is the full surviving rational-tail contribution

Here are explicit formulas so that the certificate does not hide any geometric relation. A smooth two-pointed row before a monomial multiplier is
 P_r=[T^r] E48 F_sigma C_a(psi1 T) C_b(psi2 T),
where C0=A,C1=B, a,b in{0,1}. It is eligible when3r>23+|sigma|+a+b and r=23+|sigma|+a+b modulo2. E48 F_sigma is the coefficient expression from the preceding recurrence, with kappa0=48. The one-pointed expression uses kappa0=47.

If m is the multiplicity of1 in sigma, the surviving full-Pixton tail term is DQ_r with
 Q_r=(-1)^(a+b) sum_(k=0)^m binom(m,k)k! [T^(r-1)] E47 F_(sigma minus1^k) H_(a+b+k)(K,T),
 H_even=(1-A(KT))/(KT),
 H_odd =(1+B(KT))/(KT).                    (3)
A multiplier containing either marked psi kills this term. A kappa-only multiplier restricts to the same monomial in the one-pointed kappa classes.

For verification of (3), at the rational tail the standard 3-spin edge factor is
 [zeta_tail(1-A(zeta_main KT))+zeta_main(1+B(zeta_main KT))]/(KT).
The rational vertex factor is zeta_tail, and its two marked leg factors are(-zeta_tail)^(a+b). The selected tail1-insertions contribute zeta_tail^k k!, with binom(m,k) choices. Selecting the required parity gives exactly (3). Only1-insertions can land on Mbar0,3; all others have positive degree there. The tail graph has no automorphism factor and first Betti number zero. The normalization E F_sigma differs from the standard labelled kappa-operator convention by(-1)^length(sigma); its tail and core signs give exactly the sign displayed in (3).

All other graph terms disappear after Lambda: a nonseparating graph kills lambda24, and positive-genus splitting kills lambda24 lambda23. The only surviving rational tree with two markings is this single3-valent rational tail. Thus the use of (3) is a direct specialization of the full Chow-theoretic Pixton relation, not a conjecture about completeness of relations.

### Boundary vanishing and well-definedness on CH(M25)

Define the codimension60 class
 c=(1/2)xi_irr,*(Lambda beta)
   +xi_1,*(Lambda(lambda1-K)rho).           (4)
It restricts to zero on every normalized boundary divisor:

* On Delta_irr, self-intersection of the first term is -Lambda L beta= D Lambda K rho, by (2). The factor1/2 accounts for the two ordered branches. The second term pulls back on D to -D Lambda K rho, so these cancel.
* On Delta_1, beta restricts to zero on D, since both marked psi classes are zero on the3-pointed rational tail. The remaining self-intersection has normal class -(K+psi_ell). On Mbar1,1, psi_ell=lambda1 and lambda1^2=0. Hence it is Lambda K^2rho=0 by (2).
* Every other pullback has a nonseparating or positive-genus splitting in the genus24 core, where Lambda restricts to zero. This also handles all additional branches in the self-intersection formulas.

Therefore f -> integral_Mbar25 f_tilde c factors through CH^12(M25;Q): a difference of extensions is supported on the boundary, and its pairing is zero by localization and the projection formula. This is the crucial additional functional; merely extending a kappa polynomial to the compactification would not suffice.

## 3. Its computable numerical values

For a degree12 kappa polynomial f, put
 A(f)=integral_Mbar24,2 Lambda beta f(kappa_mark2),
 B(f)=integral_Mbar24,1 Lambda rho [f(kappa_mark1)-K partial_(kappa1)f(kappa_mark1)].
Gluing gives
 integral_Mbar25 f_tilde c=(1/2)A(f)+(1/24)B(f).     (5)
Indeed, the elliptic vertex has kappa1=psi1=lambda1, higher kappa_i=0, and integral_Mbar1,1 lambda1=1/24. This proves both the derivative term and the stack normalizations in (5).

For explicit computation, set
 C_g=l_g(kappa_(g-2))*(2g-1)!!/(2g-1)!,
which is nonzero. For a kappa partition mu and psi exponents a1,...,an of total degree g-2+n, the Hodge integral divided by C_g is
 sum_(set partitions P of the indices of mu)
 (-1)^(length(mu)-|P|) (2g-3+n+|P|)!
 /[prod_(blocks E of P)(2 sum_(i in E)mu_i+1)!! * prod_j(2a_j-1)!!].    (6)
For zero psi exponents the instances used here follow by the string equation, with(-1)!!=1. Formula (6) is the inverse of the permutation-cycle psi-pushforward identity; notably there is no extra block factorial in its inversion coefficient. The multiset Bell recurrence in `dual.py` evaluates this sum exactly modulo the chosen prime.

For the genus25 ordinary functionals (n=0), the factorial in (6) is(47+|P|)!. For A in genus24,n2 it is also(47+|P|)!, and for B in genus24,n1 it is(46+|P|)!. Thus, in the normalization used by the verifier, the new column is12A+B, namely24/C24 times (5). All scaling constants are nonzero.

## 4. The lower bound44 and conclusion

The44 classes are precisely the upper-bound survivors kappa_mu, mu in S. Use43 ordinary functionals
 f -> l25(f kappa_nu)/C25,
where the43 degree11 partitions nu are explicitly listed in `lower_columns.json`, and append the new functional24/C24 times (5).

The verifier computes all44by44 matrix entries from (6), beta,rho and (5). Every rational certificate denominator is checked invertible modulo1000003, and the double-factorial denominators are invertible there as well. Its determinant is
 540716 modulo1000003,
which is nonzero. Therefore this rational intersection matrix is invertible overQ. The44 classes are consequently linearly independent in CH^12(M25;Q), hence in R^12(M25).

Combined with the upper bound from the33 independent relations among77 generators, this proves

    dim_Q R^12(M25)=44.

The final extra check that the new functional annihilates all59 target FZ rows independently tests the gluing signs, tail coefficient conventions and factors1/2 and1/24. It is not used instead of the exact certificate or the nonzero lower determinant.
