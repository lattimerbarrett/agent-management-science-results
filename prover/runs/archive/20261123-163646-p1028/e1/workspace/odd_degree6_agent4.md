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
