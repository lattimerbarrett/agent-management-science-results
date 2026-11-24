# Degree6 exclusion for every even n>=12
We prove R_uv<=n/4-11/8 for any connected simple6regular graph G (n even>=12). Then6nR<=3n(2n-11)/4, below/equal desired even targets. n10 degree6 is already dense.

## Acyclic integral quarter-flow bounds
If a simple graph on a vertices admits unit flow with edge capacities1/4, integral maxflow after scaling by4 gives a flow with every active edge current1/4. Delete directed cycles to make its support acyclic. Order vertices topologically. Each prefix has outgoing scaled current at most4, so the sum of the index lengths of active edges is at most4(a-1).
For a balanced vertex with k incoming and k outgoing active edges, the sum of incident index lengths is at least k(k+1)>=6k-6 (all integersk>=0). A single source of outflow4 has no incoming active edges (else following them backwards leads to a source, itself, impossible); its incident index-length sum>=10. The sink likewise has bound10. Thus if M is active-edge count,
 8(a-1)>=6(M-4)-6(a-2)+20=6M-6a+8,
so M<=(7a-8)/3. Energy is at most (7a-8)/48.
With two sources each netoutflow2 and one sink of inflow4, write source incoming degreesk1,k2, hence outgoing degreesk_i+2. Their incident length costs are >=k_i^2+3k_i+3>=6k_i+1. The sink costs10. Balanced vertices give
8(a-1)>=6(M-4)-6(a-3)+2+10=6M-6a+6,
so M<=7(a-1)/3, energy<=7(a-1)/48.
With scaled flow value2, two edge-disjoint simple paths suffice, yielding energy<=(a-1)/8.

## No2cut
If every u-v cut has size>=4, quarter-capacity maxflow exists on G. The first bound yields R_uv<=(7n-8)/48<=n/4-11/8 when n>=12 (equivalent5n>=58).

## There is a2cut
Choose a maximal nested chain of size2 u-v cuts, with endpoint tails containing u and v and ordinary intervening layers, exactly as in the established max2cut proof. All original vertices have degree6. Each ordinary layer has h=2 or4 outside incidences, m=3b-h/2 internal edges, and b>=7: simplicity m<=b(b-1)/2 rules out b2..6, while singleton cannot have degree6 with h<=4.
The same cut-condition proof gives internal currents bounded1/4 when outside edges each carry1/2. Including allocated outside-edge energyh/8, its cost is at most
m/16+h/8=3b/16+3h/32<=b/4,
sinceb>=7 andh<=4.

Each endpoint tail A has a>=7 vertices, two incoming outside incidences, and an extraction of1 at its target v. Its assigned outside-edge energy is1/4. We show its prescribed-flow minimum internal energy E satisfies
 E<=a/4-15/16,
so its cost is <=a/4-11/16. Two endpoint discounts total11/8.
As in the existing cap proof, maximality provides quarter-capacity feasibility, unless both incoming incidences are at the target (then E=0). The graph induced by the tail is connected by parity. There are three cases.
1. Distinct ports, neither equal target. Their degrees in A are5, all others6. If7<=a<=11, the complement-Laplacian estimate gives lambda2>=2*5-a+2=12-a. The demand vector has squared norm3/2, hence E<=3/[2(12-a)]<=a/4-15/16 (five rational checks). Ifa12 or13, the two-source acyclic bound E<=7(a-1)/48 is enough. Ifa>=14, the elementary quarter-capacity bound E<=m/16=(3a-1)/16 is enough.
2. Distinct ports with target equal one port. The net scaled demand is2 from the other port to the target. Two edge-disjoint paths give E<=(a-1)/8<=a/4-15/16 for alla>=7.
3. Coincident ports. If they equal target, E=0. Otherwise a single source of scaled value4 gives E<=(7a-8)/48<=a/4-15/16 for alla>=8. The casea7 cannot occur: degree sequence4,6,6,6,6,6,6 would require K7 missing one edge, which has two degree5 vertices, not one degree4. Thus a>=8.
In the zero-energy case, a>=7 so the asserted bound is positive.
Summing ordinary costs and the two endpoint costs gives R_uv<=n/4-11/8.
