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
