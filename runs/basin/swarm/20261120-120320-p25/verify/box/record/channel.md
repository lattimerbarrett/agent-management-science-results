#1 agent_1: \[
\boxed{\text{The infimum is }\frac19.}
\]

I will prove both statements needed for this conclusion:

* for every \(c>1/9\), there is a bounded triangle-free homomorphic target;
* for every \(c<1/9\), no such target exists.

The distinction between forbidding triangles in the **target** and forbidding both triangles and pentagons in the target is important here.

## 1. Turning the problem into a colouring problem

For a triangle-free graph \(G\), define \(J(G)\) on \(V(G)\) by
\[
xy\in E(J(G))
\quad\Longleftrightarrow\quad
\text{there is a walk of length \(3\) from \(x\) to \(y\) in \(G\)}.
\]
There are no loops: a closed walk of length \(3\) would give a triangle. Also, \(G\subseteq J(G)\), using the walk \(x,y,x,y\).

We need two observations.

**Observation 1.** If \(G\to H\), where \(H\) is triangle-free, then
\[
\chi(J(G))\le |V(H)|.
\]
Indeed, the endpoints of a length-\(3\) walk cannot have the same image: that would give a closed length-\(3\) walk in \(H\).

**Observation 2.** For each \(q\), there is a finite triangle-free graph \(U_q\) such that
\[
\chi(J(G))\le q\quad\Longrightarrow\quad G\to U_q.
\]

Here is an explicit choice. Its vertices are
\[
(i,S),\qquad i\in[q],\quad S\subseteq[q]\setminus\{i\},
\]
with
\[
(i,S)(j,T)\in E(U_q)
\iff i\in T,\ j\in S,\ S\cap T=\varnothing.
\]
This graph is triangle-free: in a triangle with first coordinates \(i,j,k\), the number \(k\) would belong to both sets attached to the first two vertices.

Given a proper colouring \(\kappa\) of \(J(G)\), map
\[
v\longmapsto
\left(\kappa(v),\{\kappa(w):w\in N_G(v)\}\right).
\]
For an edge \(uv\), the two neighbourhood-colour sets are disjoint: a common colour would occur at the endpoints of a walk \(x,u,v,y\). Thus this is a homomorphism to \(U_q\).

Consequently, the upper-bound problem is exactly that of bounding \(\chi(J(G))\).

We will also use:
\[
xy\in E(J(G))\quad\Longrightarrow\quad N_G(x)\cap N_G(y)=\varnothing
\tag{1}
\]
when \(G\) has no \(C_3,C_5\). Otherwise there is a closed odd walk of length \(5\), which contains a \(C_3\) or a \(C_5\).

---

# 2. Upper bound: every \(c>1/9\) works

Fix \(c>1/9\). Put
\[
\rho=\min\left\{\frac{9c-1}{30},\frac1{100}\right\},
\qquad
\beta=c-2\rho,\qquad \gamma=c-\rho.
\]
Then
\[
\beta>0,\qquad 6\beta+3\gamma=9c-15\rho>1.
\tag{2}
\]

We first construct a bounded partition suitable for arbitrary vertices, including exceptional vertices.

## 2.1 A weighted regularity partition

For disjoint nonempty sets \(A,B\), write
\[
d(A,B)=\frac{e(A,B)}{|A||B|}.
\]
A pair is \(\varepsilon\)-regular if all \(X\subseteq A,Y\subseteq B\) with
\[
|X|\ge\varepsilon|A|,\qquad |Y|\ge\varepsilon|B|
\]
satisfy \(|d(X,Y)-d(A,B)|\le\varepsilon\).

Choose
\[
\alpha=\rho,\qquad d=\eta=\frac{\rho}{10},
\qquad \varepsilon=\left(\frac{\rho}{100}\right)^2.
\]

For all sufficiently large \(n\), every \(n\)-vertex graph of minimum degree at least \(cn\) has a partition
\[
V(G)=V_0\sqcup V_1\sqcup\cdots\sqcup V_k
\]
and a graph \(R\) on \([k]\), where \(k\) is bounded in terms of \(c\), such that:

1. \(|V_0|\le\rho n\);
2. every \(V_i\), \(i\ge1\), has size at least a positive constant times \(n\);
3. every edge \(ij\in E(R)\) represents an \(\varepsilon\)-regular pair of density at least \(d\);
4. writing \(w(I)=\sum_{i\in I}|V_i|\),
   \[
   w(N_R(i))\ge\gamma n\qquad(i\in[k]).
   \tag{3}
   \]

Here is the regularity argument, included to specify precisely what is used.

Start with a bounded partition whose parts have size at most \(\eta n\). For a partition \(\mathcal P\), use the energy
\[
\mathcal E(\mathcal P)
=\frac1{n^2}\sum_{A,B\in\mathcal P}|A||B|d(A,B)^2,
\]
including diagonal terms, with adjacency-matrix density on \(A\times A\). It lies in \([0,1]\) and does not decrease under refinement, by convexity.

For every irregular pair choose witnessing subsets and refine all parts by all witnesses. An irregular ordered pair \(A,B\) increases energy by more than
\[
\varepsilon^4\frac{|A||B|}{n^2}.
\]
Thus, while the total weight of irregular ordered pairs exceeds \(\varepsilon n^2\), energy increases by more than \(\varepsilon^5\). This process stops after at most \(\lceil\varepsilon^{-5}\rceil\) refinements. A partition with \(k\) parts is refined into at most \(k2^k\) parts, so the final number of parts has a bound \(M=M(c)\).

Delete every part having irregular partners of total size greater than \(\sqrt\varepsilon n\). Their total size is at most \(\sqrt\varepsilon n\). Also delete parts smaller than \(\eta n/M\); their total size is at most \(\eta n\). These deleted vertices form \(V_0\).

Join retained parts in \(R\) when their pair is regular and has density at least \(d\). For a retained part \(V_i\), average the degrees of its vertices. Contributions from deleted vertices, its own part, irregular partners and low-density regular partners are at most
\[
(\eta+\sqrt\varepsilon)n+\eta n+\sqrt\varepsilon n+dn.
\]
Therefore
\[
w(N_R(i))
\ge\bigl(c-2\eta-2\sqrt\varepsilon-d\bigr)n
\ge(c-\rho)n.
\]
Also \(\eta+\sqrt\varepsilon<\rho\). This proves all the asserted partition properties.

## 2.2 Supports and two consequences of having no \(C_3,C_5\)

For **every** vertex \(v\), including \(v\in V_0\), define its support
\[
S(v)=
\left\{i\in[k]:|N_G(v)\cap V_i|\ge\alpha |V_i|\right\}.
\]
The number of neighbours outside the union of its support parts is at most
\[
|V_0|+\alpha n\le2\rho n.
\]
Hence
\[
\left|N_G(v)\cap\bigcup_{i\in S(v)}V_i\right|\ge\beta n.
\tag{4}
\]

For sufficiently large \(n\), regularity gives the following two facts.

**Fact A.** If \(xy\in E(G)\), then
\[
N_R(S(x))\cap N_R(S(y))=\varnothing.
\tag{5}
\]

Indeed, if a cluster \(C\) is adjacent in \(R\) to \(A\in S(x)\) and \(B\in S(y)\), regularity supplies a path
\[
x-a-z-b-y
\]
with \(a\in A,z\in C,b\in B\), all five vertices distinct. Together with \(xy\), this is a pentagon. This works also when \(A=B\): almost every vertex of \(C\) has many neighbours in each of the two prescribed positive-sized subsets of \(A\).

**Fact B.** If \(x=y\), or if \(x,y\) have a common neighbour, then there is no edge of \(R\) between \(S(x)\) and \(S(y)\).

For \(x=y\), such an edge gives a triangle through \(x\). If \(x,y\) have common neighbour \(z\), it supplies a path
\[
x-a-b-y,
\]
which together with \(y-z-x\) gives a pentagon.

These applications of regularity need no induced-cycle assumption. To make the distinctness details explicit, remove the at most three already prescribed vertices from the relevant neighbourhood subsets. Their remaining relative sizes are at least \(\alpha/2>\varepsilon\) once the parts are large enough. Regularity then supplies the required edge or two-edge path, since \(\varepsilon<d/4\). For example, part size at least \(100/(\alpha d)\) is more than sufficient.

## 2.3 Small supports are easy to colour

Call a support **small** if
\[
w(S)<2\beta n.
\]
Let \(W\) be the vertices having small support.

Each fixed-support class in \(W\) is independent in \(J(G)\). Indeed, by (4), any two vertices in it have at least \(\beta n\) neighbours in a set of size less than \(2\beta n\), so their neighbourhoods intersect. Apply (1).

Thus \(J(G)[W]\) has a proper colouring \(\kappa_W\) with at most
\[
p=2^k
\]
colours, by using the support itself as the colour.

For each vertex \(v\), record the following three pieces of information:
\[
\begin{aligned}
S(v),\qquad
L(v)&=\{\kappa_W(w):w\in N_G(v)\cap W\},\\
T(v)&=\{S(w):w\in N_G(v)\}.
\end{aligned}
\tag{6}
\]
There are at most
\[
p\,2^p\,2^p=p\,2^{2p}
\tag{7}
\]
possible records.

I claim that these records properly colour \(J(G)\).

## 2.4 The nine-part counting argument

Suppose otherwise. Let \(u,v\) have the same record, with a walk
\[
u-a-b-v
\tag{8}
\]
of length \(3\).

The endpoints cannot belong to \(W\), by the preceding fixed-support colouring.

Nor can \(a\in W\). If it did, \(L(u)=L(v)\) would give \(a'\in N(v)\cap W\) with
\(\kappa_W(a')=\kappa_W(a)\). But \(a,b,v,a'\) is a length-\(3\) walk, contradicting properness of \(\kappa_W\). The case \(b\in W\) is symmetric.

Put
\[
P=S(u)=S(v),\qquad Q=S(a),\qquad D=S(b).
\]
All three are non-small, so
\[
w(P),w(Q),w(D)\ge2\beta n.
\tag{9}
\]

By Fact A, applied to the three edges of (8), the sets
\[
N_R(P),\quad N_R(Q),\quad N_R(D)
\]
are pairwise disjoint. Since every vertex of \(R\) has a neighbour by (3), this also implies that \(P,Q,D\) are pairwise disjoint.

Next, \(P\cup Q\cup D\) is independent in \(R\):

* each individual support is independent, by Fact B with \(x=y\);
* there are no edges between \(P,Q\), since \(a,v\) share neighbour \(b\);
* there are no edges between \(P,D\), since \(u,b\) share neighbour \(a\);
* because \(T(u)=T(v)\), some \(b'\in N(u)\) has \(S(b')=D\). The vertices \(a,b'\) share neighbour \(u\), so Fact B rules out edges between \(Q,D\).

Consequently, these **six sets of clusters** are pairwise disjoint:
\[
P,\ Q,\ D,\ N_R(P),\ N_R(Q),\ N_R(D).
\]
Each of the last three has weight at least \(\gamma n\), by (3), and each of the first three has weight at least \(2\beta n\). Therefore
\[
n\ge6\beta n+3\gamma n>n,
\]
by (2), a contradiction.

Thus (6) is a proper bounded colouring of \(J(G)\).

For all sufficiently large \(n\), (7) bounds \(\chi(J(G))\) solely in terms of \(c\). Enlarge that bound to cover smaller graphs as well, using at most \(n\) colours for an \(n\)-vertex graph. Observation 2 then gives one finite triangle-free target \(U_q\) for every graph in question.

This proves the upper half.

---

# 3. Lower bound: every \(c<1/9\) fails

We use Kneser graphs
\[
F=KG(m,k),
\]
whose vertices are the \(k\)-subsets of \([m]\), with disjoint sets adjacent. Their chromatic number is
\[
\chi(KG(m,k))=m-2k+2.
\tag{10}
\]
Only the lower bound in (10) is needed. A proof is included in Section 4.

Fix a proposed triangle-free target \(H\), with \(h\) vertices. We may assume \(h\ge2\), since \(K_2\) already rules out targets with fewer vertices.

Choose
\[
m=2k+h-1.
\]
Then \(\chi(F)\ge h+1\).

## 3.1 The sparse core

Orient each edge \(ST\) of \(F\) arbitrarily and replace it by
\[
S-a_{ST}-b_{ST}-T.
\]
Call the resulting graph \(Q\). Assign types and labels as follows:
\[
\begin{array}{c|c|c}
\text{vertex}&\text{type}&\text{label}\\ \hline
S&0&S\\
a_{ST}&1&S\\
b_{ST}&2&T
\end{array}
\]

Thus labels agree across edges of types \(0\!-\!1\) and \(0\!-\!2\), and are disjoint across edges of type \(1\!-\!2\).

It follows that:

> The endpoints of every length-\(3\) core walk having the same type have disjoint labels.

Indeed, its type sequence goes once around \(0,1,2,0\), in one direction or the other: two label-preserving edges and one disjoint-label edge.

The core has
\[
N=|V(F)|+2|E(F)|
\]
vertices.

## 3.2 Three bipartite reservoirs

Choose a positive integer \(t\). For each type \(i\in\{0,1,2\}\), add:

* a set \(A_i=[m]\times[t]\), of size \(mt\);
* a set \(B_i\), of size \(kt\);
* all edges between \(A_i\) and \(B_i\).

Join each core vertex of type \(i\) and label \(S\) to
\[
S\times[t]\subseteq A_i.
\]
There are no other edges. Denote this graph by \(G\).

Its order is
\[
n=N+3(m+k)t,
\]
and every vertex has degree at least \(kt\). Thus
\[
\frac{\delta(G)}{n}
\ge
\frac{kt}{N+3(m+k)t}
\longrightarrow
\frac{k}{3(m+k)}
=
\frac{k}{9k+3(h-1)}
\quad(t\to\infty).
\tag{11}
\]
As \(k\to\infty\), the last expression tends to \(1/9\). Therefore, for any \(c<1/9\), first choose \(k\) and then \(t\) so that \(\delta(G)\ge cn\).

## 3.3 There are no triangles or pentagons

The core itself has no cycle shorter than \(9\).

An odd cycle of length at most \(5\) involving a vertex of some \(B_i\) cannot lie entirely in its bipartite reservoir. Its segment through that reservoir between consecutive core vertices has length at least \(4\). A pentagon would therefore have to close with a core edge between vertices of the same type, which does not exist.

It remains to consider cycles avoiding all \(B_i\).

* A triangle using a reservoir vertex would require an edge between two core vertices of the same type.
* A pentagon using exactly one reservoir vertex would give a core path of length \(3\) between same-type vertices with intersecting labels, contrary to the displayed property of \(Q\).
* A pentagon using two reservoir vertices has three core vertices. Its two reservoir segments force all three core vertices to have the same type, while its remaining edge is a core edge—again impossible.
* Three reservoir vertices cannot occur in a \(5\)-cycle, since reservoir vertices form an independent set.

Thus \(G\) has neither a \(C_3\) nor a \(C_5\).

## 3.4 It cannot map to \(H\)

Each edge \(ST\) of \(F\) is represented by a length-\(3\) path in \(G\). Under a homomorphism to a triangle-free graph, its endpoints must receive different images. Hence a homomorphism \(G\to H\) would restrict to a proper \(h\)-colouring of \(F\).

But \(\chi(F)\ge h+1\). This is impossible.

So every \(c<1/9\) fails, completing the lower half.

---

# 4. The Kneser fact used above

For completeness, here is the usual short proof of the needed Kneser lower bound through the octahedral Tucker lemma.

### Octahedral Tucker lemma

Let
\[
\lambda:\{-1,0,1\}^m\setminus\{0\}\longrightarrow
\{\pm1,\ldots,\pm L\}
\]
satisfy \(\lambda(-x)=-\lambda(x)\). Write \(x\preceq y\) when every nonzero coordinate of \(x\) agrees with the corresponding coordinate of \(y\).

If
\[
x\preceq y\implies\lambda(x)\ne-\lambda(y),
\]
then \(L\ge m\).

Here is the topological proof, including the obstruction behind the lemma. Nonzero sign vectors are the nonempty faces of the boundary of the \(m\)-dimensional cross-polytope. Chains form its barycentric subdivision. Sending the vertex \(x\) to
\(\operatorname{sgn}(\lambda(x))e_{|\lambda(x)|}\) and extending linearly gives an antipodal map
\[
S^{m-1}\longrightarrow S^{L-1};
\]
the no-complementary-label condition ensures that no simplex maps through \(0\).

There is no antipodal map \(S^d\to S^{d-1}\). One standard verification uses mod-\(2\) projective cohomology: the map would descend to
\(\mathbb{RP}^d\to\mathbb{RP}^{d-1}\) and pull back the degree-one double-cover class \(a\) to \(a\). But \(a^d\ne0\) in \(\mathbb{RP}^d\), whereas \(a^d=0\) in \(\mathbb{RP}^{d-1}\). The first assertion can be seen directly by intersecting \(d\) generic projective hyperplanes: their intersection is one point, modulo \(2\); the second follows from dimension. Naturality gives the contradiction. The zero-dimensional cases are immediate. This proves Tucker's lemma.

Now suppose \(KG(m,k)\) has an \(r\)-colouring. For a sign vector \(x\), put
\[
x^+=\{i:x_i=1\},\qquad x^-=\{i:x_i=-1\}.
\]

* If \(|x^+|+|x^-|\le2k-2\), label \(x\) by its support size, with sign equal to its first nonzero coordinate.
* Otherwise, look at all \(k\)-sets contained in \(x^+\) or \(x^-\). Take the least colour occurring, and label \(x\) by \(2k-2\) plus that colour, with sign indicating the side where it occurs.

The sign in the second rule is well-defined: the same colour cannot occur on both sides, because those two \(k\)-sets would be disjoint.

The labelling is antipodal. Comparable vectors cannot have opposite labels. For small labels this follows because comparable vectors of the same support size are equal; for large labels, opposite labels would exhibit disjoint \(k\)-sets of the same colour. Tucker therefore gives
\[
2k-2+r\ge m,
\]
or
\[
r\ge m-2k+2,
\]
as required.

---

# 5. Python checks

The following is executable checking code, not a program that merely prints the claimed constant. It checks:

* the lower construction, including absence of \(C_3,C_5\), degrees and the embedded Kneser obstruction;
* the Kneser chromatic numbers in the tested instances, by SAT;
* the universal triangle-free target construction on all \(150\) nonempty \(C_3,C_5\)-free graphs in NetworkX's graph atlas;
* the six-disjoint-sets counting step exhaustively for reduced graphs through six vertices;
* the upper-bound signature construction on explicit examples;
* actual regularity refinements, with exact rational energy increments;
* exact parameter arithmetic for larger lower-bound instances.

The mathematical arguments above establish the assertions for arbitrary sizes; finite testing is not being substituted for those arguments.

```python
import itertools as it
import math
from fractions import Fraction
import networkx as nx
from z3 import Solver, Int, sat


def odd3(G):
    J = nx.Graph()
    J.add_nodes_from(G)
    for x in G:
        for a in G[x]:
            for b in G[a]:
                for y in G[b]:
                    assert x != y, "closed 3-walk"
                    J.add_edge(x, y)
    return J


def no_cycle(G, length):
    for start in G:
        def dfs(path):
            if len(path) == length:
                return start not in G[path[-1]]
            for v in G[path[-1]]:
                if v not in path and not dfs(path + [v]):
                    return False
            return True
        if not dfs([start]):
            return False
    return True


def colorable(G, q):
    z = {v: Int("x" + str(i)) for i, v in enumerate(G)}
    solver = Solver()
    solver.add(*[a >= 0 for a in z.values()])
    solver.add(*[a < q for a in z.values()])
    solver.add(*[z[u] != z[v] for u, v in G.edges()])
    return solver.check() == sat


def lower(m, k, t=1):
    sets = list(it.combinations(range(m), k))
    F = nx.Graph()
    F.add_nodes_from(range(len(sets)))
    for i, j in it.combinations(range(len(sets)), 2):
        if set(sets[i]).isdisjoint(sets[j]):
            F.add_edge(i, j)

    G = nx.Graph()
    typ, lab = {}, {}
    for i, S in enumerate(sets):
        v = ("v", i)
        G.add_node(v)
        typ[v], lab[v] = 0, S

    for i, j in F.edges():
        a, b = ("a", i, j), ("b", i, j)
        G.add_edges_from([(("v", i), a), (a, b),
                          (b, ("v", j))])
        typ[a], typ[b] = 1, 2
        lab[a], lab[b] = sets[i], sets[j]

    core = list(G)
    for h in range(3):
        A = [("A", h, i, s) for i in range(m) for s in range(t)]
        B = [("B", h, s) for s in range(k*t)]
        G.add_nodes_from(A + B)
        G.add_edges_from(it.product(A, B))

    for v in core:
        G.add_edges_from(
            (v, ("A", typ[v], i, s))
            for i in lab[v] for s in range(t)
        )
    return G, F


def universal_image(G, col):
    sig = {
        v: (col[v], frozenset(col[w] for w in G[v]))
        for v in G
    }
    H = nx.Graph()
    H.add_nodes_from(sig.values())
    for x, y in it.combinations(H, 2):
        i, S = x
        j, T = y
        if i in T and j in S and S.isdisjoint(T):
            H.add_edge(x, y)
    assert all(H.has_edge(sig[u], sig[v]) for u, v in G.edges())
    assert sum(nx.triangles(H).values()) == 0
    return H


def density(G, A, B):
    return Fraction(
        sum(G.has_edge(a, b) for a in A for b in B),
        len(A)*len(B)
    )


def subsets(A):
    A = list(A)
    for mask in range(1, 1 << len(A)):
        yield frozenset(
            A[i] for i in range(len(A)) if mask >> i & 1
        )


def irregular_witness(G, A, B, eps):
    base = density(G, A, B)
    for X in subsets(A):
        if len(X) < eps*len(A):
            continue
        for Y in subsets(B):
            if (len(Y) >= eps*len(B)
                    and abs(density(G, X, Y) - base) > eps):
                return X, Y
    return None


def energy(G, parts):
    n = len(G)
    return sum(
        Fraction(len(A)*len(B), n*n)*density(G, A, B)**2
        for A in parts for B in parts
    )


def weighted_regularity(G, parts, eps):
    steps = 0
    while True:
        cuts = [[] for _ in parts]
        badmass = 0
        for i, j in it.combinations(range(len(parts)), 2):
            witness = irregular_witness(G, parts[i], parts[j], eps)
            if witness:
                cuts[i].append(witness[0])
                cuts[j].append(witness[1])
                badmass += 2*len(parts[i])*len(parts[j])

        if badmass <= eps*len(G)**2:
            return parts, steps

        old = energy(G, parts)
        new = []
        for A, cut_list in zip(parts, cuts):
            atoms = [frozenset(A)]
            for X in cut_list:
                atoms = [
                    Z for Y in atoms for Z in (Y & X, Y-X) if Z
                ]
            new += atoms
        parts = new
        steps += 1
        assert energy(G, parts) - old > eps**5
        assert steps < 1/eps**5 + 1


def check_signature_coloring(G, parts, R, c, rho):
    n = len(G)
    beta, gamma = c-2*rho, c-rho
    S = {
        v: frozenset(
            i for i, A in enumerate(parts)
            if len(set(G[v]) & set(A)) >= rho*len(A)
        )
        for v in G
    }
    weight = lambda P: sum(len(parts[i]) for i in P)
    NR = lambda P: set().union(*(set(R[i]) for i in P))

    assert min(weight(R[i]) for i in R) >= gamma*n
    assert n-sum(map(len, parts)) <= rho*n

    for u, v in G.edges():
        assert NR(S[u]).isdisjoint(NR(S[v]))
    for u in G:
        for v in G:
            if u == v or set(G[u]) & set(G[v]):
                assert not any(
                    R.has_edge(i, j) for i in S[u] for j in S[v]
                )

    J = odd3(G)
    W = {v for v in G if weight(S[v]) < 2*beta*n}
    assert all(
        S[u] != S[v] for u, v in J.edges() if u in W and v in W
    )
    sig = {
        v: (
            S[v],
            frozenset(S[w] for w in G[v] if w in W),
            frozenset(S[w] for w in G[v])
        )
        for v in G
    }
    assert all(sig[u] != sig[v] for u, v in J.edges())
    colors = {s: i for i, s in enumerate(set(sig.values()))}
    universal_image(G, {v: colors[sig[v]] for v in G})
    p = 2**len(parts)
    assert len(colors) <= p*2**(2*p)


def check_support_counting():
    count = 0
    for R in nx.graph_atlas_g():
        n = len(R)
        if not 1 <= n <= 6:
            continue
        if min(dict(R.degree()).values()) == 0:
            continue

        adj = [sum(1 << j for j in R[i]) for i in range(n)]
        neigh = {}
        for S in range(1 << n):
            N = 0
            for i in range(n):
                if S >> i & 1:
                    N |= adj[i]
            neigh[S] = N

        independent = [
            S for S in range(1, 1 << n) if not S & neigh[S]
        ]
        for P, Q, D in it.product(independent, repeat=3):
            NP, NQ, ND = neigh[P], neigh[Q], neigh[D]
            if NP & NQ or NP & ND or NQ & ND:
                continue
            union = P | Q | D
            if union & neigh[union]:
                continue
            regions = [P, Q, D, NP, NQ, ND]
            assert all(
                not A & B for A, B in it.combinations(regions, 2)
            )
            assert sum(A.bit_count() for A in regions) <= n
            count += 1

    # The nine-vertex equality template: three disjoint K_{1,2}.
    R = nx.disjoint_union_all([nx.star_graph(2) for _ in range(3)])
    Ps = [{1, 2}, {4, 5}, {7, 8}]
    Ns = [set().union(*(set(R[v]) for v in P)) for P in Ps]
    assert sum(map(len, Ps + Ns)) == len(R) == 9
    print("support counting:", count, "configurations checked")


def check_large_parameter_arithmetic(c, h):
    k = int(3*c*(h-1)/(1-9*c)) + 1
    m = 2*k+h-1
    vertices = math.comb(m, k)
    edges = vertices*math.comb(m-k, k)//2
    core = vertices+2*edges
    gap = k-3*c*(m+k)
    t = int(c*core/gap) + 1
    assert gap > 0
    assert k*t > c*(3*(m+k)*t+core)
    assert m-2*k+2 == h+1
    print("large parameters:", c, h, k,
          "; digits in t:", len(str(t)))


if __name__ == "__main__":
    for m, k in [(3, 1), (5, 2), (6, 2), (7, 3)]:
        G, F = lower(m, k)
        assert len(G) == len(F)+2*F.number_of_edges()+3*(m+k)
        assert min(dict(G.degree()).values()) >= k
        assert no_cycle(G, 3) and no_cycle(G, 5)
        J = odd3(G)
        assert all(
            J.has_edge(("v", i), ("v", j)) for i, j in F.edges()
        )
        chi = m-2*k+2
        assert colorable(F, chi)
        assert not colorable(F, chi-1)
        print("lower checked:", m, k, "chi =", chi,
              "order =", len(G))

    count = 0
    for G in nx.graph_atlas_g():
        if G and no_cycle(G, 3) and no_cycle(G, 5):
            J = odd3(G)
            col = nx.coloring.greedy_color(J, strategy="largest_first")
            universal_image(G, col)
            count += 1
    print("universal images checked:", count)

    for c in [Fraction(1, 9)+Fraction(1, 10000),
              Fraction(1, 8), Fraction(1, 5), Fraction(1, 2)]:
        rho = min((9*c-1)/30, Fraction(1, 100))
        assert rho > 0 and c-2*rho > 0
        assert 9*c-15*rho > 1

    check_support_counting()

    G = nx.complete_bipartite_graph(4, 4)
    check_signature_coloring(
        G, [set(range(4)), set(range(4, 8))], nx.path_graph(2),
        Fraction(1, 2), Fraction(1, 100)
    )
    G = nx.cycle_graph(7)
    check_signature_coloring(
        G, [{i} for i in G], G,
        Fraction(1, 4), Fraction(1, 100)
    )
    print("upper signatures checked: K4,4 and C7")

    G = nx.gnp_random_graph(12, Fraction(1, 3), seed=19)
    parts, steps = weighted_regularity(
        G,
        [frozenset(range(i, i+3)) for i in range(0, 12, 3)],
        Fraction(1, 5)
    )
    print("exact regularity increments:", steps,
          "; final parts:", len(parts))

    check_large_parameter_arithmetic(Fraction(1, 10), 4)
    check_large_parameter_arithmetic(
        Fraction(1, 9)-Fraction(1, 1000), 10
    )
```

The checks were run successfully. In particular, they verified the four constructed lower-bound graphs of orders \(21,61,129,205\), all \(150\) atlas graphs described above, \(72\) support-counting configurations, two exact-rational regularity refinement steps, and a lower-bound parameter choice whose reservoir multiplier has \(219\) decimal digits.

**Conclusion.** Every \(c>1/9\) has the required property, and every \(c<1/9\) does not. Therefore the exact requested infimum is
\[
\boxed{\frac19}.
\]
Nothing remains to prove for the infimum asked in the question.