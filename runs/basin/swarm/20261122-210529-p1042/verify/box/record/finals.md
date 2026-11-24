# agent_1: last reply

Here is one uniform answer. The formulas use gcds of finite, explicitly specified lists of integers. They are large formulas, but are nonrecursive: in particular, they do not contain unevaluated homology groups, matrix ranks, or Smith normal forms.

Write \(\mathbf1_P=1\) if a statement \(P\) holds, and \(0\) otherwise. A sum with an empty indexing set is zero.

## Explicit arithmetic functions used in the answer

Define two sets of ordered pairs of subsets of \([m]\):
\[
\begin{split}
\mathcal R_m
 &=\{(A,B):A\cap B=\varnothing,\ |A|\ge3,\ |A|+|B|\le m-3\},\\
\mathcal C_m
 &=\{(C,D):C\cap D=\varnothing,\ |D|\le m-5,\
                  m-|C|-|D|\le2\}.
\end{split}
\]
Their sizes are explicitly
\[
 R_m=\sum_{a=3}^{m-3}\binom ma
                  \sum_{b=0}^{m-a-3}\binom{m-a}{b},
\qquad
 C_m=\sum_{e=0}^{2}\binom me
                  \sum_{d=0}^{m-5}\binom{m-e}{d}.
\]
Put \(L_m=\min(R_m,C_m)\).

The next definition involves only sums, products, and gcds of zeros and ones. Set \(\Delta_0(m)=1\). For \(1\le j\le L_m\), let
\[
\boxed{\quad
\Delta_j(m)=
\gcd\left\{
\left|
 \sum_{\pi\in S_j}\operatorname{sgn}(\pi)
 \prod_{\ell=1}^j
 \mathbf1_{A_\ell\subseteq C_{\pi(\ell)}}
 \mathbf1_{B_\ell\subseteq D_{\pi(\ell)}}
\right|:
\begin{array}{l}
(A_1,B_1),\ldots,(A_j,B_j)\text{ distinct in }\mathcal R_m,\\
(C_1,D_1),\ldots,(C_j,D_j)\text{ distinct in }\mathcal C_m
\end{array}
\right\}.
\quad}                                                    \tag{1}
\]
The gcd of a list consisting entirely of zeros is zero.

Finally, define
\[
\begin{split}
\rho_m&=\sum_{j=1}^{L_m}\mathbf1_{\Delta_j(m)>0},\\
Q_m&=\sum_{a=3}^{m-6}\binom ma
                     \sum_{b=3}^{m-a-3}\binom{m-a}{b},\\
a_m&=R_m-Q_m-\rho_m,\\
b_m&=a_m+\frac{m^4+14m^3-m^2+34m+24}{24},                 \tag{2}\\
\mu_t(m)&=\sum_{j=1}^{L_m}
 \mathbf1_{\{\Delta_j(m)>0,\ \Delta_j(m)=t\Delta_{j-1}(m)\}}
 \qquad(t\ge2).
\end{split}
\]

Thus every function in (1)–(2) is a specified finite arithmetic function of \(m\).

## Answer

For every \(m\ge7\),
\[
\boxed{
 |K_m|\ \simeq\
 \bigvee^{a_m} S^{m-3}
 \ \vee\
 \bigvee^{b_m} S^{m-2}
 \ \vee\
 \bigvee_{t=2}^{L_m!}
       \bigvee^{\mu_t(m)}M(\mathbb Z/t\mathbb Z,m-3).
}                                                        \tag{3}
\]
In particular, the only sphere dimensions are \(m-3,m-2\), and every Moore space has bottom dimension \(m-3\). The formulas above specify every cyclic order and every multiplicity. The very generous finite upper limit \(L_m!\) can be used without any exceptions.

For example, actual evaluations give
\[
\begin{split}
|K_7|&\simeq M(\mathbb Z/2,4)\ \vee\ \bigvee^{309}S^5,\\
|K_8|&\simeq M(\mathbb Z/2,5)\
       \vee\ \bigvee^{14}S^5\
       \vee\ \bigvee^{493}S^6.
\end{split}                                               \tag{4}
\]

The rest of the answer proves (3), including why the arithmetic formulas determine the homotopy type, and gives executable checks.

---

# Proof

All chain complexes and homology groups below have integer coefficients, and reduced chains are used.

Put
\[
(k_1,k_2,k_3,k_4)=(2,2,2,m-5).
\]
Notice the two useful facts
\[
k_i\ge2,\qquad \sum_i k_i=m+1.                              \tag{5}
\]

## 1. Relaxing row restrictions

Let \(J\) be the complex imposing just the column restrictions. Thus
\[
J=\{1,2,3,4\}^{*m},
\]
a join of \(m\) four-point spaces.

For \(S\subseteq[4]\), let \(X_S\) impose the row restrictions only for rows in \(S\). In particular,
\[
X_\varnothing=J,\qquad X_{[4]}=K_m.
\]

We need a simple observation about a complex \(X_S\) having an unrestricted row \(r\notin S\).

Fix the part \(\sigma\) of a face outside row \(r\). If \(\sigma\) does not occupy every column, pair faces by adding or removing the row-\(r\) vertex in the smallest unoccupied column. This is an acyclic matching: the map taking a face to its part outside row \(r\) is order-preserving, and in each fiber the matching is the standard cone matching.

The only nontrivial critical faces occupy every column and avoid row \(r\). Consequently,
\[
X_S\simeq\text{a wedge of }(m-1)\text{-spheres}
\qquad(S\ne[4]).                                         \tag{6}
\]
The possibility of a wedge with zero spheres is included.

If \(|S|=3\), the total capacity outside its unique unrestricted row \(r\) is
\[
m+1-k_r\le m-1.
\]
There is then no full-column critical face. Therefore
\[
X_S\text{ is contractible when }|S|=3.                    \tag{7}
\]

Here and below, the augmented matching can equivalently be converted to an ordinary matching by retaining one vertex as the basepoint.

## 2. An exact complex associated with the four restrictions

For each face \(F\) of \(J\), let
\[
T(F)=\{i: F\text{ satisfies the restriction in row }i\}.
\]
This set is nonempty. Indeed, violation of all four restrictions would require at least
\[
\sum_i(k_i+1)=m+5
\]
vertices, whereas a face of \(J\) has at most \(m\) vertices.

The augmented simplex chain complex on \(T(F)\), summed over all faces \(F\), gives an exact sequence of chain complexes
\[
0\longrightarrow \widetilde C(K_m)
 \longrightarrow \bigoplus_{|S|=3}\widetilde C(X_S)
 \longrightarrow \bigoplus_{|S|=2}\widetilde C(X_S)
 \longrightarrow \bigoplus_{|S|=1}\widetilde C(X_S)
 \longrightarrow \widetilde C(J)
 \longrightarrow0.                                      \tag{8}
\]

Write
\[
W=\widetilde H_{m-1}(J),\quad
M_i=\widetilde H_{m-1}(X_{\{i\}}),\quad
M_{ij}=\widetilde H_{m-1}(X_{\{i,j\}}).
\]
Equations (6)–(8), or the long exact sequences obtained by breaking (8) into short exact sequences, imply that all reduced homology of \(K_m\) vanishes except possibly in dimensions
\[
m-4,\quad m-3,\quad m-2.
\]
More precisely, it is the homology of
\[
\bigoplus_{i<j}M_{ij}
   \xrightarrow{d_2}
\bigoplus_i M_i
   \xrightarrow{d_1}
W,                                                       \tag{9}
\]
with
\[
\begin{split}
\widetilde H_{m-4}(K_m)&=\operatorname{coker}d_1,\\
\widetilde H_{m-3}(K_m)&=\ker d_1/\operatorname{im}d_2,\\
\widetilde H_{m-2}(K_m)&=\ker d_2.
\end{split}                                               \tag{10}
\]
In particular, the last group is free abelian.

## 3. Explicit descriptions of these lattices

Let \(e_1,e_2,e_3,e_4\) denote the four vertices of a column. Then
\[
W=\left(\ker(\mathbb Z^4\xrightarrow{\text{sum}}\mathbb Z)\right)^{\otimes m}.
\]
Use the basis
\[
x_1=e_1-e_4,\quad x_2=e_2-e_4,\quad x_3=e_3-e_4.
\]
Thus \(W\) has a basis of words of length \(m\) in \(x_1,x_2,x_3\).

More generally, if row \(r\) is unrestricted, the top cycles of \(X_S\) have the basis
\[
\bigotimes_{j=1}^m(e_{a_j}-e_r),                            \tag{11}
\]
where \(a_j\ne r\) and each restricted row occurs at most its capacity.

To see this directly, coefficients on full faces avoiding row \(r\) determine any top cycle uniquely, by the zero-sum relation in each column. Expanding (11) supplies exactly that cycle, and does not increase any restricted-row count.

In the \(x\)-basis, \(M_i\), for \(i=1,2,3\), is the coordinate subgroup spanned by words with at most two occurrences of \(x_i\). Set
\[
U=M_1+M_2+M_3,\qquad Q=W/U.
\]
The group \(Q\) is free on words in which each of \(x_1,x_2,x_3\) occurs at least three times. Its rank is exactly \(Q_m\) in (2).

Also, the three coordinate subgroups have zero triple intersection: a word of length \(m\ge7\) cannot have all three counts at most two. Hence
\[
0\longrightarrow M_{12}\oplus M_{13}\oplus M_{23}
 \longrightarrow M_1\oplus M_2\oplus M_3
 \longrightarrow U\longrightarrow0                       \tag{12}
\]
is exact.

Eliminating the exact part (12) from (9) gives
\[
\widetilde H_{m-3}(K_m)
 \cong
 \frac{\ker(M_4\longrightarrow Q)}
      {M_{14}+M_{24}+M_{34}},
\qquad
\widetilde H_{m-4}(K_m)
 \cong\operatorname{coker}(M_4\longrightarrow Q).           \tag{13}
\]

## 4. The map \(M_4\to Q\) is onto

Use row \(3\) as the unrestricted row in (11). A basis of \(M_4\) consists of tensor words in
\[
y_1=x_1-x_3,\qquad y_2=x_2-x_3,\qquad y_4=-x_3
\]
having at most \(m-5\) occurrences of \(y_4\).

Consider a basis word of \(Q\). It has at least three occurrences each of \(x_1,x_2,x_3\). Replace every \(x_1\) by \(x_1-x_3\), every \(x_2\) by \(x_2-x_3\), and retain the \(x_3\)'s. The resulting tensor belongs to \(M_4\): there are at least six non-\(x_3\) positions.

Its expansion equals the original word plus words with fewer occurrences of \(x_1,x_2\) in total. Induction on that total, discarding words zero in \(Q\), proves surjectivity. Thus
\[
\widetilde H_{m-4}(K_m)=0.                                \tag{14}
\]

Put
\[
N=M_4/(M_{14}+M_{24}+M_{34}).
\]
Equations (13)–(14) give a short exact sequence
\[
0\longrightarrow \widetilde H_{m-3}(K_m)
 \longrightarrow N\longrightarrow Q\longrightarrow0.
\]
Since \(Q\) is free,
\[
N\cong \widetilde H_{m-3}(K_m)\oplus\mathbb Z^{Q_m}.        \tag{15}
\]

## 5. A \(0/1\) presentation of \(N\)

Continue to use the \(y_1,y_2,y_4\) basis.

The subgroups \(M_{14}\) and \(M_{24}\) are coordinate subgroups: they impose, respectively, at most two occurrences of \(y_1\) and of \(y_2\). After quotienting by them, the remaining basis words have at least three occurrences each of \(y_1,y_2\).

The capacity on \(y_4\) is now automatic: such a word has at most \(m-6\) occurrences of \(y_4\). The surviving basis can therefore be indexed by \(\mathcal R_m\), where \(A\) is the set of \(y_1\)-positions and \(B\) the set of \(y_4\)-positions.

To describe \(M_{34}\), use row \(2\) as the unrestricted row. Its basis consists of words in
\[
z_1=e_1-e_2=y_1-y_2,\quad
z_3=e_3-e_2=-y_2,\quad
z_4=e_4-e_2=y_4-y_2
\]
with at most two occurrences of \(z_3\) and at most \(m-5\) occurrences of \(z_4\). These words are indexed by \(\mathcal C_m\), taking \(C,D\) as the \(z_1,z_4\)-positions.

The coefficient of row \((A,B)\) in the column \((C,D)\) is
\[
(-1)^{m-|A|-|B|}
 \mathbf1_{A\subseteq C}\mathbf1_{B\subseteq D}.
\]
Changing signs of rows removes the sign. Hence \(N\) has the explicit presentation matrix
\[
P_m[(A,B),(C,D)]
 =\mathbf1_{A\subseteq C}\mathbf1_{B\subseteq D},
\qquad
(A,B)\in\mathcal R_m,\ (C,D)\in\mathcal C_m.               \tag{16}
\]

This proves the presentation, not just its ranks over a field.

By the integral Smith theorem, the gcds of the \(j\)-rowed minors of \(P_m\) are its determinantal divisors. Formula (1) is precisely the permutation expansion of those minors. Consequently:

* its rank is \(\rho_m\);
* its nonzero invariant factors are
  \(\Delta_j(m)/\Delta_{j-1}(m)\), \(1\le j\le\rho_m\);
* the multiplicity of a nontrivial invariant factor \(t\) is \(\mu_t(m)\).

Every minor has absolute value at most \(j!\), by its permutation expansion. Thus no nontrivial invariant factor exceeds \(L_m!\).

Combining this with (15) proves
\[
\widetilde H_{m-3}(K_m)
 \cong
 \mathbb Z^{a_m}\oplus
 \bigoplus_{t=2}^{L_m!}(\mathbb Z/t)^{\mu_t(m)}.             \tag{17}
\]
In particular, the quantity \(a_m\) in (2) is a nonnegative integer.

## 6. The other Betti number

A face with row sizes \(s_1,s_2,s_3,s_4\) occurs
\[
\frac{m!}{s_1!s_2!s_3!s_4!(m-s_1-s_2-s_3-s_4)!}
\]
times. Hence the reduced Euler characteristic is an explicit alternating sum of these numbers.

Summing first over \(s_4\), using
\[
\sum_{d=0}^{q}(-1)^d\binom nd=(-1)^q\binom{n-1}{q}
\quad(q<n),
\]
gives
\[
(-1)^{m-2}\widetilde\chi(K_m)
 =
 \sum_{\substack{0\le u,v,w\le2\\s=u+v+w\le4}}
 (-1)^s
 \frac{m!}{u!v!w!(m-s)!}
 \binom{m-s-1}{4-s}.
\]
Expanding this degree-four expression yields
\[
(-1)^{m-2}\widetilde\chi(K_m)
 =\frac{m^4+14m^3-m^2+34m+24}{24}.                         \tag{18}
\]

Only the two homology groups in dimensions \(m-3,m-2\) remain, and the latter is free. Equations (17)–(18) therefore show that its rank is \(b_m\) in (2).

## 7. Passing from homology to homotopy

First, \(K_m\) is simply connected.

It has the entire one-skeleton of \(J\). A triangle of \(J\) missing from \(K_m\) must consist of three vertices in one row of capacity two. Choose a vertex in another row and a column outside the triangle. Coning the triangle's boundary to this vertex fills that boundary by three triangles of \(K_m\). Thus every triangular relation in \(J\) already holds in \(K_m\).

The join \(J\) is simply connected, so \(K_m\) is simply connected. Its homology vanishes through dimension \(m-4\), by (10) and (14). Repeated application of Hurewicz now shows that \(K_m\) is \((m-4)\)-connected.

We use the following elementary consequence of Hurewicz and Whitehead:

> If a simply connected space is \((n-1)\)-connected, its reduced homology is concentrated in dimensions \(n,n+1\), and \(H_{n+1}\) is free, then it is a wedge of \(n\)-spheres, \((n+1)\)-spheres, and Moore spaces \(M(\mathbb Z/t,n)\), with multiplicities determined by its homology.

For completeness, represent generators of \(H_n\) by \(n\)-spheres using Hurewicz. For a generator of order \(t\), the degree-\(t\) multiple is nullhomotopic, so the map extends over \(M(\mathbb Z/t,n)\). Their wedge maps to the space and is an isomorphism on \(H_n\). Relative Hurewicz then shows that generators of the free \(H_{n+1}\) can be represented by \((n+1)\)-spheres. The resulting map is a homology equivalence between simply connected spaces, and hence a homotopy equivalence.

Apply this with \(n=m-3\) and use (17)–(18). This proves (3).

---

# Python computation and independent checks

The following is ordinary Python using the provided Sage library. It evaluates the answer efficiently using exact Smith computations; the determinantal-divisor theorem proves that this computes the arithmetic functions (1)–(2).

It also independently constructs the original simplicial complexes for \(m=7,8\), computes their integral simplicial homology, compares every group with the answer, and checks the Euler-characteristic calculation by a separate face-count sum.

```python
from sage.all import matrix, ZZ, SimplicialComplex
from itertools import combinations, product
from math import comb, factorial

def index_sets(m):
    full = (1 << m) - 1
    rows, cols = [], []

    # Rows: (A,B), disjoint, |A| >= 3, at least 3 outside A union B.
    for A in range(1 << m):
        if A.bit_count() < 3:
            continue
        rest = full ^ A
        B = rest
        while True:
            if m - A.bit_count() - B.bit_count() >= 3:
                rows.append((A, B))
            if B == 0:
                break
            B = (B - 1) & rest

    # Columns: E is the set of z_3 positions, with |E| <= 2;
    # D is the set of z_4 positions, with |D| <= m-5.
    for e in range(3):
        for positions in combinations(range(m), e):
            E = sum(1 << j for j in positions)
            rest = full ^ E
            D = rest
            while True:
                C = rest ^ D
                if D.bit_count() <= m - 5:
                    cols.append((C, D))
                if D == 0:
                    break
                D = (D - 1) & rest

    return rows, cols

def wedge_data(m):
    assert m >= 7
    rows, cols = index_sets(m)

    P = matrix(
        ZZ, len(rows), len(cols),
        lambda i, j: int(
            (rows[i][0] & ~cols[j][0]) == 0 and
            (rows[i][1] & ~cols[j][1]) == 0
        )
    )

    # Exact integral invariant factors, not modular ranks.
    diagonal = list(P.elementary_divisors())
    rho = sum(d != 0 for d in diagonal)
    torsion_orders = [int(d) for d in diagonal if d > 1]

    R = sum(
        comb(m, a) * sum(comb(m-a, b)
                         for b in range(m-a-2))
        for a in range(3, m-2)
    )
    C = sum(
        comb(m, e) * sum(comb(m-e, d)
                         for d in range(m-4))
        for e in range(3)
    )
    assert R == len(rows)
    assert C == len(cols)

    Q = sum(
        comb(m, a) * comb(m-a, b)
        for a in range(3, m-5)
        for b in range(3, m-a-2)
    )
    a = R - rho - Q
    E_numerator = m**4 + 14*m**3 - m**2 + 34*m + 24
    assert E_numerator % 24 == 0
    E = E_numerator // 24
    b = a + E
    assert a >= 0 and b >= 0

    # Return bottom sphere count, top sphere count, and Moore orders.
    return a, b, torsion_orders

def independently_check(m):
    a, b, torsion = wedge_data(m)
    capacities = [2, 2, 2, m-5]

    # Every face extends to a full-column face:
    # a missing column can be filled because total capacity is m+1.
    facets = [
        tuple(4*j + x for j, x in enumerate(word))
        for word in product(range(4), repeat=m)
        if all(word.count(i) <= capacities[i] for i in range(4))
    ]
    K = SimplicialComplex(facets)
    H = K.homology(algorithm="no_chomp")

    inv_bottom = list(H[m-3].invariants())
    inv_top = list(H[m-2].invariants())

    assert inv_bottom.count(0) == a
    assert inv_top.count(0) == b
    assert sorted(int(x) for x in inv_bottom if x > 1) == torsion
    assert all(x == 0 for x in inv_top)
    assert all(
        len(group.invariants()) == 0
        for dimension, group in H.items()
        if dimension not in (m-3, m-2)
    )

    # Independent face-count Euler characteristic.
    alternating_faces = 0
    for sizes in product(*[range(c+1) for c in capacities]):
        total = sum(sizes)
        if total <= m:
            number = factorial(m) // factorial(m-total)
            for s in sizes:
                number //= factorial(s)
            alternating_faces += (-1)**total * number

    reduced_euler = -alternating_faces
    assert reduced_euler == (-1)**(m-2) * (b-a)

    print(m, "sphere counts:", a, b,
          "Moore orders:", torsion)
    print("Independent integral simplicial homology:", H)

for m in (7, 8):
    independently_check(m)

print("All assertions passed.")
```

I ran these checks. They returned the two homotopy types in (4), and all assertions passed. The checks use the original complexes, not just their presentation matrices.

Thus (1)–(3), proved above for every \(m\ge7\), give the complete requested finite wedge, with explicit arithmetic functions for all dimensions, orders, and multiplicities. Nothing remains unresolved in the stated determination.