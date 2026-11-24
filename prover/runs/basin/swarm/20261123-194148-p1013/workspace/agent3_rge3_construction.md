# r>=3 sharp construction via J requiring three active matching parts
All edge arguments below use the classical Simonovits linear-forest D(n,r,q) structure theorem.

W=K1 join C4; D=gem=K1 join P4. Let J3=K1 join (W disjoint-union D).
It has chromatic number4 and its outer cone-vertex is critical. J3 embeds T3 with oneinternal P3: map cone-center to P3center and W,D hubs to its twoleaves, put C4 and P4 in remainingtwo cleanparts. It does NOT embed T3 with matchings in atmosttwo parts: if cone-center x is unmatched, N(x) is bipartite+bothmatching and W-free; if x matched, N(x)=universal u join (bipartite+atmostonematching), and W mustuseu while disjoint gem awayfromu is impossible. J3 DOES embed with three matchingparts: x paired u; W usesu and a cleanC4, gem uses oneinternal edgeineachremainingpart.

For r>3 set Jr=join of (r-3) independentpaletteclasses of size S>2r with J3; J3 itself whenr3. A paletteclass has >=3vertices in some hostpart; since hostinternaldegree<=1, nojoinedvertex canuse thispart. Distinctpaletteclasses reserve distinctparts. Thus Jr is free in T_r+matchingsin<=2parts and embeds with3activeparts. Jr has criticalvertex and a P3decomposition (palettesinr-3cleanparts). Simonovits D theorem now implies ex(n,Jr)<=t_r(n)+n/r+C_J: noexception canhaveunboundedneighborsinallparts (criticalvertexembedding); assign eachto amissedpart, replacebadcrosspatterns bypurevertices toforcealloppositebulkadjacencies. P3decomposition forbids internaldegree>=2. Atmosttwobulkparts containmatchingedges, because3activeparts embedJr. BoundedexceptionscontributeO1.

Let Fk be the friendshipfan: k triangles with commoncenter and otherwisevertexdisjoint. Let Br,k=joinof(r-2) paletteclasses with Fk. Let H=Jr disjointunion Br,k. Bothcomponentshavecriticalvertices. H has linearforest decomposition P3 disjointunion kK2, henceDtheorem applies. Pick fixedk>C_J+2.

The graph U=universalvertex join [T_r(n-1)+ (k-1)matchingedgesinonepart] is H-free. Ifhubunused, Jr cannotembedmatching-onepartcore. IfhubinJr, Br,k awayneedskmatchingedges (paletteforcing). IfhubinBr,k, Jr awayimpossible. Thereforeex(n,H)>=t_r(n)+ceil(n/r)-1+(k-1)>t_r(n)+n/r+C_J.

Analyze edgeextremalG viaD. Atmostoneexceptionx hasunboundedneighborsineverypart, becauseeachsuchvertexcanrealizeonecriticalcomponentandtwowouldrealizeH. Withnone, assignexceptions tomissedparts andobtainoppositebulk-completeness asabove. Sincee(G)>=t+cn, therearelinearlymanybulkedges; boundedcomponents⇒linearmatching. ThisallowsBr,k disjointfromANYfixedJr, henceG mustbeJr-free. Contradictionto edgecomparisonwithex(n,Jr). Thusall edgeextremahaveoneuniversal-typeexceptionx.

G-x mustbe BOTH Jr-free AND Br,k-free: anycopyofonecomponentcombineswiththeotherusingx+unusedbulkvertices. Therefore completingx touniversal issafe, soedgeextremalityforcesfullyuniversalx. Everyotherexception isassignedtomissedpart. Br,k-freeness forbidskdisjointinternalbulkedges, henceonlyboundedlymanybulkcomponentshavenonedges; allinternaledgesareboundedO_H(1), andallassignedexceptioninternaledgesalsoO1. Consequently ex(n,H)<=t_r(n)+n/r+C_H, and all edgeextremaare universaljoin bounded-editsofbalancedT_r(n-1).

Theircycleconstant relativeT_r(n) is q^-2, q=(r-1)/r. The H-free graph T_r(n)+maximum matchingsinTWOparts hascycleconstant exp(2/(r-1))>q^-2. (Cyclelemmasfromagent2.) Thus noedgeextremumiscycleextremumforlargebalancedn.

Caveat: the D theorem must be cited with exact symmetry/exception hypotheses; generalcycleextremalstructureis NOT used in this construction-side proof.
