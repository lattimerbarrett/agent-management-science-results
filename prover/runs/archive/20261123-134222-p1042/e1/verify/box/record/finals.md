# agent_1: last reply

Put
\[
a_m=\frac{m(m-1)(m-2)(m-7)}{24},
\qquad
b_m=\frac{m^4+2m^3+11m^2+10m+12}{12}.
\]
We prove that
\[
\boxed{\displaystyle
|K_m|\simeq
\left(\bigvee^{a_m}S^{m-3}\right)
\vee M(\mathbb Z/2\mathbb Z,m-3)
\vee\left(\bigvee^{b_m}S^{m-2}\right).}
\]

The proof below uses a small, exact integer computation, independent of \(m\). Standalone Sage/Python code verifying that computation—and checking the other algebraic formulas—is included at the end.

## 1. Eliminating the fourth row

Write \(q=m-5\). Filter the augmented simplicial chain complex of \(K_m\) by the number \(a\) of vertices in the first three rows.

Fix a face \(A\) in those rows, and let \(U\) be its unused columns. The possible fourth-row vertices form the complex
\[
\{B\subseteq U:|B|\le q\}.
\]
If \(|U|>q\), its reduced integral homology is concentrated in degree \(q-1=m-6\), where it is
\[
\Lambda^q\operatorname{Aug}(\mathbb Z^U).
\]
If \(|U|\le q\), it is a simplex and has zero reduced homology.

Since \(a\le6<m\), there is always an unused column. Thus there is no exceptional empty-column case. The only surviving terms have \(0\le a\le4\). The spectral sequence has just one nonzero row and therefore collapses.

Here is a convenient explicit description of the resulting chain complex.

### The algebraic model

Use symbols \(x_j,y_{rj}\), where \(j\in[m]\) and \(1\le r\le3\), subject to:

* the \(x_j\)'s anticommute;
* the \(y_{rj}\)'s commute and commute with the \(x_j\)'s;
* any product containing two symbols from the same column is zero.

Let \(B_{m,s}(c_1,c_2,c_3)\) be the free abelian group on monomials of total degree \(s\), with at most \(c_r\) symbols of the form \(y_{rj}\). Give a monomial chain degree equal to its number of \(y\)'s. Define
\[
d(y_{rj})=x_j,\qquad d(x_j)=0
\]
using the odd Leibniz rule, and put \(x=\sum_jx_j\). Define
\[
D_m^s(c)=B_{m,s}(c)\big/xB_{m,s-1}(c).
\tag{1}
\]

For a fixed colored set \(A\) of size \(a\), the corresponding coefficient group in (1) is
\[
\Lambda^{s-a}\left(\mathbb Z^{[m]\setminus\operatorname{cols}(A)}
 \big/\mathbb Z\sum e_j\right).
\]
For \(s=4\), this is precisely the exterior-complement description of the fourth-row homology:
\[
\Lambda^{m-5}\operatorname{Aug}(\mathbb Z^U)
\cong
\Lambda^{4-a}\left(\mathbb Z^U/\mathbb Z\sum e_j\right)
 \otimes\det\operatorname{Aug}(\mathbb Z^U).
\]
The orientation of \(A\), combined with the determinant factor, gives the fixed orientation of \([m]\). Under this identification, deleting a colored vertex becomes \(d(y_{rj})=x_j\). Consequently
\[
\boxed{\displaystyle
\widetilde H_{m-6+a}(K_m;\mathbb Z)
\cong H_a\bigl(D_m^4(2,2,2)\bigr).}
\tag{2}
\]

All the complexes in (2) are complexes of free abelian groups.

## 2. A small local calculation and an anchor exact sequence

For a fixed support of \(s\) columns, \(B_{m,s}(c)\) is, after an orientation change, the augmented chain complex of the three-row complex on those columns with row capacities \(c\). Chain degree \(a\) corresponds to simplicial degree \(a-1\).

The following is the only finite homology calculation needed. Entries not displayed are zero.
\[
\begin{array}{c|c|c|c}
s&c&\text{ranks of successive boundaries}&H_*(B_{\text{one support},s}(c))\\ \hline
4&(2,2,2)&1,11,43,52&H_3=\mathbb Z,\ H_4=\mathbb Z^2\\
3&(1,2,2)&1,8,16&H_3=\mathbb Z^2\\
2&(0,2,2)&1,3&H_2=\mathbb Z\\
2&(1,1,2)&1,5&H_2=\mathbb Z^2\\
1&(0,1,2)&1&H_1=\mathbb Z\\
1&(1,1,1)&1&H_1=\mathbb Z^2
\end{array}
\tag{3}
\]
Permutations of the capacities give the corresponding statements. Every nonzero Smith entry of every boundary in this table is \(1\); thus the table includes integral torsion information, not merely rational ranks.

Choose an anchor column \(h\). Eliminating
\[
x_h=-\sum_{j\ne h}x_j
\]
gives a short exact sequence
\[
0\longrightarrow B_{m-1,s}(c)
\longrightarrow D_m^s(c)
\longrightarrow
\bigoplus_{r:c_r>0}D_{m-1}^{s-1}(c-e_r)[1]
\longrightarrow0.
\tag{4}
\]
Indeed, the first term consists of monomials without a colored vertex in column \(h\); the quotient records its color when it is present.

Apply (4) successively to the capacity lists appearing in (3). It follows inductively that
\[
H_a(D^3(1,2,2))=0\quad(a<3).
\tag{5}
\]
For example, its quotients involve \(D^2(0,2,2)\) and \(D^2(1,1,2)\), then the two \(D^1\)-types in (3). Their local \(B\)-complexes have homology only in their top chain degree.

Now set \(n=m-1\). Equations (3)–(5) imply
\[
H_a(D_m^4(2,2,2))=0\quad(a\le2)
\tag{6}
\]
and give a presentation
\[
H_3(D_m^4(2,2,2))=M_4[n]/I,
\tag{7}
\]
where \(M_4[n]\) is free on symbols \(g_S\), one for each four-subset \(S\subseteq[n]\). Here \(I\) is the connecting image of the three auxiliary groups \(H_3(D_n^3(1,2,2))\).

We next determine this presentation completely.

## 3. Determining the connecting image

### A primitive local coordinate

On a monomial \(x_jy_A\) with three \(y\)'s and four distinct columns, define \(\phi\) as follows:
\[
\phi=
\begin{cases}
+1,&\text{double row, single row is }(1,2),(2,3),(3,1),\\
-1,&\text{the reverse ordered pairs},\\
0,&\text{the three rows are all different}.
\end{cases}
\tag{8}
\]
It annihilates boundaries. On the integral cycle group of the local four-column complex its image is exactly \(6\mathbb Z\). Hence \(\phi/6\) is a primitive coordinate on its \(H_3=\mathbb Z\). These statements are checked over \(\mathbb Z\) in the code below.

Thus, if an auxiliary cycle is represented by a colored cubic polynomial \(z\), its connecting image is represented by \(xz\), and
\[
\delta(z)_S=\frac16\sum_{\substack{T\subseteq S\\|T|=3}} f_z(T),
\tag{9}
\]
where \(f_z(T)\) is the signed color-type sum specified by (8).

### Every relation lies rationally in the pair-incidence span

Consider the auxiliary capacity list \((1,2,2)\), with row \(1\) deficient. The cycle condition says
\[
dz=xw
\tag{10}
\]
for an integral colored quadratic polynomial \(w\).

For each triple \(T\), let \(Z_{223}(T)\), for example, denote the sum of coefficients in \(z\) on assignments having colors \(2,2,3\). Then
\[
f_z=Z_{223}-Z_{221}+Z_{331}-Z_{332}.
\]
On summing the coefficients of \(w\) over the three pairs in \(T\), equation (10) gives
\[
\begin{aligned}
W_{22}&=Z_{221}+Z_{223},&
W_{33}&=Z_{331}+Z_{332},\\
W_{12}&=2Z_{221}+Z_{123},&
W_{13}&=2Z_{331}+Z_{123}.
\end{aligned}
\]
Therefore
\[
f_z(T)=\sum_{\substack{P\subseteq T\\|P|=2}} h(P),
\qquad
h=w_{22}-w_{33}+w_{13}-w_{12},
\]
where \(h(P)\) is integral. Substituting in (9),
\[
\boxed{\displaystyle
\delta(z)_S=\frac13\sum_{\substack{P\subseteq S\\|P|=2}}h(P).}
\tag{11}
\]
The other deficient rows give the same assertion after relabeling.

Define incidence vectors
\[
r_A=\sum_{\substack{|S|=4\\S\supseteq A}}g_S.
\]
Equation (11) proves
\[
I\otimes\mathbb Q\subseteq
\operatorname{span}_{\mathbb Q}\{r_P:|P|=2\}.
\tag{12}
\]

### All singleton and pair incidence relations occur integrally

Put
\[
h_r=\sum_jy_{rj},
\qquad
E_r=\sum_{i<j}y_{ri}y_{rj}.
\]
Then
\[
dh_r=x,\qquad dE_r=xh_r.
\]

For a fixed column \(a\), the auxiliary polynomial
\[
z_a=(y_{1a}-y_{2a})E_3
\]
satisfies the capacities \((1,2,2)\) and is a cycle modulo \(x\). Its signed type sum is
\[
f_{z_a}(T)=2\,1_{\{a\subseteq T\}}.
\]
Equation (9) consequently gives
\[
\delta(z_a)=r_{\{a\}}.
\]

For distinct columns \(a,b\), use
\[
z_{ab}=(y_{1a}-y_{2a})(y_{2b}-y_{3b})h_3.
\]
Again it satisfies the capacities and is a cycle modulo \(x\). Its signed type sum is
\[
f_{z_{ab}}(T)=-3\,1_{\{\{a,b\}\subseteq T\}},
\]
so that
\[
\delta(z_{ab})=-r_{\{a,b\}}.
\]
Thus
\[
L:=\langle r_A:|A|=1\text{ or }2\rangle\subseteq I.
\tag{13}
\]

## 4. The incidence quotient and the surviving \(2\)-torsion

We need the following integral incidence calculation:
\[
\boxed{\displaystyle
M_4[n]/L\cong
\mathbb Z^{\binom n4-\binom n2}\oplus\mathbb Z/2,
\qquad n\ge6.}
\tag{14}
\]

Here is a proof, including the integral lattice issue.

Call \(A=\{a_1<\cdots<a_j\}\subseteq[n]\) ballot if \(a_i\ge2i\). In the free group \(M_k[n]\), the vectors
\[
b_A^k=\sum_{\substack{|T|=k\\T\supseteq A}}T,
\qquad |A|\le\min(k,n-k),\quad A\text{ ballot},
\tag{15}
\]
form an integral basis.

For \(k\le n/2\), this follows by induction, separating subsets and ballot indices according to whether they contain \(n\); the resulting matrix is block triangular with unimodular diagonal blocks. For \(k>n/2\), take complements and use
\[
b_A^k\longmapsto
\sum_{B\subseteq A}(-1)^{|B|}b_B^{n-k}.
\]
Every subset of a ballot set is ballot, so this change is triangular with diagonal entries \(\pm1\).

Let \(I_{s,4}:M_s[n]\to M_4[n]\) be the inclusion matrix. Counting intermediate subsets gives
\[
I_{s,4}(b_A^s)=
\binom{4-|A|}{s-|A|}b_A^4.
\]
For \(s=1,2\), the sum of the two image lattices is therefore diagonal in (15), with entries
\[
\begin{array}{c|ccc}
|A|&0&1&2\\ \hline
\text{entry}&\gcd(4,6)=2&\gcd(1,3)=1&1.
\end{array}
\]
There are \(\binom n2\) basis vectors of ranks at most \(2\), since they form the corresponding basis of \(M_2[n]\). This proves (14). Its torsion generator is
\[
w_n=b_\varnothing^4=\sum_{|S|=4}g_S.
\tag{16}
\]

By (12), (13), and (14), \(M_4[n]/I\) has the free rank in (14), and can differ from (14) only by killing its unique element of order \(2\).

That element does **not** die. Fix any six-subset \(J\subseteq[n]\), and define
\[
Q(v)=\sum_{\substack{S\subseteq J\\|S|=4}}v_S\pmod2.
\]
For any actual relation (11),
\[
\sum_{\substack{S\subseteq J\\|S|=4}}\delta(z)_S
=
\frac13\binom42\sum_{\substack{P\subseteq J\\|P|=2}}h(P)
=
2\sum_{\substack{P\subseteq J\\|P|=2}}h(P),
\]
which is even. Thus \(Q\) annihilates \(I\), whereas
\[
Q(w_n)=\binom64=15\equiv1\pmod2.
\]
Consequently
\[
H_3(D_m^4(2,2,2))
\cong
\mathbb Z^{\binom{m-1}4-\binom{m-1}2}\oplus\mathbb Z/2
=
\mathbb Z^{a_m}\oplus\mathbb Z/2.
\tag{17}
\]

## 5. The remaining homology rank

The complex \(D_m^4(2,2,2)\) ends in chain degree \(4\), so its \(H_4\) is free. Its chain-group ranks are
\[
R_a=c_a\binom ma\binom{m-a-1}{4-a},
\qquad
(c_0,c_1,c_2,c_3,c_4)=(1,3,9,24,54).
\]
The numbers \(c_a\) count assignments of \(a\) columns to three rows, no row occurring more than twice.

By (6) and (17), if \(b=\operatorname{rank}H_4(D_m^4)\), then
\[
b-a_m=\sum_{a=0}^4(-1)^aR_a
=\frac{m^4+14m^3-m^2+34m+24}{24}.
\]
Hence
\[
b=b_m.
\]
Together with (2), we have proved
\[
\widetilde H_i(K_m;\mathbb Z)=
\begin{cases}
\mathbb Z^{a_m}\oplus\mathbb Z/2,&i=m-3,\\
\mathbb Z^{b_m},&i=m-2,\\
0,&\text{otherwise}.
\end{cases}
\tag{18}
\]

## 6. From homology to the homotopy decomposition

First, \(K_m\) is simply connected. Let
\[
J_m=[4]*[4]*\cdots*[4]
\]
be the join of its \(m\) column sets. This is \((m-2)\)-connected. It has the same \(1\)-skeleton as \(K_m\).

Every triangle of \(J_m\) missing from \(K_m\) consists of three vertices in one row of capacity \(2\). Choose a vertex in another row and an unused column. Coning the boundary of the missing triangle to this vertex uses three triangles belonging to \(K_m\). Thus every missing triangular relation already holds in \(\pi_1(K_m)\). Since \(J_m\) is simply connected, so is \(K_m\).

Equation (18) and the Hurewicz theorem now imply that \(K_m\) is \((m-4)\)-connected.

We use a standard elementary consequence of Hurewicz:

> If \(X\) is \((n-1)\)-connected, \(n\ge2\), and its reduced homology is concentrated in degrees \(n,n+1\), then
> \[
> H_n(X)=\mathbb Z^a\oplus\bigoplus_i\mathbb Z/t_i,\qquad
> H_{n+1}(X)=\mathbb Z^b
> \]
> implies
> \[
> X\simeq\bigvee^a S^n\vee\bigvee_iM(\mathbb Z/t_i,n)\vee\bigvee^bS^{n+1}.
> \]

For completeness, Hurewicz gives representatives for the generators of \(H_n\); a representative of order \(t\) extends over the degree-\(t\) Moore space. Also \(\pi_{n+1}(X)\to H_{n+1}(X)\) is onto: choose a wedge \(Y\) of \(n\)-spheres mapping onto \(\pi_n(X)\), and apply relative Hurewicz to the \(n\)-connected mapping-cylinder pair \((X,Y)\). The boundary of a relative lift is zero because \(\pi_n(Y)\to H_n(Y)\) is an isomorphism. Sphere representatives for a basis of \(H_{n+1}\), together with the preceding maps, give a homology equivalence from the stated wedge to \(X\). The simply connected homological Whitehead theorem makes it a homotopy equivalence.

Apply this with \(n=m-3\ge4\) and (18). This proves the boxed decomposition.

---

## 7. Executable exact checks

The following is standalone Python using SageMath. It was run successfully. It:

* constructs all six finite augmented chain complexes in (3);
* computes their **integral Smith forms**, not numerical ranks;
* checks the primitive normalization \(\phi/6\);
* checks every local color pattern in the pair-decomposition identity;
* expands the explicit auxiliary cycles and checks their differentials and connecting coefficients;
* independently checks the incidence lattice calculation for \(n=6,7,8,9\);
* verifies the Euler polynomial symbolically.

```python
from sage.all import (
    ZZ, QQ, matrix, vector, gcd, PolynomialRing, factorial, prod
)
from itertools import combinations, product
from collections import defaultdict
from math import comb

def local(q, b):
    C = [[] for _ in range(q + 1)]
    for a in range(q + 1):
        for J in combinations(range(q), a):
            for R in product(range(3), repeat=a):
                if all(R.count(r) <= b[r] for r in range(3)):
                    C[a].append(tuple(zip(J, R)))
    ids = [{f:i for i, f in enumerate(L)} for L in C]
    D = {}
    for a in range(1, q + 1):
        D[a] = matrix(ZZ, len(C[a-1]), len(C[a]))
        for j, f in enumerate(C[a]):
            for i in range(a):
                D[a][ids[a-1][f[:i] + f[i+1:]], j] = (-1)**i
    ranks = [0]
    for a in range(1, q + 1):
        S = D[a].smith_form(transformation=False)
        nz = [abs(S[i,i]) for i in range(min(S.dimensions()))
              if S[i,i]]
        assert all(t == 1 for t in nz)  # integral primitivity
        ranks.append(len(nz))
        if a >= 2:
            assert D[a-1] * D[a] == 0
    H = tuple(len(C[a]) - ranks[a] -
              (ranks[a+1] if a < q else 0)
              for a in range(q + 1))
    return C, D, H, ranks[1:]

expected = [
    (4, (2,2,2), (0,0,0,1,2)),
    (3, (1,2,2), (0,0,0,2)),
    (2, (0,2,2), (0,0,1)),
    (2, (1,1,2), (0,0,2)),
    (1, (0,1,2), (0,1)),
    (1, (1,1,1), (0,2)),
]
for q, b, H in expected:
    C, D, h, r = local(q, b)
    assert h == H
    print(q, b, "boundary ranks", r, "homology ranks", h)

cyclic = {(0,1), (1,2), (2,0)}
def cweight(R):
    cnt = [R.count(r) for r in range(3)]
    if 2 not in cnt:
        return 0
    return 1 if (cnt.index(2), cnt.index(1)) in cyclic else -1

C, D, _, _ = local(4, (2,2,2))
phi = vector(ZZ, [
    (-1)**next(j for j in range(4)
               if j not in [u for u,r in f])
    * cweight([r for u,r in f])
    for f in C[3]
])
assert phi * D[4] == 0
K = D[3].right_kernel_matrix()  # saturated integral kernel
assert gcd(list(phi * K.transpose())) == 6
print("primitive local functional: gcd = 6")

# Coefficientwise verification of the pair-decomposition identity.
for R in product(range(3), repeat=3):
    if R.count(0) > 1 or any(R.count(r) > 2 for r in (1,2)):
        continue
    rhs = 0
    for i,j in combinations(range(3), 2):
        rs = sorted((R[i], R[j]))
        rhs += (int(rs == [1,1]) - int(rs == [2,2])
                + int(rs == [0,2]) - int(rs == [0,1]))
    assert cweight(list(R)) == rhs

# Squarefree colored polynomials: monomials are tuples (column,row).
def mul(A, B):
    out = defaultdict(int)
    for a,u in A.items():
        for b,v in B.items():
            if len({j for j,r in a+b}) == len(a+b):
                out[tuple(sorted(a+b))] += u*v
    return {a:u for a,u in out.items() if u}

def diff(r, s, j):
    return {((j,r),):1, ((j,s),):-1}

def derivative(z):
    out = defaultdict(int)
    for A,c in z.items():
        for k,(j,r) in enumerate(A):
            out[j, A[:k]+A[k+1:]] += c
    return {a:u for a,u in out.items() if u}

def times_x(w, n):
    return {(j,A):c for A,c in w.items() for j in range(n)
            if j not in [i for i,r in A]}

for n in range(6, 11):
    h = {((j,2),):1 for j in range(n)}
    E = {((i,2),(j,2)):1
         for i,j in combinations(range(n),2)}
    u, v = diff(0,1,0), diff(1,2,1)
    tests = [
        (mul(u,E), mul(u,h), {0}, 2),
        (mul(mul(u,v),h), mul(u,v), {0,1}, -3),
    ]
    for z,w,mark,scale in tests:
        assert all(
            sum(r == 0 for j,r in A) <= 1 and
            all(sum(r == s for j,r in A) <= 2 for s in (1,2))
            for A in z
        )
        assert derivative(z) == times_x(w,n)
        f = defaultdict(int)
        for A,c in z.items():
            f[tuple(j for j,r in A)] += c*cweight([r for j,r in A])
        for T in combinations(range(n),3):
            assert f[T] == scale*int(mark <= set(T))
        for S in combinations(range(n),4):
            val = sum(f[T] for T in combinations(S,3))
            assert val == (6 if len(mark) == 1 else -6) * \
                          int(mark <= set(S))
print("auxiliary cycles and connecting coefficients checked")

# Independent finite checks of the integral ballot/incidence calculation.
for n in range(6,10):
    F = list(combinations(range(n),4))
    ballot = [
        A for j in range(min(4,n-4)+1)
        for A in combinations(range(1,n+1),j)
        if all(a >= 2*(i+1) for i,a in enumerate(A))
    ]
    U = matrix(ZZ, [
        [int(set(a-1 for a in A) <= set(S)) for S in F]
        for A in ballot
    ])
    assert abs(U.det()) == 1
    rows = [A for j in (1,2)
            for A in combinations(range(n),j)]
    N = matrix(ZZ, [
        [int(set(A) <= set(S)) for A in rows] for S in F
    ])
    T = N.smith_form(transformation=False)
    nz = [abs(T[i,i]) for i in range(min(T.dimensions())) if T[i,i]]
    assert nz.count(1) == comb(n,2)-1
    assert nz.count(2) == 1 and len(nz) == comb(n,2)
print("incidence lattices checked for n=6,7,8,9")

P = PolynomialRing(QQ, 'm')
m = P.gen()
def binpol(z,k):
    return prod(z-i for i in range(k))/factorial(k)

a = m*(m-1)*(m-2)*(m-7)/24
r = [binpol(m,k)*[1,3,9,24,54][k]*binpol(m-k-1,4-k)
     for k in range(5)]
b = a + sum((-1)**k*r[k] for k in range(5))
assert b == (m**4+2*m**3+11*m**2+10*m+12)/12
print("Euler polynomial:", b)
```

In particular, the finite calculation, the integral lattice argument, and the parity argument together establish the unique \(\mathbb Z/2\)-summand uniformly for every \(m\ge7\), rather than extrapolating it from small values.

# agent_2: last reply

Completed and checked:

- Exact integral homology computations for \(m=7,\ldots,11\), confirming the stated ranks and unique \(\mathbb Z/2\) summand.
- All finite auxiliary chain complexes needed in the uniform proof.
- Primitivity of the local homology coordinate \(\phi/6\).
- Explicit singleton and pair relations, including their signs and coefficients.
- The Euler-characteristic polynomial giving the claimed sphere multiplicity.

A compact, self-contained executable certificate is saved as `workspace/agent2_compact_core_certificate.py`; broader checks and outputs are also saved.

The team’s mathematical proof is complete. Agent 1 is assembling the final proof and runnable certificate; no mathematical steps remain outstanding.

# agent_3: last reply

Uniform homology calculation completed and checked.

- Proved
  \[
  \widetilde H_{m-3}(K_m;\mathbb Z)
  \cong \mathbb Z^{\binom m4-\binom m3}\oplus\mathbb Z/2.
  \]
- Proved vanishing below degree \(m-3\) by the anchor-column exact sequence.
- Derived explicit singleton and pair relations and proved the unique \(2\)-torsion class survives using a uniform parity functional.
- Supplied the determinant calculation identifying the polynomial chain model with the row-four spectral reduction.
- Wrote and ran exact Python checks of all universal cycle identities, projection coefficients, and local cocycle identities.

Files:
- `workspace/agent3_uniform_homology.md`
- `workspace/agent3_polynomial_checks.py`
- `workspace/agent3_polynomial_checks.json`

Together with the teammates’ Euler-characteristic, incidence-lattice, and topological splitting arguments, the mathematical proof is complete. Agent 1 is assembling the final presentation.

# agent_4: last reply

Completed the topological and integral-linear-algebra parts of the proof:

- Proved simple connectivity by explicitly filling every missing triangle.
- Constructed elementary collapses reducing the dimension to \(m-2\).
- Proved the Hurewicz and Moore-space splitting statements needed to turn the computed homology into the asserted homotopy type.
- Proved, using an integral ballot-subset basis, that
  \[
  \mathbb Z^{\binom n4}/\langle r_i,r_{ij}\rangle
  \cong \mathbb Z^{\binom n4-\binom n2}\oplus\mathbb Z/2,
  \]
  with the total sum of generators representing the torsion class.
- Executed exhaustive topological checks for \(m=7,8,9\), and exact integral incidence-matrix checks for \(n=6,\ldots,10\).

Proofs and reproducible checks are saved in:
- `workspace/agent4_topology.md`
- `workspace/agent4_topology_checks.py`
- `workspace/agent4_incidence_lemma.md`
- `workspace/agent4_incidence_checks.py`

The team’s uniform homology argument now supplies the remaining ingredient. No mathematical steps remain unresolved; agent_1 is assembling the complete proof and code.