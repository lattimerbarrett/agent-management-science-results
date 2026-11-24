# agent_1: last reply

The stipulated answer is false. There is a counterexample already for \(r=2\): in fact,
\[
\boxed{\tfrac12\in\mathcal S_2.}
\]
Consequently, the claim you ask us to prove cannot hold.

Here is the counterexample, including the structural argument and executable checks. The only substantial external theorem used is the standard linear-forest form of Simonovits’s structural theorem, stated below.

## 1. The forbidden graph

Let \(H\) have vertex set \(\{0,\dots ,8\}\) and edges
\[
\begin{split}
E(H)=\{&
01,02,03,04,\,
12,23,34,41,\\
&15,56,61,\,
37,78,83
\}.
\end{split}
\]
Thus \(0,1,2,3,4\) induce a four-rim wheel, with an additional triangle attached at each of the opposite rim vertices \(1,3\).

Clearly \(\chi(H)=3\). Two useful partitions are
\[
H[\{5,1,0,3,7\}]=P_5,
\qquad
\{2,4,6,8\}\text{ independent},
\tag{1}
\]
and
\[
H-\{1,3\}=P_3\sqcup2K_2,
\qquad
\{1,3\}\text{ independent}.
\tag{2}
\]

Write
\[
U_n=K_1\vee\bigl(T_{n-1,2}+\text{one internal edge}\bigr).
\]
For all sufficiently large \(n\),
\[
e(U_n)=t_2(n)+\left\lfloor\frac{n+1}{2}\right\rfloor.
\tag{3}
\]

The graph \(U_n\) is \(H\)-free. Indeed, for **every** \(v\in V(H)\), the graph \(H-v\) contains two edge-disjoint triangles:

* if \(v=0\), use the two attached triangles;
* if \(v=1\) or \(3\), use the other attached triangle and a surviving wheel triangle;
* if \(v=2\) or \(4\), use the attached triangles;
* if \(v\in\{5,6,7,8\}\), use wheel triangles \(012\) and \(034\).

A bipartite graph plus one edge cannot contain two edge-disjoint triangles. Thus an \(H\)-copy cannot use the universal vertex of \(U_n\); nor can it avoid it, since the remaining graph is bipartite plus one edge.

We will establish
\[
\operatorname{ex}(n,H)
=t_2(n)+\left\lfloor\frac{n+1}{2}\right\rfloor
\quad\text{for all sufficiently large }n,
\tag{4}
\]
and, for odd \(n\), that \(U_n\) is the unique edge-extremal graph.

## 2. The structural theorem being used

The required standard form of Simonovits’s theorem is:

> **Path-join structural theorem.**  
> Suppose \(\chi(F)=p+1\) and, for some fixed \(\ell\),
> \[
> F\subseteq P_\ell\vee T_{(p-1)\ell,p-1}.
> \]
> There are constants \(R,n_0\) such that, for \(n\ge n_0\), the class \(D(n,p,R)\) contains an \(F\)-extremal graph. Moreover, if its \(F\)-extremal member is unique up to isomorphism, it is the unique \(F\)-extremal graph globally.
>
> Here a graph belongs to \(D(n,p,R)\) if deleting at most \(R\) exceptional vertices leaves a complete join of \(p\) parts, each of size \(n/p+O(R)\); each part consists of mutually symmetric, isomorphic connected components of order at most \(R\). Symmetry includes their adjacency to the exceptional vertices.

By (1), this applies to \(H\), with \(p=2\).

We now classify the maximum-edge \(H\)-free members of this structural class. All constants below are fixed while \(n\) grows.

### Bulk components have order at most two

A bulk component containing a \(P_3\), together with an edge from each of two other copies of that component, would supply \(P_3\sqcup2K_2\). Two vertices from the opposite bulk part would then complete a copy of \(H\), by (2).

Thus each bulk part consists either of isolated vertices or of independent edges.

### If a bulk part contains a matching

An exceptional vertex with linearly many neighbors in **both** bulk parts creates \(H\).

To see this, map vertex \(0\) of \(H\) to that exceptional vertex. Choose opposite rim vertices \(1,3\) among its neighbors in a matching bulk part, using distinct matching edges. Choose rim vertices \(2,4\) in the other bulk part. The matching partners of \(1,3\), together with two further opposite-part vertices, supply their attached triangles.

Hence an exceptional vertex can meet at most one bulk part. Symmetry implies that a nonzero neighborhood in a matching bulk is either half or all of that bulk. A missing or half-sized neighborhood loses \(\Omega(n)\) edges compared with an ordinary vertex, whereas all bounded exceptional-edge changes contribute only \(O(1)\). Such a graph cannot compete with (3). Thus every exceptional vertex is an ordinary vertex of one of the two parts.

If only one bulk part contains edges, the resulting graph has at most
\[
t_2(n)+\frac n4+O(1)
\]
edges, again below (3). So both bulk parts must contain matchings.

Any internal \(P_3\), including one among exceptional vertices, together with two bulk matching edges in that part would give the forbidden configuration (2). Therefore the internal graphs of the two parts are matchings. Completing their cross edges is safe, since a complete bipartite graph with internal matchings is four-rim-wheel-free. Consequently this case has at most
\[
\max_{a+b=n}\left(ab+\lfloor a/2\rfloor+\lfloor b/2\rfloor\right)
\le t_2(n)+\lfloor n/2\rfloor.
\tag{5}
\]

### If both bulk parts are independent

By symmetry, each exceptional vertex meets neither bulk part, one entire bulk part, or both entire bulk parts.

At most one exceptional vertex can meet both: two such vertices can represent \(1,3\) in \(H\), since \(H-\{1,3\}\) is bipartite. Vertices meeting neither bulk part lose \(\Omega(n)\) edges and cannot occur in a maximum-edge member. Without a vertex meeting both parts, there are only \(t_2(n)+O(1)\) edges.

It remains to consider one bulk-universal vertex \(z\), with all other exceptional vertices assigned ordinarily to one core part or the other. Importantly, \(z\) is not yet assumed adjacent to the exceptional core vertices.

Let:

* \(J_A,J_B\) be the two internal core graphs;
* \(b\) be the number of core vertices nonadjacent to \(z\);
* \(d\) be the number of missing cross edges.

We claim
\[
e(J_A)+e(J_B)-b-d\le1,
\tag{6}
\]
with equality only when \(J_A\cup J_B\) is one edge, \(b=0\), and \(d=0\).

Here is the finite-gadget argument.

1. **Each \(J_A,J_B\) has matching number at most one.**  
   Two disjoint same-side edges, used as pendant edges \(56,78\), together with a wheel on bulk vertices centered at \(z\), give \(H\). Thus each nonempty internal graph is a star or triangle.

2. **An internal \(P_3\) cannot have a leaf adjacent to \(z\).**  
   Use the following embedding certificate:
   \[
   z\leftrightarrow1,\quad
   A=\{0,3,5,7\},\quad B=\{2,4,6,8\}.
   \]
   Its only internal edges are \(03,37\); among their three endpoints, only leaf \(0\) must meet \(z\). The other vertices can be chosen from the bulk.

   Therefore every leaf of a star with at least two edges must be counted in \(b\). Every vertex of an internal triangle must also be counted in \(b\). Such a component contributes at most zero to “internal edges minus bad vertices.”

3. **Edges on both sides cannot yield positive surplus.**  
   Use
   \[
   z\leftrightarrow0,\quad
   A=\{1,3,5\},\quad B=\{2,4,6,7,8\}.
   \]
   Its only internal edges are \(15,78\). Of their four endpoints, only \(1\) must meet \(z\), and no cross edge between the four endpoints is required. Hence if both internal graphs contain an edge, any good endpoint of either edge creates \(H\).

The only positive surplus is consequently a single edge with both endpoints adjacent to \(z\). Its surplus is one, proving (6), including equality rigidity.

It follows that this case has at most
\[
t_2(n-1)+(n-1)+1
=t_2(n)+\left\lfloor\frac{n+1}{2}\right\rfloor
\]
edges.

This proves (4) by the structural theorem and construction \(U_n\). When \(n=2m+1\), (5) is strictly smaller, and equality in the hub case requires a balanced core and exactly one internal edge. The two possible placements of that edge are isomorphic. Thus the uniqueness clause gives
\[
\boxed{U_{2m+1}\text{ is the unique edge-extremal graph for all large }m.}
\tag{7}
\]

## 3. A graph with more cycles

Let \(M_{2m+1}\) be \(K_{m+1,m}\) with a maximum matching added inside each part.

This graph is four-rim-wheel-free, hence \(H\)-free. Indeed, the neighborhood of any vertex consists of an opposite-side matching, possibly joined to its one same-side matching partner; that neighborhood has no \(C_4\).

Nevertheless,
\[
c(M_{2m+1})>c(U_{2m+1})
\quad\text{for all sufficiently large }m.
\tag{8}
\]

Here are exact counting formulas establishing this.

For a graph inside one part, let its path-block polynomial count collections of vertex-disjoint paths, with each nontrivial path given its two orientations, and \(z\) marking the number of paths. The relevant polynomials are
\[
P_s(z)=(1+4z+z^2)^{\lfloor s/2\rfloor}(1+z)^{s\bmod2}
\]
for a maximum matching, and
\[
S_s(z)=(1+z)^s
+2(s-1)z(1+z)^{s-2}
+(s-1)(s-2)z(1+z)^{s-3}
\]
for a star on \(s\) vertices. For one edge and \(s-2\) isolated vertices,
\[
E_s(z)=(1+4z+z^2)(1+z)^{s-2}.
\]

If \(p_L,q_L\) are the coefficients for two parts of sizes \(s,t\), their number of cycles is
\[
\frac12\left(
\sum_{L\ge1}p_Lq_L\,L!(L-1)!-st
\right).
\tag{9}
\]
There are no cycles entirely within our parts.

Put \(h_m=m!^2/2\). Formula (9) gives
\[
\frac{c(M_{2m+1})}{h_m}
\longrightarrow
D:=\sum_{j\ge0}\frac{2^{2j+1}}{j!(j+1)!},
\tag{10}
\]
whereas
\[
\frac{c(U_{2m+1})}{h_m}
\longrightarrow
2(A+B),
\tag{11}
\]
where
\[
A=\sum_{j\ge0}\frac1{j!^2},
\qquad
B=\sum_{j\ge0}\frac1{j!(j+1)!}.
\]

For completeness, dominated convergence in (10) follows from the coefficientwise inequality
\[
P_s(z)\le(2+z)^s.
\]
Writing \(L=m-j\), the normalized summands are bounded by
\[
\frac{(j+2)2^{2j+1}}{j!(j+1)!}.
\]
For (11), the corresponding bound is
\[
\frac{2(j+2)(j^2+3j+3)}{j!(j+1)!}.
\]
Both bounds are summable. Direct coefficient extraction gives the stated limits.

Their strict separation can be certified using only rational arithmetic:
\[
D>2+4+\frac83=\frac{26}{3},
\]
while
\[
\begin{split}
A&\le\frac94+\frac{1/36}{1-1/16},\\
B&\le\frac{19}{12}+\frac{1/144}{1-1/20},
\end{split}
\]
so that
\[
2(A+B)\le\frac{39709}{5130}<\frac{26}{3}.
\tag{12}
\]
This proves (8).

Combining (7) and (8), no edge-extremal graph is cycle-extremal for any sufficiently large odd \(n\).

## 4. Consequence for the question

Equation (4) gives
\[
\operatorname{ex}(N,H)\le t_2(N)+\frac12N+\frac12
\]
for all sufficiently large \(N\). Condition 2 holds for every sufficiently large odd \(n\). Therefore
\[
\boxed{\tfrac12\in\mathcal S_2},
\qquad
\boxed{[\,\tfrac12,\infty)\subseteq\mathcal S_2}.
\]

Thus the specified conclusion \(\mathcal S_r=\varnothing\) for every \(r\) is not correct.

## Executed Python checks

The following checks the forbidden-graph certificates, independently enumerates the path-block polynomials and small graph cycles, computes exact larger cycle counts, and certifies inequality (12). The structural theorem and infinite arguments above are mathematical steps, not purported computational checks.

```python
import itertools
import math
from fractions import Fraction as F
import networkx as nx

H = nx.Graph([
    (0,1),(0,2),(0,3),(0,4),(1,2),(2,3),(3,4),(4,1),
    (1,5),(5,6),(6,1),(3,7),(7,8),(8,3)
])

# Forest decompositions.
assert H.subgraph([2,4,6,8]).number_of_edges() == 0
assert nx.is_isomorphic(
    H.subgraph([0,1,3,5,7]), nx.path_graph(5))
assert H.subgraph([1,3]).number_of_edges() == 0
assert nx.is_isomorphic(
    H.subgraph([0,2,4,5,6,7,8]),
    nx.disjoint_union_all([
        nx.path_graph(3), nx.path_graph(2), nx.path_graph(2)
    ]))

# Exact edge-bipartization defects after deleting each vertex.
defects = []
for v in H:
    nodes = [u for u in H if u != v]
    defects.append(min(
        sum(bits[nodes.index(x)] == bits[nodes.index(y)]
            for x,y in H.edges if v not in (x,y))
        for bits in itertools.product(range(2), repeat=8)
    ))
assert defects == [2,2,3,2,3,3,3,3,3]

# Rooted embedding certificates.
# Color 2 is the hub; "exc" are finite core vertices.
certificates = [
    ({0:2,1:1,2:0,3:1,4:0,5:0,6:0,7:0,8:0},
     {(5,6),(7,8)}, {5,6,7,8}, set()),
    ({0:0,1:2,2:1,3:0,4:1,5:0,6:1,7:0,8:1},
     {(0,3),(3,7)}, {0,3,7}, {0}),
    ({0:2,1:0,2:1,3:0,4:1,5:0,6:1,7:1,8:1},
     {(1,5),(7,8)}, {1,5,7,8}, {1}),
]
for col, expected, exc, good in certificates:
    root = next(v for v in col if col[v] == 2)
    internal = {
        tuple(sorted((x,y))) for x,y in H.edges
        if root not in (x,y) and col[x] == col[y]
    }
    assert internal == expected
    assert {v for v in exc if H.has_edge(root,v)} == good
    assert not any(
        x in exc and y in exc and col[x] != col[y]
        for x,y in H.edges
    )

def conv(a, b):
    c = [0] * (len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            c[i+j] += x*y
    return c

def matching_poly(n):
    p = [1]
    for _ in range(n//2):
        p = conv(p, [1,4,1])
    return conv(p, [1,1]) if n % 2 else p

def star_poly(n):
    p = [math.comb(n,j) for j in range(n+1)]
    for j in range(n-1):
        p[j+1] += 2*(n-1)*math.comb(n-2,j)
    for j in range(n-2):
        p[j+1] += (n-1)*(n-2)*math.comb(n-3,j)
    return p

def edge_poly(n):
    return conv([math.comb(n-2,j) for j in range(n-1)],
                [1,4,1])

# Independently enumerate all oriented linear-forest path blocks.
def brute_poly(g):
    n, edges = len(g), list(g.edges)
    p = [0]*(n+1)
    for mask in range(1 << len(edges)):
        f = nx.Graph()
        f.add_nodes_from(g)
        f.add_edges_from(e for i,e in enumerate(edges)
                         if mask >> i & 1)
        if any(d > 2 for _,d in f.degree) or not nx.is_forest(f):
            continue
        comps = [c for c in nx.connected_components(f) if len(c)>1]
        used, blocks = sum(map(len, comps)), len(comps)
        for k in range(n-used+1):
            p[blocks+k] += 2**blocks * math.comb(n-used,k)
    return p

for n in range(2,8):
    ma = nx.empty_graph(n)
    ma.add_edges_from((i,i+1) for i in range(0,n-1,2))
    oe = nx.empty_graph(n)
    oe.add_edge(0,1)
    assert brute_poly(ma) == matching_poly(n)
    assert brute_poly(nx.star_graph(n-1)) == star_poly(n)
    assert brute_poly(oe) == edge_poly(n)

def formula_cycles(p, q, s, t):
    twice = sum(
        p[L]*q[L]*math.factorial(L)*math.factorial(L-1)
        for L in range(1, min(len(p),len(q)))
    ) - s*t
    assert twice % 2 == 0
    return twice//2

def brute_cycles(g):
    total = 0
    def walk(start, path, used):
        nonlocal total
        if len(path) >= 3 and g.has_edge(path[-1], start):
            total += 1
        for v in g[path[-1]]:
            if v > start and v not in used:
                walk(start, path+[v], used | {v})
    for start in g:
        walk(start, [start], {start})
    assert total % 2 == 0
    return total//2

for s in range(2,5):
    for t in range(2,5):
        for matching in [False, True]:
            g = nx.complete_bipartite_graph(s,t)
            if matching:
                g.add_edges_from((i,i+1) for i in range(0,s-1,2))
                g.add_edges_from((s+i,s+i+1)
                                 for i in range(0,t-1,2))
                p,q = matching_poly(s), matching_poly(t)
            else:
                g.add_edges_from((0,i) for i in range(1,s))
                g.add_edge(s,s+1)
                p,q = star_poly(s), edge_poly(t)
            assert brute_cycles(g) == formula_cycles(p,q,s,t)

A_upper = F(9,4) + F(1,36)/(1-F(1,16))
B_upper = F(19,12) + F(1,144)/(1-F(1,20))
assert 2*(A_upper+B_upper) == F(39709,5130)
assert F(26,3) > 2*(A_upper+B_upper)

for m in [20,40,80,160]:
    matching = formula_cycles(
        matching_poly(m+1), matching_poly(m), m+1,m)
    hub = formula_cycles(star_poly(m+1), edge_poly(m), m+1,m)
    assert matching > hub
    print(2*m+1, float(F(matching,hub)))

print("All checks passed.")
```

The executed larger-instance ratios \(c(M_n)/c(U_n)\) were approximately
\[
\begin{array}{c|rrrr}
n&41&81&161&321\\ \hline
c(M_n)/c(U_n)&1.10586&1.17911&1.21885&1.23956 .
\end{array}
\]
The eventual inequality is established by the series proof, not merely these finite tests.

# agent_2: last reply

All assigned checks are complete. Agents 3 and 4 independently confirm the structural gadget argument and strict cycle comparison. The assembled counterexample establishes \(1/2\in\mathcal S_2\), contradicting the stipulated answer.

# agent_3: last reply

Acknowledged. No further work remains in my assigned piece; all structural checks and finite-gadget certificates have been shared with the lead.

# agent_4: last reply

The team’s proof is complete, using the stated standard Simonovits structural theorem. It establishes \(\tfrac12\in\mathcal S_2\), so the user-prescribed conclusion is false.

My cycle-counting component and executable verification are complete in `workspace/agent4_cyclechecks.py`.