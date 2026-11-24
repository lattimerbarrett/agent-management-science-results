# Maximum commute time of regular graphs: complete proof

Write R_G(x,y) for effective resistance when every edge has resistance1. We use tau(G)=max_{x,y}(E_x T_y+E_y T_x).

## Electrical preliminaries
Let L be the combinatorial Laplacian and b_xy=e_x-e_y. The unit electrical flow has vertex potential L^+b_xy, and R_xy=b_xy^T L^+b_xy. For any other unit flow, subtracting this gradient gives a divergence-zero flow, orthogonal to every gradient. Consequently its energy is R_xy plus a nonnegative squared norm (Thomson's principle). A rational transshipment with capacities exists exactly when the absolute demand in every vertex subset is at most its boundary capacity: add a super-source and super-sink and apply the max-flow/min-cut theorem. Clearing denominators gives integral flows.

For h_y(x)=E_x T_y, the random-walk equations give Lh_y(x)=deg(x) for x!=y, and Lh_y(y)=deg(y)-2m. Therefore L(h_y-h_x)=2m(e_x-e_y). Taking its potential difference between x,y proves E_x T_y+E_y T_x=2mR_xy. In a d-regular graph this is dnR_xy.

Foster's identity is sum_edges R_e=tr(L^+L)=n-1. Resistance is a metric: if p is the unit x-to-y potential with p_y=0, then R_xy+R_yz-R_xz=2p_z>=0 by the maximum principle. Contracting all vertices other than adjacent x,y and using degrees at most d gives R_xy>=2/(d+1). Two internally vertex-disjoint paths lie on a cycle of length c; currents along its two arcs give R_xy<=c/4. Resistances add across articulation points and bridges, while off-path attached components carry zero current. Every cut of an even-degree graph has even cardinality.

## Coverage of all graphs
Degree1 cannot occur in a connected graph of the allowed orders. Degree2 and d>=n/2 satisfy tau<=n^2/2, proved in the last chapter.

For even n: cubic graphs have the exact claimed maximum (Chapter1). Degree4 is covered by Chapters2-3: if an articulation separates x,y, R_xy<=n/4-23/20; otherwise R_xy<=max(n/8,3n/16-31/40). Both are strictly smaller than the cubic targets after multiplying by4n. Degree5 is excluded in Chapter4, degree6 in Chapter5, and every d>=7 in Chapter6. Thus every even order is completely covered.

For odd n the common degree is even. Degree4 is sharp, proved in Chapters2-3 and constructed in Chapter12. Degree6 is excluded in Chapter7, degree8 in Chapters8-10, and every even degree d>=10 in Chapter11. Thus every odd order is completely covered.

## Exact finite local4 table
For two-connected networks on b vertices, let C_b be the largest resistance from the unique degree2 port when all other vertices have degree4; let M_b be the largest resistance between the two degree2 ports when all other vertices have degree4. The exact exhaustive table is:

|b|6|7|8|9|10|11|12|13|
|---|---|---|---|---|---|---|---|---|
|C_b|4/5|104/115|36/35|52/45|31/20|91/55|9/5|343/180|
|M_b|5/4|4/3|3/2|19/12|2|25/12|9/4|7/3|

Every entry is recomputed by RUN_ALL.py. The strong all-order local bounds in Chapter2 imply C_b<=3b/16-13/40 and M_b<=(3b+2)/16. Thus b>=14 contributes cap defect >=6/5 or middle defect >=1/2, enough to exclude it from the residue optimization. Chapter3 gives the exact five-state min-plus computation, with defects (7/5,23/20,149/115,7/5,139/90) for n modulo5=0,1,2,3,4.

## Degree-four reduction at even orders
The four-regular analysis also bounds every pair, without assuming odd n, by R<=n/4-23/20 when a separating articulation exists, and by R<=max(n/8,3n/16-31/40) otherwise. These bounds are proved in Chapter3 before the odd-order residue optimization. Multiplying by4, each is strictly below 3n/2-33/4 for n>=10: the three comparisons reduce respectively to n/2>73/20, n>33/4, and3n/4>103/20. Thus degree4 cannot exceed either even-order cubic target. Together with Chapters4,5,6, this covers EVERY degree at even orders.

## Small editorial clarifications
When assigning off-path subtrees in the block-path arguments, an off-path subtree at an articulation shared by two path blocks may be assigned to either. The excess deficit at that articulation is precisely the number of edges entering off-path subtrees, not twice that number. A block of order at most d has at least one deficient vertex other than its at most two path articulation vertices; its own off-path subtree guarantees its assigned order at least d+1. These observations justify the counting in Chapter11.

At a terminal atom with coincident incoming incidences at the target, the internal current is zero; its order is at least6 in the four-regular argument, so all claimed positive-discount bounds remain valid. In all other coincidence cases the stated maximum-cut refinement conditions or the explicitly included finite cases apply.

The chapters below include all-order arguments, exact finite exceptions, the degree reductions, and explicit extremal constructions. Arithmetic checks use exact rational numbers throughout.


---

# Chapter 1: even_cubic_proof.md

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


---

# Chapter 2: maximal_2cut_chain_agent4.md

# Maximal nested two-cut chain proof: internal local bound
Let H be a simple 2-vertex-connected graph on B vertices; s,t have degree 2 and all other vertices degree4. We prove R(s,t)<=(3B+2)/16.

Choose a maximal nested chain {s}=S_0 < S_1 < ... < S_k=V\{t} of s,t-separating cuts of size2. The layers A_i=S_i\S_(i-1) are nonempty. Edges joining different layers or an endpoint are called outside edges. At a layer A, let p be the number of edges entering it from earlier layers. Exactly p leave to later layers; p=1 or2, because the two bounding cuts have size2 and an edge bypassing A belongs to both; p=0 would disconnect A. Thus the total number h of outside-edge incidences is2p in{2,4}.

For U subset A put sigma(U)=number of entering-edge incidences at U minus leaving-edge incidences at U. The cut S_(i-1) union U has size 2+|delta_A(U)|-sigma(U). If sigma(U)>0, connectedness, even cut parity, and maximality imply |delta_A(U)|>=sigma(U)+2: otherwise this cut has size0 (impossible) or2 (a strict refinement). Apply the same reasoning to A\U for negative sigma. Hence for every U with sigma nonzero, |delta_A(U)|>=|sigma(U)|+2>=2|sigma(U)|, since |sigma|<=2.

Put current1/2 on every outside edge, oriented from earlier to later layers. Inside A this imposes vertex injections sigma(v)/2. The capacitated transshipment cut criterion, with every internal edge capacity1/4, is exactly |sigma(U)|/2 <= |delta_A(U)|/4, verified above. Thus a feasible flow exists with each internal current of absolute value<=1/4. Its energy is at most m_A/16=(2|A|-h/2)/16.

The number E_out of outside edges satisfies 2E_out=4+sum_A h_A; the4 accounts for edges incident to s,t. Therefore outside-edge energy E_out/4=1/2+sum_A h_A/8. Layer A has total charged cost at most |A|/8+3h/32. For h2, simple degree counting gives m=2|A|-1<=|A|(|A|-1)/2, hence |A|>=5 and its cost<=3|A|/16. For h4, the same count gives either |A|=1 or |A|>=4. A singleton with two entering and two leaving edges separates s,t when deleted (no bypassedge), contradicting 2-vertex-connectivity. If |A|>=6 the bound |A|/8+3/8<=3|A|/16 holds. Cases4,5 are checked exactly by workspace/check_chain_small_atoms_agent4.py: respectively maximum prescribed-current energy1/4,1/3, giving charged costs3/4,5/6, both <=3|A|/16. The checker enumerates every simple graph with m=2b-2 edges and each possible distribution of its degree deficits into two entering and two leaving incidences; it rejects only those violating the rigorously necessary cut condition above.

Summing gives R<=1/2+sum3|A|/16=1/2+3(B-2)/16=(3B+2)/16 by Thomson's principle. All flow interfaces match because every outside edge was assigned exactly1/2.

# Cap local bound
Let s have degree2, every other vertex degree4, and assume two-vertex-connectivity. Fix target t distinct from s. Then R(s,t)<=3B/16-13/40.

Choose a maximal nested chain of size-two st cuts beginning with {s}, ending at the inclusion-maximal such cut. Ordinary layers are handled exactly as above. The final tail A contains t and has exactly two incoming external-edge incidences and none outgoing. Its size a is at least5 because its internal edges number2a-1 and the graph is simple. Give every external edge current1/2. The tail injections are +1/2 at each incoming port and -1 at t (combine if coincident). For U not containing t, write l(U) for incoming incidences at U; maximality implies internalcut(U)>=l(U)+2 if l(U)>0; complement handles subsets containing t. Thus quarter-capacity transshipment is feasible, giving tail energy <=(2a-1)/16. If a>=10 this is <=3a/16-51/80. For a5..9 the sharper same bound is verified exhaustively by workspace/check_cap_uniform_tail.py: uniform injection energy maxima3/10,73/180,37/70,59/90,21/20. To see this enumerates every tail, attach new root s by one edge to each of its two distinct deficient-degree-three ports, obtaining a cap on a+1 vertices. If both incoming incidences coincided at one vertex, its deficit is2; then if that vertex is not t, choosing it alone gives a size-two cut strictly extending the maximal chain. If it is t, two-vertex-connectivity forces the whole tail to consist of that vertex, since deleting t would otherwise disconnect the tail remainder from s. The singleton tail cannot have degree4 with only2external incidences in a simple graph. Thus the two ports are distinct, so the checker applies.

The outside-edge count is now 2E_out=2+sum_ordinary h+2 (the first2 is degree of s and final2 is tail incidences). Charging h/8 to each ordinary layer and1/4 to tail leaves sourcecharge1/4. Therefore R <=1/4+3(B-1-a)/16+1/4+(3a/16-51/80) =3B/16-13/40.


---

# Chapter 3: odd4_upper_agent1.md

# Sharp upper bound for every connected 4-regular graph of odd order n>=15
Use the local lemmas proved in maximal_2cut_chain_agent4.md and the exact finite checks local4_exact*.json.
Notation: B is a two-connected block's number of vertices. For a one-port block (port degree2, others4), put epsilon=B/4-max_v R(port,v). For a two-port block (both ports degree2, others4), put delta=(B-1)/4-R(ports).
For B=6,...,13 the exact finite maxima are:
one-port R: 4/5,104/115,36/35,52/45,31/20,91/55,9/5,343/180;
two-port R: 5/4,4/3,3/2,19/12,2,25/12,9/4,7/3.
For B>=14, the strong local lemmas give epsilon>=B/16+13/40>=6/5 and delta>=(B-6)/16>=1/2.

First consider vertices u,v having no separating articulation. They lie in a common block. The maximal-nested-two-cut proof applies directly to the entire graph: ordinary singleton layers cannot occur because each would separate u from v. If the u-v edge-connectivity is>=4, a quarter-capacity unit flow has energy<=m/16=n/8. Otherwise use a maximal chain of nested size-two u-v cuts. It has two terminal atoms. The same terminal-atom proof as for caps bounds prescribed-flow internal energy in each atom A by 3|A|/16-51/80, using exactly the finite uniform-cap-tail checks for |A|<=9 and quarter-capacity for |A|>=10. Coincident incoming incidences at a vertex different from the target violate maximality; if both incidences meet the target itself, zero internal flow suffices and is even cheaper. Ordinary layers cost<=3|A|/16 including their allocated outside-edge energy. Each terminal atom's allocated outside energy is1/4. Thus R(u,v)<=3n/16-31/40.
Both n/8 and 3n/16-31/40 are below n/4-C for n>=15 and every C in {7/5,23/20,149/115,139/90}: indeed the worst C is139/90; 15/8>139/90 and 15/16+31/40>139/90.

Now suppose articulations separate u,v. Each cut vertex of a 4-regular graph belongs to exactly two nontrivial blocks, with degree2 in each (blocks have minimum degree2). Therefore the block-cut tree's unique u-v chain has two terminal blocks and some internal blocks. Effective resistance is the sum of resistances across these blocks; all components off the chain carry zero electrical current. Assign the vertices in each off-chain subtree to the chain block where it attaches, counting its attachment vertex only in the chain block.
Every off-chain component has at least five vertices: adjoining its attachment as a degree2 port gives a connected cap with root degree2 and all other vertices4, whose minimum order is6 by the simple degree count. Thus a block having any off-chain port receives at least five extra assigned vertices.
For any 2-connected B-vertex block, two internally vertex-disjoint paths give R<=B/4. Consequently any internal chain block with an off-chain port has defect (assigned_vertices-1)/4-R>=1. Any terminal block with an off-chain port has defect assigned_vertices/4-R>=5/4. These are too costly to improve any candidate optimum (minimum ordinary cap epsilon is7/10; maximum candidate global defect is139/90<17/10). For a fully formal bound including arbitrary mixtures, treat such branching internal blocks as arbitrary-residue edges of cost>=1, branching terminal blocks as arbitrary-residue caps of cost>=5/4; the min-plus comparison below discards them.

It remains only chain blocks having no off-chain ports. The terminal ones are precisely the one-port networks, internal ones the two-port networks. Orders below6 are impossible by degree counting. If terminal orders are a,b and internal orders B_i, then n=a+b-1+sum_i(B_i-1), and
R(u,v)=n/4-[epsilon_a+epsilon_b-1/4+sum_i delta_(B_i)].
The exact finite table for B11..13 is dominated in its order-residue class by the B6..10 table. Generic caps of epsilon>=6/5 and generic internal blocks of delta>=1/2 cannot improve any candidate. The remaining min-plus optimization on order residues modulo5 is checked exactly in check_odd_minplus_agent1.py; its global defect minima for n mod5 =0,1,2,3,4 are respectively 7/5,23/20,149/115,7/5,139/90. Multiplying R by4n gives exactly the proposed odd-n formula.


---

# Chapter 4: even_degree5_agent1.md

# Complete even-n degree5 upper bound
We show Ruv<=3n/10-33/20 for all connected5regular graphs of even n>=12. This is stronger than both required normalized even targets after multiplication by5. At n10 degree5 is dense, already handled.

## DAG flow estimate
For an acyclic integerflow on a simple a-vertex graph, edgecurrents<=C and totalpositiveinjection<=F, a topologicalordering gives sum j_e*indexdistance<=F(a-1). Totalcurrent on distance1edges<=C(a-1), so 2sum j_e-C(a-1)<=F(a-1). Therefore sum j_e²<=C sum j_e<=C(F+C)(a-1)/2. Integerflow feasibility follows maxflow after denominatorclearing; cyclecancellation preservescapacity. This proves: unitflow capacity1/4 =>energy<=5(a-1)/32; internalcapacity1/3 with half-interface injections=>energy<=2(a-1)/9; internalcapacity1/4 with third-interface injections=>energy<=5(a-1)/32.

## Networks having no separating bridge
Let H be connected and simple, all vertices degree5 except that either or both marked terminals may have degree4. Suppose no bridge separates the terminals. If terminal edgeconnectivity is2 or3 we prove the strong bound R<=3|H|/10-33/20.
Choose maximalnested terminal cuts of sizek (k=2or3). Give every outsideedge current1/k. For an ordinarylayer A, entering and leavingcounts equal, totalexternalincidences h<=2k. For U proper inside A, maximality and terminal mincutk imply c_A(U)>=|sigma(U)|+1 whenever sigma!=0. Thus internalcapacity1/(k+1) realizes the imposed injections, since |sigma|<=k and |sigma|+1>=(k+1)|sigma|/k. The same argument applies to the two terminaltails, for U excluding its target. All ordinaryvertices degree5. Since h even and suminternaldegrees=5a-h is even, ordinary a is even. Simplicity rules out a<=4, hencea>=6.
For k2 the ordinarychargedcost is <=2(a-1)/9+h/8<=2(a-1)/9+1/2<=3a/10. For k3 it is <=5(a-1)/32+h/18<=5(a-1)/32+1/3<=3a/10.
For k3 everytail has a>=6 by simplicity, even with its targetdegree4. Its chargedcost is <=5(a-1)/32+1/6, so its defect against3a/10 is >=23a/160-1/96>=33/40.
For k2 a tail whose targetdegree5 has a even and a>=6. Its defect is3a/10-1/4-E. For a>=12, the DAG estimate E<=2(a-1)/9 gives defect(14a-5)/180>=33/40. Exceptions:
* a6: the graph isK6-edge; uniformhalf injection at its two deficient endpoints, extraction at anytarget, has E<=1/4.
* a8: write Htail=K8-C. If the two incoming incidences are distinct, Delta(C)<=3, so lambda_max(L_C)<=6. If they coincide atw, C has degree4 atw, degree2 elsewhere; the signlessLaplacian test vector with value3 atw,1 elsewhere gives lambda_max(L_C)<=lambda_max(Q_C)<=6. Thus lambda2(L_Htail)>=2; the injectionnorm²<=2 gives E<=1.
* a10: scale6, so currents are0,1,2, totalpositiveinjection<=6. The topologicallengthbudget is54. For eachdistance ell there are at most10-ell edges, each contributing cost j*ell and energynumeratorj² forj0,1,2. The exhaustive finite integerknapsack check check_d5_tail10_agent1.py proves maximum69. Hence E<=69/36=23/12 and defect>=5/6>33/40.
A tail whose targetdegree4 has a odd and a>=7. For a>=11 the DAG defect(14a-5)/180>=33/40. Exceptions:
* a7: unless both incoming incidences equalthetarget (zero demand), its complement has either maximumdegree2, or onevertexofdegree3, atmostoneofdegree2, allothersdegree1. Put weight2 at the degree3vertex and1 elsewhere. Every signlessLaplacian rowratio is<=5, so lambda2(L_Htail)>=7-5=2. Injectionnorm²<=2 gives E<=1 and defect>=17/20>33/40.
* a9: exact exhaustive checker check_d5_tail9_cap7.py, covering coincidentports, distinctports, and oneportattarget, proves E<=13/8 (actual maxima40/53,239/462,10/53). Thus defect>=33/40.
Summing ordinarylayers andtwotaildefects gives R<=3|H|/10-33/20.

If terminaledgeconnectivity>=4, quartercapacityflow gives R<=5(|H|-1)/32. In particular for two degree4terminals and b>=6 this implies R<=3b/10-1. For a degree5 and degree4 terminal and oddb>=9 it implies R<=3b/10-53/40. For two degree5terminals and b>=12 it implies R<=3b/10-33/20.
The remaining oddb7 network with onlyone degree4vertex is unique up toisomorphism (complementdegree2 atport,1 elsewhere); exactchecker check_d5_tail9_cap7.py gives port eccentricity11/24<31/40=3*7/10-53/40.

## Reassemble bridges
For arbitrary u,v in a5regular graph, if no separatingbridge, apply the preceding argument to the wholegraph (u,v bothdegree5). Otherwise remove precisely the k>=1 bridges on the bridge-treepath fromu tov. The resulting k+1 connectedcomponents partition all n vertices; all offpathsubtrees stayinside their attachedcomponent. Their vertices allhave degree5 except the onepathport in each terminalcomponent (degree4), and the twopathports in each internalcomponent (degree4 each ifdistinct). No remainingbridge separates its markedterminals. Terminalcomponentorder is odd>=7, internalcomponentorder is even>=6. Thus terminalcomponentresistances are<=3b/10-53/40 each, and internalcomponentresistances<=3b/10-1 each. Coincident markedterminals have resistancezero and satisfythese samebounds by the elementaryminimumorders. Adding k bridge-resistances gives
 Ruv<=3n/10-2*(53/40)-(k-1)+k=3n/10-33/20.
Therefore 5Ruv<=3n/2-33/4, completing the evendegree5 upper bound.


---

# Chapter 5: even_degree6_agent1.md

# Even-n degree6 upper bound
All graphs here are simple connected6-regular, and n>=14 (n<=12 is dense and already controlled). Every cut is even.

A basic integral-flow fact: suppose a simple graph on a vertices supports a flow with integer edge currents0 or1, total positive vertex injection at most4, and no directed cycle. In a topological ordering, each cut has at most4 units crossing it, so sum_over_active_edges(indexdistance)<=4(a-1). At mosta-1 edges have distance1 and every other edge has distance>=2; thus the numberM of active edges obeys 2M-(a-1)<=4(a-1), i.e.M<=floor(5(a-1)/2). An undirected capacity-one flow can be made integral then cycles cancelled. Scaling by1/4, a quarter-capacity electrical competitor has energy at mostfloor(5(a-1)/2)/16.

If u,v have edge-connectivity>=4, maxflow gives such a quarter-capacity unit flow on the whole graph. Hence Ruv<=5(n-1)/32, and 6Ruv<=15(n-1)/16<=3n/2-33/4 for n>=13.

Otherwise minimumuvcut is2. Choose a maximal nested chain of2-edgeuvcuts. There are two terminal tails and ordinary intervening layers. Each ordinary layer A has h=2or4 external incidences, with equal entering/leaving counts. Exactly as in maximal_2cut_chain_agent4.md, uniformhalf current on outsideedges extends to internal currents with capacity1/4. (All cuts are even and no proper refinement of the chain has size2.) If a=|A| thenm=(6a-h)/2, giving energyplusassignedoutsidecharge at mostm/16+h/8=(6a+3h)/32. Simplicity implies a>=7, because6a-h<=a(a-1) andh<=4. Thus (6a+3h)/32<=a/4.

Each terminal tail A contains one ofu,v and has precisely two incoming incidences. Its sizea>=7. Prescribed +1/2 at each incoming incidence and -1 at the target admits quarter-capacity internal flow by the same maximality argument. Integralquarterflow, then cycle cancellation and the basic fact, gives internalenergyE<=floor(5(a-1)/2)/16. If a>=8, its charged defect satisfies
 a/4-1/4-E >=11/16.
For a8 this is exact integer arithmetic; for a>=9 the weaker bound (3a-3)/32>=3/4 suffices.
If a7, degreecount forces A=K7 minusoneedge, the two incoming incidences being at its missing-edgeendpoints. Uniformhalf injection at these two ports, extraction1 at any target has energy at most3/14: if targetisnotaport, the injectionvector is symmetric in the two ports, so deleting their edge doesnotaffect the K7 solution, and energy=(1/4+1/4+1)/7=3/14. If targetisaport, the antisymmetric injection vector has energy(1/4+1/4)/5=1/10. Thus the defect is at least7/4-1/4-3/14=9/7>11/16.

Summing the two tails and all ordinarylayers yields Ruv<=n/4-11/8 and therefore6Ruv<=3n/2-33/4. This is no larger than either even-n target normalized byn. Multiplication byn proves the required upper bound for every6-regular graph of allowed even order.

Coincident incoming incidences at the target cause zero internal demand, and are cheaper; if coincident elsewhere, maximality forbids them. All tail capacities and arguments remain valid. Tail graphs are connected by Eulerian parity and originalconnectedness.


---

# Chapter 6: even_degree7plus_agent3.md

# Rigorous exclusion of all degrees d>=7 for even n>=10
Let G be connected, simple and dregular, not complete. Unit resistances throughout.

## Two adjacent-edge lower bounds
For every edge uv, R_uv>=r0=2/(d+1), by contracting all other vertices to one vertex.
Call uv a twin edge if N[u]=N[v]. For a nontwin edge choose distinct w in N(u)\N[v], z in N(v)\N[u]; existence of both follows regularity. Test the Dirichlet variational principle R_uv>= (f(u)-f(v))^2/E(f) with f(u)=1,f(v)=-1,f(w)=epsilon,f(z)=-epsilon and all other potentials zero. The diagonal and offdiagonal terms give
E(f)=2(d+1)-4epsilon+2(d+1_{wz in E})epsilon^2
<=2(d+1)-4epsilon+2(d+1)epsilon^2.
Set epsilon=1/(d+1), to obtain R_uv>=r1=2(d+1)/[d(d+2)]. Thus g=r1-r0=2/[d(d+1)(d+2)].

## At least 3n/2 nontwin edges when d>=5
Closed-neighborhood twin equivalence classes are cliques. If one has size a, every vertex in it has external degree d+1-a. No class can have size d or d+1: in either case its vertices and their remaining neighbor(s) form an isolated K_{d+1}, contrary to connected noncompleteness. Hence every external degree is >=2.
Let A be the set of vertices with external degree2; each such class has size d-1. Each vertex x outside such a class adjacent to it is adjacent to its d-1 members. It must be a singleton twin class: a twin y of x would, with the d-1 class members, form a complete K_{d+1} component. Let B consist of all these outside neighbors. Each B vertex has external degree d and is adjacent to exactly d-1 vertices of A, because it cannot touch two disjoint classes of size d-1. Consequently (d-1)|B|=2|A|. Every remaining vertex C has external degree>=3. Thus twice the number of nontwin edges is at least
2|A|+d|B|+3|C|=3n+(d-5)|A|/(d-1)>=3n.

## Foster + shortest path
Foster gives sum_e R_e=n-1. If P is a shortest u-v path of length l, the resistance triangle inequality and the edge lower bounds imply
R_uv<=sum_{e in P}R_e
<=n-1-(dn/2-l)r0-(3n/2-l)g.
This uses 3n/2-l>=0, which holds as l<=n-1. Closed neighborhoods of the vertices at path positions0,3,6,... are disjoint, so floor(l/3)+1<=n/(d+1). Hence l<=3n/(d+1)-1.
Substitution and simplification give
 dR_uv <= [(d^2+8d+3)/((d+1)(d+2))] n -d-2+2/(d+2).
For d>=7, the coefficient is <=3/2, since their difference is d(d-7)/[2(d+1)(d+2)]. The constant is at most its d7 value -79/9<-33/4. Thus
 dR_uv < 3n/2-33/4,
below both even-n target normalized resistances.
If G is complete, R=2/n and dR<2, also trivially below the target for n>=10.
The commute is ndR, giving the desired exclusion of every d>=7.


---

# Chapter 7: odd_degree6_agent4.md

# Universal degree-six upper bound at odd orders n>=15
For every connected simple 6-regular graph on n>=15 vertices and every u,v,
R(u,v) <= n/6 - 139/135.
This is stronger than every required odd-order target divided by6n.

## Valid two-level cut decomposition
If the u,v edge connectivity is at least6, a unit flow bounded by1/6 has energy <=3n/36=n/12, which suffices for n>=15. Otherwise min connectivity is2 or4 (all cuts are even).

If it is2 choose a maximal nested chain of size-two u,v cuts. If it is4 start instead with a maximal chain of size-four cuts. At the ends there are point-terminal tails; an ordinary layer between two size-two cuts has p incoming and p outgoing incidences, p=1 or2, all current1/2. For p1 no further subdivision is needed. For p2 let L,R be the sets of vertices incident to its incoming/outgoing incidences. Select a maximal nested chain of size-four u,v cuts inside this layer that contain ALL L and exclude ALL R. If L and R overlap or there are no such cuts, do not subdivide. These cuts have no overlap with the original size-two boundary edges. Endpoint tails behind size-two cuts are treated likewise: insert all nested size-four cuts containing the two boundary ports and excluding the point terminal. Thus only transitions2->4,4->2 occur, and those transitions have no bypass edges. Between equal-size cuts, bypasses are allowed. Put currents1/2 on all size-two-interface edges and1/4 on all size-four-interface edges, oriented u to v. These assignments agree on every physical edge, because edges common to multiple interfaces occur only among constant-size interfaces.

Every resulting internal atom admits a flow bounded by1/6 completing its prescribed boundary current. Here are the cut checks; all follow from even cut parity and maximality.
* Between equal2 interfaces, for sigma=incoming-minus-outgoing incidence count, a nonzero sigma has internalcut c>=|sigma|+2. If |sigma|2 and c4 there would be a missing size-four cut separating all left ports from all right ports; hence c>=6. Thus c>=3|sigma|, exactly the capacity condition for current sigma/2 with capacity1/6.
* Between equal4 interfaces, c>=|sigma|+2>=3|sigma|/2 since |sigma|<=4. This supplies current sigma/4.
* For transition2->4 let l=0,1,2 and r=0,...,4 be incidence counts in a subset. Its required net current is l/2-r/4. For l2, any proper subset containing all left ports creates a size-two/four refinement unless c+r>=6, so c>=6-r. For l0 apply the same to the complement: c>=2+r. For l1, no further size-two cut implies c>=max(3-r,r-1). These inequalities, with c congruent l+r mod2, give c>=6|l/2-r/4| by checking r0,...,4. Empty/full subsets have zero demand. Reverse transition is symmetric.
* At a point-terminal tail with2 boundary incidences and no remaining eligible4 cut, subsets not containing the point have boundary count l0,1,2, demand l/2, and c>=l+2; if l2,c4 would be an eligible4 cut, so c>=6. At a tail with4 boundary incidences, c>=l+2>=3l/2 for l<=4, giving demand l/4. Complement handles subsets containing the target.
Thus the standard capacitated-transshipment cut criterion proves existence of all internal flows independently, with matching interfaces. Thomson bounds each atom's internal energy by m/36, where m=(6a-h)/2, a its order and h its external incidence count.

## Charging the energy
Charge half of each outside edge's energy to each of its endpoint atoms. Use a/6 as the budget of an atom of order a. Ordinary atom types:
* 2->2, h2 or4: cost <=a/12+h/9. Simplicity forces a>=7, so budget margin>=5/36.
* 2->4 or4->2, h6: cost<=a/12+7/24. It is singleton, or a>=6; a non-singleton has margin>=5/24.
* 4->4, h2,4,6,8: cost<=a/12+5h/288. It is singleton (necessarily h6) or a>=6. If a>=7 its margin>=4/9. If a6,h6 the graph is K6; prescribed vertex injections have squared norm<=3/8, hence internal energy<=1/16; total charged cost<=1/4, margin>=3/4. If a6,h8 the graph is K6 minus one edge, lambda2=4 and squared injection norm<=3/4, hence internal energy<=3/16; charged cost<=7/16 and margin>=9/16.
The size restrictions follow directly from 6a-h<=a(a-1). Atoms of order2,3,4,5 are impossible for h<=8.

A singleton2<->4 atom has excess5/24 over its1/6 budget. A singleton4->4 atom has excess1/48. No two singleton atoms are adjacent. Indeed if consecutive interfaces have sizes p,q,r<=4, and singleton overlap counts x=(p+q-6)/2,y=(q+r-6)/2, simplicity allows at most one edge directly joining the two singleton vertices, so q<=x+y+1, implying p+r>=10, impossible.
Charge singleton2->4 to its right neighbor, singleton4->2 to its left neighbor, and singleton4->4 arbitrarily to a neighbor. Then a non-singleton2->2 atom receives no charge; a transition atom receives at most one charge<=5/24; a4->4 atom receives at most two totaling<=5/12. The margins above pay all these charges.

## Endpoint margins
A point->2 tail receives no singleton charge. Its size a>=7. For a>=9, generic sixth-capacity energy and outside charge1/4 give budget margin a/12-2/9>=19/36>139/270. For a7 the graph is K7 minus an edge; uniform half-port injection has energy<=3/14, giving margin59/84. For a8 with distinct ports, minimum internal degree5 gives lambda2>=4 and injection squared norm<=3/2, so energy<=3/8, giving margin17/24. Coincident ports at a nonterminal would produce an eligible4 cut, so were subdivided; at the target zero internal flow suffices.

A point->4 tail receives at most one singleton charge<=5/24. For a>=10 generic internal energy a/12-1/18 and outside charge1/8, after singleton charge, give margin a/12-5/18>=5/9>139/270. Orders a<7 are impossible by simple degree count. For a7,8,9 exact exhaustive certification workspace/check_d6_tail4_agent4.py proves maximum prescribed quarter-port injection energy respectively45/224,129/448,5/14. All satisfy E<=a/6-1/3-139/270, exactly enough to pay outside charge1/8 and singleton charge5/24 while retaining margin139/270. Exhaustivity: port deficits partition4, hence complement degree sequence a-7+deficit; enumerate the5 partitions of4, every graph with that degree sequence, and every target. Reject only targets violating the necessary maximality inequality internalcut(U)>=portincidences(U)+2 for subsets excluding target. The graph generator's twin pruning is justified in enumerate_local4.py and preserves all possibilities.

There are two endpoint atoms. After all singleton charges, each retains budget margin>=139/270; all other atoms have nonnegative margins. Therefore R<=n/6-139/135 as claimed.


---

# Chapter 8: odd_degree8_core_agent2.md

# Odd-order degree8 upper, core proof
Let gamma=139/360. We prove R_uv<=n/8-2gamma for every simple connected8regular graph of oddorder n>=17. At n15 degree8 is dense and already excluded.

Use the valid two-level (width2/4) cut hierarchy proved in odd_degree6_agent4.md. Its construction and transshipment capacity proof depend only on Eulerian parity, not on degree6, so they apply unchanged to8regular graphs. All prescribed internal flows can be bounded by1/6; edges on width2 interfaces carry1/2 and width4 interfaces1/4. Unlike the failed arbitrary-width construction, transitions2↔4 contain all left ports and exclude all rightports; hence no shared edges between unequalwidth interfaces and assignments agree.

If lambda(u,v)>=6, a sixth-capacity flow has integral unit-edge support after scaling6. Acyclic support of value6 with M edges on n vertices has M<=3n-4: balancedvertex incident index-length sum>=q(q+1)>=8q-12; source/sink eachhave6distinctneighbors so incidentlengthsum>=21. Thus12(n-1)>=8(M-6)-12(n-2)+42=8M-12n+18. Integral M gives M<=3n-4. Hence R<=(3n-4)/36<n/8-139/180 for n>=17.

Assume lambda2or4 and use the hierarchy. For any atom of a vertices and prescribed flow, scale12: integral capacities2, totalpositiveinjection<=12. Let W=sum integer edgecurrents and L=sum current*indexlength in an acyclic flow. L<=12(a-1). At a vertex with incomingweighteddegree q, its minimum incoming incidentlength is >=q^2/4+q/2, since the graph simple and edgeweight<=2; same for outgoing. Summing and Cauchy gives 2L>=W^2/(2a)+W. If W>=6a-3 this exceeds24(a-1), so integer W<=6a-4. Therefore energy<=2W/144<=a/12-1/18. (If a=1 and zero demand choose energy0.)

Allocate half of every interface-edge energy to each endpoint atom. Ordinary types:
* 2→2: h2or4, allocatedoutsideenergy h/8<=1/2.
* 2↔4: h6, outsideenergy3/8.
* 4→4: h2,4,6,8, outsideenergy h/32<=1/4.
Simplicity implies a singleton or a>=8: h<=8 and8a-h<=a(a-1) ruleout2<=a<=7. At a8, h8 and the atom isK8, so this is only4→4. Atoms a9+ are ordinary. A singleton mustbe4→4,h8, with energy1/4 andbudget1/8, excess1/8. Two such singletons cannotbeadjacent: the size4 cut between them would consistoffour parallel edges. Charge each singleton arbitrarily toone neighboring nonsingleton. Then2→2 receivesnone;2↔4 receivesatmostone charge1/8;4→4 receivesatmosttwo charges1/4. In every case outsideenergy plus charges<=1/2.

For every nonsingleton a>=11, internalenergy plus these charges <=a/12-1/18+1/2=a/12+4/9<=a/8. For a8,K8 has oneexternalport pervertex and injectionnorm^2<=1/2, so internalenergy<=1/16 and totaloutside+charges<=1/2; total<=9/16<1=a/8. For a9 write atom=K9-F with |F|=h/2<=4, so lambda2>=9-(|F|+1)>=4. Any boundarydemand has totalpositive<=1 andnorm²<=2, hence energy<=1/2; total<=1<a/8. For a10, exactfinite atomchecks in check_d8_ordinary_atoms_agent3.py certify:
(A)transition2↔4, deficit6 and current L/2-R/4, sums L2,R4: Emax=54/121<=3/4;
(B)4→4, deficit8 and current(L-R)/4, sums L=R=4: Emax=9/16<=3/4.
Thus adding outside+charges<=1/2 gives <=5/4=a/8. For4→4,a10,h<=6, the complement gap is >=8-h and norm²<=h²/32, hence E<=h²/[32(8-h)]<=9/16, which is below a/8-h/32-1/4 for h2,4,6. Ordinary2→2,a10 is analytical: complement has degree1+deficit and totaldeficit<=4. Anderson-Morley lambda_max(L_complement)<=max_edge(deg_i+deg_j)<=6, hence lambda2>=4. Norm²<=2 gives E<=1/2; plusoutside<=1/2 isbelow10/8. Consequently all ordinarybudgets pay singleton charges.

It remains to establish the endpoint-tail bounds: each retains margin>=gamma againsta/8 afteritsoutsidecharge andatmostone singletoncharge. These are proved independently in d8_endpoints_agent4.md, reviewed by agents2and3: point→2,a9..13 spectralgap16-a andnorm²<=2; point→4,a9..12 spectralgap14-a andnorm²<=13/8; point→4,a13 reverseunique-source quadraticDAGbound W<=71 andE<=71/72 (or targetportF<=9). Alltailsa>=14 use genericDAGestimate. Everytail has combinedoutside-plus-singleton charge<=1/4. Summing two endpointmargins gives R<=n/8-139/180, whence8R<=n-278/45, enough every odd residue.


---

# Chapter 9: d8_endpoints_agent4.md

# Degree-eight endpoint atoms: all orders, analytic proof
Use the valid two-level2/4-cut decomposition from odd_degree6_agent4.md, but every original vertex now has degree8. Point-terminal atoms have h2 or4 boundary incidences, hence size a>=9 by simplicity. Uniform boundary currents are1/2 or1/4. The internal transshipment has capacities1/6 by the degree-independent even-cut argument already proved. The required endpoint defect, after assigned outside energy and singleton charges, is gamma=139/360.

## General DAG estimate
Scale by12. Integer internal flows have edge capacity2 and total positive injection<=12. Cancel cycles and topologically order a vertices. Write W=sum_e j_e and L=sum_e j_e times indexdistance. Then L<=12(a-1). At a vertex with total incoming q and outgoing r, capacity2 and simplicity force weighted incident length at least q^2/4+q/2+r^2/4+r/2: fill the nearest predecessor/successor slots, two units per edge, to minimize length. Summing and Cauchy gives 2L >= W^2/(2a)+W. Substituting W=6a-3 exceeds24(a-1) by3+9/(2a)>0, so integer W<=6a-4. Energy <=2W/144<=a/12-1/18.
For a>=14, outside energy plus any singleton charge is at most1/4 (h2 tail has outside1/4 and no singleton charge; h4 tail has outside1/8 and at most one singleton charge1/8). Thus defect against a/8 is >=a/24-7/36>=7/18>139/360.

## Dense tails of orders9..13
Let p_v be the port-incidence deficits, sum p=h. The internal graph is K_a minus a graph with degrees a-9+p_v. For any graph Q, lambda_max(L_Q)<=max_{xy edge}(deg_Q(x)+deg_Q(y)): use the oriented incidence matrix and its edge-by-edge Gram matrix row absolute sums. Therefore lambda_2(internal)>=18-a-h. For an injection vector j of zero sum, energy j^T L^+ j <= ||j||^2/lambda_2.

For h2 the prescribed injection is p/2-unit_at_target, with squared norm<=2. Consequently E<=2/(16-a). For a9,10,11,12,13, the exact rational inequalities a/8-1/4-2/(16-a)>=139/360 hold (checker attached). This covers distinct/coincident ports, whether or not at the target.

For h4, a non-target vertex cannot have p_v4: it would induce a further nested size-four cut, contrary to maximality. Thus the squared injection norm of p/4-unit_at_target is <=13/8. The gap18-a-h=14-a gives E<=13/[8(14-a)]. For a9..12 these exact inequalities a/8-1/4-E>=139/360 hold.

It remains h4,a13. If at least one port incidence meets the target, reverse the flow: its total positive injection is at most9 in scale12. The elementary DAG estimate sum j^2<=C(F+C)(a-1)/2 gives energy<=11(a-1)/144=11/12, sufficient. If no port meets the target, reverse the flow to have a UNIQUE source, the target, of net supply12. In an acyclic flow its incoming flow is zero and outgoing flow12. Hence sum_out q^2>=144+(W-12)^2/12 and sum_in q^2>=W^2/12. The weighted-length lower bound sharpens to
2L >=36+[(W-12)^2+W^2]/48+W.
If W>=72, the RHS is at least291, contradicting2L<=288. Thus W<=71 and E<=2W/144=71/72. Finally13/8-1/4-71/72>=139/360. This includes the worst outside-plus-singleton charge1/4.

Every endpoint atom therefore retains margin >=139/360 after its assigned outside energy and possible singleton charge. The proof is fully analytic; workspace/check_d8_endpoints_agent4.py checks every finite rational inequality and both symbolic DAG substitutions.


---

# Chapter 10: d8_ordinary_checks_agent3.md

# Degree8 ordinary small-atom finite checks
Use the two-level2/4 interface decomposition from odd_degree6_agent4.md, whose cut-capacity proof depends only on parity, not regular degree. Internal capacities1/6 and outside currents1/2 or1/4 remain feasible at degree8.
The general integral DAG bound E<=a/12-1/18 follows by scaling by12, edge capacity2, positive injection<=12. If W is total integer edge current and L its total topological index-length, L<=12(a-1). Minimal incident weighted length for incoming/outgoing weights q,r is at least(q^2+r^2)/4+(q+r)/2. Cauchy yields2L>=W^2/(2a)+W. AtW=6a-3 the latter is24a-21+9/(2a)>24(a-1), so W<=6a-4 and E<=2W/144<=a/12-1/18.

Only singleton4->4 atoms are possible; theirh8 outside edges cost1/4 against budget1/8, excess1/8. They cannot be adjacent, by the same singleton adjacency argument. Charge either neighbor. Every ordinary2->2 atom receives no charge, transition2<->4 at most1/8, and4->4 at most1/4. Simplicity forces ordinary2->2/transition atoms order>=9, and4->4 nonsingletons order>=8 (order8 onlyh8).
After generic DAG bound and allocated outside energy, the only cases not already within budgeta/8 are exactly the following:
2->2: h4, a9,10; outsideenergyh/8, nocharge.
2->4: h6,a9,10; outsideenergy3/8, onecharge1/8.
4->4: h8,a8,9,10, orh6,a9; outsideenergyh/32, twocharges1/4.
Otherh values and orders follow by elementary rational substitution in E<=a/12-1/18.

The runnable checker check_d8_ordinary_atoms_agent3.py exhaustively enumerates every port-deficit partition p_1+...+p_a=h; the internal graph has degree sequence8-p_i, so its complement has degree sequencea-9+p_i. The degree-sequence generator is exhaustive up to admissible permutations by the already documented twin pruning. For each graph the checker iterates every allocation0<=L_i<=p_i with the specified total entering incidences and setsR_i=p_i-L_i. Since all such allocations are tested, graph symmetries between equal-degree vertices lose no flow configurations. It solves the grounded rational Laplacian once and computes j^T L^+ j for each injection j=L/2-R/2 (2->2), L/2-R/4 (2->4), or(L-R)/4(4->4). No cut-condition filters are used.

It is legitimate to skip disconnected internal graphs in these finite cases. If an a<=10 graph with total deficit h<=8 is disconnected with component ordersr_i, then h>=sum r_i(9-r_i). For a8,9 the minimum possible bound is respectively22,16 (partition1,a-1), already>8. For a10 it is8, with equality only at component orders1,9, and then the graph is an isolated vertex plusK9, with all outside ports at the isolated vertex. The K9 component has no outside incidence and would disconnect the original graph. Thus no valid atom is discarded.

Results(maxE, requiredthreshold):
2->2 a9,h4:1/4,5/8; a10,h4:9/26,3/4.
2->4 a9,h6:1/4,5/8; a10,h6:54/121,3/4.
4->4 a8,h8:1/16,1/2; a9,h8:5/16,5/8; a10,h8:9/16,3/4; a9,h6:3/20,11/16.
Every comparison passes exactly. Complete counts/witnesses are in d8_ordinary_atoms_agent3.json.


---

# Chapter 11: odd_degree10plus_agent1.md

# Odd-order reduction: all even degrees d>=10
The following argument bounds every connected simple even-d-regular graph, independentlyof parityn:
 d Ruv <= [(d²+15d-8)/(2(d+1)²)] n -(d³+4d²+15d-8)/(2(d+1)²).
For d10 coefficient1 and constant771/121>278/45; for d>=12 coefficient<=1 and constant>d/2+1>=7. Therefore it is strictlybelow every requiredodd normalizedtarget n-c, c<=278/45.

## Ordered chord-count lemma
Let bipartitegraph have ordered parts A1..Ar andB1..Bl, and satisfy: edgesAiBj,AkBh withi<k,j>h implyk=i+1,j=h+1. Ifv=r+l>=2, it hasatmost3v/2-2edges. Inductonv. Thev2caseisobvious. Ifavertexhasdegree<=1, deleteit anduseinduction (remainingv>=2), givingevenstrongerbound. Otherwise allverticesdegree>=2. LetA1's first/lastneighborsbeBj,Bk. BjhasanotherneighborAh,h>=2. Theinversionforcesh2,k=j+1, soA1hasexactlytwoneighborsBj,Bj+1, andBjhasexactlyneighborsA1,A2. Ifj>1, B1's twoneighborsbothafterA1giveaninversionwithA1Bj; onehasindex>=3, impossible. Thusj1. DeletingA1,B1 deletesexactly3edges; remainingorderedgraphhastheproperty, soinductiongives3+3(v-2)/2-2=3v/2-2. (Ifonepartemptytheboundtriviallyholdswhenv>=2.)

## Local block bound
LetB bea two-connectedblock, b itsorder, allitsdegreesatmostd, and Delta=sum_x(d-deg_Bx). Fixu,v. ChooseashortestcycleCcontainingthem, lengthc. Neitherendpointcanhaveachord, because thatshortensonearc. Chordsjoininteriorsofthetwoarcs (a same-arcchordshortens). Twoinvertedcrosschords mustoccupyconsecutiveverticesonbotharcs: otherwise switchingarcsatthesetwochords givesashorteruvcycle. Thusthechordlemmayieldsatmost3(c-2)/2-2chordswhenc>=4.
AnoutsidevertexhasatmostthreeCneighborsoneacharc; otherwiseitsfirst/lastneighborscanbejoinedthroughitin2edges, shorteningthecycle. Therefore totaldegreeincidencesonC areatmost2c+3c-10+6(b-c)=6b-c-10. Ontheotherhandtheyareatleastdc-Delta. Hence
 (d+1)c<=6b-10+Delta.
Ifc3andb>=4, everyoutsidevertexhasatmost3Cneighbors. Thusdc-Delta<=6+3(b-3)=3b-3, whichimpliesthesameboundbecauseb>=4. Theonlyexcludedcaseisb3, handledbelow.
Adjacentedgeeffective resistanceinsideB isatleast2/(d+1): contractallothervertices; theresultingdirectedgeisinparallelwithtwoseriesbundlesofatmostd-1unitresistors. Foster'sidentitysum_edgesR_e=b-1andtheresistancetriangleinequalityalongbothuvarcsgive
 2Ruv<=sum_(e in C)R_e<=b-1-2(m-c)/(d+1),
where2m=db-Delta. Substitutecycleboundtoobtain
 Ruv<=A b+Q Delta-C0,
 A=(d+13)/(2(d+1)²), Q=(d+3)/(2(d+1)²), C0=1/2+10/(d+1)².
Forb3, Bistriangle, Delta=3(d-2), andtheRHSsimplifiesto d(d+2)/(d+1)²>=2/3=Ruv. Sotheboundholdsforallblocks.

## Reassemble blockpath
Everyblockofaneven-regulargraphhasallitsdegreesEVEN: theedgesleavinganycomponentatacutvertexformacutandhenceareeven, andtheblock'sdegreesfollow. Inparticulartherearenobridgesandallblocksare2connectedoforder>=3.
Forfixedu,v followtheunique block-cutpath, withkblocks. Assignalloffpathvertices to thepathblockwheretheirsubtreeattaches. Letw_i beassignedorderincludingtheblock'sownvertices. Then sumw_i=n+k-1.
An offpathportx hasblockdegreea>=2, soitsdeficitd-a<=d-2. Everyoffpathcomponentattachedtherecontainsatleastd+1vertices: togetherwithxitisagraphwhereallnonrootverticeshavedegreedandtherootdegreebetween2andd-2; simplicityforcesorder>=d+2. Thus theterm A*(assignedsidevertices) morethanpaysitsdeficit Q*(d-a), since A(d+1)>Q(d-2). Differentoffpathportsreceive disjointvertices.
Thetwoblocksmeetingatanyinternalpatharticulationhavecombineddeficitd there, because theirdegrees sumtod unlessoffpathcomponentsalsoattachthere. Anyextraoffpathdeficitiscoveredbytheprecedingsidecharge. Endpointarticulations arehandledidentically asoffpathports. Consequently sum_i[A b_i+Q Delta_i]<=A(n+k-1)+Qd(k-1).
Alsoeachw_i>=d+1: ifthereisnooffpathport, atmosttwoverticesofitsblockhavedegreelessthand, andb_i>=3, henceatleastonefull-degreevertexforcesb_i>=d+1; ifanoffpathportexists, itsassignedsidealonehas>=d+1vertices. Thereforek<=(n-1)/d.
Seriesresistancelawandthelocalboundyield
 Ruv<=A(n+k-1)+Qd(k-1)-kC0
     =A n-A-dQ+k*(d-4)/(d+1)².
Substitutingk<=(n-1)/dandmultiplyingbydprovesthestatedbound.


---

# Chapter 12: odd_lower_proof.md

# Odd-n lower bound
Use unit resistors and the commute identity C_uv=4n R_uv in a 4regular graph.
A cap C_b has b vertices, one distinguished vertex p of degree2, all others degree4.
A bulk B_b has b vertices, distinguished p,q of degree2, all others degree4.
The explicitly listed edge sets are in odd_construction.py. Exact grounded Laplacian inversions in check_modules() give:
C6: R-ecc(p)=4/5; C7:104/115; C9:52/45; C10:31/20;
B6: R(p,q)=5/4; B8:3/2.
In every case this also equals the full resistance diameter (the code checks this exactly).

Take two caps, and place a sequence of bulks between them. Identify cap/bulk ports consecutively, using each bulk's two ports once; the right cap's port is identified with the final bulk port. If there are no bulks, identify the caps' ports. The result is connected, simple and4regular: each identified pair contributes degree2+2=4, with no other identification. Its order is a+b-1+sum(bulk_order-1). Choose farthest vertices from the ports in the two caps. By the series law at articulation vertices their resistance is the sum of cap eccentricities and bulk port resistances.

For n mod5 use the following caps and optional exceptional bulk, then add k copies of B6, where k is the unique nonnegative integer making the order n:
 residue0: C6,C10; base order15, base resistance47/20.
 residue1: C6,C6; base order11, base resistance8/5.
 residue2: C6,C7; base order12, base resistance196/115.
 residue3: C6,C6 with B8; base order18, base resistance31/10.
 residue4: C6,C9; base order14, base resistance88/45.
For odd n>=15, the smallest orders in the five classes are15,21,17,23,19 respectively; thus k>=0 in every permitted case.
Every B6 increases order by5 and resistance by5/4. Therefore n/4-R is constant within each residue, with values
7/5,23/20,149/115,7/5,139/90.
Multiplying R by4n gives exactly the five claimed odd-n lower bounds.

Furthermore the chosen pair realizes the constructed graph's resistance diameter: each module has diameter equal to its distinguished distance/eccentricity, so any pair in different modules has distance at most the sum between the two extreme cap vertices; any pair in one module is bounded by that module's diameter, also at most that sum. Series additivity at identified ports proves the assertion. Full exact resistance matrices verify this independently for every odd n15..65 when odd_construction.py is run.


---

# Chapter 13: degree2_dense_agent1.md

# Degree 2 and dense-degree reductions
For a d-regular graph, commute time is dn R_uv.
If d=2 the connected graph is C_n, whose resistance diameter is floor(n^2/4)/n. Thus commute diameter <=n^2/2.
If d>=n/2, let H be the complement. For every x perpendicular to 1,
x^T L_G x=n||x||^2-x^T L_H x >=(2d-n+2)||x||^2,
since x^T L_H x=sum_edges(x_i-x_j)^2<=2(n-1-d)||x||^2.
Consequently R_uv <=2/(2d-n+2), and
dR_uv<=2d/(2d-n+2)<=n/2, where the last inequality is exactly
(n-2)(2d-n)>=0. Again commute diameter <=n^2/2.
All proposed targets exceed n^2/2 on the stated domains. Even n=2mod4 target difference is n(4n-27)/4; even n=0mod4 is n(4n-33)/4. These are positive for n>=10. [CORRECTION: differences actually n(4n-27)/4? target 3n(2n-9)/4 -n^2/2 =n(4n-27)/4, yes.] Odd difference is n(n/2-c) with c at most278/45<15/2. Thus degree2 and d>=n/2 are rigorously excluded from sharpness and satisfy the required bounds.
