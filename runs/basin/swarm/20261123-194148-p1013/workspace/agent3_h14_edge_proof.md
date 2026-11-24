# H14: boundary a=1/4 construction for r=2
Finite graph and exhaustive verifications: agent3_h14_checks.py. The finite facts used below have all been actually checked by exhaustive 2^14 partitions.

Facts: H chromatic3, criticalvertex13; H embeds P4 join I and claw join I; H embeds completebipartite with3P3 inonepart; H doesnotembed ifthatpart is unionofmatching and <=2triangles; H embeds completebipartite with3matchingedges EACHpart, butnot ifonepart arbitrarymatching andotherpart <=2matchingedges. Mixed witness: internal P3 x-y-z inA and edge p-q inB, withp complete toP3 andq having NO requiredP3neighbors, suffices toembedH (allothervertices use bulk).

Apply classicalSimonovitslinearforestDtheorem (H embeds P4 join I): edgeextremalH-freeG has boundedexceptionalset and completebipartitejoin of boundedsymmetriccomponents outsideit. Noexception can haveunboundedneighborhoods inBOTHbulkparts: thatwouldrealizeH with13atthatvertex. Assign each exception toamissedbulkpart. Anyexception not complete tooppositebulk canbereplacedbypurevertex, gainingunboundedlymanyedgesandlosingonlyboundedexceptionedges; Hsafesincenewvertexcanbemaptofreshbulkvertexofitsassignedpart. Thus eachexceptionis anticompleteownbulk andcompleteoppositebulk; crossholesonlyamongexceptions.

P4/clawdecompositionsforceALLinternalcomponents(includingexceptions)tobeP3,K3,K2,K1. RepeatedP3componentsinbulk wouldrealize3P3decomposition, forbidden; sameforK3. Hencebulkcomponentsarematchings, saveboundedvertices. Bothbulkpartscannotcontainlinearmatching(3edgesineachpartrealizesH). Lowerconstructiongives t2+n/4+O1, soexactlyonepartA haslinearmatchingbulk; B hasonlyboundedinternaledges.

B cannotcontainANY P3 (henceanyK3), because mixedP3B+edgeA witnesscanuseonebulkAmatchingedge andallremainingverticesinbulk; allneededcrossedgesarepresent. ThusB ismatching. B hasatmost2matchingedges,because3Bmatchingedges+3bulkAedgesrealizeH.
A hasatmost2nonmatchingcomponents, because3ofthesecontain3P3 andindependentBbulk realizesH. IfA hasnonnmatchingcomponent,andBhasq>=1edges, eachBedgeendpointmustmiss atleastonevertex of EACHfixedP3inA; otherwisethatendpointplaysp inthemixedwitness. Soatleast2qcrossholes. DeleteqBinternaledgesandfillALLcrossholes: edgegain>=q>0; resultinggraphHfreebecauseit iscompletebipartitewithA matching+atmost2triangles. Contradictiontoedgeextremality. ThereforeeitherB isemptyorA allmatching. InbothcasesfillingALLcrossholesisHsafe,soedgeextremalityforcesfullcrosscompletion.

Consequently edgeextrema areamong:
(A) completebipartite A,B, B independent, A matching+atmost2componentsP3/K3;
(B) completebipartite A,B, A allmatching, B matchingatmost2edges.
Forfixeda=|A| familyA maximizesinternaledgesby2K3+maximumremainingmatching: floor(a/2)+3 (a>=6), whereasfamilyBhasatmostfloor(a/2)+2. The smalla casesirrelevantforlargeedgeextremals.
Atn=4k and a=2k+d, familyA e-[t2(n)+k+3] = -d^2+floor(d/2), strictlynegativeford!=0. Thusall edgeextremaarebalancedK_{2k,2k} with2K3+(k-3)K2 inONEpart. Thisgraphisuniqueuptoisomorphism.

AllsufficientlylargeN: sameclassificationyields ex(N,H)<=t2(N)+N/4+C (orDdirectlyyieldsit).

Comparecycles withbalancedK_{2k,2k}+kK2 inA +2K2 inB. ThisHfreebyfinitefactminothermatchingedges3; edgecountisexactlyonebelowedgeoptimum. RelativebaselinebalancedK+perfectmatchingA, 2triangleperturbationinA adds3internaledgesandhasfirstcyclecoefficient3beta; 2Bmatchingedgesaddsfirstcyclecoefficient4beta, beta>0. Shapeeffects offiniteperturbationarelowerorder. Hencealternativehasmorecyclesforalllargek. Need useagent2's explicit coefficient proof/code tofinishanalyticcomparison.
