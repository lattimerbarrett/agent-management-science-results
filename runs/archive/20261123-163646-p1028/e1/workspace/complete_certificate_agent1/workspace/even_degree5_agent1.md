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
