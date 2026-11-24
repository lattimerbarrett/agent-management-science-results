import networkx as nx,z3,json,sys
sys.path.insert(0,'workspace');from agent3_packing_host import packing_embedding
Fs=nx.Graph([(0,6),(0,9),(0,11),(1,6),(1,11),(2,7),(2,8),(2,9),(2,10),(3,5),(3,6),(3,11),(4,5),(4,11),(6,11),(7,11),(8,11),(9,11),(10,11)])
Fp=nx.Graph(json.load(open('workspace/agent3_allcycle_p4_counter.json'))['edges'])
assert len(Fs)==12 and len(Fp)==20
assert nx.is_bipartite(Fs.subgraph(set(Fs)-{11})) and nx.is_bipartite(Fp.subgraph(set(Fp)-{0}))
assert not nx.is_bipartite(Fs) and not nx.is_bipartite(Fp)
assert packing_embedding(Fs,nx.star_graph(3)) is None
assert packing_embedding(Fp,nx.path_graph(4)) is None
for T in [nx.path_graph(4),nx.star_graph(4),nx.cycle_graph(3)]:assert packing_embedding(Fs,T) is not None
for T in [nx.path_graph(5),nx.star_graph(3),nx.cycle_graph(3),nx.cycle_graph(4)]:assert packing_embedding(Fp,T) is not None
for T in nx.nonisomorphic_trees(5):
 assert packing_embedding(Fs,T) is not None and packing_embedding(Fp,T) is not None
for F in [Fs,Fp]:
 x={v:z3.Bool('x'+str(v)) for v in F};s=z3.Solver()
 for v in F:s.add(z3.PbLe([(x[w]==x[v],1) for w in F[v]],1))
 assert s.check()==z3.sat
F=nx.disjoint_union_all([Fs,Fs,Fp,Fp]);H=F.copy();H.add_node(64);H.add_edges_from((64,v) for v in range(64));assert len(H)==65
open('workspace/agent4_cone_union_graph.json','w').write(json.dumps(dict(edges=list(H.edges()),n=65)))
text=r'''# Actual counterexample to the unique-max-tree closure (r=3)

Let S be agent3's 12-vertex graph in Slack #190 (the edge list is in the
accompanying executed script), and P the 20-vertex graph in
agent3_allcycle_p4_counter.json. Certified properties:

* S has chromatic number 3 and a critical vertex. It embeds in the one-part
  P4-packing, K1,4-packing and C3-packing hosts, but NOT the claw-packing host.
  Consequently the connected trees T for which the T-packing host is S-free
  are exactly the subtrees of the 4-vertex claw.
* P has chromatic number 3 and a critical vertex. It embeds in the one-part
  claw-packing, P5-packing, C3-packing and C4-packing hosts, but NOT the
  P4-packing host. Its allowed connected trees are exactly the subtrees of P4.
* BOTH S and P embed in a complete bipartite graph with matchings in BOTH
  parts. This is checked directly by Boolean colors with at most one
  monochromatic neighbor at every vertex.

Let F=2S disjoint-union 2P and H=K1 join F. H has 65 vertices and chromatic
number 4, and the outer cone vertex is critical. Every proper 3-coloring of
F has at least four vertices in EACH color, because F has four disjoint
3-chromatic components. Conversely its minimum color-class size is four,
since each component has a critical vertex.

Consider a complete tripartite graph with arbitrarily many copies of a tree
T inside ONE part A. If the outer vertex of H is placed in a clean part,
its neighborhood is the complete bipartite T-packing host. Thus H embeds
there precisely when both S and P embed there. If the outer vertex is placed
at an internal vertex x of A, its neighborhood is complete tripartite with
part sizes deg_T(x), b, c; the first part is independent because T is a tree.
It cannot contain F if deg_T(x)<4.

Therefore BOTH the 4-vertex path and 4-vertex claw packing hosts are H-free.
EVERY tree on at least five vertices yields H: it contains a 5-vertex tree,
and each of the three 5-vertex tree types contains the certified obstruction
for S and the certified obstruction for P. Copies of S,P can use distinct
copies of T. Every cycle-packing host also contains H: use the C3/C4
certificates for short cycles and P4/P5 for longer cycles.

In particular this is a genuine single critical forbidden graph for which
there are TWO incomparable largest allowed trees of the SAME order, with
DIFFERENT wedge counts, even though all cycle-packing hosts contain H.
The proposed rooted/tree principal-ideal closure is FALSE for r>=3.

Moreover two linearly active internal parts already give H: choose the outer
vertex in the third part and use the both-matching embeddings of S,P.
The standard Simonovits edge decomposition consequently gives linear excess
n/4+O(1), not n/3. This last sentence invokes that genuine classical edge
structure theorem; it is not needed just to refute the combinatorial closure.

This does NOT itself separate edge and cycle extremizers: the shape penalty
at order four is too small. It establishes that the general sharp-threshold
proof must genuinely control/realize different maximal tree phases.
'''
open('workspace/agent4_cone_union_lemma.md','w').write(text)
open('workspace/agent4_cone_union_checks.py','w').write(open(__file__).read())
print('All cone-union base assertions pass; constructed H65.')
