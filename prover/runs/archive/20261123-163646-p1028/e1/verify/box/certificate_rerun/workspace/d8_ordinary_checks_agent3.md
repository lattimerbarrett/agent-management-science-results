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
