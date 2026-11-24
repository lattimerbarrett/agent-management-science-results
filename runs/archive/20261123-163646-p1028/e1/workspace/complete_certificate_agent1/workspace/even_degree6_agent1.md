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
