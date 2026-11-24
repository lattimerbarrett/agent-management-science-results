# Exact cubic resistance diameter
Let G be a connected simple cubic graph of even order n>=10. Its maximum effective resistance is at most n/2-9/4 for n=2 mod4, and at most n/2-11/4 for n=0 mod4. Both are attained.

Delete all bridges. The resulting components (bridge-blocks) form a tree when contracted. Each non-singleton component B is bridgeless and has maximum degree 3, and is consequently 2-vertex-connected: a cut vertex in a bridgeless component would need at least two edges into each of at least two components. Thus any a,b in B lie on a simple cycle of length <=b=|B|. Sending current along the two arcs gives R_B(a,b)<=b/4. A component with h incident bridges has h distinct degree-2 vertices (the ports); the remaining vertices have degree3.

Every component of G separated by deleting just one bridge has at least5 vertices. Indeed, if its order is s its internal degree sum is 3s-1, whence s odd, and simplicity rules out s=1,3.

Fix vertices x,y. If they lie in the same bridge-block, their resistance is at most n/4, which is no larger than the asserted bound (check n>=10 and its two residues). Otherwise let B_1,...,B_l be the bridge-block path between them, l>=2. Resistance is the sum of its l-1 bridges and the internal two-terminal resistances R_i; all off-path branches carry zero current. Put r_i=1 for end blocks, 2 for internal blocks, h_i equal to the number of incident bridges. Assign to B_i all vertices of the off-path branches attached to it and write w_i for its augmented order. These sets partition V(G), so sum w_i=n, and w_i>=b_i+5(h_i-r_i).

Define D_i=w_i/2-1-R_i. Then R_G(x,y)=n/2-1-sum D_i. The following bounds prove the claim:
* Each end block has D_i>=5/8. Equality can occur only for b=5,h=1,w=5; any end block not of this form has D_i>=9/8.
* Each internal block has D_i>=0. Any internal block other than b=4,h=2,w=4 has D_i>=1/2.

Verification: for a nontrivial block with at least one off-path branch, b>=3 and the cycle bound gives D>=b/4+5(h-r)/2-1>=9/4. A singleton block has h=3 and R=0; for an end its w>=11 and D>=9/2, and for an internal block w>=6 and D>=2. A branchless end block has h=1, b odd and b>=5. For b=5, exact rooted enumeration gives R<=7/8, hence D>=5/8. For b=7 the enumeration gives R<=11/8, hence D>=9/8. For b>=9, the cycle bound gives D>=b/4-1>=5/4. A branchless internal block has h=2 and b even >=4, so D>=b/4-1, yielding 0 at4 and >=1/2 at6 or more.

The only finite enumeration used above is reproduced completely in check_even_terminals.py: fix root0's neighbors1,2 by relabeling, enumerate every subset of the remaining possible edges, test the required degree sequence and bridgelessness, and invert the reduced integer Laplacian exactly over Q. Order5 has 1 labeling and max7/8; order7 has54 labelings and max11/8. Thus no graph is omitted.

We have sum D>=5/4 always, yielding n/2-9/4. If no exceptional block occurs then n=5+5+4(l-2)=2 mod4. For n=0 mod4 some block is exceptional and sum D>=7/4, proving n/2-11/4.

For attainment, take two one-port end caps and k diamond blocks K4 minus an edge, joining successive ports by single bridges. Cap5 has edge set 01,02,13,14,23,24,34, port0 and distinguished vertex3, with R(0,3)=7/8. Cap7 has edge set 01,02,12,13,24,35,36,45,46,56, port0 and distinguished vertex5, with R(0,5)=11/8. Diamond ports are its two nonadjacent degree2 vertices, with resistance1. All other vertices have degree3 after joining, so the graph is simple connected cubic. Two cap5's give n=10+4k and resistance 2(7/8)+k+(k+1)=n/2-9/4. Cap5 plus cap7 give n=12+4k and resistance 7/8+11/8+k+(k+1)=n/2-11/4. Multiplication by 3n gives exactly the even-n formula for the cubic subclass, by the commute-time/effective-resistance identity.
