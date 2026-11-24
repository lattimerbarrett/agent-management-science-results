# Equal-density, sharply different wedge pairs
For odd k>=3 put D=2(k-1)^2 and let F be D internally vertex-disjoint paths of length k with common endpoints.
Then v=2k(k^2-3k+3), e=2k(k-1)^2 and rho=e/v=(k-1)^2/(k^2-3k+3), decreasing to 1.
Its wedge count W(F)=sum binom(d,2)=D(D+k-2), so W(F)/v~2k.
It is strictly balanced: prune degree-one vertices from a candidate density>1 subgraph; what remains consists of t whole endpoint-to-endpoint paths. Its density tk/[t(k-1)+2] is strictly increasing in t, so only t=D maximizes it.

Construct a connected (2k-2)-regular core C on 4k vertices as follows. In each of two copies of K_{2k}, remove a perfect matching, choose a remaining edge ab, remove both chosen edges, and cross-connect the corresponding endpoints. C remains regular and connected, with a two-edge cut separating the copies. Subdivide every core edge to length k-1 to produce F'. Since k-1 is even, F' is bipartite. Direct counting gives |F'|=2v and e(F')=2e.

A connected regular graph C is strictly balanced: any proper vertex subset has average degree strictly less than its regular degree (by connectivity), and deleting edges also strictly reduces density. Uniform subdivision preserves strict balance for density>1, since after pruning leaves any candidate subgraph is the subdivision of a core subgraph and its edge/vertex ratio is x*ell/[1+(ell-1)*x], a strictly increasing function of the core edge/vertex ratio x. Hence F' is strictly balanced.

Its wedge density is W(F')/(2v)=[(2k-2)(2k-3)/2+(k-2)(k-1)]/[1+(k-2)(k-1)], tending to 3, unlike F's unbounded wedge density.

Cut a central edge from each of the two subdivided cross-connecting paths, allocating floor((k-2)/2) internal vertices on one path and ceil((k-2)/2) on the other to the first half. The halves G,G' are isomorphic by swapping chosen-edge endpoints. Each has v vertices and e-1 edges. Thus F' is two copies of G joined by two edges.

This is a FINITE COMPONENT construction only; it does not by itself prove a global H-free extremal characterization. The missing global structural argument must not be claimed as proved.
