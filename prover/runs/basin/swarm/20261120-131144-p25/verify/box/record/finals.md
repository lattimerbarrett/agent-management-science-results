# agent_1: last reply

The infimum is
\[
\boxed{\frac19}.
\]

In fact, the following two statements hold.

* If \(c>1/9\), there is a finite triangle-free graph receiving a homomorphism from every graph in the question.
* If \(c<1/9\), no finite triangle-free graph has that property.

We prove both statements. The proof uses two classical theorems: the degree form of Szemerédi’s regularity lemma and the Borsuk–Ulam theorem. All the applications and the graph constructions are proved below.

## 1. Wide colourings

Call a vertex set \(W\) **wide** if no walk of length three has both endpoints in \(W\). Walks here may repeat vertices. In particular, a wide set is independent: an edge gives a length-three walk by traversing it three times.

A **wide colouring** is a colouring whose colour classes are wide.

### Lemma 1: a bounded wide colouring gives a bounded triangle-free target

For every positive integer \(m\), there is a finite triangle-free graph \(\Omega_m\) such that every graph with a wide \(m\)-colouring maps to \(\Omega_m\).

**Proof.** The vertices of \(\Omega_m\) are pairs
\[
(i,A),\qquad i\in[m],\quad A\subseteq[m]\setminus\{i\}.
\]
Declare \((i,A)\) and \((j,B)\) adjacent precisely when
\[
i\in B,\qquad j\in A,\qquad A\cap B=\varnothing.
\]

This graph is triangle-free. Indeed, in a purported triangle with first coordinates \(i,j,k\), adjacency to the first vertex would put \(i\) into the second and third sets, contradicting the disjointness required between those sets.

Given a wide colouring \(\phi:V(G)\to[m]\), put
\[
A_v=\{\phi(w):w\in N_G(v)\}.
\]
Map \(v\) to \((\phi(v),A_v)\). For an edge \(uv\), the two cross-membership conditions hold. Also \(A_u\cap A_v=\varnothing\): otherwise a neighbour of \(u\) and a neighbour of \(v\) of the same colour would be the endpoints of a length-three walk. Thus this map is a homomorphism. ∎

### Lemma 2: adding a wide set

Suppose \(W\) is wide in \(G\), and \(G-W\) has a wide \(m\)-colouring. Then \(G\) has a wide \((2m+1)\)-colouring.

**Proof.** First observe that \(N_G(W)\) is independent. An edge between two of its vertices would give a length-three walk between vertices of \(W\).

For vertices outside \(W\), refine the given colouring by the bit recording membership in \(N_G(W)\). Give \(W\) one new colour.

Consider a length-three walk with endpoints outside \(W\). If it stays outside \(W\), its endpoints have different original colours. Otherwise, it has exactly one internal vertex in \(W\), since \(W\) is independent. Write it, in the appropriate direction, as
\[
x-w-b-y,\qquad w\in W.
\]
Here \(x,b\in N(W)\), whereas \(y\notin N(W)\), because \(N(W)\) is independent. Thus the new bits distinguish its endpoints. Walks with both endpoints in \(W\) are excluded by the hypothesis. ∎

We will also use this elementary observation:

> A graph containing neither \(C_3\) nor \(C_5\) has no odd closed walk of length at most five.

Indeed, a shortest odd closed subwalk is an odd cycle.

---

## 2. The upper bound: every \(c>1/9\) works

Fix \(c>1/9\). Write
\[
\gamma=c-\frac19,\qquad
\alpha=\frac{\gamma}{100},\qquad
d=\frac{\alpha^2}{100},\qquad
\varepsilon=\frac{d^2}{100}.
\]
These choices satisfy
\[
6(c-\varepsilon-\alpha)+3(c-d-2\varepsilon)>1. \tag{1}
\]

Let \(G\) be an \(n\)-vertex graph with no \(C_3\) or \(C_5\), and with \(\delta(G)\ge cn\).

### 2.1. Regularity and the reduced graph

Use the degree form of the regularity lemma, with parameters \(\varepsilon,d\). It supplies a spanning subgraph \(G'\) and a partition
\[
V(G)=V_0\cup V_1\cup\cdots\cup V_k
\]
such that:

* \(|V_0|\le\varepsilon n\);
* \(|V_1|=\cdots=|V_k|=L\);
* \(k\) is bounded in terms of \(c\);
* each \(V_i\), \(i\ge1\), is independent in \(G'\);
* every pair \((V_i,V_j)\) is either empty in \(G'\), or is \(\varepsilon\)-regular of density greater than \(d\);
* every vertex loses at most \((d+\varepsilon)n\) incident edges.

Let \(R\) be the reduced graph of the nonempty regular pairs. For \(v\in V_i\),
\[
(c-d-\varepsilon)n
 \le d_{G'}(v)
 \le d_R(i)L+|V_0|.
\]
Consequently,
\[
\delta(R)\ge(c-d-2\varepsilon)k. \tag{2}
\]

All uses below require only that \(L\) exceed a constant depending on our parameters. Since \(k\) is bounded, we may assume this by treating the finitely many smaller values of \(n\) separately.

For every \(v\in V(G)\), define its support
\[
A(v)=\{i\in[k]:|N_G(v)\cap V_i|\ge\alpha L\}. \tag{3}
\]

### 2.2. Three consequences of the forbidden cycles

The following properties hold:
\[
\begin{array}{ll}
\text{(a)}& A(v)\text{ is independent in }R;\\[1mm]
\text{(b)}& uv\in E(G)\ \Longrightarrow\
 A(u)\cap A(v)=\varnothing
 \text{ and }
 N_R(A(u))\cap N_R(A(v))=\varnothing;\\[1mm]
\text{(c)}& u-v-w\text{ is a path}\ \Longrightarrow\
 E_R(A(u),A(w))=\varnothing.
\end{array} \tag{4}
\]

Here and below \(N_R(A)\) is the union of the open neighbourhoods of the vertices in \(A\).

We justify all three properties.

* If an edge of \(R\) joined two indices in \(A(v)\), regularity would give an edge between the corresponding two large subsets of \(N_G(v)\), producing a triangle. This proves (a).
* If \(uv\) is an edge and \(i\in A(u)\cap A(v)\), choose a neighbour \(j\) of \(i\) in \(R\), which exists by (2). Regularity gives a length-two path, through \(V_j\), between \(N(u)\cap V_i\) and \(N(v)\cap V_i\). Together with \(uv\) this is a \(C_5\).
* More generally, if \(i\in A(u)\), \(\ell\in A(v)\), and \(i-j-\ell\) is a walk in \(R\), regularity gives a length-two path between those two neighbour sets through \(V_j\). Again, adding \(u,v\) and the edge \(uv\) produces a \(C_5\). This proves the remaining assertion of (b).
* Finally, if \(u-v-w\) is a path and a regular pair joined an index in \(A(u)\) to one in \(A(w)\), it would supply a length-three \(u,w\)-path. Its union with \(u-v-w\) is a \(C_5\), proving (c).

For completeness, the elementary regularity fact used here is that in an \(\varepsilon\)-regular pair of density greater than \(d\), all but \(\varepsilon L\) vertices on one side have at least \((d-\varepsilon)|U|\) neighbours in any fixed subset \(U\) of the other side with \(|U|\ge\varepsilon L\). Thus a middle vertex can be chosen with neighbours in both prescribed endpoint sets. Taking \(L\) sufficiently large also allows avoidance of the finitely many already specified vertices.

### 2.3. Remove boundedly many wide sets

For \(i\in[k]\), put
\[
W_i=\{v:|N_G(v)\cap V_i|>L/2\}.
\]
Each \(W_i\) is wide. If a length-three walk had endpoints \(u,v\in W_i\), their neighbourhoods in \(V_i\) would intersect. Appending the resulting length-two walk would give an odd closed walk of length five.

Let
\[
T=V(G)\setminus\bigcup_{i=1}^k W_i.
\]
For every \(v\in T\), each cluster contains at most \(L/2\) neighbours of \(v\). Hence
\[
cn\le d_G(v)
 \le \varepsilon n+\frac{|A(v)|L}{2}+\alpha kL.
\]
Since \(kL\le n\), this yields
\[
|A(v)|\ge 2(c-\varepsilon-\alpha)k. \tag{5}
\]

### 2.4. A triangle-free quotient of \(G[T]\)

Assign each vertex \(v\) the finite type
\[
\tau(v)=
\left(
 A(v),\
 \{A(w):w\in N_G(v)\}
\right). \tag{6}
\]
There are at most
\[
K=2^{\,k+2^k}
\]
types.

Let \(J\) be the quotient on the types occurring in \(T\): two types are joined if an edge of \(G[T]\) joins vertices of those types. Property (4b), together with the nonemptiness in (5), shows that there are no loops.

We claim that \(J\) is triangle-free.

Suppose three types form a triangle, with supports \(A_1,A_2,A_3\), and write
\[
B_i=N_R(A_i).
\]
By (4b), the \(A_i\) are pairwise disjoint, and the \(B_i\) are pairwise disjoint.

Moreover, every two supports \(A_i,A_j\) are anticomplete in \(R\). To see this, use the third type as the middle type. The neighbour-support information in (6) ensures that some actual vertex of that middle type has neighbours with supports \(A_i\) and \(A_j\). These are distinct vertices, so (4c) applies.

Together with (4a), this proves that the following six sets are mutually disjoint:
\[
A_1,A_2,A_3,B_1,B_2,B_3.
\]
But (2) and (5) give
\[
\begin{aligned}
k
&\ge \sum_{i=1}^3(|A_i|+|B_i|)\\
&\ge \left[
6(c-\varepsilon-\alpha)+3(c-d-2\varepsilon)
\right]k\\
&>k,
\end{aligned}
\]
by (1). This contradiction proves the claim.

The type map is therefore a homomorphism \(G[T]\to J\) to a triangle-free graph of bounded order. Its vertex labels give a wide colouring of \(G[T]\): a length-three walk whose endpoints have the same label would map to a length-three closed walk in a triangle-free graph.

Finally, partition \(\bigcup_iW_i\) into at most \(k\) disjoint wide sets and add them back using Lemma 2. We obtain a wide colouring of all of \(G\), with a number of colours bounded solely in terms of \(c\).

The finitely many small orders excluded earlier also have a uniform bound, by using distinct colours. Lemma 1 now supplies one finite triangle-free target \(H_c\).

Thus every \(c>1/9\) has the required property.

---

## 3. The lower bound: no \(c<1/9\) works

Fix \(0\le c<1/9\), and let \(H\) be any finite triangle-free graph. We construct a counterexample for this particular \(H\).

We may assume \(h=|V(H)|\ge1\), since an empty target plainly cannot work.

### 3.1. Finite near-antipodal graphs

We need a classical consequence of Borsuk–Ulam.

**Antipodal covering fact.** The sphere \(S^d\) cannot be covered by \(d+1\) closed sets, none containing an antipodal pair.

Here is the deduction. If \(C_0,\ldots,C_d\) were such a cover, define
\[
f_i(x)=\operatorname{dist}(x,C_i)-\operatorname{dist}(-x,C_i).
\]
Empty sets can be discarded, and nonempty sets repeated if necessary. The vector \(f(x)\) has a negative and a positive coordinate. Its projection onto the \(d\)-dimensional hyperplane with coordinate sum zero is therefore nonzero. Normalizing produces a continuous odd map \(S^d\to S^{d-1}\), contrary to Borsuk–Ulam.

Fix \(d=h^3\). For a sufficiently small \(\eta>0\), take a finite \(\eta/4\)-net \(X\subset S^d\), and form the graph \(B\) on \(X\) by
\[
xy\in E(B)\quad\Longleftrightarrow\quad \|x+y\|<\eta. \tag{7}
\]

Then
\[
\chi(B)\ge d+2>h^3. \tag{8}
\]
Indeed, a colouring with at most \(d+1\) colours, with each colour class thickened by closed balls of radius \(\eta/4\), would give the forbidden antipodal cover. Two net points whose balls contain antipodal points have sum of norm at most \(\eta/2\), so they cannot have the same colour.

Choose \(\eta<2/5\). Then \(B\) has no \(C_3\) or \(C_5\). More generally, an odd closed walk of length \(\ell\) in (7) would, by alternating the successive sums, imply
\[
2<\ell\eta,
\]
which is impossible for \(\ell=3,5\).

For a direction \(z\in S^d\), consider the cap
\[
I_z=\{x\in X:\langle x,z\rangle>2\eta\}. \tag{9}
\]
Each cap is wide in \(B\). A length-three walk from \(x\) to \(y\) gives
\[
\|x+y\|<3\eta,
\]
whereas two points of (9) satisfy
\[
\|x+y\|\ge \langle x+y,z\rangle>4\eta.
\]

For a uniformly random \(z\), each fixed point belongs to \(I_z\) with the same probability \(p\). For fixed dimension \(d\),
\[
p\longrightarrow\frac12\qquad\text{as }\eta\longrightarrow0. \tag{10}
\]

### 3.2. A three-colourable graph with no homomorphism to \(H\)

Let
\[
F=B\times K_3
\]
be the categorical product:
\[
(x,i)(y,j)\in E(F)
\quad\Longleftrightarrow\quad
xy\in E(B),\ i\ne j.
\]
It has three independent parts
\[
F_i=X\times\{i\}.
\]
The projection to \(B\) shows that \(F\) contains no \(C_3\) or \(C_5\).

We claim
\[
F\nrightarrow H. \tag{11}
\]

Suppose otherwise. For each \(x\in V(B)\), record the function
\[
f_x:[3]\to V(H),\qquad f_x(i)=f(x,i).
\]
For an edge \(xy\) of \(B\), we have
\[
f_x(i)f_y(j)\in E(H)\qquad(i\ne j).
\]
In particular, \(f_x\ne f_y\): equality would make that function a homomorphism \(K_3\to H\), impossible. Thus the \(h^3\) possible functions properly colour \(B\), contradicting (8). This proves (11).

The inverse images of the caps \(I_z\) are wide in \(F\).

### 3.3. Dense padding

Choose \(p'<1/2\) such that
\[
\frac{p'}{3(1+p')}>c. \tag{12}
\]
This is possible exactly because \(c<1/9\).

Choose \(\eta\) small enough that the cap probability \(p\) in (10) exceeds \(p'\). For all sufficiently large \(m\), there are directions
\[
z_1,\ldots,z_m
\]
such that every \(x\in X\) belongs to at least \(p'm\) of their caps.

One way to see this is to choose the directions independently. Hoeffding’s inequality and a union bound give failure probability at most
\[
|X|\exp\bigl(-2(p-p')^2m\bigr)<1
\]
for sufficiently large \(m\).

Put \(q=\lfloor p'm\rfloor\). Add, for each \(i\in[3]\),

* an independent set \(P_i=\{p_{i,1},\ldots,p_{i,m}\}\);
* an independent set \(Q_i\) of size \(q\);
* all edges between \(P_i\) and \(Q_i\);
* the edge \((x,i)p_{i,j}\) exactly when \(x\in I_{z_j}\).

Retain every edge of \(F\), and add no other edges. Call the resulting graph \(G\).

#### There are no triangles or \(5\)-cycles

Triangles are excluded by the independence of \(F_i,P_i,Q_i\), together with triangle-freeness of \(F\).

For a \(5\)-cycle containing a vertex of \(Q_i\), its two neighbours belong to \(P_i\). The remaining length-three path between these two vertices would have its two internal vertices in \(Q_i\cup F_i\), an independent set. This is impossible.

Consider a \(5\)-cycle containing no vertex of any \(Q_i\).

* With no \(P\)-vertex, it would lie in \(F\).
* With exactly one \(P\)-vertex, its remaining length-three path would join two vertices in one cap, contradicting the cap’s wideness in \(F\).
* With two \(P\)-vertices, their common neighbour on the cycle forces them to belong to the same \(P_i\). The other two \(F\)-vertices would then both belong to \(F_i\), but would have to be adjacent.

These exhaust the possibilities.

#### The minimum degree approaches \(n/9\)

Every original vertex has at least \(p'm\) neighbours in its corresponding \(P_i\). Vertices of \(P_i\) have at least \(q\) neighbours, and vertices of \(Q_i\) have \(m\) neighbours. Thus
\[
\delta(G)\ge q,
\qquad
|V(G)|=|V(F)|+3m+3q.
\]
Consequently,
\[
\frac{\delta(G)}{|V(G)|}
\ge
\frac{\lfloor p'm\rfloor}
 {|V(F)|+3m+3\lfloor p'm\rfloor}
\longrightarrow
\frac{p'}{3(1+p')}>c.
\]
For sufficiently large \(m\), therefore, \(\delta(G)\ge c|V(G)|\).

Finally, \(G\nrightarrow H\), because its subgraph \(F\) does not map to \(H\).

This proves the lower bound for every \(c<1/9\).

---

## 4. Executable checks

The following Python performs actual finite checks, rather than printing the claimed threshold. It:

1. independently checks the \(C_3,C_5\) detector by enumerating cycles;
2. exhaustively checks the wide-colouring target construction on all triangle-free graphs of order at most five;
3. exhaustively checks the wide-set extension lemma on those graphs;
4. constructs a geometric padded example and checks its minimum degree, absence of \(C_3,C_5\), cap wideness, and failure to map to \(K_2\);
5. checks the upper-bound parameter inequality using exact rational arithmetic.

Floating-point geometry is used only to generate a candidate graph. The subsequent graph checks use exact integer bitsets.

```python
import math
import itertools
import numpy as np
from fractions import Fraction

def graph(n, edges):
    a = [0] * n
    for u, v in edges:
        assert u != v
        a[u] |= 1 << v
        a[v] |= 1 << u
    return a

def bits(x):
    while x:
        b = x & -x
        yield b.bit_length() - 1
        x -= b

def edges(a):
    for u, x in enumerate(a):
        for v in bits(x & ~((1 << (u + 1)) - 1)):
            yield u, v

def odd3(a):
    """Adjacency bitsets for existence of a length-three walk."""
    out = []
    for u in range(len(a)):
        z = 0
        for v in bits(a[u]):
            for w in bits(a[v]):
                z |= a[w]
        out.append(z)
    return out

def no35(a):
    # An odd closed walk of length five exists iff C3 or C5 exists.
    two = []
    for x in a:
        z = 0
        for v in bits(x):
            z |= a[v]
        two.append(z)
    return all(not (two[u] & two[v]) for u, v in edges(a))

def trianglefree(a):
    return all(not (a[u] & a[v]) for u, v in edges(a))

def bipartite(a):
    col = {}
    for s in range(len(a)):
        if s in col:
            continue
        col[s] = 0
        stack = [s]
        while stack:
            u = stack.pop()
            for v in bits(a[u]):
                if v not in col:
                    col[v] = 1 - col[u]
                    stack.append(v)
                elif col[v] == col[u]:
                    return False
    return True

def wide(q, col):
    return all(
        col[u] != col[v]
        for u, x in enumerate(q) for v in bits(x)
    )

def omega(m):
    vs = [
        (i, A)
        for i in range(m)
        for A in range(1 << m)
        if not ((A >> i) & 1)
    ]
    es = []
    for p, (i, A) in enumerate(vs):
        for r in range(p):
            j, B = vs[r]
            if ((B >> i) & 1) and ((A >> j) & 1) and not (A & B):
                es.append((p, r))
    return vs, graph(len(vs), es)

def partitions(n):
    """All set partitions, represented as canonical colour lists."""
    def rec(a):
        if len(a) == n:
            yield a
            return
        for c in range(max(a, default=-1) + 2):
            yield from rec(a + [c])
    yield from rec([])

checked = 0

for n in range(1, 6):
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        a = graph(n, [
            e for j, e in enumerate(pairs) if (mask >> j) & 1
        ])

        # Independent brute-force verification of the C3,C5 detector.
        brute_no35 = True
        for length in (3, 5):
            if length > n:
                continue
            for cyc in itertools.permutations(range(n), length):
                if all(
                    (a[cyc[j]] >> cyc[(j + 1) % length]) & 1
                    for j in range(length)
                ):
                    brute_no35 = False
                    break
            if not brute_no35:
                break
        assert no35(a) == brute_no35

        if not trianglefree(a):
            continue
        q3 = odd3(a)

        # Verify Lemma 1 for every wide colouring.
        for col in partitions(n):
            if not wide(q3, col):
                continue
            m = max(col) + 1
            vs, om = omega(m)
            lookup = {v: j for j, v in enumerate(vs)}
            f = []
            for u in range(n):
                A = 0
                for v in bits(a[u]):
                    A |= 1 << col[v]
                f.append(lookup[(col[u], A)])
            assert all(
                (om[f[u]] >> f[v]) & 1 for u, v in edges(a)
            )
            checked += 1

        # Verify Lemma 2 for every wide set and every wide
        # colouring of its complement.
        for W in range(1 << n):
            if any(q3[u] & W for u in bits(W)):
                continue
            T = [v for v in range(n) if not ((W >> v) & 1)]
            ind = graph(len(T), [
                (i, j)
                for i in range(len(T)) for j in range(i)
                if (a[T[i]] >> T[j]) & 1
            ])
            qi = odd3(ind)
            NW = 0
            for v in bits(W):
                NW |= a[v]
            for co in partitions(len(T)):
                if not wide(qi, co):
                    continue
                col = [(-1, False)] * n
                for i, v in enumerate(T):
                    col[v] = (co[i], bool((NW >> v) & 1))
                assert wide(q3, col)

for m in range(1, 6):
    _, om = omega(m)
    assert trianglefree(om)

print("Exhaustively checked wide-colouring maps:", checked)
print("Extension lemma checked on every triangle-free graph",
      "with <=5 vertices.")

# Geometric example: near-antipodal C101 on the circle.
L, m = 101, 601
X = np.array([
    (math.cos(2 * math.pi * j / L),
     math.sin(2 * math.pi * j / L))
    for j in range(L)
])
step = (L - 1) // 2
B = graph(L, [(j, (j + step) % L) for j in range(L)])
eta = max(
    np.linalg.norm(X[u] + X[v]) for u, v in edges(B)
) * 1.00001
assert 5 * eta < 2

Z = np.array([
    (math.cos(2 * math.pi * j / m),
     math.sin(2 * math.pi * j / m))
    for j in range(m)
])
inc = X @ Z.T > 2 * eta
q = int(inc.sum(axis=1).min())

nf = 3 * L
N = nf + 3 * m + 3 * q
es = []

# F = B x K3.
for u, v in edges(B):
    for i in range(3):
        for j in range(3):
            if i != j:
                es.append((3 * u + i, 3 * v + j))

# Padding.
for i in range(3):
    P = nf + i * m
    Q = nf + 3 * m + i * q
    for j in range(m):
        for k in range(q):
            es.append((P + j, Q + k))
    for b in range(L):
        for j in np.flatnonzero(inc[b]):
            es.append((3 * b + i, P + int(j)))

G = graph(N, es)
assert no35(G)
assert not bipartite(G)       # Thus G does not map to K2.
delta = min(x.bit_count() for x in G)
assert delta >= q

# Check all cap sets directly, with exact graph operations.
qb = odd3(B)
for j in range(m):
    I = sum(1 << b for b in range(L) if inc[b, j])
    assert all(not (qb[b] & I) for b in bits(I))

print("Geometric example:", N, "vertices,",
      sum(x.bit_count() for x in G) // 2, "edges")
print("Minimum degree:", delta,
      "ratio:", float(Fraction(delta, N)))
print("Verified: no C3 or C5; not homomorphic to K2;",
      "every cap is wide.")

# With gamma=c-1/9 in (0,1), the surplus in (1), divided by
# gamma, is 9-6/100-3*gamma/10**6-12*gamma**3/10**14.
assert (
    9 - Fraction(6, 100)
      - Fraction(3, 10**6)
      - Fraction(12, 10**14)
) > 0
print("Exact coefficient bound verifies the error margin",
      "for every c>1/9.")
```

The executed output was:
```text
Exhaustively checked wide-colouring maps: 6108
Extension lemma checked on every triangle-free graph with <=5 vertices.
Geometric example: 2970 vertices, 607311 edges
Minimum degree: 292 ratio: 0.09831649831649832
Verified: no C3 or C5; not homomorphic to K2; every cap is wide.
Exact coefficient bound verifies the error margin for every c>1/9.
```

We have proved both required halves, so the requested infimum is exactly \(\boxed{1/9}\). Nothing remains to prove for the infimum question.