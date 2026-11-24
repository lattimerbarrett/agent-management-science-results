# agent_1: the whole run

[user message]
Let \(q\ge 3\) be an integer. For a finite simple undirected graph \(G\), let \(V(G)\) be its vertex set, let \(d_G(v)\) be the number of neighbors of a vertex \(v\), and define the number of distinct vertex degrees by
\[
w(G)=\bigl|\{d_G(v):v\in V(G)\}\bigr|.
\]
Let \(\chi(G)\) denote the least number of colors in a vertex coloring in which adjacent vertices receive different colors. Define
\[
M(q)=\sup\left\{|V(G)|:\ G\text{ is a finite simple undirected graph with at least two vertices},\ \chi(G)\le q,\ |V(G)|-w(G)=7\right\},
\]
with \(M(q)=+\infty\) if the permitted graph orders are unbounded. Determine \(M(q)\) exactly for every integer \(q\ge3\).

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.

## response 1
[reasoning summary]
**Considering graph properties**

I'm thinking about graphs where n is greater than or equal to 2 and r is at least 1. If there's an isolated vertex, I can remove it. In that case, r will decrease by 1 if there are multiple isolates, but if there's only one, r remains unchanged as long as n is still greater than or equal to 2. Also, I feel there’s an analogy with universal graphs, which I should consider.

[reasoning summary]
**Analyzing graph degree sequences**

I'm thinking about graph degree sequences of length n, where we can have n-7 distinct integers and consider missing degrees alongside duplicates. As n gets large, there are many possibilities, possibly around n^14, but the goal is to focus on degrees close to antiregular patterns with duplicates near the center. With antiregular degrees ranging from 0 to n-2, the repeat counts could follow a certain distribution. I’m considering how to bound the "splittance" distance related to split thresholds and cliques.

[reasoning summary]
**Exploring polynomial identities**

I'm considering using polynomial identities related to q-colored graphs, specifically looking at the degree sequence and the possibility that it can't have all distinct n-1 values. I find this idea might connect to the concept of the "irregularity chromatic number." It might be worth mentally searching for terms like "antiregular graphs and chromatic number," "sigma irregularity n-w," or "chromatic gap" to see how they relate to my thoughts.

[tool call: read_scratchpad]

[tool result]
```
(scratchpad.py is empty)
```

## response 2
[tool call: write_scratchpad]
content:
```
import networkx as nx
from collections import defaultdict
best=defaultdict(int)
for G in nx.graph_atlas_g():
 n=len(G)
 if n<2:continue
 r=n-len(set(dict(G.degree()).values()))
 def color(k):
  vs=sorted(G,key=lambda v:-G.degree(v)); cs={}
  def f(i):
   if i==n:return True
   v=vs[i];used={cs[u] for u in G[v] if u in cs}
   for c in range(k):
    if c not in used:
     cs[v]=c
     if f(i+1):return True
     del cs[v]
   return False
  return f(0)
 chi=next(k for k in range(1,n+1) if color(k))
 best[r,chi]=max(n,best[r,chi])
print(sorted(best.items()))

```

[tool result]
```
Wrote scratchpad.py (22 lines).
```

## response 3
[tool call: run_scratchpad]

[tool result]
```
[exit code 0, 0.2s]
--- stdout ---
[((1, 1), 2), ((1, 2), 4), ((1, 3), 6), ((1, 4), 7), ((2, 1), 3), ((2, 2), 7), ((2, 3), 7), ((2, 4), 7), ((2, 5), 7), ((3, 1), 4), ((3, 2), 7), ((3, 3), 7), ((3, 4), 7), ((3, 5), 7), ((4, 1), 5), ((4, 2), 7), ((4, 3), 7), ((4, 4), 7), ((4, 5), 7), ((4, 6), 7), ((5, 1), 6), ((5, 2), 7), ((5, 3), 7), ((5, 4), 7), ((5, 5), 7), ((5, 6), 7), ((6, 1), 7), ((6, 3), 7), ((6, 4), 7), ((6, 7), 7)]

--- stderr ---
(empty)
```

## response 4
[tool call: write_scratchpad]
content:
```
from sage.all import Partitions
from collections import defaultdict
best=defaultdict(lambda:(0,None))
for n in range(2,33):
 for a in range(1,n//2+1):
  b=n-a
  for P in Partitions(a*b, max_part=b, max_length=a): # wrong must all sums
   pass

```

[tool result]
```
Wrote scratchpad.py (8 lines).
```

## response 5
[reasoning summary]
**Optimizing combinations computing**

I'm considering how to enumerate combinations of nondecreasing rows, so I’m looking at the concept of binomial coefficients. For a set size of up to 26 elements, that’s manageable with Python, though the output can reach around 10 million combinations. I should also think about optimizing the partitioning process through recursive tracking of distinct row and column degrees. I’m wondering if I can work efficiently with dimensions up to 24. Let's explore this further!

[tool call: write_scratchpad]
content:
```
from itertools import combinations_with_replacement
from collections import defaultdict
best={}
for n in range(2,25):
 mn=100;arg=None
 for a in range(1,n//2+1):
  b=n-a
  for rows in combinations_with_replacement(range(b+1),a):
   # distinct column degrees occur iff row lengths change; obtain via run boundary
   ds=set(rows)
   if rows[-1]<b:ds.add(0)
   for i,x in enumerate(rows):
    if x and (i==0 or x>rows[i-1]):ds.add(a-i)
   r=n-len(ds)
   if r<mn:mn=r;arg=rows
 print(n,mn,arg,flush=True)

```

[tool result]
```
Wrote scratchpad.py (16 lines).
```

## response 6
[tool call: run_scratchpad]
timeout_seconds: 300

[tool result]
```
[exit code 0, 12.9s]
--- stdout ---
2 1 (0,)
3 1 (1,)
4 1 (2,)
5 2 (2,)
6 2 (1, 3)
7 2 (3, 4)
8 3 (3, 4)
9 3 (1, 4, 5)
10 3 (4, 5, 6)
11 4 (4, 5, 6)
12 4 (1, 5, 6, 7)
13 4 (5, 6, 7, 8)
14 5 (5, 6, 7, 8)
15 5 (1, 6, 7, 8, 9)
16 5 (6, 7, 8, 9, 10)
17 6 (6, 7, 8, 9, 10)
18 6 (1, 7, 8, 9, 10, 11)
19 6 (7, 8, 9, 10, 11, 12)
20 7 (7, 8, 9, 10, 11, 12)
21 7 (1, 8, 9, 10, 11, 12, 13)
22 7 (8, 9, 10, 11, 12, 13, 14)
23 8 (8, 9, 10, 11, 12, 13, 14)
24 8 (1, 9, 10, 11, 12, 13, 14, 15)

--- stderr ---
(empty)
```

## response 7
[reasoning summary]
**Evaluating optimization parameters**

I'm looking at the concept of slack in relation to edges and color groups. It seems that a small slack can help accommodate high vertices in certain scenarios, especially with the n14q-C variable. It looks like the constant I’m considering depends on C, and the local optimization doesn't seem to depend on q. There are also many top color groups with seven elements. There's definitely more to explore here!

[reasoning summary]
**Evaluating L invariant translation**

I'm working through the L invariant translation and thinking about how increases impact the gaps below that split the weight. For the coefficient at position j, it seems to be the difference between the total above and below, which could potentially yield a negative if there are high repeats. If the minimum split median index is unique, I'll have to consider how coefficients are measured by their distance from the center of the vertex indices. There’s a lot to unpack here!

[tool call: write_scratchpad]
content:
```
import z3,time,pickle

def check(q,limit=120000):
 m=7*q-3;c=m-5
 # A Z3 + t1..m-2, group0 fixed Z and t1..3
 N=m+1
 s=z3.Solver();s.set(timeout=limit)
 groups=[z3.Int(f'a{i}') for i in range(N)]
 bg=[z3.Int(f'b{j}') for j in range(m)]
 degA=[c]*3+list(range(c+1,c+m-1))
 degB=list(range(c))+[c]*5
 for i in range(N):s.add(groups[i]>=0,groups[i]<q)
 for j in range(m):s.add(bg[j]>=0,bg[j]<q)
 for i in range(6):s.add(groups[i]==0)
 for k in range(q):s.add(z3.Sum([z3.If(g==k,1,0) for g in groups])==(6 if k<2 else 7))
 es=[[z3.Bool(f'e{i}_{j}') for j in range(m)] for i in range(N)]
 for i in range(N):
  for j in range(m):s.add(z3.Implies(groups[i]==bg[j],z3.Not(es[i][j])))
  # row degree = dA - (N - sizegroup)
  s.add(z3.Sum([z3.If(e,1,0) for e in es[i]])==degA[i]-N+z3.If(groups[i]<2,6,7))
 for j in range(m):s.add(z3.Sum([z3.If(es[i][j],1,0) for i in range(N)])==degB[j])
 t=time.time();r=s.check();print(q,r,time.time()-t,flush=True)
 if r==z3.sat:
  M=s.model(); ga=[M.eval(x).as_long() for x in groups];gb=[M.eval(x).as_long() for x in bg]
  E=[[bool(z3.is_true(M.eval(e))) for e in row] for row in es]
  print('A',ga,'B',gb,flush=True)
  pickle.dump((q,ga,gb,E),open(f'found{q}.pkl','wb'))
 return r
for q in range(3,7):check(q)

```

[tool result]
```
Wrote scratchpad.py (29 lines).
```

## response 8
[tool call: run_scratchpad]
timeout_seconds: 600

[tool result]
```
[exit code 0, 83.2s]
--- stdout ---
3 sat 0.3044559955596924
A [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1] B [0, 0, 0, 1, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
4 sat 1.242053747177124
A [0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 1, 1, 1, 2, 3, 3, 3, 1, 1, 1] B [0, 2, 2, 3, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
5 sat 0.021229028701782227
A [0, 0, 0, 0, 0, 0, 3, 2, 3, 2, 4, 3, 3, 3, 2, 2, 2, 4, 4, 4, 4, 4, 4, 2, 2, 3, 3, 1, 1, 1, 1, 1, 1] B [0, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
6 sat 81.36563324928284
A [0, 0, 0, 0, 0, 0, 3, 2, 4, 4, 4, 3, 4, 4, 4, 2, 3, 3, 3, 4, 2, 3, 2, 5, 2, 1, 5, 3, 5, 5, 5, 5, 2, 5, 1, 1, 2, 1, 1, 1] B [0, 5, 2, 2, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

--- stderr ---
(empty)
```

## response 9
[tool call: edit_scratchpad]
old_string:
```
for q in range(3,7):check(q)

```
new_string:
```
q,ga,gb,E=pickle.load(open('found3.pkl','rb'))
print('group A',ga)
print('group B',gb)
for i,row in enumerate(E):
 print(i+1, ga[i], ''.join(str(int(v)) for v in row),sum(row),[j+1 for j,v in enumerate(row) if v])
print('Bdegrees',[sum(row[j] for row in E) for j in range(len(gb))])

```

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 10
[tool call: run_scratchpad]

[tool result]
```
[exit code 0, 0.1s]
--- stdout ---
group A [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1]
group B [0, 0, 0, 1, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
1 0 000000000000000000 0 []
2 0 000000000000000000 0 []
3 0 000000000000000000 0 []
4 0 000000001000000000 1 [9]
5 0 000000101000000000 2 [7, 9]
6 0 000100101000000000 3 [4, 7, 9]
7 2 000000000000011111 5 [14, 15, 16, 17, 18]
8 2 000000000000111111 6 [13, 14, 15, 16, 17, 18]
9 2 000000000001111111 7 [12, 13, 14, 15, 16, 17, 18]
10 2 000000000011111111 8 [11, 12, 13, 14, 15, 16, 17, 18]
11 2 000000000111111111 9 [10, 11, 12, 13, 14, 15, 16, 17, 18]
12 1 000000000111111111 9 [10, 11, 12, 13, 14, 15, 16, 17, 18]
13 2 000100010111111111 11 [4, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18]
14 1 000000011111111111 11 [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
15 2 000111010111111111 13 [4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18]
16 1 000001111111111111 13 [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
17 1 000011111111111111 14 [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
18 1 001011111111111111 15 [3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
19 1 011011111111111111 16 [2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
Bdegrees [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 13, 13, 13, 13]

--- stderr ---
(empty)
```

## response 11
[reasoning summary]
**Organizing table output**

I’m thinking about how to express the table using the interval "a..b." It seems like the rows 7-11 in the formula are representing a matrix, and I could simplify things by listing all 19 matrix strings. My goal is to have a complete table that proves everything thoroughly. I should probably write Python code to compute or verify every step that can be checked. That’ll help in ensuring accuracy and clarity!

[tool call: write_scratchpad]
content:
```
from itertools import combinations
import sympy as sp

# Symbolic checks of all polynomial identities in the upper bound.
m, q, a = sp.symbols('m q a', integer=True)
i = sp.symbols('i', integer=True, positive=True)
assert sp.simplify(sp.summation(i, (i, 1, m)) + sp.summation(i, (i, 1, m-1)) - m**2) == 0
assert sp.expand(m + 2*(m-1) + 2*(m-2) + 2*(m-3)) == 7*m-12
assert sp.simplify(sp.summation(i+1, (i, 1, m)) + sp.summation(2*m+1-i, (i, m+1, 2*m)) - (m*m+2*m)) == 0
assert sp.expand((m+1) + 2*m + 2*(m-1) + 2*(m-2)) == 7*m-5
assert sp.expand(a*(a-1) - 2*(6*a-21)) == (a-6)*(a-7)
assert sp.expand((m*(m-1) - (m*m-7*m+12))/2) == 3*m-6
assert sp.expand((m*(m+1) - (m*m-5*m+6))/2) == 3*m-3
assert sp.expand((3*m-6)-(6*m-21*q)) == -3*(m-7*q+2)
assert sp.expand((3*m-3)-(6*(m+1)-21*q)) == -3*(m-7*q+3)
# Independent finite checks of gap minimization, including exhaustive
# choices of all seven zero positions for small m.
for M in range(4, 13):
    we = [min(j, 2*M-j) for j in range(1, 2*M)]
    wo = [j+1 if j <= M else 2*M+1-j for j in range(1, 2*M+1)]
    assert sum(we)-sum(sorted(we)[-7:]) == M*M-7*M+12
    assert sum(wo)-sum(sorted(wo)[-7:]) == M*M-5*M+5
    assert {j+1 for j,x in enumerate(we) if x >= M-3} == set(range(M-3, M+4))
    if M <= 9:
        assert min(sum(we)-sum(we[j] for j in Z) for Z in combinations(range(len(we)), 7)) == M*M-7*M+12
        assert min(sum(wo)-sum(wo[j] for j in Z) for Z in combinations(range(len(wo)), 7)) == M*M-5*M+5
print('Symbolic identities and finite gap-minimization checks passed.')

def interval(lo, hi):
    return set(range(lo, hi+1))

# Neighbors in B, indexed from 1.
rows = [set(), set(), set(), {9}, {7,9}, {4,7,9}]
rows += [interval(21-i,18) for i in range(7,12)]
rows += [interval(10,18), {4,8}|interval(10,18), interval(8,18),
         {4,5,6,8}|interval(10,18), interval(6,18), interval(5,18),
         {3}|interval(5,18), {2,3}|interval(5,18)]
assert len(rows) == 19
ca = [0]*6 + [2]*5 + [1,2,1,2,1,1,1,1]
cb = [0]*18
cb[3] = 1
cb[6] = cb[8] = 2

adj = [set() for _ in range(37)]
colors = ca+cb

def edge(u,v):
    assert u != v
    adj[u].add(v)
    adj[v].add(u)

for u in range(19):
    for v in range(u+1,19):
        if ca[u] != ca[v]:
            edge(u,v)
for u,row in enumerate(rows):
    for j in row:
        edge(u,19+j-1)

def verify(Q):
    n = len(adj)
    assert n == 14*Q-5
    assert len(colors) == n and set(colors) == set(range(Q))
    for u in range(n):
        assert u not in adj[u]
        for v in adj[u]:
            assert u in adj[v]
            assert colors[u] != colors[v]
    degrees = [len(S) for S in adj]
    assert set(degrees) == set(range(n-7)) # 0,...,n-8
    assert n-len(set(degrees)) == 7
    return degrees

d = verify(3)
assert d[:19] == [13]*3 + list(range(14,30))
assert d[19:] == list(range(13)) + [13]*5
print('37-vertex base verified: 3 colors, degrees 0,...,29, deficiency 7.')

for Q in range(4,31):
    n = len(adj)
    old_degrees = [len(S) for S in adj]
    # New H: n,...,n+6; new L: n+7,...,n+13.
    adj.extend(set() for _ in range(14))
    colors.extend([Q-1]*7 + [0]*7)
    for h in range(7):
        for u in range(n):
            edge(n+h,u)
        # Bipartite staircase: H row degrees 0,...,6;
        # L column degrees 6,...,0.
        for ell in range(h):
            edge(n+h,n+7+ell)
    assert [len(adj[u]) for u in range(n)] == [x+7 for x in old_degrees]
    assert [len(adj[n+h]) for h in range(7)] == list(range(n,n+7))
    assert [len(adj[n+7+ell]) for ell in range(7)] == list(range(6,-1,-1))
    verify(Q)
print('All extension constructions for q=4,...,30 verified.')

```

[tool result]
```
Wrote scratchpad.py (96 lines).
```

## response 12
[tool call: run_scratchpad]
timeout_seconds: 60

[tool result]
```
[exit code 1, 0.3s]
--- stdout ---
(empty)
--- stderr ---
Traceback (most recent call last):
  File "scratchpad.py", line 11, in <module>
    assert sp.expand(a*(a-1) - 2*(6*a-21)) == (a-6)*(a-7)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError

```

## response 13
[tool call: edit_scratchpad]
old_string: assert sp.expand(a*(a-1) - 2*(6*a-21)) == (a-6)*(a-7)
new_string: assert sp.expand(a*(a-1) - 2*(6*a-21) - (a-6)*(a-7)) == 0

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 14
[tool call: edit_scratchpad]
old_string:
```
assert sp.expand((3*m-6)-(6*m-21*q)) == -3*(m-7*q+2)
assert sp.expand((3*m-3)-(6*(m+1)-21*q)) == -3*(m-7*q+3)
```
new_string:
```
assert sp.expand((3*m-6)-(6*m-21*q) + 3*(m-7*q+2)) == 0
assert sp.expand((3*m-3)-(6*(m+1)-21*q) + 3*(m-7*q+3)) == 0
```

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 15
[tool call: run_scratchpad]
timeout_seconds: 60

[tool result]
```
[exit code 0, 0.2s]
--- stdout ---
Symbolic identities and finite gap-minimization checks passed.
37-vertex base verified: 3 colors, degrees 0,...,29, deficiency 7.
All extension constructions for q=4,...,30 verified.

--- stderr ---
(empty)
```

## response 16
[message]
\[
\boxed{M(q)=14q-5\qquad(q\ge3).}
\]

I will prove the upper bound, give constructions attaining it, and provide executable Python verifying the construction and the algebraic calculations used below.

## 1. Two degree-gap inequalities

Write the degrees of an \(n\)-vertex graph in nondecreasing order:
\[
d_1\le d_2\le\cdots\le d_n,
\qquad g_i=d_{i+1}-d_i.
\]
The condition \(n-w(G)=7\) says precisely that **seven of the gaps \(g_i\) are zero**. Every other gap is a positive integer.

### Even order

Let \(n=2m\), and put
\[
D=\sum_{i=m+1}^{2m}d_i-\sum_{i=1}^{m}d_i.
\]
Expanding in gaps gives
\[
D=\sum_{i=1}^{2m-1}\min(i,2m-i)\,g_i.
\]
The weights are
\[
1,2,\ldots,m-1,m,m-1,\ldots,2,1,
\]
whose sum is \(m^2\). To minimize \(D\), the seven zero gaps must occupy the seven largest weights, and all remaining gaps must equal \(1\). Those seven weights sum to
\[
m+2(m-1)+2(m-2)+2(m-3)=7m-12.
\]
Consequently,
\[
\boxed{D\ge m^2-7m+12.} \tag{1}
\]

Equality has a useful consequence. The seven zero gaps are exactly those with indices
\[
m-3,m-2,\ldots,m+3.
\]
Thus, for some integer \(a=d_1\ge0\), the degree multiset consists of all integers from \(a\) to \(a+2m-8\), with
\[
c=a+m-4
\]
occurring eight times instead of once. In particular, the lower half of the degree list contains vertices of degree
\[
c\ge m-4. \tag{2}
\]

### Odd order

Let \(n=2m+1\), and put
\[
L=\sum_{i=m+1}^{2m+1}d_i-\sum_{i=1}^{m}d_i.
\]
Here
\[
L=d_1+\sum_{i=1}^{2m}c_i g_i,
\qquad
c_i=
\begin{cases}
i+1,&i\le m,\\
2m+1-i,&i>m.
\end{cases}
\]
The weights have sum \(m^2+2m\). Their seven largest values sum to
\[
(m+1)+2m+2(m-1)+2(m-2)=7m-5.
\]
Therefore
\[
L\ge m^2-5m+5.
\]
But \(L\) is even: if \(A\) is the upper \(m+1\) vertices and \(B\) the lower \(m\), then
\[
L=2\bigl(e(G[A])-e(G[B])\bigr).
\]
Since \(m^2-5m+5\) is odd, this improves to
\[
\boxed{L\ge m^2-5m+6.} \tag{3}
\]

We will only need these calculations for \(m\ge4\).

## 2. The upper bound

Fix a proper coloring with \(q\) colors, allowing unused colors.

For any vertex set \(A\), let \(a_i\) be the number of its vertices of color \(i\), and let \(F_A\) be the number of nonedges within \(A\). Every same-color pair is a nonedge, so
\[
F_A\ge\sum_{i=1}^{q}\binom{a_i}{2}.
\]
For every nonnegative integer \(a\),
\[
\binom a2-(6a-21)=\frac{(a-6)(a-7)}2\ge0.
\]
Hence
\[
\boxed{F_A\ge6|A|-21q.} \tag{4}
\]
Equality requires every \(a_i\) to be \(6\) or \(7\).

Graphs of order at most \(37\) already satisfy the desired upper bound for every \(q\ge3\). Thus we may use the preceding gap inequalities without concern about small orders.

### Even order

Let \(n=2m\), with \(A\) the upper half of the degree list and \(B\) the lower half. Since
\[
D=2\bigl(e(G[A])-e(G[B])\bigr),
\]
inequality (1) gives
\[
F_A+e(G[B])
=\frac{m(m-1)-D}{2}
\le3m-6.
\]
Together with (4),
\[
6m-21q\le3m-6,
\]
and therefore
\[
m\le7q-2. \tag{5}
\]

Suppose equality held in (5). All the inequalities used must then be equalities. In particular:

* \(B\) is independent;
* every color occurs \(6\) or \(7\) times in \(A\);
* equality holds in (1).

The last point and (2) give a vertex of \(B\) of degree at least \(m-4\). But every vertex of \(B\) has no neighbors in \(B\), and misses at least the six vertices of its own color in \(A\). Its degree is therefore at most \(m-6\), a contradiction.

Thus
\[
\boxed{n\le14q-6\quad\text{when \(n\) is even}.} \tag{6}
\]

### Odd order

Let \(n=2m+1\), with \(|A|=m+1\) and \(|B|=m\), again taking the highest degrees in \(A\). By (3),
\[
F_A+e(G[B])
=\frac{m(m+1)-L}{2}
\le3m-3.
\]
Using (4),
\[
6(m+1)-21q\le3m-3,
\]
so
\[
m\le7q-3.
\]
Consequently,
\[
\boxed{n\le14q-5\quad\text{when \(n\) is odd}.} \tag{7}
\]

Equations (6) and (7) prove
\[
M(q)\le14q-5.
\]

## 3. A construction attaining the bound

### A \(37\)-vertex, \(3\)-colorable base graph

Take vertices
\[
A=\{a_1,\ldots,a_{19}\},\qquad B=\{b_1,\ldots,b_{18}\}.
\]

Partition \(A\) into three color classes:
\[
\begin{aligned}
A_0&=\{a_1,\ldots,a_6\},\\
A_1&=\{a_{12},a_{14},a_{16},a_{17},a_{18},a_{19}\},\\
A_2&=\{a_7,a_8,a_9,a_{10},a_{11},a_{13},a_{15}\}.
\end{aligned}
\]
Within \(A\), join precisely the pairs belonging to different classes. Let \(B\) be independent.

The neighbors in \(B\) of the vertices of \(A\) are specified below. An interval denotes all its integer indices.
\[
\begin{array}{c|l}
i&\{j:a_ib_j\in E\}\\ \hline
1,2,3&\varnothing\\
4&\{9\}\\
5&\{7,9\}\\
6&\{4,7,9\}\\
7\le i\le11&[21-i,18]\\
12&[10,18]\\
13&\{4,8\}\cup[10,18]\\
14&[8,18]\\
15&\{4,5,6,8\}\cup[10,18]\\
16&[6,18]\\
17&[5,18]\\
18&\{3\}\cup[5,18]\\
19&\{2,3\}\cup[5,18]
\end{array}
\]

Color \(b_4\) with color \(1\), color \(b_7,b_9\) with color \(2\), and all other vertices of \(B\) with color \(0\). The table contains no edge whose endpoints have the same color.

Directly from the table, the degrees in \(A\) are
\[
13,13,13,14,15,\ldots,29,
\]
while those in \(B\) are
\[
0,1,2,\ldots,12,13,13,13,13,13.
\]
Thus the degree set is exactly \(\{0,1,\ldots,29\}\). The graph has \(37\) vertices and \(30\) distinct degrees, as required.

### An extension adding \(14\) vertices and one color

Suppose an \(n\)-vertex graph has a proper \(q\)-coloring and degree set
\[
\{0,1,\ldots,n-8\}.
\]
Add two independent sets
\[
H=\{h_0,\ldots,h_6\},\qquad
T=\{t_0,\ldots,t_6\}.
\]
Join every vertex of \(H\) to every old vertex, and join \(h_i\) to \(t_j\) exactly when \(j<i\). Add no other edges.

Give \(H\) a new color and give all of \(T\) any one old color. This is a proper \((q+1)\)-coloring.

The degrees are:

* old vertices: their former degrees plus \(7\), giving \(7,\ldots,n-1\);
* vertices of \(H\): \(n,n+1,\ldots,n+6\);
* vertices of \(T\): \(6,5,\ldots,0\).

The new degree set is therefore
\[
\{0,1,\ldots,n+6\},
\]
and the number of vertices minus the number of distinct degrees remains \(7\).

Starting with the \(37\)-vertex base and applying this extension \(q-3\) times produces a \(q\)-colorable graph of order
\[
37+14(q-3)=14q-5.
\]
This proves the matching lower bound.

## 4. Executable verification

The following code checks the symbolic identities in the upper-bound calculation, independently checks the gap minimizations, constructs the base graph, verifies every edge and degree, and checks successive extensions. The infinite family is justified by the extension proof above, not merely by these finite tests.

```python
from itertools import combinations
import sympy as sp

# ---------- Upper-bound calculations ----------

m, q, a = sp.symbols("m q a", integer=True)
i = sp.symbols("i", integer=True, positive=True)

# Sum of even-order gap weights.
assert sp.simplify(
    sp.summation(i, (i, 1, m))
    + sp.summation(i, (i, 1, m-1)) - m**2
) == 0

assert sp.expand(
    m + 2*(m-1) + 2*(m-2) + 2*(m-3)
) == 7*m - 12

# Sum of odd-order gap weights.
assert sp.simplify(
    sp.summation(i+1, (i, 1, m))
    + sp.summation(2*m+1-i, (i, m+1, 2*m))
    - (m*m + 2*m)
) == 0

assert sp.expand(
    (m+1) + 2*m + 2*(m-1) + 2*(m-2)
) == 7*m - 5

# Integer tangent bound and subsequent algebra.
assert sp.expand(
    a*(a-1) - 2*(6*a-21) - (a-6)*(a-7)
) == 0
assert sp.expand(
    (m*(m-1) - (m*m-7*m+12))/2
) == 3*m - 6
assert sp.expand(
    (m*(m+1) - (m*m-5*m+6))/2
) == 3*m - 3
assert sp.expand(
    (3*m-6) - (6*m-21*q) + 3*(m-7*q+2)
) == 0
assert sp.expand(
    (3*m-3) - (6*(m+1)-21*q) + 3*(m-7*q+3)
) == 0

# Independently minimize by choosing the seven zero-gap positions.
for M in range(4, 13):
    even = [min(j, 2*M-j) for j in range(1, 2*M)]
    odd = [
        j+1 if j <= M else 2*M+1-j
        for j in range(1, 2*M+1)
    ]
    assert sum(even) - sum(sorted(even)[-7:]) == M*M-7*M+12
    assert sum(odd) - sum(sorted(odd)[-7:]) == M*M-5*M+5

    # Equality positions for the even-order inequality.
    assert {
        j+1 for j, weight in enumerate(even) if weight >= M-3
    } == set(range(M-3, M+4))

    if M <= 9:
        for weights, answer in [
            (even, M*M-7*M+12),
            (odd, M*M-5*M+5),
        ]:
            actual = min(
                sum(weights) - sum(weights[j] for j in zeros)
                for zeros in combinations(range(len(weights)), 7)
            )
            assert actual == answer

print("Symbolic identities and gap-minimization checks passed.")

# ---------- The 37-vertex base graph ----------

def interval(lo, hi):
    return set(range(lo, hi+1))

rows = [set(), set(), set(), {9}, {7, 9}, {4, 7, 9}]
rows += [interval(21-i, 18) for i in range(7, 12)]
rows += [
    interval(10, 18),
    {4, 8} | interval(10, 18),
    interval(8, 18),
    {4, 5, 6, 8} | interval(10, 18),
    interval(6, 18),
    interval(5, 18),
    {3} | interval(5, 18),
    {2, 3} | interval(5, 18),
]
assert len(rows) == 19

ca = [0]*6 + [2]*5 + [1, 2, 1, 2, 1, 1, 1, 1]
cb = [0]*18
cb[3] = 1
cb[6] = cb[8] = 2

adj = [set() for _ in range(37)]
colors = ca + cb

def edge(u, v):
    assert u != v
    adj[u].add(v)
    adj[v].add(u)

for u in range(19):
    for v in range(u+1, 19):
        if ca[u] != ca[v]:
            edge(u, v)

for u, row in enumerate(rows):
    for j in row:
        edge(u, 19+j-1)

def verify(Q):
    n = len(adj)
    assert n == 14*Q - 5
    assert len(colors) == n
    assert set(colors) == set(range(Q))

    for u in range(n):
        assert u not in adj[u]
        for v in adj[u]:
            assert u in adj[v]
            assert colors[u] != colors[v]

    degrees = [len(neighbors) for neighbors in adj]
    assert set(degrees) == set(range(n-7))  # 0,...,n-8
    assert n - len(set(degrees)) == 7
    return degrees

degrees = verify(3)
assert degrees[:19] == [13]*3 + list(range(14, 30))
assert degrees[19:] == list(range(13)) + [13]*5
print("37-vertex base verified.")

# ---------- Repeated extension ----------

for Q in range(4, 31):
    n = len(adj)
    old_degrees = [len(neighbors) for neighbors in adj]

    # H has indices n,...,n+6; T has indices n+7,...,n+13.
    adj.extend(set() for _ in range(14))
    colors.extend([Q-1]*7 + [0]*7)

    for h in range(7):
        for u in range(n):
            edge(n+h, u)
        for t in range(h):
            edge(n+h, n+7+t)

    assert [len(adj[u]) for u in range(n)] == [
        d+7 for d in old_degrees
    ]
    assert [len(adj[n+h]) for h in range(7)] == list(range(n, n+7))
    assert [len(adj[n+7+t]) for t in range(7)] == list(range(6, -1, -1))
    verify(Q)

print("All extensions for q=4,...,30 verified.")
```

The executed checks passed.

**Conclusion:** the supremum is attained, and \(M(q)=14q-5\) for every integer \(q\ge3\). Nothing remains unresolved.
