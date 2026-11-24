# agent_1: last reply

Here is an explicit integer-arithmetic answer. The formulas are larger than polynomial multiplicity formulas, but have the advantage that they require no auxiliary topological invariants, recurrences, or unspecified matrix ranks. They use only finite sums, products, and gcds, with all indexing sets specified in terms of \(m\).

Put
\[
p=\sum_{a=0}^{4}2^a\binom ma,\qquad
q=3\left(\binom m4+(m-2)\binom m3\right),\qquad h=\min(p,q).
\]

## 1. Explicit functions specifying the answer

The following \(q p\) integers \(b_{uv}\), all in \(\{0,1,-1\}\), specify the arithmetic functions in the answer.

Index the columns by
\[
(S,\alpha),\qquad S\subseteq[m],\quad |S|\leq4,\quad
\alpha:S\longrightarrow\{1,2\}.
\]
Order them first by \(|S|\), then lexicographically.

For a four-element set \(A\) and a function \(c:A\to\{1,2,3\}\), define
\[
L_{S,\alpha}(A,c)=
\begin{cases}
(-1)^{|\{j\in S:c(j)=3\}|},
&
\begin{array}{l}
S\subseteq A,\quad c(j)=3\quad(j\in A\setminus S),\\[-2pt]
c(j)\in\{\alpha(j),3\}\quad(j\in S);
\end{array}\\[4pt]
0,&\text{otherwise}.
\end{cases}                                                    \tag{1}
\]

For each \(i=1,2,3\), include the following rows, in the indicated order.

* For every \(A\in\binom{[m]}4\), a row with entry
  \[
  L_{S,\alpha}(A,i^A).
  \]
* For every \(T\in\binom{[m]}3\), let \(j_T=\min([m]\setminus T)\). Include a row with entry
  \[
  \sum_{a=1}^3
  L_{S,\alpha}\bigl(T\cup\{j_T\},\,i^T\cup\{j_T\mapsto a\}\bigr).
  \]
* Put \(a_i=\min(\{1,2,3\}\setminus\{i\})\). For every
  \(T\in\binom{[m]}3\) and \(j\notin T\), include a row with entry
  \[
  L_{S,\alpha}\bigl(T\cup\{j\},\,i^T\cup\{j\mapsto a_i\}\bigr).
  \]

Use lexicographic order within each family. These are the integers \(b_{uv}\), \(1\leq u\leq q\), \(1\leq v\leq p\).

Define \(\Delta_0=1\). For \(1\leq a\leq h\), define the following explicit nonnegative integer:
\[
\Delta_a=
\gcd_{\substack{1\leq u_1<\cdots<u_a\leq q\\
                 1\leq v_1<\cdots<v_a\leq p}}
\left|
 \sum_{\pi\in\mathfrak S_a}\operatorname{sgn}(\pi)
       \prod_{\ell=1}^a b_{u_\ell,v_{\pi(\ell)}}
\right|.                                                       \tag{2}
\]
The gcd of a family consisting entirely of zeros is zero.

Finally, put
\[
\epsilon(x)=
\begin{cases}0&x=0,\\1&x>0,\end{cases}
\qquad
r=\sum_{a=1}^h\epsilon(\Delta_a),\qquad
d_a=\frac{\Delta_a}{\Delta_{a-1}}\quad(1\leq a\leq r).           \tag{3}
\]
The quotients in (3) are always positive integers.

With these explicit functions of \(m\), the answer is
\[
\boxed{\displaystyle
 |K_m|\simeq
 \bigvee^{\,q-r} S^{m-3}\ \vee\
 \bigvee^{\,p-r} S^{m-2}\ \vee\
 \bigvee_{\substack{1\leq a\leq r\\d_a>1}}
       M(\mathbb Z/d_a\mathbb Z,m-3).
}                                                               \tag{4}
\]
Repeated values among the \(d_a\)'s mean repeated Moore-space summands. Thus (1)–(3) specify every multiplicity and every cyclic order by bounded integer-arithmetic formulas. In particular, (4) does **not** mean “take the homology of another complex” or “find an unspecified Smith normal form.”

For illustration, exact evaluation gives
\[
\begin{aligned}
|K_7|&\simeq \bigvee^{309}S^5\ \vee M(\mathbb Z/2,4),\\
|K_8|&\simeq \bigvee^{14}S^5\ \vee\bigvee^{493}S^6\
                 \vee M(\mathbb Z/2,5),\\
|K_9|&\simeq \bigvee^{42}S^6\ \vee\bigvee^{751}S^7\
                 \vee M(\mathbb Z/2,6).
\end{aligned}                                                   \tag{5}
\]

Hereafter, I prove the formula for every \(m\geq7\), and give executable Python that evaluates it and independently checks the original simplicial chain complex.

---

## 2. A small chain model

Write \(k=m-5\). Use commuting symbols \(u_{ij}\), where \(i=1,2,3\), and anticommuting symbols \(v_j\), where \(j\in[m]\). Products containing two symbols with the same column index are zero.

The *weight* of a monomial is its total number of symbols; its chain degree is its number of \(u\)'s. Define
\[
d(u_{ij})=v_j,\qquad d(v_j)=0,
\]
with signs obtained by anticommuting the \(v\)'s. Thus \(d^2=0\). Put \(e=\sum_jv_j\).

Let \(D^a\) be the weight-\(a\) complex, and put
\[
C^a=D^a/eD^{a-1}.
\]
A subscript “cap” means that monomials with more than two \(u\)'s of any one of the three colors are omitted. The differential preserves this subcomplex.

We will use
\[
\widetilde H_{m-6+s}(K_m;\mathbb Z)
       \cong H_s(C^4_{\mathrm{cap}}).                           \tag{6}
\]

### Proof of (6)

Fix a face \(\sigma\) using only rows \(1,2,3\), and let \(s=|\sigma|\). The available row-four vertices form the \((k-1)\)-skeleton of a simplex on \(m-s\) vertices.

Its augmented homology is zero if \(s\geq5\), because then the whole simplex is available. If \(s\leq4\), its only augmented homology is in degree \(k-1\), and is
\[
\Lambda^k W,\qquad
W=\ker\bigl(\mathbb Z^{[m]\setminus\operatorname{col}(\sigma)}
                    \xrightarrow{\ \sum\ }\mathbb Z\bigr).
\]
The determinant pairing identifies this group with
\[
\Lambda^{4-s}
\left(
 \mathbb Z^{[m]\setminus\operatorname{col}(\sigma)}
 \big/\mathbb Z\sum_{j\notin\operatorname{col}(\sigma)}v_j
\right).                                                       \tag{7}
\]
Under this identification, deleting a colored vertex in column \(j\) becomes exterior multiplication by \(v_j\), with the usual orientation sign.

Filter the augmented simplicial chain complex by the number of vertices in rows \(1,2,3\). Taking row-four homology first leaves just the groups (7). They form exactly \(C^4_{\mathrm{cap}}\). There is only one nonzero row in this spectral sequence, so it collapses, with no extension ambiguity. The degree shift is \(k-1=m-6\). This proves (6). ∎

---

## 3. The unrestricted complex has an explicit integral basis

For \(0\leq a\leq4\), the unrestricted complex \(D^a\) splits over the \(a\)-element column sets. For a fixed column set it is the tensor product of \(a\) copies of
\[
\mathbb Z\{u_1,u_2,u_3\}\longrightarrow\mathbb Z\{v\},
\qquad u_i\longmapsto v.
\]
Consequently
\[
H_s(D^a)=0\quad(s\ne a),\qquad
H_a(D^a)\cong\mathbb Z^{\,2^a\binom ma}.                         \tag{8}
\]

Exterior multiplication by \(e\) gives exact sequences
\[
0\longrightarrow C^{a-1}
 \xrightarrow{\ e\ }D^a\longrightarrow C^a\longrightarrow0,     \tag{9}
\]
with harmless degree signs on the first map.

For completeness, exactness can be checked separately for each fixed colored monomial. On the remaining columns, multiplication by \(e\) is the exterior Koszul complex of a primitive vector. It is exact. There is at least one remaining column, since \(a\leq4<m\).

It follows inductively from (8)–(9) that
\[
H_s(C^4)=0\quad(s\ne4),\qquad H_4(C^4)\cong\mathbb Z^p.         \tag{10}
\]

Here is an integral basis, not just a rank calculation. Set
\[
x_{ij}=u_{ij}-u_{3j}\quad(i=1,2),\qquad w_j=u_{3j}.
\]
For \(S,\alpha\) as in Section 1, let
\[
z_{S,\alpha}=
 \left(\prod_{j\in S}x_{\alpha(j),j}\right)
 \left(
 \sum_{\substack{B\subseteq[m]\setminus S\\|B|=4-|S|}}
       \prod_{j\in B}w_j
 \right).                                                       \tag{11}
\]
These are cycles modulo \(e\): differentiating the second factor gives \(e\) times the analogous expression of weight one less.

They form an integral basis of \(H_4(C^4)\). Indeed, the terms with \(|S|=4\) give the tensor-product basis in (8). In (9), the connecting map takes the remaining terms in (11), up to signs, to the analogous basis of \(H_3(C^3)\). Induction proves both generation and integral independence.

Notice that the coefficient of a colored monomial \((A,c)\) in (11) is exactly (1).

---

## 4. The effect of the three capacity restrictions

Consider the quotient complex
\[
Q=C^4/C^4_{\mathrm{cap}}.
\]
A forbidden monomial has at least three vertices of one color. Since its total weight is four, it cannot violate two colors. Thus
\[
Q=Q_1\oplus Q_2\oplus Q_3,
\]
and \(Q\) has chain groups only in degrees three and four.

For a fixed color \(i\), the degree-four coordinates are:

* \(A_A\), for four vertices all colored \(i\);
* \(E_{T,j,a}\), for three vertices \(T\) colored \(i\) and a fourth vertex \(j\notin T\) colored \(a\ne i\).

The degree-three summand belonging to a triple \(T\) is
\[
\mathbb Z^{[m]\setminus T}/\mathbb Z\sum_{j\notin T}v_j.
\]
The boundary map \(Q_4\to Q_3\) is surjective: for each \(T,j\), a monomial with triple \(T\) of color \(i\) and the vertex \(j\) of another color maps to \(v_j\).

A degree-four element is a cycle precisely when, for every \(T\),
\[
 A_{T\cup\{j\}}+\sum_{a\ne i}E_{T,j,a}
\]
is independent of \(j\notin T\). Denote this common integer by \(B_T\).

It follows that the following are free integral coordinates on \(H_4(Q_i)\):
\[
\begin{array}{ll}
A_A,&A\in\binom{[m]}4,\\
B_T,&T\in\binom{[m]}3,\\
E_{T,j,a_i},&T\in\binom{[m]}3,\ j\notin T.
\end{array}                                                     \tag{12}
\]
The other \(E\)-coordinate is recovered integrally as
\[
E_{T,j,a}=B_T-A_{T\cup\{j\}}-E_{T,j,a_i}.
\]
Therefore
\[
H_s(Q)=0\quad(s\ne4),\qquad H_4(Q)\cong\mathbb Z^q.             \tag{13}
\]

Now express the images of the basis cycles (11) in coordinates (12). Their \(A\)-coordinates, \(B\)-coordinates, and \(E\)-coordinates are exactly the three families of entries specified in Section 1. Thus the homomorphism
\[
H_4(C^4)\longrightarrow H_4(Q)
\]
is represented by the explicit integer array \((b_{uv})\).

The long exact homology sequence, together with (10) and (13), consequently gives
\[
\begin{aligned}
H_4(C^4_{\mathrm{cap}})&\cong\ker(b:\mathbb Z^p\to\mathbb Z^q),\\
H_3(C^4_{\mathrm{cap}})&\cong\operatorname{coker}
                                    (b:\mathbb Z^p\to\mathbb Z^q),\\
H_s(C^4_{\mathrm{cap}})&=0\qquad(s\ne3,4).
\end{aligned}                                                   \tag{14}
\]

The integral determinantal-divisor theorem says exactly that the explicitly defined integers (2)–(3) satisfy
\[
\begin{aligned}
\ker b&\cong\mathbb Z^{p-r},\\
\operatorname{coker}b
 &\cong\mathbb Z^{q-r}\oplus
       \bigoplus_{\substack{1\leq a\leq r\\d_a>1}}\mathbb Z/d_a.
\end{aligned}                                                   \tag{15}
\]
This also proves the integrality assertions following (3).

Combining (6), (14), and (15) establishes all the claimed homology groups.

---

## 5. Why these homology groups determine the homotopy type here

Two further points are needed: a dimension bound and simple connectivity.

### Dimension bound

Project the face poset onto its row-\(1,2,3\) part \(\sigma\). In the fiber over \(\sigma\), let \(j\) be the smallest unused column. Match a row-four face not containing \(j\) with the face obtained by adding \((4,j)\), whenever allowed.

This matching is acyclic in each fiber, and hence acyclic on the whole face poset. Apart from the basepoint, its unmatched faces have:

* \(s\leq4\) colored vertices;
* exactly \(k=m-5\) row-four vertices.

Their dimensions are
\[
s+k-1\leq m-2.
\]
If \(s\geq5\), the row-four fiber is a full nonempty simplex and has no unmatched face. Discrete Morse theory therefore gives a CW model for \(K_m\) of dimension at most \(m-2\).

### Simple connectivity

Let \(J\) be the join of the \(m\) four-point column sets. It is simply connected. The complexes \(K_m\) and \(J\) have the same one-skeleton.

A triangle of \(J\) missing from \(K_m\) consists of three vertices in a row whose capacity is two. Its boundary bounds a disk in \(K_m\): cone that boundary to a vertex in a different row and a column outside the triangle. All three cone triangles belong to \(K_m\).

Thus adding the missing triangles does not change the fundamental group, and
\[
\pi_1(K_m)=\pi_1(J)=0.
\]

By (14), reduced homology vanishes below dimension \(n=m-3\). The Hurewicz theorem, applied inductively, now shows that \(K_m\) is \((n-1)\)-connected. Its CW dimension is at most \(n+1\).

Finally, an \((n-1)\)-connected CW complex of dimension at most \(n+1\), for \(n\geq2\), is a wedge of \(n\)-spheres, \((n+1)\)-spheres, and Moore spaces \(M(\mathbb Z/t,n)\). One way to see this is to use cellular cancellation to obtain cells only in dimensions \(0,n,n+1\). The attaching maps are then classified by an integer matrix, and integral changes of cellular bases put that matrix in Smith form.

Applying this observation to (15) proves precisely (4).

---

## 6. Executable Python and independent checks

The following is Python using Sage’s exact integer and finite-field arithmetic. It does three things:

1. constructs the array specified in Section 1;
2. evaluates the answer exactly;
3. independently enumerates the original faces of \(K_7\), constructs all its augmented simplicial boundary matrices, checks \(d^2=0\), and compares its homology over \(\mathbb F_2,\mathbb F_3\) with the formula.

The Smith calculation is merely an efficient way to evaluate the gcd formulas (2); the proof above does not depend on experimental Smith calculations.

```python
from sage.all import ZZ, GF, matrix
from itertools import combinations, product

def answer_matrix(m):
    assert m >= 7
    cols = [
        (S, cs)
        for s in range(5)
        for S in combinations(range(m), s)
        for cs in product((0, 1), repeat=s)
    ]
    As = list(combinations(range(m), 4))
    Ts = list(combinations(range(m), 3))

    rows = []
    for i in range(3):
        rows += [(i, 'A', A) for A in As]
        rows += [(i, 'B', T) for T in Ts]
        rows += [
            (i, 'E', T, j)
            for T in Ts for j in range(m) if j not in T
        ]

    row_index = {r: k for k, r in enumerate(rows)}
    M = matrix(ZZ, len(rows), len(cols), sparse=True)

    # Expand the explicit cycles (11).
    for col, (S, cs) in enumerate(cols):
        available = [j for j in range(m) if j not in S]
        for extra in combinations(available, 4-len(S)):
            A = tuple(sorted(S + extra))
            for mask in product((0, 1), repeat=len(S)):
                color = {j: 2 for j in A}
                coefficient = 1
                for j, a, bit in zip(S, cs, mask):
                    color[j] = a if bit == 0 else 2
                    if bit:
                        coefficient = -coefficient

                for i in range(3):
                    T = tuple(j for j in A if color[j] == i)

                    if len(T) == 4:
                        M[row_index[i, 'A', A], col] += coefficient

                    if len(T) == 3:
                        j = next(j for j in A if j not in T)
                        other = next(a for a in range(3) if a != i)
                        if color[j] == other:
                            M[row_index[i, 'E', T, j], col] += coefficient

                    for T in combinations(A, 3):
                        j = next(j for j in A if j not in T)
                        first_outside = next(
                            x for x in range(m) if x not in T
                        )
                        if (j == first_outside
                                and all(color[t] == i for t in T)):
                            M[row_index[i, 'B', T], col] += coefficient
    return M

def homotopy_data(m):
    M = answer_matrix(m)
    diagonal = M.elementary_divisors()
    rank = sum(d != 0 for d in diagonal)
    torsion = [int(d) for d in diagonal if d > 1]
    return {
        "sphere_dimension_1": m-3,
        "sphere_multiplicity_1": M.nrows()-rank,
        "sphere_dimension_2": m-2,
        "sphere_multiplicity_2": M.ncols()-rank,
        "Moore_dimension": m-3,
        "Moore_orders": torsion,
    }

def check_original_complex(m, primes=(2, 3)):
    caps = (2, 2, 2, m-5)
    faces = [[] for _ in range(m+1)]

    # 0 means unused column; 1,2,3,4 specify the occupied row.
    for assignment in product(range(5), repeat=m):
        if all(assignment.count(i+1) <= caps[i] for i in range(4)):
            F = tuple(
                4*j + assignment[j]-1
                for j in range(m) if assignment[j] != 0
            )
            faces[len(F)].append(F)

    indices = [
        {F: i for i, F in enumerate(level)}
        for level in faces
    ]
    ranks = {p: [0]*(m+2) for p in primes}
    previous = {p: None for p in primes}

    for s in range(1, m+1):
        entries = {}
        for col, F in enumerate(faces[s]):
            for j in range(s):
                G = F[:j] + F[j+1:]
                entries[indices[s-1][G], col] = (-1)**j

        for p in primes:
            B = matrix(
                GF(p), len(faces[s-1]), len(faces[s]),
                entries, sparse=True
            )
            if previous[p] is not None:
                assert (previous[p] * B).is_zero()
            previous[p] = B
            ranks[p][s] = B.rank()

    M = answer_matrix(m)
    for p in primes:
        rank = M.change_ring(GF(p)).rank()
        expected = [0]*(m+1)
        # Index s denotes homological dimension s-1.
        expected[m-2] = M.nrows()-rank
        expected[m-1] = M.ncols()-rank

        actual = [
            len(faces[s])-ranks[p][s]-ranks[p][s+1]
            for s in range(m+1)
        ]
        assert actual == expected, (m, p, actual, expected)

    return list(map(len, faces))

for m in (7, 8, 9):
    print(m, homotopy_data(m))

print("Original K_7 face counts:", check_original_complex(7))
```

I ran these exact computations. The integral calculations gave
\[
\begin{array}{c|c|c}
m&(q,p)&\text{nonzero diagonal entries}\\ \hline
7&(630,939)&1^{629},2\\
8&(1218,1697)&1^{1203},2\\
9&(2142,2851)&1^{2099},2.
\end{array}
\]
The independent enumeration of \(K_7\) gave augmented face counts
\[
1,\ 28,\ 336,\ 2100,\ 7140,\ 12600,\ 10080,\ 2520.
\]
Its reduced Betti numbers were \(1,310\) in dimensions \(4,5\) over \(\mathbb F_2\), and \(0,309\) in those dimensions over \(\mathbb F_3\), with all others zero, agreeing with (5).

**What has been proved:** formula (4), with the completely specified arithmetic functions (1)–(3), gives the homotopy type for every integer \(m\geq7\). Every sphere dimension, Moore-space dimension, cyclic order, and multiplicity is specified. Nothing remains conditional on a homology calculation or on a conjectural stabilization pattern.