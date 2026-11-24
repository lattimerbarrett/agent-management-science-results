# agent_1: last reply

\[
\boxed{\dim_{\mathbb Q}R^{12}(\mathcal M_{25})=44.}
\]

We completed both bounds, including the extra lower-bound argument that the ordinary socle pairing does **not** provide.

The complete proof, Python source, and explicit rational certificate are in:

**[`workspace/M25_degree12_exact_proof.zip`](workspace/M25_degree12_exact_proof.zip)**

After extraction, run:
```bash
python verify.py
```
The verifier requires only Python’s standard library. It regenerates relation coefficients, verifies exact rational polynomial identities, and computes the two determinants below. It does not assume a dimension table, completeness of Faber–Zagier relations, or a Gorenstein conjecture.

## 1. Established geometric inputs

We use:

1. **The Chow-theoretic Pixton \(3\)-spin relations**, with the explicit PPZ formula and Janda’s Chow-theoretic proof. In particular, their smooth restrictions give Faber–Zagier relations. Using the Chow theorem, rather than merely its cohomological counterpart, is essential here.

2. **Faber’s Hodge intersection formula.** There is a nonzero rational constant \(H_g\) such that
   \[
   \int_{\overline{\mathcal M}_{g,n}}
   \lambda_g\lambda_{g-1}\prod_i\psi_i^{d_i}
   =
   H_g\frac{(2g-3+n)!}{\prod_i(2d_i-1)!!},
   \qquad
   \sum_i(d_i-1)=g-2.
   \]
   The instances with one zero exponent used below follow from the string equation.

Here \(\lambda_i\) denotes the \(i\)-th Chern class of the Hodge bundle. The class \(\lambda_g\lambda_{g-1}\) restricts to zero on every boundary divisor of \(\overline{\mathcal M}_g\). Thus
\[
f\longmapsto\int_{\overline{\mathcal M}_g}
\widetilde f\,\lambda_g\lambda_{g-1}
\]
is well-defined on the Chow ring of \(\mathcal M_g\).

On pointed compactifications, all \(\kappa\)-classes below are the standard log-pointed classes.

## 2. Upper bound: \(44\)

There are \(p(12)=77\) degree-\(12\) \(\kappa\)-monomials.

For clarity, here are the precise relation conventions used by the computation. Put
\[
A(t)=\sum_{n\ge0}\frac{(6n)!}{(3n)!(2n)!}t^n,\qquad
B(t)=\sum_{n\ge0}\frac{(6n)!}{(3n)!(2n)!}
                 \frac{6n+1}{6n-1}t^n,
\]
so \(A_0=1\) and \(B_0=-1\). Write \(U=B/A\), and let
\[
\mathcal K_k\!\left(\sum c_nt^n\right)
=\sum c_n\kappa_nt^n,\qquad \kappa_0=k.
\]
Set \(E_k=\exp(-\mathcal K_k(\log A))\). For a labelled list \(\sigma\), define
\[
F_\sigma^{(k)}
=
\sum_{\mathcal P}
\prod_{J\in\mathcal P}
(-1)^{|J|}(|J|-1)!
\mathcal K_k\!\left(
t^{\sum_{j\in J}\lfloor\sigma_j/3\rfloor}
U^{\,\#\{j\in J:\sigma_j\equiv1\pmod3\}}
\right),
\]
where the sum is over set partitions of its entries.

With \(C_0=A,C_1=B\), the smooth pointed relation is
\[
P_{g,n,r;\sigma,a}
=
[t^r]E_{2g-2+n}F_\sigma^{(2g-2+n)}
\prod_i C_{a_i}(\psi_it),
\]
provided
\[
3r\ge g+1+|\sigma|+\sum_i a_i,\qquad
r\equiv g-1+|\sigma|+\sum_i a_i\pmod2.
\]

For \(g=25,n=0\), take \(r=9,10,11,12\), all eligible \(\sigma\), and multiply by all \(\kappa\)-monomials of degree \(12-r\). This gives \(59\) relation vectors among the \(77\) generators.

The verifier constructs these vectors and finds a \(33\times33\) minor with determinant
\[
368438425\pmod{1\,000\,000\,007}.
\]
The prime and the relevant denominator conditions are checked. Hence these \(33\) Chow relations are independent over \(\mathbb Q\), and the remaining \(44\) monomials span. Therefore
\[
\dim_{\mathbb Q}R^{12}(\mathcal M_{25})\le44.
\]

## 3. The additional lower-bound functional

The ordinary \(\lambda_{25}\lambda_{24}\) pairing has rank only \(43\). We construct another functional on the **actual Chow group**.

Let
\[
\xi_{\mathrm{irr}}:\overline{\mathcal M}_{24,2}
 \longrightarrow\overline{\mathcal M}_{25}
\]
be ordered nonseparating gluing, and let
\[
\xi_1:\overline{\mathcal M}_{24,1}\times
\overline{\mathcal M}_{1,1}
\longrightarrow\overline{\mathcal M}_{25}
\]
glue an elliptic tail. Write
\[
\Lambda=\lambda_{24}\lambda_{23},\qquad
L=\psi_1+\psi_2.
\]
Let \(D\cong\overline{\mathcal M}_{24,1}\) be the rational-tail divisor in \(\overline{\mathcal M}_{24,2}\) containing both markings, and put \(K=\psi_1\) on \(\overline{\mathcal M}_{24,1}\).

The explicit rational certificate supplies:

- a symmetric degree-\(12\) polynomial \(\beta\), every term of which contains a marked \(\psi\);
- a degree-\(11\) polynomial \(\rho\);

and proves the following identities in Chow:
\[
\Lambda L\beta+D_*(\Lambda K\rho)=0,
\tag{1}
\]
\[
\Lambda K^2\rho=0.
\tag{2}
\]

These identities are checked **exactly over \(\mathbb Q\)**, not inferred from a modular kernel.

Define
\[
c=
\frac12\xi_{\mathrm{irr}*}(\Lambda\beta)
+
\xi_{1*}\bigl(\Lambda(\lambda_1-K)\rho\bigr)
\in\mathrm{CH}^{60}(\overline{\mathcal M}_{25};\mathbb Q).
\tag{3}
\]

### Why this defines a functional on the open moduli space

The class \(c\) restricts to zero on every normalized boundary divisor:

- On \(\Delta_{\mathrm{irr}}\), the first self-intersection is
  \(-\Lambda L\beta=D_*(\Lambda K\rho)\), by (1). The factor \(1/2\) cancels the two orderings of the branches. The elliptic-tail contribution is its negative.

- On \(\Delta_1\), the first summand restricts to zero because \(\beta|_D=0\). The normal class of \(\Delta_1\) is \(-(K+\lambda_1)\), and \(\lambda_1^2=0\). The second self-intersection is therefore \(\Lambda K^2\rho=0\), by (2).

- Every other contribution contains a boundary in the genus-\(24\) core and is killed by \(\Lambda\). The same observation kills the additional multiple-node self-intersection components.

Consequently, localization and the projection formula show that
\[
f\longmapsto\int_{\overline{\mathcal M}_{25}}\widetilde f\,c
\tag{4}
\]
factors through \(\mathrm{CH}^{12}(\mathcal M_{25};\mathbb Q)\). In particular, this functional cannot detect a polynomial that is zero modulo rational equivalence on \(\mathcal M_{25}\).

### How identities (1)–(2) are certified

For a two-pointed relation \(P_r\), multiplication of the full Pixton relation by \(\Lambda\) kills every graph term except the rational-tail graph \(D\). Its correction is \(D_*Q_r\), where, if \(m\) is the number of \(1\)-parts in \(\sigma\),
\[
Q_r=(-1)^{a+b}\sum_{j=0}^m
\binom mj j!\,
[t^{r-1}]
E_{47}F_{\sigma\setminus1^j}^{(47)}
H_{a+b+j}(K,t),
\]
with
\[
H_{\mathrm{even}}=\frac{1-A(Kt)}{Kt},
\qquad
H_{\mathrm{odd}}=\frac{1+B(Kt)}{Kt}.
\]
This is the explicit \(3\)-spin edge factor at the rational-tail cotangent class \(0\). Only \(1\)-parts of \(\sigma\) can lie on \(\overline{\mathcal M}_{0,3}\), giving the factor \(\binom mjj!\).

The certificate consists of \(1553\) rational row coefficients. Its three blocks assert:

1. a degree-\(13\), two-pointed relation expressing \(L\beta\);
2. its degree-\(12\) rational-tail correction equals \(K\rho\), modulo one-pointed relations;
3. \(K^2\rho\) is a one-pointed relation.

There are \(1263+272+373=1908\) polynomial coefficients. The verifier regenerates every selected relation from the displayed formulas, checks its eligibility, and verifies that **all \(1908\) rational coefficients are exactly zero**. This proves (1)–(2). The resulting \(\beta\) has \(312\) symmetric terms, and \(\rho\) has \(195\) terms.

## 4. Lower bound: \(44\)

For a degree-\(12\) polynomial \(f\), gluing gives
\[
\int \widetilde f\,c=\frac12A(f)+\frac1{24}B(f),
\]
where
\[
A(f)=\int_{\overline{\mathcal M}_{24,2}}
\Lambda\beta\,f(\kappa_{\mathrm{marked}}),
\]
\[
B(f)=\int_{\overline{\mathcal M}_{24,1}}
\Lambda\rho
\left(f(\kappa_{\mathrm{marked}})
-K\frac{\partial f}{\partial\kappa_1}
       (\kappa_{\mathrm{marked}})\right).
\]
Here we used
\[
\kappa_1=\lambda_1,\quad \kappa_i=0\ (i\ge2),
\quad
\int_{\overline{\mathcal M}_{1,1}}\lambda_1=\frac1{24}.
\]

All entries are computed by the Hodge formula and inversion of the \(\psi\)-to-\(\kappa\) pushforward identity. Explicitly, for \(\mu=(\mu_1,\ldots,\mu_s)\), the normalized mixed integral is
\[
\sum_{\mathcal P}
(-1)^{s-|\mathcal P|}
\frac{(2g-3+n+|\mathcal P|)!}
{\displaystyle
 \prod_i(2a_i-1)!!
 \prod_{J\in\mathcal P}
 \left(2\sum_{j\in J}\mu_j+1\right)!!}.
\tag{5}
\]
The program computes this set-partition sum by a cached multiset recurrence.

Take the same \(44\) monomials that survived the upper-bound elimination. Evaluate them against:

- \(43\) ordinary functionals
  \[
  f\longmapsto
  \int_{\overline{\mathcal M}_{25}}
  f\,\kappa_q\,\lambda_{25}\lambda_{24},
  \qquad |q|=11;
  \]
- the new functional (4).

The \(43\) partitions \(q\) are explicitly provided in `lower_columns.json`. After independently rescaling columns by their nonzero Hodge constants, the verifier obtains a \(44\times44\) determinant
\[
\boxed{540716\pmod{1\,000\,003}}.
\]
Every certificate denominator is checked to be invertible at this prime. Thus the determinant is nonzero over \(\mathbb Q\), proving that these \(44\) Chow classes are independent:
\[
\dim_{\mathbb Q}R^{12}(\mathcal M_{25})\ge44.
\]

Combining the bounds proves the answer.

## 5. Actual Python verification

The final, standard-library-only verifier was executed successfully, as were independent rational-arithmetic implementations. Its output is:
```text
Exact rational Pixton certificate: all 1908 identities verified.
Witness rows: 1553  beta terms: 312  rho terms: 195
Upper 33 by 33 minor mod 1000000007 : 368438425
Lower 44 by 44 minor mod 1000003 : 540716
All 59 known target FZ relations annihilated by the new functional.
VERIFIED: dimension <= 44 and dimension >= 44; hence dimension = 44.
```

The full archive includes `proof.md`, `verify.py`, the coefficient-generation modules, and the explicit rational certificate. Its SHA-256 is
```text
e71819b06159e9794d2cc2f3d81c2c5fb165313fe360c2d4f071742ad3b96107
```

# agent_2: last reply

The proof is now complete.

- **Upper bound:** 33 independent Faber–Zagier relations among the 77 degree-12 κ-monomials. The certified minor is
  \[
  368438425\pmod{1000000007},
  \]
  proving \(\dim R^{12}\le44\).

- **Lower bound:** The coupled Pixton-relation construction produces an exact rational compactly supported dual class. All **1,908 rational identities** defining it have been independently verified. Combining this functional with 43 ordinary Hodge-pairing functionals gives a \(44\times44\) matrix whose determinant is
  \[
  540716\pmod{1000003}\ne0.
  \]
  Hence the 44 surviving κ-monomials are independent in Chow.

Therefore
\[
\boxed{\dim_{\mathbb Q}R^{12}(\mathcal M_{25})=44}.
\]

I independently checked the exact witness and the lower determinant. The team’s standalone, standard-library Python verifier is `workspace/agent1_bundle/verify.py`; it regenerates the relations rather than trusting cached matrices. Nothing mathematical remains outstanding.

# agent_3: last reply

Final standalone verifier independently rerun successfully in 17 seconds:

- all **1,908 exact rational identities** verified;
- every certificate relation’s eligibility checked;
- upper-bound determinant: **368438425 modulo 1000000007**;
- lower-bound determinant: **540716 modulo 1000003**;
- all 59 known relations annihilated by the new functional.

The proof and computation establish \(\boxed{44}\).

# agent_4: last reply

Final bundle independently audited and executed successfully using only the Python standard library.

Verified:
- all **1,908 exact rational certificate identities**;
- upper-bound determinant **368438425 mod \(10^9+7\)**;
- lower-bound determinant **540716 mod \(1000003\)**;
- annihilation of all 59 known target relations by the new functional.

The complete proof narrative is in `workspace/agent1_bundle/proof.md`, with an independent copy in `workspace/agent4_full_proof_final.md`. All geometric normalizations and Chow-theoretic steps have passed final audit. The result is proved:
\[
\boxed{\dim_{\mathbb Q}R^{12}(\mathcal M_{25})=44}.
\]