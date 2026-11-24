import networkx as nx,itertools
for n in range(7,15):
 for j in range(2,n-1):
  for k in range(2,n-1):
   if abs(j-k)<=1:continue
   G=nx.cycle_graph(n)
   G.remove_edges_from([(0,1),(j,j+1),(k,k+1)])
   add=[(0,j),(j+1,k+1),(k,1)] if j<k else [(0,j),(j+1,k),(k+1,1)]
   G.add_edges_from(add)
   assert nx.is_connected(G) and all(d==2 for _,d in G.degree()),(n,j,k)
print('All 3-switch reconnection cases n7..14 passed')
text=r'''# Deterministic 3-switch for a low-degree exceptional vertex, r>=3

Let x-u be an edge of an oriented long cycle C, with u in regular part A.
Choose another edge w-v, where w is in a part B to which x will acquire
new edges. Assume u,v,w and the subsequently chosen z,t are regular.
Write x-u as the first edge in the linear ordering around C.

For each candidate cut z-t not adjacent to these edges:
* if w-v precedes z-t, delete x-u,w-v,z-t and add x-w,v-t,z-u;
* if z-t precedes w-v, delete x-u,w-v,z-t and add x-w,v-z,t-u.
Both reconnections give ONE cycle of the same length (verified exhaustively
for every pair of cut positions on cycles of lengths 7 through 14).

Put Cpart=part(v). In the first ordering the added old-vertex edges exist
except for o(n) choices provided z is outside A and t outside Cpart.
In the second ordering it suffices that t is outside A and z outside Cpart.
For every vertex part P, on every interval of an oriented cycle,
    #edges with source in P - #edges with target in P
has absolute value at most one (the difference telescopes).
Consequently across BOTH ordering regions the total number of forbidden cuts
from A is at most |A intersect V(C)|+1, and from Cpart at most
|Cpart intersect V(C)|+1. Thus at least
    |C| - |A intersect C| - |Cpart intersect C| - o(n) - O(1)
choices work. If all parts have size n/r+o(n), and |C|>(1-epsilon)n,
this is at least (1-2/r-epsilon-o(1))*n, positive for r>=3.

If x acquires Omega(n) neighbors in B, each old long cycle with a specified
edge x-u has Omega(n^2) switched images. If u is restricted to a set S,
a resulting cycle has at most O(|S| n) inverse switch descriptions:
the new neighbor w of x determines the first cut, choose old u in S, and
choose the remaining cut location. Thus cycles lost by deleting x-S can be
charged to gained cycles with factor O(|S|/n), provided x's other incident
cycle edge remains in the final graph. If both incident edges lie in S,
compose two switches; the charge becomes O((|S|/n)^2).

This is a rigorous long-cycle comparison tool, NOT by itself a complete
cycle-structure theorem. Additional required ingredients are an explicit
comparison handling short cycles and the periodic r=2 case, and the
structural bootstrap that puts every exceptional vertex in this setting.
'''
open('workspace/agent4_switch_lemma.md','w').write(text)
open('workspace/agent4_switch_check.py','w').write(open(__file__).read())
