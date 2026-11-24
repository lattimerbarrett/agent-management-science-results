from pathlib import Path
from math import comb
from fractions import Fraction as F
N=10000;N0=10**8
assert F(N,2)-40*100-40==960
assert 7*(N0-N)>comb(N,2)
text=r'''# Elementary replacement for stability in the counterexample

Use H with edges 04,07,08,17,18,27,28,34,35,48,58,78. H-8 is a tree T on seven vertices. Hence every neighborhood of an H-free graph is T-free. A T-free graph is 5-degenerate (minimum degree 6 greedily embeds every 7-vertex tree), so e(G[N(v)]) <= 5 d(v).

Fix n>=10000 and minimum degree >= n/2-10. For d=d(v), counting degrees within N(v) gives
 d(d-n/2-10) <= 2e(N(v)) <= 10d,
so maximum degree <=n/2+20. For an arbitrary vertex v, let A=N(v), a=|A|. Its cut has at least
 a(n/2-10)-2e(A) >= a(n/2-20) >= (n/2-10)(n/2-20) >= n^2/4-15n
edges. Therefore a maximum cut has at most 15n missing cross-edges, and its parts have sizes n/2 +/- 4sqrt(n).

If a vertex has t internal neighbors, maximum-cut optimality gives at least t cross-neighbors. At least t^2-15n edges occur between these two sets within N(v). The neighborhood edge bound gives t^2<=20n. Thus internal degree <=5sqrt(n), and every vertex misses <=9sqrt(n)+10 cross-neighbors. Every four same-part vertices consequently have at least
 n/2-40sqrt(n)-40 >= 960
common opposite neighbors. This last inequality holds for all n>=10000 since on writing sqrt(n)=100+y the expression is 960+60y+y^2/2.

H has independent-set deletions leaving respectively a claw, P4, and triangle plus an isolated vertex. Each such four-vertex internal configuration therefore embeds H, using four common opposite neighbors. Thus both internal graphs consist of P3, P2, and isolates. Minimum degree now gives part imbalance <=12 and at most24 missing cross-neighbors per vertex.

If e>=f(n)=max_a[a(n-a)+floor(2a/3)], then at least one part has >n/6-1 internal edges, hence >96. If the other part has edge xy, delete from the first part the at most48 vertices nonadjacent to x or y; at most96 internal edges are incident with them. An internal edge uv remains. Map7,8,0,4 to u,v,x,y. Choose3=w in the first part adjacent to y, and1,2,5 as three distinct common opposite neighbors of u,v,w. This embeds all twelve edges of H. Hence the other part is independent, and e<=f(n), with equality forcing the full cross graph.

The elementary f bounds t2(n)+n/3-1 <= f(n) <= t2(n)+n/3+1 imply f(n)-f(n-1)>n/2-3. Starting with a graph above f(n), delete vertices of degree <n/2-10. Its defect above f increases by >7 per deletion. It cannot stop at order >=10000 by the preceding local result, and for initial n>=10^8 cannot reach order10000, since 7(10^8-10000)>binom(10000,2). Thus ex(n,H)=f(n) for every n>=10^8.

At n=6k, f is uniquely maximized by a=3k, and equality forces a P3-factor in that part. The exact cycle comparison in agent1_counterexample.py and agent2_counterexample_proof.md establishes that the H-free graph with parts3k+1,3k-1 and k P3's plus an isolate in the larger part has strictly more cycles for all sufficiently large k. Therefore 1/3 belongs to S2.
'''
Path('workspace/agent1_elementary_counterexample.md').write_text(text)
print('Elementary proof saved; all explicit threshold checks passed.')
