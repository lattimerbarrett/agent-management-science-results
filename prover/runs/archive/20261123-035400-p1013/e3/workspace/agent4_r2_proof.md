# r=2 endpoint, conditional only on standard Simonovits edge decomposition theorem

Let H be the 8-vertex graph in agent4_H8.json. Its independent-set deletion
minimal family is exactly {K3,K1,3,P4}; exhaustive verifier agent4_h8_verify.py.
Moreover H has a vertex v whose deletion is bipartite, and admits a two-part
coloring with one induced edge in each color class.

Use the standard bounded-block edge decomposition theorem in this precise
form: if chi(H)=r+1 and H embeds into P_l join T_{(r-1)l,r-1}, all sufficiently
large edge-extremal H-free graphs admit deletion of O_H(1) vertices leaving
a complete join of r classes of order n/r+O_H(1), each a disjoint union of
connected blocks of bounded order. (The usual theorem also gives symmetry
of blocks, which is unnecessary below.)

For r=2, each core class has no K3,claw,P4, since any such occurrence extends
to H using the other core class. Thus it is a disjoint union of paths of
order<=3. Both core classes cannot contain an edge: the two-edge coloring
of H extends greedily across the complete join. Hence only one core class
is nontrivial.

Each exceptional x has <=D_H neighbors in some core class. Otherwise H
embeds with its critical vertex mapped to x and H-v bipartitely into the
core, since H-v is fixed. Assign x to such a sparse class. This yields a
partition into two parts of size n/2+O(1), bounded internal exceptional
degree and total O(n) core edges. Consequently e(G)<=t2(n)+n/3+O(1):
core internal edges <=2/3 times the active class order; exceptional internal
edges O(1), exceptional cross edges at most the complete-bipartite bound.
The matching lower bound comes from balanced complete joins with a maximum
P3 forest in one class.

Therefore for any edge-extremal G and any vertex x,
deg(x)>=ex(n,H)-ex(n-1,H)>=n/2-O(1).
For exceptional x assigned above, this implies only O(1) missing cross
neighbors. Core vertices have at most O(1) missing cross neighbors too
(the only possible missing neighbors are exceptional).

Now any internal K3,claw,P4, even involving exceptional vertices, extends
to H by selecting the boundedly many other-color vertices in a common
cross neighborhood. Thus both full partition classes are P3 forests.
If both have an edge, use the fixed two-edge coloring of H: choose those
edges, then greedily add all remaining vertices, avoiding the O(1) cross
nonneighbors of previously chosen vertices. The edges themselves must be
cross-complete to one another; choose the edge in the active abundant core
class to avoid cross defects of endpoints of the other edge. There are
Omega(n) such edges, since edge extremality and the n/3 lower bound force
Omega(n) internal edges. This embeds H, contradiction.

Hence one full class is independent and the other a P3 forest. Completing
all cross edges remains H-free, by the exact deletion family; extremality
forces all cross edges present.

For n=6k the maximum edge objective is uniquely at |A|=3k, with A=kP3:
for |A|=3k+t,
e(G)-[9k^2+2k] <= -t^2+t-ceil(t/3), strictly negative for all t!=0.
At t=0 equality forces k disjoint P3s. Thus all edge-extremizers have the
same cycle count.

The alternate H-free graph is |A|=3k+1, |B|=3k-1, A=kP3+one isolated.
Agent1 proved its cycle ratio over the edge-extremizer converges to a
number >1, with positive rational series certificate 16715/46656.
This proves infinitely many n have no common extremizer and the endpoint
upper bound ex(n,H)<=t2(n)+n/3+O(1), conditional on the quoted standard edge
decomposition theorem.
