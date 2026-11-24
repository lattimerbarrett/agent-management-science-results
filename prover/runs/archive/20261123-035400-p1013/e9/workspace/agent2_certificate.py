import networkx as nx,itertools,json
from pathlib import Path
# Executable certificate shared with team.
Path('workspace/agent2_certificate.py').write_text(Path(__file__).read_text())
EDGES=[(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(1,4),(1,5),(1,6),(2,6),(2,7),(3,7)]
H=nx.Graph(EDGES)
def indeps(G):
 for mask in range(1<<len(G)):
  I={v for v in G if mask>>v&1}
  if not G.subgraph(I).number_of_edges(): yield I

def sub_P3union(F):
 return all(len(C)<=3 and F.subgraph(C).number_of_edges()<len(C) and max(dict(F.subgraph(C).degree()).values(),default=0)<=2 for C in nx.connected_components(F))

assert not nx.is_bipartite(H)
col={0:0,1:1,2:1,3:1,4:2,5:2,6:2,7:0}
assert all(col[u]!=col[v] for u,v in H.edges())
inds=list(indeps(H))
assert all(not sub_P3union(H.subgraph(set(H)-I)) for I in inds)
checks=[({2,3,4,5},[(0,1),(0,6),(1,6)]),({3,4,5,6},[(0,1),(0,2),(2,7)]),({4,5,6,7},[(0,1),(0,2),(0,3)])]
for I,E in checks:
 assert I in inds
 assert {frozenset(e) for e in H.subgraph(set(H)-I).edges()}=={frozenset(e) for e in E}
F=H.copy();F.remove_node(0);assert nx.is_tree(F)
A=nx.disjoint_union_all([nx.path_graph(2)]*4);J=nx.full_join(A,A,rename=('a','b'))
GM=nx.algorithms.isomorphism.GraphMatcher(J,H)
assert GM.subgraph_is_monomorphic()
A=nx.empty_graph(8);A.add_edge(0,1);J=nx.full_join(A,A,rename=('a','b'));GM1=nx.algorithms.isomorphism.GraphMatcher(J,H)
print('Single-edge in each part contains H:',GM1.subgraph_is_monomorphic())
if GM1.subgraph_is_monomorphic():print('witness',next(GM1.subgraph_monomorphisms_iter()))
maxinds=[I for I in inds if not any(I<J for J in inds)]
print('Maximal independent residuals:',[(sorted(I),sorted(H.subgraph(set(H)-I).edges())) for I in maxinds])
print('Independent deletion certificates checked:',len(inds))
print('Proper 3-coloring checked:',col)
print('H minus 0 is tree checked; matching-both-sides embedding:',next(GM.subgraph_monomorphisms_iter()))
print('Every independent deletion fails to leave a disjoint union of P3 subgraphs: checked.')
# The last assertion proves every complete join (disjoint P3 union) JOIN independent is H-free, for all sizes.
from fractions import Fraction
for n in range(1,1001):
 t=n*n//4
 M=max(a*(n-a)+(2*a)//3 for a in range(n+1))
 assert M<=Fraction(t)+Fraction(n,3)+1
 if n%6==0:
  m=n//6
  assert M==9*m*m+2*m
  assert [a for a in range(n+1) if a*(n-a)+(2*a)//3==M]==[3*m]
print('Template edge optimization checked for n=1,...,1000.')
Path('workspace/agent2_r2_proof.md').write_text(r'''# Complete r=2 positive endpoint: edge/structure portion

Let H have vertices 0,...,7 and edges
01,02,03,04,05,06,14,15,16,26,27,37.
It is 3-chromatic (triangle 016, and coloring classes {0,7},{1,2,3},{4,5,6}).
Let P mean any disjoint union of P1,P2,P3. Every P join I is H-free:
the six maximal independent sets of H are
{1,2,3}, {2,3,4,5}, {3,4,5,6}, {0,7}, {1,7}, {4,5,6,7}.
Deleting these leaves a claw, triangle, P4, claw, claw, claw, respectively.
Thus deleting any independent set never leaves a subgraph of P.

Three explicit residual witnesses are:
H-{4,5,6,7}=claw 0-{1,2,3};
H-{3,4,5,6}=P4 1-0-2-7;
H-{2,3,4,5}=triangle 016 plus isolated 7.
Also H-0 is a tree. Finally the partition {0,1,7}|{2,3,4,5,6}
has just one internal edge in each part (01 and 26).

## Structural lemma
For every fixed D>=0, all sufficiently large H-free graphs G with
minimum degree at least n/2-D and e(G)>=t2(n)+n/3-O(1)
are subgraphs of P join I, with all their internal edges retained.
Here the constant in O(1) is fixed independently of n.

Proof. Erdos-Simonovits stability applies since minimum degree gives
e(G)>=t2(n)-O(n), and H has chromatic number 3. Take a maximum cut A|B.
It is balanced to within o(n), has o(n^2) internal edges and misses o(n^2)
cross edges. We first show maximum internal degree is o(n).
For fixed eta>0, all but o(n) vertices miss at most eta*n/(2|H|)
cross edges. If v has at least eta*n internal neighbors, maximality of
the cut gives it at least eta*n cross neighbors too. Embed the bipartite
tree H-0 into its neighbors, its two classes on opposite sides, avoiding
the exceptional o(n) vertices. Greedily, each choice has at least
eta*n-o(n)-|H|*eta*n/(2|H|)>0 possibilities. This embeds even the full
cone over H-0, hence H, contradiction. Since eta was arbitrary, every
vertex has internal degree o(n), and consequently cross degree n/2-o(n).
Every vertex therefore misses o(n) cross edges, uniformly.

The three residual witnesses above now forbid an internal claw, P4,
or triangle: choose the extra same-side isolated vertex if needed and
then the remaining four independent-side vertices in successive common
cross neighborhoods, each of size n/2-o(n). Thus every internal component
is P1,P2,P3. If a=|A|, b=|B|, minimum degree gives
b+2,a+2>=n/2-D. Hence a,b=n/2+O_D(1) and each vertex misses at most
2D+4 cross neighbors.

There are at least n/3-O(1) internal edges in total because cross edges
are at most t2(n). Thus one side, say A, has linearly many vertex-disjoint
internal edges. If yz is an edge of B, choose an internal edge ux of A
such that all four edges between {u,x} and {y,z} are present; bounded
cross defects make this possible. Map 0,1,2,6 to u,x,y,z. Choose 7 in
A adjacent to y, then 3 in B adjacent to u and 7, then 4,5 in B adjacent
to u,x, always choosing distinct vertices. Again bounded cross defects
make these choices possible. This embeds H. Therefore B is independent,
proving the lemma.

## Linear upper bound by induction
There exists C such that ex(n,H)<=f(n):=t2(n)+n/3+C for all n.
Choose N so the structural lemma with D=0 and edge hypothesis e>=t2+n/3
holds for n>N. Choose C>=2 covering all n<=N. Induct. If an H-free graph
has e>f(n), deletion of any vertex and induction give
d(v)>f(n)-f(n-1)=floor(n/2)+1/3>=n/2-1/6,
so its integral degree is at least n/2. Apply the structural lemma.
Its edge count is at most
max_a [a(n-a)+floor(2a/3)] <= t2(n)+n/3+1,
contradiction. The final inequality follows by completing the square:
a(n-a)+2a/3=n^2/4+n/3+1/9-(a-n/2-1/3)^2.

## All large edge-extremizers have the asserted exact form
The construction P join I gives ex(n,H)>=t2(n)+n/3-2.
Consequently, for every vertex of an edge-extremizer,
d(v)>=ex(n,H)-ex(n-1,H)>=n/2-C-3.
The structural lemma applies with fixed D=C+3, so it lies inside P join I.
Completing all missing cross edges remains H-free, by the independent-
deletion certificate. Extremality therefore forces all cross edges.

At n=6m write |P|=3m+s. Then
 e <= 9m^2+2m-s^2+floor(2s/3).
The last two terms are <=0, with equality only at s=0. Equality in the
internal bound 3e(P)<=2|P| then forces exactly m disjoint P3 components.
Thus the unique large edge-extremizer is A_m=(m P3) join I_(3m).

The competitor B_m=((m-1)P3 disjoint-union 2P2) join I_(3m-1) is H-free
and has one fewer edge. Agent4's exact cycle polynomial argument proves
c(B_m)>c(A_m) for every sufficiently large m. Therefore H proves
[1/3,infinity) is contained in S_2.
''')
